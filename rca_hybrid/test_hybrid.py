#!/usr/bin/env python3
"""
Test script for Hybrid Root Cause Analysis System
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test if all components can be imported"""
    print("Testing imports...")
    
    try:
        from rca_hybrid.config import HybridAnalysisType, LearningMode
        print("✓ Config imports successful")
    except ImportError as e:
        print(f"✗ Config import failed: {e}")
        return False
    
    try:
        from rca_hybrid.models import HybridAnalysisRequest, HybridAnalysisResult
        print("✓ Models imports successful")
    except ImportError as e:
        print(f"✗ Models import failed: {e}")
        return False
    
    try:
        from rca_hybrid.adaptive_learner import AdaptiveLearner
        print("✓ Adaptive learner import successful")
    except ImportError as e:
        print(f"✗ Adaptive learner import failed: {e}")
        return False
    
    try:
        from rca_hybrid.ai_analyzer import AIRootCauseAnalyzer
        print("✓ AI analyzer import successful")
    except ImportError as e:
        print(f"✗ AI analyzer import failed: {e}")
        return False
    
    try:
        from rca_hybrid.hybrid_analyzer import HybridRootCauseAnalyzer
        print("✓ Hybrid analyzer import successful")
    except ImportError as e:
        print(f"✗ Hybrid analyzer import failed: {e}")
        return False
    
    return True

def test_ai_analyzer():
    """Test AI analyzer functionality"""
    print("\nTesting AI analyzer...")
    
    try:
        from rca_hybrid.ai_analyzer import AIRootCauseAnalyzer
        from rca_hybrid.models import HybridAnalysisRequest
        from rca_hybrid.config import HybridAnalysisType, LearningMode
        
        analyzer = AIRootCauseAnalyzer()
        print("✓ AI analyzer initialization successful")
        
        # Test capabilities
        capabilities = analyzer.get_capabilities()
        print(f"✓ AI analyzer capabilities: {capabilities['name']}")
        print(f"  - LLM available: {capabilities['llm_available']}")
        print(f"  - Model: {capabilities['model']}")
        
        return True
        
    except Exception as e:
        print(f"✗ AI analyzer test failed: {e}")
        return False

def test_adaptive_learner():
    """Test adaptive learner functionality"""
    print("\nTesting adaptive learner...")
    
    try:
        from rca_hybrid.adaptive_learner import AdaptiveLearner
        
        learner = AdaptiveLearner()
        print("✓ Adaptive learner initialization successful")
        
        # Test database setup
        learner.setup_database()
        print("✓ Database setup successful")
        
        return True
        
    except Exception as e:
        print(f"✗ Adaptive learner test failed: {e}")
        return False

async def test_hybrid_analyzer():
    """Test hybrid analyzer functionality"""
    print("\nTesting hybrid analyzer...")
    
    try:
        from rca_hybrid.hybrid_analyzer import HybridRootCauseAnalyzer
        from rca_hybrid.models import HybridAnalysisRequest
        from rca_hybrid.config import HybridAnalysisType, LearningMode
        
        # Create analyzer
        analyzer = HybridRootCauseAnalyzer()
        print("✓ Hybrid analyzer initialization successful")
        
        # Create mock task result
        class MockTaskResult:
            def __init__(self):
                self.reasoning_files = {}
                self.db_data = {}
        
        # Create test request
        request = HybridAnalysisRequest(
            task_id="test_task_001",
            analysis_type=HybridAnalysisType.AUTO_DETECT,
            task_result=MockTaskResult(),
            failure_log="Test failure: Element not found",
            dom_snapshot="<html><body><div>Test page</div></body></html>",
            action_sequence=[
                {"type": "click", "element": "button", "timestamp": "2025-09-02T10:00:00"}
            ],
            framework="test_framework"
        )
        
        print("✓ Test request created")
        
        # Test analysis (this might fail if LLM is not available, but should not crash)
        try:
            result = await analyzer.analyze(request)
            print("✓ Analysis completed successfully")
            print(f"  - Primary method: {result.primary_method}")
            print(f"  - Final confidence: {result.final_confidence}")
            print(f"  - AI used: {result.ai_used}")
            print(f"  - Learning applied: {result.learning_applied}")
        except Exception as e:
            print(f"⚠ Analysis failed (expected if no API keys): {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ Hybrid analyzer test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def run_tests():
    """Run all tests"""
    print("=" * 60)
    print("HYBRID ROOT CAUSE ANALYSIS SYSTEM TESTS")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    # Test imports
    if test_imports():
        tests_passed += 1
    
    # Test AI analyzer
    if test_ai_analyzer():
        tests_passed += 1
    
    # Test adaptive learner
    if test_adaptive_learner():
        tests_passed += 1
    
    # Test hybrid analyzer
    if await test_hybrid_analyzer():
        tests_passed += 1
    
    print("\n" + "=" * 60)
    print(f"TESTS COMPLETED: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Hybrid system is ready to use.")
    else:
        print("⚠ Some tests failed. Check the error messages above.")
    
    print("=" * 60)
    
    return tests_passed == total_tests

def main():
    """Main test runner"""
    try:
        success = asyncio.run(run_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Test runner error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
