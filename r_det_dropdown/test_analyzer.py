#!/usr/bin/env python3
"""
Test script for Deterministic Dropdown Analysis
Demonstrates usage with sample data
"""
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from r_det_dropdown.step_parser import DropdownStepParser
from r_det_dropdown.deterministic_analyzer import DeterministicDropdownAnalyzer
from r_det_dropdown.models import TaskResult, DropdownStep
from datetime import datetime

def create_sample_task_data():
    """Create sample task data for testing"""
    
    # Sample steps in different formats
    sample_steps_json = """
    {
        "steps": [
            {
                "step_number": 1,
                "name": "Initial Element Detection",
                "action": "Detect dropdown elements",
                "success": true,
                "timing_ms": 250,
                "elements_detected": ["dropdown", "menu"]
            },
            {
                "step_number": 2, 
                "name": "Primary Category Navigation",
                "action": "Click Men category",
                "success": true,
                "timing_ms": 300
            },
            {
                "step_number": 3,
                "name": "Subcategory Selection Validation", 
                "action": "Selected Clothing instead of Shoes",
                "success": false,
                "error_message": "Wrong subcategory selected"
            }
        ]
    }
    """
    
    sample_steps_text = """
    Step 1: Dropdown detected successfully (250ms)
    Step 2: Men category clicked - success (300ms)  
    Step 3: Selected Clothing instead of Shoes - failed
    Step 4: Nike filter not applied - failed
    Step 5: Price elements not found - failed
    Step 6: Checkout not attempted - failed
    """
    
    return sample_steps_json, sample_steps_text

def test_step_parser():
    """Test the step parser with different formats"""
    print("🧪 Testing Step Parser")
    print("=" * 50)
    
    parser = DropdownStepParser()
    sample_json, sample_text = create_sample_task_data()
    
    # Test JSON parsing
    print("📝 Testing JSON format:")
    steps_from_json = parser.parse_steps_from_input(sample_json)
    for step in steps_from_json:
        print(f"  Step {step.step_number}: {step.step_name} - {'✅' if step.success else '❌'}")
    
    print("\n📝 Testing text format:")
    steps_from_text = parser.parse_steps_from_input(sample_text)
    for step in steps_from_text:
        print(f"  Step {step.step_number}: {step.step_name} - {'✅' if step.success else '❌'}")
    
    return steps_from_json

def test_deterministic_analyzer(steps):
    """Test the deterministic analyzer"""
    print("\n🔍 Testing Deterministic Analyzer")
    print("=" * 50)
    
    analyzer = DeterministicDropdownAnalyzer()
    
    # Create sample task result
    task_result = TaskResult(
        task_id="test_task_001",
        timestamp=datetime.now(),
        task_type="dropdown_workflow",
        status="failed",
        steps=steps
    )
    
    # Sample data for analysis
    failure_log = """
    ERROR: Agent selected 'Clothing' instead of 'Shoes' subcategory
    Agent reasoning: Selected first available option without considering requirement
    """
    
    dom_snapshot = """
    <div class="dropdown-menu">
        <option value="men">Men</option>
        <option value="women">Women</option>
    </div>
    <div class="subcategory">
        <option value="clothing">Clothing</option>
        <option value="shoes">Shoes</option>
    </div>
    """
    
    action_sequence = [
        {"type": "click", "target": "dropdown", "success": True},
        {"type": "click", "target": "men", "success": True, "timing_ms": 300},
        {"type": "click", "target": "clothing", "success": True},  # Wrong choice
        {"type": "click", "target": "nike_filter", "success": False}
    ]
    
    framework = "react"
    
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
    print(f"  Total Steps: {len(result.steps)}")
    
    print(f"\n📊 Step Analysis:")
    for step in result.steps:
        status = "✅ PASS" if step.success else "❌ FAIL"
        print(f"  Step {step.step_number}: {step.step_name} - {status}")
        if step.timing_ms:
            print(f"    ⏱️  Timing: {step.timing_ms}ms")
        if step.error_message:
            print(f"    ⚠️  Error: {step.error_message}")
    
    return result

def test_algorithm_scenarios():
    """Test different failure scenarios"""
    print("\n🎭 Testing Different Scenarios")
    print("=" * 50)
    
    analyzer = DeterministicDropdownAnalyzer()
    
    scenarios = [
        {
            "name": "DOM Parsing Failure",
            "dom_snapshot": "",  # Empty DOM
            "action_sequence": [],
            "failure_log": "",
            "expected": "DOM_PARSING_FAILURE"
        },
        {
            "name": "Agent Reasoning Failure", 
            "dom_snapshot": "<div class='dropdown'>dropdown</div><div>men clothing shoes nike</div>",
            "action_sequence": [
                {"type": "click", "target": "dropdown", "success": True},
                {"type": "click", "target": "men", "success": True},
                {"type": "click", "target": "clothing", "success": True}  # Wrong choice - should be shoes
            ],
            "failure_log": "",
            "expected": "AGENT_REASONING_FAILURE"
        },
        {
            "name": "Dynamic Content Failure",
            "dom_snapshot": "<div class='dropdown'>dropdown</div><div>men</div>",
            "action_sequence": [
                {"type": "click", "target": "dropdown", "success": True},
                {"type": "click", "target": "men", "success": True, "timing_ms": 100}  # Too fast
            ],
            "failure_log": "",
            "expected": "DYNAMIC_CONTENT_FAILURE"
        },
        {
            "name": "Element Interaction Failure",
            "dom_snapshot": "<div class='dropdown'>dropdown</div><div>men shoes nike $19.99 cart checkout</div>",
            "action_sequence": [
                {"type": "click", "target": "dropdown", "success": True},
                {"type": "click", "target": "men", "success": True, "timing_ms": 600},
                {"type": "click", "target": "shoes", "success": True},
                {"type": "click", "target": "nike", "success": True},
                {"type": "click", "target": "product", "success": True},
                {"type": "click", "target": "cart", "success": True},
                {"type": "click", "target": "checkout", "success": False}  # Checkout fails
            ],
            "failure_log": "",
            "expected": "ELEMENT_INTERACTION_FAILURE"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n🧪 Scenario: {scenario['name']}")
        
        task_result = TaskResult(
            task_id=f"scenario_{scenario['name'].lower().replace(' ', '_')}",
            timestamp=datetime.now(),
            task_type="dropdown_workflow", 
            status="failed"
        )
        
        result = analyzer.analyze_task(
            task_result=task_result,
            failure_log=scenario.get("failure_log", ""),
            dom_snapshot=scenario["dom_snapshot"],
            action_sequence=scenario["action_sequence"],
            framework="react"
        )
        
        expected = scenario["expected"]
        actual = result.root_cause.value
        
        if actual == expected:
            print(f"  ✅ PASS: Expected {expected}, got {actual}")
        else:
            print(f"  ❌ FAIL: Expected {expected}, got {actual}")

def main():
    """Main test function"""
    print("🚀 Deterministic Dropdown Analysis Test Suite")
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
        output_file = Path(__file__).parent / "sample_analysis_result.json"
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
