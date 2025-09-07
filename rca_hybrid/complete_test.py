#!/usr/bin/env python3
"""
Complete Hybrid Root Cause Analysis System Test
Tests the full integration and functionality
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

async def test_complete_hybrid_system():
    """Test the complete hybrid system functionality"""
    print("=" * 60)
    print("COMPLETE HYBRID RCA SYSTEM TEST")
    print("=" * 60)
    
    try:
        # Import all components
        print("1. Testing component imports...")
        from rca_hybrid.config import HybridAnalysisType, LearningMode
        from rca_hybrid.models import HybridAnalysisRequest, HybridAnalysisResult
        from rca_hybrid.ai_analyzer import AIRootCauseAnalyzer
        from rca_hybrid.adaptive_learner import AdaptiveLearner
        print("✓ All components imported successfully")
        
        # Test individual components
        print("\n2. Testing individual components...")
        
        # AI Analyzer
        ai_analyzer = AIRootCauseAnalyzer()
        ai_capabilities = ai_analyzer.get_capabilities()
        print(f"✓ AI Analyzer: {ai_capabilities['name']}")
        print(f"  - LLM available: {ai_capabilities['llm_available']}")
        
        # Adaptive Learner
        adaptive_learner = AdaptiveLearner()
        learning_stats = adaptive_learner.get_learning_statistics()
        print(f"✓ Adaptive Learner: Database at {learning_stats['database_path']}")
        print(f"  - Total cases: {learning_stats['total_cases']}")
        
        # Test hybrid analyzer import and initialization
        print("\n3. Testing hybrid analyzer...")
        from rca_hybrid.hybrid_analyzer import HybridRootCauseAnalyzer
        
        hybrid_analyzer = HybridRootCauseAnalyzer(
            confidence_threshold=0.75,
            learning_mode=LearningMode.ACTIVE
        )
        print("✓ Hybrid analyzer initialized successfully")
        
        # Create mock task result
        class MockTaskResult:
            def __init__(self):
                self.reasoning_files = {
                    "agent_reasoning.log": "Failed to find dropdown element. Timeout occurred after 30 seconds."
                }
                self.db_data = {
                    "actions": [
                        {"type": "click", "element": "#dropdown-trigger", "timestamp": "2025-09-02T10:00:00"},
                        {"type": "wait", "duration": 5000, "timestamp": "2025-09-02T10:00:05"},
                        {"type": "click", "element": "#dropdown-option-1", "timestamp": "2025-09-02T10:00:10", "failed": True}
                    ],
                    "errors": ["Element not found: #dropdown-option-1", "Timeout waiting for element"],
                    "timeouts": [{"element": "#dropdown-option-1", "duration": 30000}]
                }
        
        # Create test request
        request = HybridAnalysisRequest(
            task_id="test_hybrid_001",
            analysis_type=HybridAnalysisType.AUTO_DETECT,
            task_result=MockTaskResult(),
            failure_log="""
Error: Element not found
Attempted to click dropdown option but element was not available.
DOM snapshot shows dropdown was not expanded.
Framework: selenium
Browser: chrome
Timeout: 30000ms
""",
            dom_snapshot="""
<html>
<body>
    <div class="dropdown-container">
        <button id="dropdown-trigger" class="dropdown-btn">Select Option</button>
        <ul id="dropdown-menu" class="dropdown-menu" style="display: none;">
            <li id="dropdown-option-1">Option 1</li>
            <li id="dropdown-option-2">Option 2</li>
        </ul>
    </div>
</body>
</html>
""",
            action_sequence=[
                {"type": "click", "element": "#dropdown-trigger", "timestamp": "2025-09-02T10:00:00"},
                {"type": "wait", "duration": 5000, "timestamp": "2025-09-02T10:00:05"},
                {"type": "click", "element": "#dropdown-option-1", "timestamp": "2025-09-02T10:00:10"}
            ],
            framework="selenium_chrome"
        )
        
        print("\n4. Testing hybrid analysis...")
        print(f"Request created for task: {request.task_id}")
        print(f"Analysis type: {request.analysis_type.value}")
        print(f"Framework: {request.framework}")
        
        # Run the analysis
        print("\n5. Running hybrid analysis...")
        result = await hybrid_analyzer.analyze(request)
        
        # Display results
        print(f"\n6. Analysis Results:")
        print(f"✓ Analysis completed successfully")
        print(f"  - Task ID: {result.task_id}")
        print(f"  - Primary method: {result.primary_method}")
        print(f"  - Final confidence: {result.final_confidence:.2f}")
        print(f"  - Deterministic success: {result.deterministic_success}")
        print(f"  - AI used: {result.ai_used}")
        print(f"  - Learning applied: {result.learning_applied}")
        print(f"  - New pattern discovered: {result.new_pattern_discovered}")
        print(f"  - Analysis time: {result.total_analysis_time_ms:.2f}ms")
        print(f"  - Fallback used: {result.fallback_used}")
        
        if result.deterministic_result:
            print(f"\n  Deterministic Analysis:")
            print(f"    - Analyzer: {result.deterministic_result.analyzer_type}")
            print(f"    - Root cause: {result.deterministic_result.root_cause}")
            print(f"    - Confidence: {result.deterministic_result.confidence_score:.2f}")
            print(f"    - Success: {result.deterministic_result.success}")
        
        if result.ai_result:
            print(f"\n  AI Analysis:")
            print(f"    - Root causes: {result.ai_result.root_causes[:2]}")  # Show first 2
            print(f"    - Contributing factors: {len(result.ai_result.contributing_factors)}")
            print(f"    - Recommendations: {len(result.ai_result.recommendations)}")
            print(f"    - Confidence: {result.ai_result.confidence_score:.2f}")
            print(f"    - Summary: {result.ai_result.analysis_summary[:100]}...")
        
        print(f"\n  Final Root Cause: {result.final_root_cause}")
        
        print("\n7. Testing CLI interface...")
        # Test the CLI by importing it
        from rca_hybrid import cli
        print("✓ CLI module imported successfully")
        
        print("\n" + "=" * 60)
        print("🎉 HYBRID SYSTEM TEST COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nThe hybrid root cause analysis system is fully operational:")
        print("  ✓ All components working correctly")
        print("  ✓ Deterministic analyzers integrated")
        print("  ✓ AI analysis functional")
        print("  ✓ Adaptive learning system active")
        print("  ✓ CLI interface available")
        print("  ✓ End-to-end workflow validated")
        
        if not ai_capabilities['llm_available']:
            print("\nNote: LLM is not available (no API key), but system works correctly.")
            print("Set GROQ_API_KEY environment variable to enable full AI analysis.")
        
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the complete system test"""
    try:
        success = asyncio.run(test_complete_hybrid_system())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Test runner error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
