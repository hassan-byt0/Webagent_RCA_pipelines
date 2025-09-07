#!/usr/bin/env python3
"""
Usage examples for the Deterministic Dropdown Root Cause Analyzer
Demonstrates different ways to provide input data and run analysis
"""
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from r_det_dropdown.step_parser import DropdownStepParser
from r_det_dropdown.deterministic_analyzer import DeterministicDropdownAnalyzer
from r_det_dropdown.models import TaskResult
from datetime import datetime

def example_1_json_input():
    """Example 1: Using JSON input format"""
    print("📝 Example 1: JSON Input Format")
    print("-" * 40)
    
    json_steps = {
        "steps": [
            {
                "step_number": 1,
                "name": "Initial Element Detection", 
                "action": "Detected dropdown menu successfully",
                "success": True,
                "timing_ms": 200,
                "elements_detected": ["dropdown", "select"]
            },
            {
                "step_number": 2,
                "name": "Primary Category Navigation",
                "action": "Clicked Men category option", 
                "success": True,
                "timing_ms": 350
            },
            {
                "step_number": 3,
                "name": "Subcategory Selection Validation",
                "action": "Selected Clothing instead of Shoes",
                "success": False,
                "error_message": "Agent selected wrong subcategory"
            },
            {
                "step_number": 4,
                "name": "Filter Application Verification", 
                "action": "Nike filter not applied",
                "success": False
            },
            {
                "step_number": 5,
                "name": "Product Analysis and Selection",
                "action": "Product analysis not attempted",
                "success": False
            },
            {
                "step_number": 6,
                "name": "Transaction Completion",
                "action": "Transaction not completed", 
                "success": False
            }
        ]
    }
    
    # Parse steps
    parser = DropdownStepParser()
    steps = parser.parse_steps_from_input(json.dumps(json_steps))
    
    # Run analysis
    analyzer = DeterministicDropdownAnalyzer()
    
    task_result = TaskResult(
        task_id="json_example_001",
        timestamp=datetime.now(),
        task_type="dropdown_workflow",
        status="failed",
        steps=steps
    )
    
    result = analyzer.analyze_task(
        task_result=task_result,
        failure_log="Agent reasoning error: Selected first available option",
        dom_snapshot="<div class='dropdown'>men women</div><div class='subcategory'>clothing shoes</div>", 
        action_sequence=[
            {"type": "click", "target": "dropdown", "success": True},
            {"type": "click", "target": "men", "success": True, "timing_ms": 350},
            {"type": "click", "target": "clothing", "success": True}  # Wrong choice
        ],
        framework="react"
    )
    
    print(f"✅ Result: {result.root_cause.value}")
    print(f"📍 Failure Step: {result.failure_step}")
    return result

def example_2_text_input():
    """Example 2: Using plain text input format"""
    print("\n📝 Example 2: Plain Text Input Format")
    print("-" * 40)
    
    text_steps = """
    Step 1: Dropdown detection - success (200ms)
    Step 2: Men category clicked - success (350ms) 
    Step 3: Selected Clothing instead of Shoes - failed
    Step 4: Nike filter application - failed
    Step 5: Product price analysis - failed  
    Step 6: Checkout process - failed
    """
    
    # Parse steps
    parser = DropdownStepParser()
    steps = parser.parse_steps_from_input(text_steps)
    
    # Run analysis
    analyzer = DeterministicDropdownAnalyzer()
    
    task_result = TaskResult(
        task_id="text_example_001",
        timestamp=datetime.now(),
        task_type="dropdown_workflow", 
        status="failed",
        steps=steps
    )
    
    result = analyzer.analyze_task(
        task_result=task_result,
        failure_log="Agent made incorrect subcategory selection",
        dom_snapshot="<select><option>men</option></select><ul><li>clothing</li><li>shoes</li></ul>",
        action_sequence=[
            {"type": "click", "target": "men", "success": True, "timing_ms": 350},
            {"type": "click", "target": "clothing", "success": True}
        ],
        framework="vue"
    )
    
    print(f"✅ Result: {result.root_cause.value}")
    print(f"📍 Failure Step: {result.failure_step}")
    return result

def example_3_dict_input():
    """Example 3: Using dictionary input format"""
    print("\n📝 Example 3: Dictionary Input Format")
    print("-" * 40)
    
    dict_steps = {
        "step_1": {
            "action": "dropdown detection", 
            "success": True,
            "timing_ms": 150
        },
        "step_2": {
            "action": "men category navigation",
            "success": True, 
            "timing_ms": 50  # Too fast!
        },
        "step_3": {
            "action": "subcategory selection",
            "success": False
        }
    }
    
    # Parse steps
    parser = DropdownStepParser()
    steps = parser.parse_steps_from_input(dict_steps)
    
    # Run analysis
    analyzer = DeterministicDropdownAnalyzer()
    
    task_result = TaskResult(
        task_id="dict_example_001",
        timestamp=datetime.now(),
        task_type="dropdown_workflow",
        status="failed", 
        steps=steps
    )
    
    result = analyzer.analyze_task(
        task_result=task_result,
        failure_log="Action performed too quickly",
        dom_snapshot="<nav class='dropdown'>men women</nav>",
        action_sequence=[
            {"type": "click", "target": "dropdown", "success": True},
            {"type": "click", "target": "men", "success": True, "timing_ms": 50}
        ],
        framework="angular"
    )
    
    print(f"✅ Result: {result.root_cause.value}")
    print(f"📍 Failure Step: {result.failure_step}")
    return result

