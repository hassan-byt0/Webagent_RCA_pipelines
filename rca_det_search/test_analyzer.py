#!/usr/bin/env python3
"""
Test script for Deterministic ArXiv Search Analysis
Demonstrates usage with sample data
"""
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from step_parser import ArxivStepParser
    from deterministic_analyzer import DeterministicArxivAnalyzer
    from models import TaskResult, ArxivSearchStep
    from config import RootCauseType
except ImportError:
    from rca_det_search.step_parser import ArxivStepParser
    from rca_det_search.deterministic_analyzer import DeterministicArxivAnalyzer
    from rca_det_search.models import TaskResult, ArxivSearchStep
    from rca_det_search.config import RootCauseType

from datetime import datetime

def create_sample_task_data():
    """Create sample task data for testing"""
    
    # Sample steps in different formats
    sample_steps_json = """
    {
        "steps": [
            {
                "step_number": 1,
                "name": "Navigation and Page Load Verification",
                "action": "Navigate to ArXiv advanced search page",
                "success": true,
                "timing_ms": 1200,
                "elements_detected": ["arxiv", "advanced search"]
            },
            {
                "step_number": 2, 
                "name": "Author Input Field Analysis",
                "action": "Input author name and use dropdown",
                "success": false,
                "error_message": "Agent entered wrong author name (hallucination)",
                "failure_classification": "hallucination"
            },
            {
                "step_number": 3,
                "name": "Classification Label Processing", 
                "action": "Select CS+Math classification",
                "success": false,
                "error_message": "Classification options not loaded"
            }
        ]
    }
    """
    
    sample_steps_text = """
    Step 1: ArXiv page navigation - success (1200ms)
    Step 2: Author input with hallucination - failed
    Step 3: Classification selection - failed (options not loaded)
    Step 4: Date input not attempted - failed
    Step 5: Search not executed - failed
    """
    
    return sample_steps_json, sample_steps_text

def test_step_parser():
    """Test the step parser with different formats"""
    print("🧪 Testing ArXiv Step Parser")
    print("=" * 50)
    
    parser = ArxivStepParser()
    sample_json, sample_text = create_sample_task_data()
    
    # Test JSON parsing
    print("📝 Testing JSON format:")
    steps_from_json = parser.parse_steps_from_input(sample_json)
    for step in steps_from_json:
        print(f"  Step {step.step_number}: {step.step_name} - {'✅' if step.success else '❌'}")
        if step.failure_classification:
            print(f"    🏷️  Failure type: {step.failure_classification}")
    
    print("\n📝 Testing text format:")
    steps_from_text = parser.parse_steps_from_input(sample_text)
    for step in steps_from_text:
        print(f"  Step {step.step_number}: {step.step_name} - {'✅' if step.success else '❌'}")
    
    return steps_from_json

def test_deterministic_analyzer(steps):
    """Test the deterministic analyzer"""
    print("\n🔍 Testing Deterministic ArXiv Analyzer")
    print("=" * 50)
    
    analyzer = DeterministicArxivAnalyzer()
    
    # Create sample task result
    task_result = TaskResult(
        task_id="arxiv_test_001",
        timestamp=datetime.now(),
        task_type="arxiv_search",
        status="failed",
        steps=steps
    )
    
    # Sample data for analysis
    failure_log = """
    ERROR: Agent entered wrong author name - hallucination detected
    Agent reasoning: Made up author name instead of using provided requirement
    """
    
    dom_snapshot = """
    <div class="arxiv-search">
        <input class="author" placeholder="Author name">
        <div class="author-dropdown" style="display:none">
            <div class="suggestion">John Doe</div>
        </div>
        <div class="classification">
            <option value="cs">Computer Science</option>
            <option value="math">Mathematics</option>
        </div>
        <input class="date" type="date">
        <button class="search">Search</button>
    </div>
    """
    
    action_sequence = [
        {"type": "input", "target": "author", "success": False, "value": "fake_author_name"},
        {"type": "select", "target": "classification", "success": False},
        {"type": "input", "target": "date", "success": False},
        {"type": "click", "target": "search", "success": False}
    ]
    
    framework = "angular"
    
    # Run analysis
    result = analyzer.analyze_task(
        task_result=task_result,
        failure_log=failure_log,
        dom_snapshot=dom_snapshot,
        action_sequence=action_sequence,
        framework=framework
    )
    
    # Print results
    print(f"🎯 Analysis Results:")
    print(f"  Task ID: {result.task_id}")
    print(f"  Framework: {result.framework}")
    print(f"  Root Cause: {result.root_cause.value}")
    print(f"  Failure Step: {result.failure_step}")
    if result.author_failure_type:
        print(f"  Author Failure: {result.author_failure_type.value}")
    if result.date_failure_type:
        print(f"  Date Failure: {result.date_failure_type.value}")
    print(f"  Total Steps: {len(result.steps)}")
    
    print(f"\n📊 Step Analysis:")
    for step in result.steps:
        status = "✅ PASS" if step.success else "❌ FAIL"
        print(f"  Step {step.step_number}: {step.step_name} - {status}")
        if step.timing_ms:
            print(f"    ⏱️  Timing: {step.timing_ms}ms")
        if step.error_message:
            print(f"    ⚠️  Error: {step.error_message}")
        if step.failure_classification:
            print(f"    🏷️  Classification: {step.failure_classification}")
    
    return result

