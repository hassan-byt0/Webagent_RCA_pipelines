#!/usr/bin/env python3
"""
Simple test to verify the deterministic dropdown analyzer works
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from r_det_dropdown.step_parser import DropdownStepParser
from r_det_dropdown.deterministic_analyzer import DeterministicDropdownAnalyzer
from r_det_dropdown.models import TaskResult
from datetime import datetime

def simple_test():
    print("🔍 Simple Deterministic Dropdown Test")
    print("=" * 40)
    
    # Create test steps
    steps_data = [
        {
            "step_number": 1,
            "name": "Initial Element Detection",
            "action": "Detected dropdown",
            "success": True
        },
        {
            "step_number": 2,
            "name": "Primary Category Navigation", 
            "action": "Clicked Men",
            "success": True,
            "timing_ms": 300
        },
        {
            "step_number": 3,
            "name": "Subcategory Selection Validation",
            "action": "Selected Clothing instead of Shoes",
            "success": False
        }
    ]
    
    # Parse steps
    parser = DropdownStepParser()
    steps = parser.parse_steps_from_input(steps_data)
    print(f"✅ Parsed {len(steps)} steps")
    
    # Create task result
    task_result = TaskResult(
        task_id="simple_test_001",
        timestamp=datetime.now(),
        task_type="dropdown_workflow",
        status="failed",
        steps=steps
    )
    
    # Run analysis
    analyzer = DeterministicDropdownAnalyzer()
    result = analyzer.analyze_task(
        task_result=task_result,
        failure_log="Agent selected wrong subcategory",
        dom_snapshot="<div class='dropdown'>men</div><div>clothing shoes</div>",
        action_sequence=[
            {"type": "click", "target": "dropdown", "success": True},
            {"type": "click", "target": "men", "success": True, "timing_ms": 300},
            {"type": "click", "target": "clothing", "success": True}
        ],
        framework="react"
    )
    
    print(f"🎯 Root Cause: {result.root_cause.value}")
    print(f"📍 Failure Step: {result.failure_step}")
    print(f"🛠️  Framework: {result.framework}")
    
    print("\n📊 Step Results:")
    for step in result.steps:
        status = "✅" if step.success else "❌"
        print(f"  {status} Step {step.step_number}: {step.step_name}")
    
    print("\n🎉 Test completed successfully!")
    return result

if __name__ == "__main__":
    simple_test()
