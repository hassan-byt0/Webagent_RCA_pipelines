"""
Adaptive Learning System for Hybrid Root Cause Analysis
Learns from AI analysis to improve deterministic algorithms
"""
import json
import sqlite3
import hashlib
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    from .models import LearningCase, PatternMatch, RuleUpdate, HybridAnalysisResult
    from .config import (logger, LEARNING_DB_CONFIG, PATTERN_RECOGNITION, 
                        ENHANCEMENT_SETTINGS, HybridAnalysisType, LearningMode)
except ImportError:
    from models import LearningCase, PatternMatch, RuleUpdate, HybridAnalysisResult
    from config import (logger, LEARNING_DB_CONFIG, PATTERN_RECOGNITION,
                       ENHANCEMENT_SETTINGS, HybridAnalysisType, LearningMode)

class AdaptiveLearner:
    """
    Learns from AI analysis results to enhance deterministic algorithms
    """
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or LEARNING_DB_CONFIG['db_path']
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.pattern_cache = {}
        self.initialize_database()
        
    def initialize_database(self):
        """Initialize the learning database"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create learning cases table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_cases (
                case_id TEXT PRIMARY KEY,
                timestamp TEXT,
                analysis_type TEXT,
                failure_log TEXT,
                dom_snapshot TEXT,
                action_sequence TEXT,
                framework TEXT,
                deterministic_root_cause TEXT,
                deterministic_confidence REAL,
                deterministic_failed BOOLEAN,
                ai_root_cause TEXT,
                ai_confidence REAL,
                ai_reasoning TEXT,
                pattern_similarity REAL,
                rule_update_applied BOOLEAN,
                validation_status TEXT
            )
        ''')
        
        # Create pattern matches table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pattern_matches (
                pattern_id TEXT PRIMARY KEY,
                similarity_score REAL,
                matched_cases TEXT,
                recommended_root_cause TEXT,
                confidence_boost REAL,
                pattern_frequency INTEGER,
                last_seen TEXT,
                created_at TEXT
            )
        ''')
        
        # Create rule updates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rule_updates (
                update_id TEXT PRIMARY KEY,
                timestamp TEXT,
                analyzer_type TEXT,
                update_type TEXT,
                rule_description TEXT,
                trigger_conditions TEXT,
                expected_root_cause TEXT,
                confidence_level REAL,
                supporting_cases TEXT,
                ai_validation BOOLEAN,
                manual_validation BOOLEAN,
                status TEXT,
                backup_created BOOLEAN
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"Learning database initialized at {self.db_path}")
    
    def store_learning_case(self, result: HybridAnalysisResult, 
                          failure_log: str, dom_snapshot: str, 
                          action_sequence: List[Dict]) -> str:
        """Store a new learning case from hybrid analysis result"""
        case_id = self._generate_case_id(result.task_id, result.timestamp)
        
        learning_case = LearningCase(
            case_id=case_id,
            timestamp=result.timestamp,
            analysis_type=result.analysis_type,
            failure_log=failure_log,
            dom_snapshot=dom_snapshot,
            action_sequence=action_sequence,
            framework=result.framework,
            deterministic_root_cause=result.deterministic_result.root_cause if result.deterministic_result else None,
            deterministic_confidence=result.deterministic_result.confidence_score if result.deterministic_result else None,
            deterministic_failed=not result.deterministic_success,
            ai_root_cause=result.ai_result.root_causes[0] if result.ai_result and result.ai_result.root_causes else "UNKNOWN",
            ai_confidence=result.ai_result.confidence_score if result.ai_result else 0.0,
            ai_reasoning=result.ai_result.analysis_summary if result.ai_result else "",
            pattern_similarity=None,
            rule_update_applied=len(result.rule_updates_made) > 0,
            validation_status='pending'
        )
        
        self._save_learning_case(learning_case)
        logger.info(f"Stored learning case: {case_id}")
        return case_id
    
    def find_similar_patterns(self, failure_log: str, dom_snapshot: str, 
                            analysis_type: HybridAnalysisType) -> List[PatternMatch]:
        """Find similar patterns in the learning database"""
        # Combine failure log and DOM for pattern matching
        combined_text = f"{failure_log} {dom_snapshot}"
        
        # Get existing cases
        similar_cases = self._get_similar_cases(combined_text, analysis_type)
        
        if not similar_cases:
            return []
        
        # Use TF-IDF for similarity calculation
        texts = [combined_text] + [case['combined_text'] for case in similar_cases]
        
        try:
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        except Exception as e:
            logger.warning(f"TF-IDF similarity calculation failed: {e}")
            return []
        
        patterns = []
        for i, case in enumerate(similar_cases):
            similarity = similarities[i]
            if similarity >= PATTERN_RECOGNITION['similarity_threshold']:
                pattern_match = PatternMatch(
                    pattern_id=f"pattern_{hashlib.md5(case['combined_text'].encode()).hexdigest()[:8]}",
                    similarity_score=similarity,
                    matched_cases=[case['case_id']],
                    recommended_root_cause=case['ai_root_cause'],
                    confidence_boost=PATTERN_RECOGNITION['confidence_boost'],
                    pattern_frequency=1,
                    last_seen=datetime.fromisoformat(case['timestamp'])
                )
                patterns.append(pattern_match)
        
        return sorted(patterns, key=lambda p: p.similarity_score, reverse=True)
    
    def generate_rule_updates(self, learning_cases: List[str], 
                            analysis_type: HybridAnalysisType) -> List[RuleUpdate]:
        """Generate rule updates based on learning cases"""
        if not learning_cases:
            return []
        
        # Analyze patterns in the cases
        patterns = self._analyze_failure_patterns(learning_cases, analysis_type)
        
        rule_updates = []
        for pattern in patterns:
            if pattern['frequency'] >= PATTERN_RECOGNITION['min_occurrences']:
                update = self._create_rule_update(pattern, analysis_type)
                if update:
                    rule_updates.append(update)
        
        return rule_updates
    
    def apply_rule_update(self, rule_update: RuleUpdate, 
                         analyzer_type: str) -> bool:
        """Apply a rule update to the specified deterministic analyzer"""
        if not ENHANCEMENT_SETTINGS['auto_update_rules']:
            logger.info(f"Auto-update disabled, storing rule update: {rule_update.update_id}")
            self._save_rule_update(rule_update)
            return False
        
        try:
            # Create backup first
            if ENHANCEMENT_SETTINGS['backup_before_update']:
                self._create_analyzer_backup(analyzer_type)
            
            # Apply the update based on analyzer type
            if analyzer_type == 'dropdown':
                success = self._update_dropdown_analyzer(rule_update)
            elif analyzer_type == 'arxiv_search':
                success = self._update_arxiv_analyzer(rule_update)
            else:
                logger.error(f"Unknown analyzer type: {analyzer_type}")
                return False
            
            if success:
                rule_update.status = 'applied'
                rule_update.backup_created = True
                logger.info(f"Successfully applied rule update: {rule_update.update_id}")
            else:
                rule_update.status = 'failed'
                if ENHANCEMENT_SETTINGS['rollback_on_failure']:
                    self._rollback_analyzer(analyzer_type)
                
            self._save_rule_update(rule_update)
            return success
            
        except Exception as e:
            logger.error(f"Error applying rule update {rule_update.update_id}: {e}")
            rule_update.status = 'error'
            self._save_rule_update(rule_update)
            return False
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get statistics about the learning system"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total cases
        cursor.execute("SELECT COUNT(*) FROM learning_cases")
        total_cases = cursor.fetchone()[0]
        
        # Cases by analysis type
        cursor.execute("""
            SELECT analysis_type, COUNT(*) 
            FROM learning_cases 
            GROUP BY analysis_type
        """)
        cases_by_type = dict(cursor.fetchall())
        
        # Failed deterministic cases
        cursor.execute("SELECT COUNT(*) FROM learning_cases WHERE deterministic_failed = 1")
        failed_deterministic = cursor.fetchone()[0]
        
        # Rule updates
        cursor.execute("SELECT status, COUNT(*) FROM rule_updates GROUP BY status")
        rule_updates_by_status = dict(cursor.fetchall())
        
        # Recent activity (last 7 days)
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        cursor.execute("SELECT COUNT(*) FROM learning_cases WHERE timestamp > ?", (week_ago,))
        recent_cases = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_cases': total_cases,
            'cases_by_type': cases_by_type,
            'failed_deterministic_cases': failed_deterministic,
            'deterministic_failure_rate': failed_deterministic / total_cases if total_cases > 0 else 0,
            'rule_updates_by_status': rule_updates_by_status,
            'recent_cases_7_days': recent_cases,
            'database_path': str(self.db_path),
            'last_updated': datetime.now().isoformat()
        }
    
    def _generate_case_id(self, task_id: str, timestamp: datetime) -> str:
        """Generate unique case ID"""
        combined = f"{task_id}_{timestamp.isoformat()}"
        return f"case_{hashlib.md5(combined.encode()).hexdigest()[:12]}"
    
    def _save_learning_case(self, case: LearningCase):
        """Save learning case to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO learning_cases VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            case.case_id, case.timestamp.isoformat(), case.analysis_type.value,
            case.failure_log, case.dom_snapshot, json.dumps(case.action_sequence),
            case.framework, case.deterministic_root_cause, case.deterministic_confidence,
            case.deterministic_failed, case.ai_root_cause, case.ai_confidence,
            case.ai_reasoning, case.pattern_similarity, case.rule_update_applied,
            case.validation_status
        ))
        
        conn.commit()
        conn.close()
    
    def _get_similar_cases(self, combined_text: str, 
                          analysis_type: HybridAnalysisType) -> List[Dict]:
        """Get similar cases from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT case_id, failure_log, dom_snapshot, ai_root_cause, timestamp
            FROM learning_cases 
            WHERE analysis_type = ? AND deterministic_failed = 1
            ORDER BY timestamp DESC
            LIMIT 100
        ''', (analysis_type.value,))
        
        cases = []
        for row in cursor.fetchall():
            case = {
                'case_id': row[0],
                'combined_text': f"{row[1]} {row[2]}",
                'ai_root_cause': row[3],
                'timestamp': row[4]
            }
            cases.append(case)
        
        conn.close()
        return cases
    
    def _analyze_failure_patterns(self, case_ids: List[str], 
                                analysis_type: HybridAnalysisType) -> List[Dict]:
        """Analyze patterns in failure cases"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get cases data
        placeholders = ','.join(['?'] * len(case_ids))
        cursor.execute(f'''
            SELECT failure_log, dom_snapshot, ai_root_cause, framework
            FROM learning_cases 
            WHERE case_id IN ({placeholders})
        ''', case_ids)
        
        cases_data = cursor.fetchall()
        conn.close()
        
        # Group by root cause and analyze patterns
        patterns_by_cause = {}
        for failure_log, dom_snapshot, ai_root_cause, framework in cases_data:
            if ai_root_cause not in patterns_by_cause:
                patterns_by_cause[ai_root_cause] = {
                    'failure_logs': [],
                    'dom_patterns': [],
                    'frameworks': [],
                    'frequency': 0
                }
            
            patterns_by_cause[ai_root_cause]['failure_logs'].append(failure_log)
            patterns_by_cause[ai_root_cause]['dom_patterns'].append(dom_snapshot)
            patterns_by_cause[ai_root_cause]['frameworks'].append(framework)
            patterns_by_cause[ai_root_cause]['frequency'] += 1
        
        # Convert to pattern list
        patterns = []
        for root_cause, data in patterns_by_cause.items():
            pattern = {
                'root_cause': root_cause,
                'frequency': data['frequency'],
                'common_keywords': self._extract_common_keywords(data['failure_logs']),
                'dom_patterns': self._extract_dom_patterns(data['dom_patterns']),
                'frameworks': list(set(data['frameworks']))
            }
            patterns.append(pattern)
        
        return patterns
    
    def _create_rule_update(self, pattern: Dict, 
                          analysis_type: HybridAnalysisType) -> Optional[RuleUpdate]:
        """Create a rule update from a pattern"""
        try:
            update_id = f"update_{hashlib.md5(str(pattern).encode()).hexdigest()[:8]}"
            
            rule_update = RuleUpdate(
                update_id=update_id,
                timestamp=datetime.now(),
                analyzer_type=analysis_type.value,
                update_type='new_rule',
                rule_description=f"Pattern-based rule for {pattern['root_cause']}",
                trigger_conditions={
                    'keywords': pattern['common_keywords'],
                    'dom_patterns': pattern['dom_patterns'],
                    'frameworks': pattern['frameworks']
                },
                expected_root_cause=pattern['root_cause'],
                confidence_level=min(0.9, 0.6 + (pattern['frequency'] * 0.05)),
                supporting_cases=[],  # Would be populated with actual case IDs
                ai_validation=True,
                manual_validation=False,
                status='pending',
                backup_created=False
            )
            
            return rule_update
            
        except Exception as e:
            logger.error(f"Error creating rule update from pattern: {e}")
            return None
    
    def _extract_common_keywords(self, texts: List[str]) -> List[str]:
        """Extract common keywords from text list"""
        if not texts:
            return []
        
        # Simple keyword extraction (could be enhanced with NLP)
        all_words = []
        for text in texts:
            words = text.lower().split()
            all_words.extend([word for word in words if len(word) > 3])
        
        # Count word frequency
        word_counts = {}
        for word in all_words:
            word_counts[word] = word_counts.get(word, 0) + 1
        
        # Return most common words
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:10] if count >= 2]
    
    def _extract_dom_patterns(self, dom_snapshots: List[str]) -> List[str]:
        """Extract common DOM patterns"""
        if not dom_snapshots:
            return []
        
        # Simple pattern extraction (could be enhanced with DOM parsing)
        patterns = []
        for dom in dom_snapshots:
            # Extract tag patterns
            import re
            tags = re.findall(r'<(\w+)', dom)
            if tags:
                patterns.extend(tags)
        
        # Return most common patterns
        pattern_counts = {}
        for pattern in patterns:
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        
        sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
        return [pattern for pattern, count in sorted_patterns[:5] if count >= 2]
    
    def _save_rule_update(self, rule_update: RuleUpdate):
        """Save rule update to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO rule_updates VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            rule_update.update_id, rule_update.timestamp.isoformat(),
            rule_update.analyzer_type, rule_update.update_type,
            rule_update.rule_description, json.dumps(rule_update.trigger_conditions),
            rule_update.expected_root_cause, rule_update.confidence_level,
            json.dumps(rule_update.supporting_cases), rule_update.ai_validation,
            rule_update.manual_validation, rule_update.status, rule_update.backup_created
        ))
        
        conn.commit()
        conn.close()
    
    def _update_dropdown_analyzer(self, rule_update: RuleUpdate) -> bool:
        """Update dropdown analyzer with new rule"""
        # This would implement actual rule updates to the dropdown analyzer
        # For now, return True to simulate successful update
        logger.info(f"Simulating dropdown analyzer update: {rule_update.rule_description}")
        return True
    
    def _update_arxiv_analyzer(self, rule_update: RuleUpdate) -> bool:
        """Update ArXiv analyzer with new rule"""
        # This would implement actual rule updates to the ArXiv analyzer
        # For now, return True to simulate successful update
        logger.info(f"Simulating ArXiv analyzer update: {rule_update.rule_description}")
        return True
    
    def _create_analyzer_backup(self, analyzer_type: str):
        """Create backup of analyzer before updating"""
        logger.info(f"Creating backup for {analyzer_type} analyzer")
        # Implementation would backup analyzer files
    
    def _rollback_analyzer(self, analyzer_type: str):
        """Rollback analyzer to previous state"""
        logger.info(f"Rolling back {analyzer_type} analyzer")
        # Implementation would restore from backup
