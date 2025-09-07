"""
Data Models for Hybrid Root Cause Analysis
"""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from enum import Enum

try:
    from .config import HybridAnalysisType, LearningMode
except ImportError:
    from config import HybridAnalysisType, LearningMode

@dataclass
class HybridAnalysisRequest:
    """Request structure for hybrid analysis"""
    task_id: str
    analysis_type: HybridAnalysisType
    task_result: Any  # TaskResult from deterministic analyzers
    failure_log: str
    dom_snapshot: str
    action_sequence: List[Dict]
    framework: str
    confidence_threshold: float = 0.75
    learning_mode: LearningMode = LearningMode.ACTIVE
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass 
class DeterministicResult:
    """Results from deterministic analysis"""
    analyzer_type: str  # 'dropdown' or 'arxiv_search'
    root_cause: str
    confidence_score: float
    failure_step: Optional[int]
    step_results: Dict[int, bool]
    analysis_time_ms: float
    success: bool
    additional_data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.additional_data is None:
            self.additional_data = {}

@dataclass
class AIAnalysisResult:
    """Results from AI-powered analysis"""
    root_causes: List[str]
    five_whys: Dict[str, List[str]]
    contributing_factors: List[str]
    recommendations: List[str]
    analysis_summary: str
    confidence_score: float
    analysis_time_ms: float
    success: bool
    framework_detected: str
    additional_data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.additional_data is None:
            self.additional_data = {}

@dataclass
class HybridAnalysisResult:
    """Final hybrid analysis result"""
    task_id: str
    analysis_type: HybridAnalysisType
    timestamp: datetime
    
    # Primary analysis path
    primary_method: str  # 'deterministic' or 'ai'
    final_root_cause: str
    final_confidence: float
    
    # Deterministic analysis results
    deterministic_result: Optional[DeterministicResult]
    deterministic_success: bool
    
    # AI analysis results  
    ai_result: Optional[AIAnalysisResult]
    ai_used: bool
    
    # Learning and adaptation
    learning_applied: bool
    new_pattern_discovered: bool
    rule_updates_made: List[str]
    
    # Performance metrics
    total_analysis_time_ms: float
    fallback_used: bool
    
    # Additional metadata
    framework: str
    learning_mode: LearningMode
    analysis_metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.analysis_metadata is None:
            self.analysis_metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        result['analysis_type'] = self.analysis_type.value
        result['learning_mode'] = self.learning_mode.value
        result['timestamp'] = self.timestamp.isoformat()
        return result

@dataclass
class LearningCase:
    """Structure for storing learning cases"""
    case_id: str
    timestamp: datetime
    analysis_type: HybridAnalysisType
    
    # Input data
    failure_log: str
    dom_snapshot: str
    action_sequence: List[Dict]
    framework: str
    
    # Deterministic analysis
    deterministic_root_cause: Optional[str]
    deterministic_confidence: Optional[float]
    deterministic_failed: bool
    
    # AI analysis
    ai_root_cause: str
    ai_confidence: float
    ai_reasoning: str
    
    # Learning metadata
    pattern_similarity: Optional[float]
    rule_update_applied: bool
    validation_status: str  # 'pending', 'validated', 'rejected'
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage"""
        result = asdict(self)
        result['analysis_type'] = self.analysis_type.value
        result['timestamp'] = self.timestamp.isoformat()
        return result

@dataclass
class PatternMatch:
    """Structure for pattern matching results"""
    pattern_id: str
    similarity_score: float
    matched_cases: List[str]
    recommended_root_cause: str
    confidence_boost: float
    pattern_frequency: int
    last_seen: datetime

@dataclass
class RuleUpdate:
    """Structure for deterministic rule updates"""
    update_id: str
    timestamp: datetime
    analyzer_type: str  # 'dropdown' or 'arxiv_search'
    update_type: str   # 'new_rule', 'modify_rule', 'enhance_pattern'
    
    # Rule details
    rule_description: str
    trigger_conditions: Dict[str, Any]
    expected_root_cause: str
    confidence_level: float
    
    # Supporting evidence
    supporting_cases: List[str]
    ai_validation: bool
    manual_validation: bool
    
    # Status
    status: str  # 'pending', 'applied', 'rejected', 'rolled_back'
    backup_created: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        return result