def example_4_different_failures():
    """Example 4: Demonstrating different types of failures"""
    print("\n📝 Example 4: Different Failure Types")
    print("-" * 40)
    
    failure_scenarios = [
        {
            "name": "DOM Parsing Failure",
            "dom_snapshot": "",  # No dropdown found
            "action_sequence": [],
            "expected": "DOM_PARSING_FAILURE"
        },
        {
            "name": "Element Interaction Failure", 
            "dom_snapshot": "<div class='dropdown'>menu</div>",
            "action_sequence": [
                {"type": "click", "target": "dropdown", "success": False}  # Interaction failed
            ],
            "expected": "ELEMENT_INTERACTION_FAILURE"
        },
        {
            "name": "Website State Failure",
            "dom_snapshot": "<div class='dropdown'>men</div><div class='products'>nike shoes</div>",
            "action_sequence": [
                {"type": "click", "target": "dropdown", "success": True},
                {"type": "click", "target": "men", "success": True, "timing_ms": 600},
                {"type": "click", "target": "shoes", "success": True},
                {"type": "click", "target": "nike", "success": True}
            ],
            "failure_log": "Server error 500: Internal server error",
            "expected": "WEBSITE_STATE_FAILURE"
        }
    ]
    
    analyzer = DeterministicDropdownAnalyzer()
    
    for scenario in failure_scenarios:
        print(f"\n🧪 Testing: {scenario['name']}")
        
        # Create minimal steps for this scenario
        steps = [
            {"step_number": 1, "name": "Initial Element Detection", "action": "test", "success": False}
        ]
        
        parser = DropdownStepParser()
        parsed_steps = parser.parse_steps_from_input(steps)
        
        task_result = TaskResult(
            task_id=f"scenario_{scenario['name'].lower().replace(' ', '_')}",
            timestamp=datetime.now(),
            task_type="dropdown_workflow",
            status="failed",
            steps=parsed_steps
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
        status = "✅" if actual == expected else "❌"
        
        print(f"  {status} Expected: {expected}")
        print(f"     Got: {actual}")

def example_5_complete_workflow():
    """Example 5: Complete successful workflow"""
    print("\n📝 Example 5: Successful Workflow")
    print("-" * 40)
    
    successful_steps = [
        {
            "step_number": 1,
            "name": "Initial Element Detection",
            "action": "Successfully detected and interacted with dropdown",
            "success": True,
            "timing_ms": 250
        },
        {
            "step_number": 2, 
            "name": "Primary Category Navigation",
            "action": "Successfully clicked Men category",
            "success": True,
            "timing_ms": 600
        },
        {
            "step_number": 3,
            "name": "Subcategory Selection Validation", 
            "action": "Successfully selected Shoes subcategory",
            "success": True
        },
        {
            "step_number": 4,
            "name": "Filter Application Verification",
            "action": "Successfully applied Nike filter and grid updated",
            "success": True
        },
        {
            "step_number": 5,
            "name": "Product Analysis and Selection",
            "action": "Successfully analyzed prices and selected cheapest",
            "success": True
        },
        {
            "step_number": 6,
            "name": "Transaction Completion",
            "action": "Successfully added to cart and completed checkout", 
            "success": True
        }
    ]
    
    parser = DropdownStepParser()
    steps = parser.parse_steps_from_input(successful_steps)
    
    analyzer = DeterministicDropdownAnalyzer()
    
    task_result = TaskResult(
        task_id="successful_workflow_001",
        timestamp=datetime.now(),
        task_type="dropdown_workflow",
        status="success",
        steps=steps
    )
    
    result = analyzer.analyze_task(
        task_result=task_result,
        failure_log="",
        dom_snapshot="<div class='dropdown'>men women</div><div>shoes clothing</div><div>nike adidas</div><div>$19.99 $29.99</div><div>cart checkout</div>",
        action_sequence=[
            {"type": "click", "target": "dropdown", "success": True},
            {"type": "click", "target": "men", "success": True, "timing_ms": 600},
            {"type": "click", "target": "shoes", "success": True},
            {"type": "click", "target": "nike", "success": True},
            {"type": "click", "target": "cheapest_product", "success": True},
            {"type": "click", "target": "cart", "success": True},
            {"type": "click", "target": "checkout", "success": True}
        ],
        framework="bootstrap"
    )
    
    print(f"✅ Result: {result.root_cause.value}")
    print(f"📍 Failure Step: {result.failure_step}")
    return result

def save_results(results):
    """Save all results to a file"""
    output_file = Path(__file__).parent / "usage_examples_results.json"
    
    results_data = []
    for result in results:
        if result:
            results_data.append(result.to_dict())
    
    with open(output_file, 'w') as f:
        json.dump(results_data, f, indent=2, default=str)
    
    print(f"\n📁 All results saved to: {output_file}")

def main():
    """Run all usage examples"""
    print("🚀 Deterministic Dropdown Analyzer - Usage Examples")
    print("=" * 60)
    
    results = []
    
    try:
        # Run all examples
        results.append(example_1_json_input())
        results.append(example_2_text_input()) 
        results.append(example_3_dict_input())
        example_4_different_failures()  # This doesn't return results
        results.append(example_5_complete_workflow())
        
        # Save results
        save_results(results)
        
        print("\n" + "=" * 60)
        print("🎉 All usage examples completed successfully!")
        print("\n💡 Key Features Demonstrated:")
        print("  • Multiple input formats (JSON, text, dictionary)")
        print("  • Different failure types detection")
        print("  • Framework-specific analysis")
        print("  • Complete workflow validation")
        print("  • Deterministic root cause classification")
        
    except Exception as e:
        print(f"❌ Error in usage examples: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
