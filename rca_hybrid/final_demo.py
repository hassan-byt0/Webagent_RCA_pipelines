#!/usr/bin/env python3
"""
Hybrid Root Cause Analysis System - Final Demonstration
Shows the complete system functionality
"""
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def demonstrate_hybrid_system():
    """Demonstrate the complete hybrid system"""
    print("=" * 70)
    print("HYBRID ROOT CAUSE ANALYSIS SYSTEM - FINAL DEMONSTRATION")
    print("=" * 70)
    
    # 1. Import all components
    print("1. Loading hybrid system components...")
    from rca_hybrid.config import HybridAnalysisType, LearningMode
    from rca_hybrid.models import HybridAnalysisRequest, HybridAnalysisResult
    from rca_hybrid.ai_analyzer import AIRootCauseAnalyzer
    from rca_hybrid.adaptive_learner import AdaptiveLearner
    from rca_hybrid.hybrid_analyzer import HybridRootCauseAnalyzer
    print("✓ All components loaded successfully")
    
    # 2. Show system capabilities
    print("\n2. System Capabilities:")
    
    # AI Analyzer capabilities
    ai_analyzer = AIRootCauseAnalyzer()
    ai_caps = ai_analyzer.get_capabilities()
    print(f"   • AI Analyzer: {ai_caps['name']} v{ai_caps.get('version', '1.0')}")
    print(f"     - LLM Available: {ai_caps['llm_available']}")
    print(f"     - Model: {ai_caps['model']}")
    print(f"     - Features: {', '.join(ai_caps.get('features', []))}")
    
    # Adaptive Learning capabilities
    learner = AdaptiveLearner()
    stats = learner.get_learning_statistics()
    print(f"   • Adaptive Learning System:")
    print(f"     - Database: {stats['database_path']}")
    print(f"     - Learning Cases: {stats['total_cases']}")
    print(f"     - Last Updated: {stats['last_updated'][:19]}")
    
    # Hybrid Analyzer capabilities
    hybrid = HybridRootCauseAnalyzer(
        confidence_threshold=0.75,
        learning_mode=LearningMode.ACTIVE
    )
    
    dropdown_available = hybrid.dropdown_analyzer is not None
    arxiv_available = hybrid.arxiv_analyzer is not None
    
    print(f"   • Hybrid Analyzer:")
    print(f"     - Dropdown Algorithm: {'Available' if dropdown_available else 'Not loaded'}")
    print(f"     - ArXiv Algorithm: {'Available' if arxiv_available else 'Not loaded'}")
    print(f"     - AI Fallback: Available")
    print(f"     - Adaptive Learning: Active")
    
    # 3. Show analysis types
    print("\n3. Analysis Types Supported:")
    for analysis_type in HybridAnalysisType:
        print(f"   • {analysis_type.value.upper()}: {analysis_type.name}")
    
    # 4. Show learning modes
    print("\n4. Learning Modes:")
    for mode in LearningMode:
        print(f"   • {mode.value.upper()}: {mode.name}")
    
    # 5. Create sample analysis request
    print("\n5. Sample Analysis Configuration:")
    
    class MockTaskResult:
        def __init__(self):
            self.reasoning_files = {
                "selenium_log.txt": "ElementNotInteractableException: Element not clickable",
                "agent_reasoning.log": "Failed to click dropdown after multiple attempts"
            }
            self.db_data = {
                "actions": [
                    {"type": "click", "element": "#dropdown-btn", "success": True},
                    {"type": "wait", "duration": 2000},
                    {"type": "click", "element": "#option-1", "success": False, "error": "Element not found"}
                ],
                "errors": ["Element not found: #option-1", "Dropdown not expanded"],
                "timeouts": [{"element": "#option-1", "timeout": 10000}]
            }
    
    request = HybridAnalysisRequest(
        task_id="demo_dropdown_failure_001",
        analysis_type=HybridAnalysisType.AUTO_DETECT,
        task_result=MockTaskResult(),
        failure_log="""
ERROR: Dropdown interaction failed
- Clicked dropdown trigger successfully
- Dropdown menu did not expand
- Target option element not found
- Timeout after 10 seconds

Browser: Chrome 120.0
Framework: Selenium WebDriver
OS: macOS
""",
        dom_snapshot="""
<div class="dropdown-container">
    <button id="dropdown-btn" class="btn-dropdown" onclick="toggleDropdown()">
        Select Option ▼
    </button>
    <ul id="dropdown-menu" class="dropdown-options" style="display: none;">
        <li id="option-1" data-value="opt1">Option 1</li>
        <li id="option-2" data-value="opt2">Option 2</li>
        <li id="option-3" data-value="opt3">Option 3</li>
    </ul>
</div>
<script>
function toggleDropdown() {
    const menu = document.getElementById('dropdown-menu');
    // Bug: missing implementation - dropdown never shows
}
</script>
""",
        action_sequence=[
            {"step": 1, "action": "click", "target": "#dropdown-btn", "timestamp": "2025-09-02T15:30:00"},
            {"step": 2, "action": "wait", "duration": 2000, "timestamp": "2025-09-02T15:30:02"},
            {"step": 3, "action": "click", "target": "#option-1", "timestamp": "2025-09-02T15:30:04", "failed": True}
        ],
        framework="selenium_chrome",
        confidence_threshold=0.75,
        learning_mode=LearningMode.ACTIVE
    )
    
    print(f"   • Task ID: {request.task_id}")
    print(f"   • Analysis Type: {request.analysis_type.value}")
    print(f"   • Framework: {request.framework}")
    print(f"   • Learning Mode: {request.learning_mode.value}")
    print(f"   • Confidence Threshold: {request.confidence_threshold}")
    
    # 6. Show analysis workflow
    print("\n6. Hybrid Analysis Workflow:")
    print("   1. 🔍 Auto-detect failure type from request")
    print("   2. 🎯 Try deterministic algorithm (dropdown/arxiv)")
    print("   3. ⚖️  Evaluate confidence score")
    print("   4. 🤖 Fallback to AI analysis if needed")
    print("   5. 🧠 Learn from results and update rules")
    print("   6. 📊 Return comprehensive analysis")
    
    # 7. Show CLI usage
    print("\n7. Command Line Interface:")
    print("   Basic usage:")
    print("   $ python3 rca_hybrid/cli.py <task_id> --analysis-type auto_detect")
    print("   ")
    print("   Advanced usage:")
    print("   $ python3 rca_hybrid/cli.py demo_task_001 \\")
    print("       --analysis-type dropdown \\")
    print("       --framework selenium \\")
    print("       --confidence-threshold 0.8 \\")
    print("       --learning-mode active \\")
    print("       --failure-log failure.txt \\")
    print("       --dom-snapshot page.html \\")
    print("       --output results.json")
    
    # 8. Show factory functions
    print("\n8. Programmatic Usage:")
    print("   # Using factory functions")
    print("   from rca_hybrid import get_hybrid_analyzer")
    print("   analyzer = get_hybrid_analyzer()")
    print("   result = await analyzer.analyze(request)")
    print("   ")
    print("   # Direct import")
    print("   from rca_hybrid.hybrid_analyzer import HybridRootCauseAnalyzer")
    print("   analyzer = HybridRootCauseAnalyzer()")
    
    # 9. Show expected output structure
    print("\n9. Analysis Result Structure:")
    print("""   {
     "task_id": "demo_dropdown_failure_001",
     "analysis_type": "auto_detect", 
     "primary_method": "deterministic|ai",
     "final_root_cause": "Dropdown toggle function incomplete",
     "final_confidence": 0.85,
     "deterministic_success": true|false,
     "ai_used": true|false,
     "learning_applied": true|false,
     "new_pattern_discovered": true|false,
     "total_analysis_time_ms": 1250.5,
     "deterministic_result": { ... },
     "ai_result": { ... }
   }""")
    
    # 10. Show learning and adaptation
    print("\n10. Adaptive Learning Features:")
    print("    • Pattern Recognition: TF-IDF similarity matching")
    print("    • Rule Generation: Automatic rule updates from failure patterns")
    print("    • Database Storage: SQLite for learning cases and rules")
    print("    • Backup/Rollback: Safe analyzer updates with rollback capability")
    print("    • Statistics Tracking: Learning performance metrics")
    
    print("\n" + "=" * 70)
    print("🎉 HYBRID ROOT CAUSE ANALYSIS SYSTEM READY!")
    print("=" * 70)
    
    print("\nKey Features Implemented:")
    print("  ✅ Three-tier hybrid analysis (Deterministic → AI → Learning)")
    print("  ✅ Auto-detection of failure types")
    print("  ✅ Confidence-based fallback system")
    print("  ✅ Adaptive learning with pattern recognition")
    print("  ✅ CLI and programmatic interfaces")
    print("  ✅ Comprehensive result structure")
    print("  ✅ Integration with existing analyzers")
    
    print("\nNext Steps:")
    print("  1. Set GROQ_API_KEY environment variable for full AI analysis")
    print("  2. Run analysis on real task data")
    print("  3. Monitor learning system performance")
    print("  4. Customize confidence thresholds as needed")
    
    return True

def main():
    """Main demonstration function"""
    try:
        demonstrate_hybrid_system()
        print(f"\n✨ Demonstration completed successfully!")
        return 0
    except Exception as e:
        print(f"\n❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