def test_algorithm_scenarios():
    """Test different failure scenarios"""
    print("\n🎭 Testing Different ArXiv Scenarios")
    print("=" * 50)
    
    analyzer = DeterministicArxivAnalyzer()
    
    scenarios = [
        {
            "name": "Website State Failure (Captcha)",
            "dom_snapshot": "<div class='captcha'>Please solve captcha</div>",
            "action_sequence": [],
            "failure_log": "ArXiv page failed to load",
            "expected": "WEBSITE_STATE_FAILURE"
        },
        {
            "name": "DOM Parsing Failure (Author Input)",
            "dom_snapshot": "<div>no author input found</div>",
            "action_sequence": [],
            "failure_log": "",
            "expected": "DOM_PARSING_FAILURE"
        },
        {
            "name": "Agent Reasoning Failure (Author Hallucination)",
            "dom_snapshot": "<input class='author'><div class='author-dropdown'></div><div class='classification'></div><input class='date'><button class='search'></button>",
            "action_sequence": [
                {"type": "input", "target": "author", "success": False, "value": "hallucinated_name"}
            ],
            "failure_log": "Agent entered wrong author name - hallucination",
            "expected": "AGENT_REASONING_FAILURE"
        },
        {
            "name": "Dynamic Content Failure (Classification)",
            "dom_snapshot": "<input class='author'><div class='author-dropdown'></div><div class='classification'></div><input class='date'><button class='search'></button>",
            "action_sequence": [
                {"type": "input", "target": "author", "success": True, "value": "valid_author"},
                {"type": "select", "target": "classification", "success": False}
            ],
            "failure_log": "",
            "expected": "DYNAMIC_CONTENT_FAILURE"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🧪 Scenario: {scenario['name']}")
        
        task_result = TaskResult(
            task_id=f"scenario_{scenario['name'].lower().replace(' ', '_')}",
            timestamp=datetime.now(),
            task_type="arxiv_search", 
            status="failed"
        )
        
        result = analyzer.analyze_task(
            task_result=task_result,
            failure_log=scenario["failure_log"],
            dom_snapshot=scenario["dom_snapshot"],
            action_sequence=scenario["action_sequence"],
            framework="angular"
        )
        
        expected = scenario["expected"]
        actual = result.root_cause.value
        
        if actual == expected:
            print(f"  ✅ PASS: Expected {expected}, got {actual}")
        else:
            print(f"  ❌ FAIL: Expected {expected}, got {actual}")

def main():
    """Main test function"""
    print("🚀 Deterministic ArXiv Search Analysis Test Suite")
    print("=" * 60)
    
    try:
        # Test step parser
        steps = test_step_parser()
        
        # Test analyzer
        result = test_deterministic_analyzer(steps)
        
        # Test different scenarios
        test_algorithm_scenarios()
        
        print("\n" + "=" * 60)
        print("🎉 All tests completed!")
        
        # Save sample result
        output_file = Path(__file__).parent / "sample_arxiv_analysis_result.json"
        with open(output_file, 'w') as f:
            json.dump(result.to_dict(), f, indent=2, default=str)
        print(f"📁 Sample result saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
