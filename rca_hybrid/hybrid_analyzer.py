"""
Hybrid Root Cause Analyzer
Combines deterministic algorithms with AI-powered analysis and adaptive learning
"""
import asyncio
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

try:
    from .models import (HybridAnalysisRequest, HybridAnalysisResult, 
                        DeterministicResult, AIAnalysisResult)
    from .config import (HybridAnalysisType, LearningMode, ConfidenceThreshold,
                        AI_MODEL_CONFIG, AI_MODEL_CONFIGS, DEFAULT_AI_PROVIDER,
                        FALLBACK_STRATEGIES, TIMEOUTS, logger)
    from .adaptive_learner import AdaptiveLearner
    from .ai_analyzer import AIRootCauseAnalyzer
except ImportError:
    from models import (HybridAnalysisRequest, HybridAnalysisResult,
                       DeterministicResult, AIAnalysisResult)
    from config import (HybridAnalysisType, LearningMode, ConfidenceThreshold,
                       AI_MODEL_CONFIG, AI_MODEL_CONFIGS, DEFAULT_AI_PROVIDER, 
                       FALLBACK_STRATEGIES, TIMEOUTS, logger)
    from adaptive_learner import AdaptiveLearner
    from ai_analyzer import AIRootCauseAnalyzer

class HybridRootCauseAnalyzer:
    """
    Hybrid analyzer that combines deterministic algorithms with AI analysis
    and includes adaptive learning capabilities
    """
    
    def __init__(self, confidence_threshold: float = 0.75,
                 learning_mode: LearningMode = LearningMode.ACTIVE,
                 ai_provider: str = None):
        self.confidence_threshold = confidence_threshold
        self.learning_mode = learning_mode
        self.adaptive_learner = AdaptiveLearner()
        
        # Select AI provider
        if ai_provider and ai_provider in AI_MODEL_CONFIGS:
            selected_config = AI_MODEL_CONFIGS[ai_provider]
            logger.info(f"Using AI provider: {ai_provider}")
        else:
            selected_config = AI_MODEL_CONFIG
            ai_provider = DEFAULT_AI_PROVIDER
            logger.info(f"Using default AI provider: {ai_provider}")
        
        self.ai_analyzer = AIRootCauseAnalyzer(model_config=selected_config)
        self.ai_provider = ai_provider
        
        # Initialize deterministic analyzers
        self._init_deterministic_analyzers()
        
        logger.info(f"Hybrid analyzer initialized with threshold: {confidence_threshold}")
    
    def _init_deterministic_analyzers(self):
        """Initialize the deterministic analyzers"""
        self.dropdown_analyzer = None
        self.arxiv_analyzer = None
        self.DropdownTaskResult = None
        self.ArxivTaskResult = None
        
        # Try to import dropdown analyzer
        try:
            import sys
            from pathlib import Path
            parent_dir = Path(__file__).parent.parent
            sys.path.insert(0, str(parent_dir))
            
            from r_det_dropdown.deterministic_analyzer import DeterministicDropdownAnalyzer
            from r_det_dropdown.models import TaskResult as DropdownTaskResult
            self.dropdown_analyzer = DeterministicDropdownAnalyzer()
            self.DropdownTaskResult = DropdownTaskResult
            logger.info("Successfully initialized dropdown analyzer")
            
        except ImportError as e:
            logger.warning(f"Failed to import dropdown analyzer: {e}")
        
        # Try to import ArXiv analyzer
        try:
            from rca_det_search.deterministic_analyzer import DeterministicArxivAnalyzer
            from rca_det_search.models import TaskResult as ArxivTaskResult
            self.arxiv_analyzer = DeterministicArxivAnalyzer()
            self.ArxivTaskResult = ArxivTaskResult
            logger.info("Successfully initialized ArXiv analyzer")
            
        except ImportError as e:
            logger.warning(f"Failed to import ArXiv analyzer: {e}")
        
        if not self.dropdown_analyzer and not self.arxiv_analyzer:
            logger.error("No deterministic analyzers available")
        else:
            analyzers_available = []
            if self.dropdown_analyzer:
                analyzers_available.append("dropdown")
            if self.arxiv_analyzer:
                analyzers_available.append("arxiv")
            logger.info(f"Available analyzers: {', '.join(analyzers_available)}")
    
    async def analyze(self, request: HybridAnalysisRequest) -> HybridAnalysisResult:
        """
        Main analysis method that orchestrates the hybrid approach
        
        Process:
        1. Try deterministic analysis first
        2. If deterministic fails or confidence low, use AI
        3. Learn from the results and update rules if needed
        """
        start_time = time.time()
        logger.info(f"Starting hybrid analysis for task: {request.task_id}")
        
        # Initialize result
        result = HybridAnalysisResult(
            task_id=request.task_id,
            analysis_type=request.analysis_type,
            timestamp=request.timestamp,
            primary_method="deterministic",
            final_root_cause="UNKNOWN",
            final_confidence=0.0,
            deterministic_result=None,
            deterministic_success=False,
            ai_result=None,
            ai_used=False,
            learning_applied=False,
            new_pattern_discovered=False,
            rule_updates_made=[],
            total_analysis_time_ms=0,
            fallback_used=False,
            framework=request.framework,
            learning_mode=request.learning_mode
        )
        
        try:
            # Step 1: Check for similar patterns first
            patterns = await self._check_similar_patterns(request)
            if patterns:
                result.learning_applied = True
                logger.info(f"Found {len(patterns)} similar patterns")
            
            # Step 2: Try deterministic analysis
            deterministic_result = await self._run_deterministic_analysis(request)
            result.deterministic_result = deterministic_result
            
            if deterministic_result and deterministic_result.success:
                result.deterministic_success = True
                
                # Check if confidence is above threshold
                if deterministic_result.confidence_score >= request.confidence_threshold:
                    result.primary_method = "deterministic"
                    result.final_root_cause = deterministic_result.root_cause
                    result.final_confidence = deterministic_result.confidence_score
                    
                    logger.info(f"Deterministic analysis successful: {result.final_root_cause} "
                              f"(confidence: {result.final_confidence:.2f})")
                else:
                    logger.info(f"Deterministic confidence too low: {deterministic_result.confidence_score:.2f}")
                    result.ai_used = True
            else:
                logger.info("Deterministic analysis failed, falling back to AI")
                result.ai_used = True
            
            # Step 3: Use AI if needed
            if result.ai_used:
                ai_result = await self._run_ai_analysis(request)
                result.ai_result = ai_result
                
                if ai_result and ai_result.success:
                    result.primary_method = "ai"
                    result.final_root_cause = ai_result.root_causes[0] if ai_result.root_causes else "UNKNOWN"
                    result.final_confidence = ai_result.confidence_score
                    
                    logger.info(f"AI analysis successful: {result.final_root_cause} "
                              f"(confidence: {result.final_confidence:.2f})")
                else:
                    # Both methods failed - use fallback
                    result.fallback_used = True
                    result.final_root_cause = "ANALYSIS_FAILURE"
                    result.final_confidence = 0.0
                    logger.warning("Both deterministic and AI analysis failed")
            
            # Step 4: Adaptive learning
            if request.learning_mode != LearningMode.PASSIVE:
                await self._apply_adaptive_learning(request, result)
            
            # Calculate total time
            result.total_analysis_time_ms = (time.time() - start_time) * 1000
            
            logger.info(f"Hybrid analysis completed in {result.total_analysis_time_ms:.2f}ms")
            return result
            
        except Exception as e:
            logger.error(f"Error in hybrid analysis: {e}")
            result.final_root_cause = "ANALYSIS_ERROR"
            result.final_confidence = 0.0
            result.total_analysis_time_ms = (time.time() - start_time) * 1000
            return result
    
    async def _check_similar_patterns(self, request: HybridAnalysisRequest) -> List[Any]:
        """Check for similar patterns in learning database"""
        try:
            patterns = self.adaptive_learner.find_similar_patterns(
                request.failure_log,
                request.dom_snapshot,
                request.analysis_type
            )
            return patterns
        except Exception as e:
            logger.warning(f"Pattern matching failed: {e}")
            return []
    
    async def _run_deterministic_analysis(self, request: HybridAnalysisRequest) -> Optional[DeterministicResult]:
        """Run the appropriate deterministic analyzer"""
        start_time = time.time()
        
        try:
            if request.analysis_type == HybridAnalysisType.DROPDOWN:
                analyzer = self.dropdown_analyzer
                task_result = self.DropdownTaskResult(
                    task_id=request.task_id,
                    timestamp=request.timestamp,
                    task_type='ecommerce_dropdown',
                    status='pending'
                )
            elif request.analysis_type == HybridAnalysisType.ARXIV_SEARCH:
                analyzer = self.arxiv_analyzer
                task_result = self.ArxivTaskResult(
                    task_id=request.task_id,
                    timestamp=request.timestamp,
                    task_type='arxiv_search',
                    status='pending'
                )
            else:
                # Auto-detect analysis type
                detected_type = self._detect_analysis_type(request)
                if detected_type == HybridAnalysisType.DROPDOWN:
                    analyzer = self.dropdown_analyzer
                    task_result = self.DropdownTaskResult(
                        task_id=request.task_id,
                        timestamp=request.timestamp,
                        task_type='ecommerce_dropdown',
                        status='pending'
                    )
                else:
                    analyzer = self.arxiv_analyzer
                    task_result = self.ArxivTaskResult(
                        task_id=request.task_id,
                        timestamp=request.timestamp,
                        task_type='arxiv_search',
                        status='pending'
                    )
            
            # Run the analysis
            det_result = analyzer.analyze_task(
                task_result=task_result,
                failure_log=request.failure_log,
                dom_snapshot=request.dom_snapshot,
                action_sequence=request.action_sequence,
                framework=request.framework
            )
            
            analysis_time = (time.time() - start_time) * 1000
            
            # Extract confidence score (may vary by analyzer)
            confidence = self._extract_confidence_score(det_result)
            
            return DeterministicResult(
                analyzer_type=request.analysis_type.value,
                root_cause=det_result.root_cause.value if hasattr(det_result.root_cause, 'value') else str(det_result.root_cause),
                confidence_score=confidence,
                failure_step=getattr(det_result, 'failure_step', None),
                step_results=self._extract_step_results(det_result),
                analysis_time_ms=analysis_time,
                success=True,
                additional_data=self._extract_additional_data(det_result)
            )
            
        except Exception as e:
            logger.error(f"Deterministic analysis failed: {e}")
            return DeterministicResult(
                analyzer_type=request.analysis_type.value,
                root_cause="DETERMINISTIC_FAILURE",
                confidence_score=0.0,
                failure_step=None,
                step_results={},
                analysis_time_ms=(time.time() - start_time) * 1000,
                success=False
            )
    
    async def _run_ai_analysis(self, request: HybridAnalysisRequest) -> Optional[AIAnalysisResult]:
        """Run AI-powered analysis"""
        start_time = time.time()
        
        try:
            ai_result = await self.ai_analyzer.analyze(request)
            return ai_result
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            analysis_time = (time.time() - start_time) * 1000
            
            # Return fallback result
            return AIAnalysisResult(
                root_causes=["AI_ANALYSIS_FAILED"],
                five_whys={},
                contributing_factors=[f"AI analysis error: {str(e)}"],
                recommendations=["Check AI service configuration"],
                analysis_summary=f"AI analysis failed: {str(e)}",
                confidence_score=0.0,
                analysis_time_ms=analysis_time,
                success=False,
                framework_detected=request.framework
            )
    
    async def _apply_adaptive_learning(self, request: HybridAnalysisRequest, 
                                     result: HybridAnalysisResult):
        """Apply adaptive learning based on the analysis result"""
        try:
            # Store the learning case
            case_id = self.adaptive_learner.store_learning_case(
                result, request.failure_log, request.dom_snapshot, request.action_sequence
            )
            
            # If deterministic analysis failed and AI succeeded, look for learning opportunities
            if not result.deterministic_success and result.ai_result and result.ai_result.success:
                # Generate rule updates if this is a recurring pattern
                similar_cases = self.adaptive_learner.find_similar_patterns(
                    request.failure_log, request.dom_snapshot, request.analysis_type
                )
                
                if len(similar_cases) >= 3:  # If we have multiple similar cases
                    rule_updates = self.adaptive_learner.generate_rule_updates(
                        [case_id], request.analysis_type
                    )
                    
                    for rule_update in rule_updates:
                        if request.learning_mode == LearningMode.AGGRESSIVE:
                            # Apply immediately
                            success = self.adaptive_learner.apply_rule_update(
                                rule_update, request.analysis_type.value
                            )
                            if success:
                                result.rule_updates_made.append(rule_update.update_id)
                        else:
                            # Store for later review
                            result.rule_updates_made.append(f"pending_{rule_update.update_id}")
                    
                    result.new_pattern_discovered = len(rule_updates) > 0
            
        except Exception as e:
            logger.warning(f"Adaptive learning failed: {e}")
    
    def _detect_analysis_type(self, request: HybridAnalysisRequest) -> HybridAnalysisType:
        """Auto-detect the analysis type based on request content"""
        failure_log_lower = request.failure_log.lower()
        dom_lower = request.dom_snapshot.lower()
        
        # Look for dropdown-specific indicators
        dropdown_indicators = ['dropdown', 'select', 'option', 'category', 'subcategory']
        arxiv_indicators = ['arxiv', 'author', 'classification', 'paper', 'search', 'academic']
        
        dropdown_score = sum(1 for indicator in dropdown_indicators 
                           if indicator in failure_log_lower or indicator in dom_lower)
        arxiv_score = sum(1 for indicator in arxiv_indicators 
                         if indicator in failure_log_lower or indicator in dom_lower)
        
        if dropdown_score > arxiv_score:
            return HybridAnalysisType.DROPDOWN
        else:
            return HybridAnalysisType.ARXIV_SEARCH
    
    def _extract_confidence_score(self, result: Any) -> float:
        """Extract confidence score from deterministic result"""
        # Different analyzers may have different confidence calculation methods
        if hasattr(result, 'confidence_score'):
            return result.confidence_score
        elif hasattr(result, 'steps') and result.steps:
            # Calculate based on step success rate
            total_steps = len(result.steps)
            successful_steps = sum(1 for step in result.steps if getattr(step, 'success', False))
            return successful_steps / total_steps if total_steps > 0 else 0.0
        else:
            # Default confidence based on success
            return 0.8 if str(result.root_cause) != 'UNKNOWN' else 0.2
    
    def _extract_step_results(self, result: Any) -> Dict[int, bool]:
        """Extract step results from deterministic analysis"""
        if hasattr(result, 'steps') and result.steps:
            return {i+1: getattr(step, 'success', False) 
                   for i, step in enumerate(result.steps)}
        else:
            return {}
    
    def _extract_additional_data(self, result: Any) -> Dict[str, Any]:
        """Extract additional data from deterministic result"""
        additional = {}
        
        # Extract common fields
        for field in ['author_failure_type', 'date_failure_type', 'framework', 'analysis_details']:
            if hasattr(result, field):
                value = getattr(result, field)
                if value:
                    additional[field] = value.value if hasattr(value, 'value') else value
        
        return additional
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the hybrid system"""
        learning_stats = self.adaptive_learner.get_learning_statistics()
        
        return {
            'hybrid_analyzer': {
                'confidence_threshold': self.confidence_threshold,
                'learning_mode': self.learning_mode.value,
                'available_analyzers': ['dropdown', 'arxiv_search'],
                'ai_model': AI_MODEL_CONFIG['model']
            },
            'learning_system': learning_stats,
            'performance': {
                'timeout_settings': TIMEOUTS,
                'fallback_strategies': FALLBACK_STRATEGIES
            }
        }
