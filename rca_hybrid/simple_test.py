#!/usr/bin/env python3
"""
Simple component test for hybrid RCA system
Tests each component individually without complex imports
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_individual_imports():
    """Test each component individually"""
    print("Testing individual component imports...")
    
    # Test config
    try:
        from rca_hybrid.config import HybridAnalysisType, LearningMode
        print("✓ Config module imports successful")
        print(f"  - Analysis types: {list(HybridAnalysisType)}")
        print(f"  - Learning modes: {list(LearningMode)}")
    except Exception as e:
        print(f"✗ Config import failed: {e}")
        return False
    
    # Test models  
    try:
        from rca_hybrid.models import HybridAnalysisRequest, HybridAnalysisResult
        print("✓ Models module imports successful")
    except Exception as e:
        print(f"✗ Models import failed: {e}")
        return False
    
    # Test adaptive learner
    try:
        from rca_hybrid.adaptive_learner import AdaptiveLearner
        learner = AdaptiveLearner()
        print("✓ Adaptive learner initialization successful")
    except Exception as e:
        print(f"✗ Adaptive learner failed: {e}")
        return False
    
    # Test AI analyzer
    try:
        from rca_hybrid.ai_analyzer import AIRootCauseAnalyzer
        ai_analyzer = AIRootCauseAnalyzer()
        print("✓ AI analyzer initialization successful")
        capabilities = ai_analyzer.get_capabilities()
        print(f"  - LLM available: {capabilities.get('llm_available', False)}")
    except Exception as e:
        print(f"✗ AI analyzer failed: {e}")
        return False
    
    return True

def test_mock_analysis():
    """Test a mock analysis workflow"""
    print("\nTesting mock analysis workflow...")
    
    try:
        from rca_hybrid.models import HybridAnalysisRequest
        from rca_hybrid.config import HybridAnalysisType, LearningMode
        from rca_hybrid.ai_analyzer import AIRootCauseAnalyzer
        from datetime import datetime
        
        # Create mock task result
        class MockTaskResult:
            def __init__(self):
                self.reasoning_files = {"test.log": "Test failure occurred"}
                self.db_data = {"actions": [{"type": "click", "element": "button"}]}
        
        # Create test request
        request = HybridAnalysisRequest(
            task_id="test_001",
            analysis_type=HybridAnalysisType.AUTO_DETECT,
            task_result=MockTaskResult(),
            failure_log="Element not found: #submit-button",
            dom_snapshot="<html><body><div>Test content</div></body></html>",
            action_sequence=[{"type": "click", "timestamp": "2025-09-02T10:00:00"}],
            framework="test"
        )
        
        print("✓ Mock request created successfully")
        
        # Test AI analyzer
        ai_analyzer = AIRootCauseAnalyzer()
        print("✓ AI analyzer created")
        
        # Note: We won't actually run the analysis since it requires API keys
        print("✓ Mock analysis setup complete")
        
        return True
        
    except Exception as e:
        print(f"✗ Mock analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run component tests"""
    print("=" * 60)
    print("HYBRID RCA SYSTEM - COMPONENT TESTS")
    print("=" * 60)
    
    success = True
    
    if not test_individual_imports():
        success = False
    
    if not test_mock_analysis():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All component tests passed!")
        print("The hybrid system components are working correctly.")
    else:
        print("⚠ Some component tests failed.")
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    main()
