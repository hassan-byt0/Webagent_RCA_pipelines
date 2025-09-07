"""
Hybrid Root Cause Analysis Package
Combines deterministic algorithms with AI-powered analysis and adaptive learning
"""

__version__ = "1.0.0"
__author__ = "WebAgent RCA Team"

# Import core configuration and types only
from .config import HybridAnalysisType, LearningMode, ConfidenceThreshold

__all__ = [
    "HybridAnalysisType",
    "LearningMode",
    "ConfidenceThreshold"
]

# Delayed imports to avoid circular dependencies
def get_hybrid_analyzer():
    """Get the hybrid analyzer class"""
    from .hybrid_analyzer import HybridRootCauseAnalyzer
    return HybridRootCauseAnalyzer

def get_ai_analyzer():
    """Get the AI analyzer class"""
    from .ai_analyzer import AIRootCauseAnalyzer
    return AIRootCauseAnalyzer

def get_adaptive_learner():
    """Get the adaptive learner class"""
    from .adaptive_learner import AdaptiveLearner
    return AdaptiveLearner
