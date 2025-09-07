#!/usr/bin/env python3
"""
Example: How to provide input to the Hybrid Root Cause Analysis Algorithm
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rca_hybrid.hybrid_analyzer import HybridRootCauseAnalyzer
from rca_hybrid.models import HybridAnalysisRequest
from rca_hybrid.config import HybridAnalysisType, LearningMode

async def example_input_methods():
    """Demonstrate different ways to provide input to the algorithm"""
    
    print("=" * 60)
    print("HOW TO PROVIDE INPUT TO THE HYBRID ALGORITHM")
    print("=" * 60)
    
    # Initialize the analyzer
    analyzer = HybridRootCauseAnalyzer(
        confidence_threshold=0.75,
        learning_mode=LearningMode.ACTIVE
    )
    
    # METHOD 1: Complete Input Structure
    print("\n1. COMPLETE INPUT STRUCTURE:")
    print("-" * 40)
    
    class TaskResult:
        """Your task result object"""
        def __init__(self):
            self.reasoning_files = {
                "agent_log.txt": "Failed to click element #submit-btn. Timeout after 30s.",
                "selenium_log.txt": "ElementNotInteractableException: Element is not clickable"
            }
            self.db_data = {
                "actions": [
                    {"type": "navigate", "url": "https://example.com", "success": True},
                    {"type": "click", "element": "#dropdown-trigger", "success": True},
                    {"type": "wait", "duration": 5000},
                    {"type": "click", "element": "#option-1", "success": False}
                ],
                "errors": ["Element not found: #option-1"],
                "timeouts": [{"element": "#option-1", "duration": 30000}]
            }
    
    # Create the complete request
    request = HybridAnalysisRequest(
        task_id="example_task_001",
        analysis_type=HybridAnalysisType.AUTO_DETECT,  # Let algorithm decide
        task_result=TaskResult(),
        failure_log="""
ERROR: Failed to complete dropdown selection
- Successfully clicked dropdown trigger
- Dropdown appeared to expand
- Target option #option-1 not found
- Operation timed out after 30 seconds
- Browser: Chrome 120.0
- Framework: Selenium WebDriver
""",
        dom_snapshot="""
<div class="form-container">
    <select id="dropdown-trigger" class="custom-dropdown">
        <option value="">Select an option</option>
    </select>
    <div id="dropdown-options" style="display: none;">
        <div class="option" data-value="1">Option 1</div>
        <div class="option" data-value="2">Option 2</div>
    </div>
</div>
""",
        action_sequence=[
            {"step": 1, "action": "click", "element": "#dropdown-trigger"},
            {"step": 2, "action": "wait", "duration": 5000},
            {"step": 3, "action": "click", "element": "#option-1", "failed": True}
        ],
        framework="selenium_chrome"
    )
    
    print("✓ Request created with all fields populated")
    print(f"  Task ID: {request.task_id}")
    print(f"  Analysis Type: {request.analysis_type.value}")
    print(f"  Framework: {request.framework}")
    
    # METHOD 2: Minimal Input (Required Fields Only)
    print("\n2. MINIMAL INPUT (Required Fields Only):")
    print("-" * 40)
    
    minimal_request = HybridAnalysisRequest(
        task_id="minimal_example",
        analysis_type=HybridAnalysisType.AUTO_DETECT,
        task_result=TaskResult(),  # Can be minimal
        failure_log="Element not clickable",
        dom_snapshot="<button id='btn'>Click me</button>",
        action_sequence=[{"action": "click", "element": "#btn"}],
        framework="selenium"
    )
    
    print("✓ Minimal request created")
    print("  Only required fields provided")
    
    # METHOD 3: Specific Algorithm Input
    print("\n3. SPECIFIC ALGORITHM INPUT:")
    print("-" * 40)
    
    # For dropdown-specific analysis
    dropdown_request = HybridAnalysisRequest(
        task_id="dropdown_specific",
        analysis_type=HybridAnalysisType.DROPDOWN,  # Force dropdown algorithm
        task_result=TaskResult(),
        failure_log="Dropdown cascade failure",
        dom_snapshot="<select><option>Item 1</option></select>",
        action_sequence=[{"action": "select", "element": "select"}],
        framework="selenium"
    )
    
    # For ArXiv search analysis
    arxiv_request = HybridAnalysisRequest(
        task_id="arxiv_specific", 
        analysis_type=HybridAnalysisType.ARXIV_SEARCH,  # Force ArXiv algorithm
        task_result=TaskResult(),
        failure_log="Search form submission failed",
        dom_snapshot="<form><input name='query'><button>Search</button></form>",
        action_sequence=[{"action": "submit", "form": "search_form"}],
        framework="selenium"
    )
    
    print("✓ Algorithm-specific requests created")
    print(f"  Dropdown analysis: {dropdown_request.analysis_type.value}")
    print(f"  ArXiv analysis: {arxiv_request.analysis_type.value}")
    
    # Run analysis (example with the first request)
    print("\n4. RUNNING ANALYSIS:")
    print("-" * 40)
    try:
        result = await analyzer.analyze(request)
        print("✓ Analysis completed successfully")
        print(f"  Primary method: {result.primary_method}")
        print(f"  Final confidence: {result.final_confidence:.2f}")
        print(f"  Root cause: {result.final_root_cause}")
    except Exception as e:
        print(f"⚠ Analysis failed (expected without API keys): {e}")
    
    return True

def show_input_field_details():
    """Show detailed explanation of each input field"""
    print("\n" + "=" * 60)
    print("DETAILED INPUT FIELD EXPLANATIONS")
    print("=" * 60)
    
    fields = {
        "task_id": {
            "type": "str",
            "required": True,
            "description": "Unique identifier for the analysis task",
            "example": "dropdown_failure_001"
        },
        "analysis_type": {
            "type": "HybridAnalysisType",
            "required": True,
            "description": "Type of analysis to perform",
            "options": ["DROPDOWN", "ARXIV_SEARCH", "AUTO_DETECT"],
            "example": "HybridAnalysisType.AUTO_DETECT"
        },
        "task_result": {
            "type": "Object",
            "required": True,
            "description": "Your task execution result with reasoning files and database data",
            "fields": {
                "reasoning_files": "Dict of log files with failure information",
                "db_data": "Database information about actions taken"
            }
        },
        "failure_log": {
            "type": "str",
            "required": True,
            "description": "Detailed failure log or error message",
            "example": "ElementNotInteractableException: Element not clickable at coordinates (100, 200)"
        },
        "dom_snapshot": {
            "type": "str",
            "required": True,
            "description": "HTML snapshot of the page at time of failure",
            "example": "<div class='container'><button id='btn'>Click</button></div>"
        },
        "action_sequence": {
            "type": "List[Dict]",
            "required": True,
            "description": "Sequence of actions that led to the failure",
            "example": "[{'action': 'click', 'element': '#btn', 'timestamp': '2025-09-02T10:00:00'}]"
        },
        "framework": {
            "type": "str",
            "required": True,
            "description": "Web automation framework used",
            "examples": ["selenium", "playwright", "puppeteer", "cypress"]
        },
        "confidence_threshold": {
            "type": "float",
            "required": False,
            "description": "Minimum confidence for deterministic analysis",
            "default": 0.75,
            "range": "0.0 - 1.0"
        },
        "learning_mode": {
            "type": "LearningMode",
            "required": False,
            "description": "How aggressively the system should learn",
            "options": ["PASSIVE", "ACTIVE", "AGGRESSIVE"],
            "default": "ACTIVE"
        }
    }
    
    for field, info in fields.items():
        print(f"\n{field.upper()}:")
        print(f"  Type: {info['type']}")
        print(f"  Required: {info['required']}")
        print(f"  Description: {info['description']}")
        
        if 'options' in info:
            print(f"  Options: {info['options']}")
        if 'example' in info:
            print(f"  Example: {info['example']}")
        if 'examples' in info:
            print(f"  Examples: {info['examples']}")
        if 'default' in info:
            print(f"  Default: {info['default']}")
        if 'range' in info:
            print(f"  Range: {info['range']}")
        if 'fields' in info:
            print(f"  Fields:")
            for subfield, subdesc in info['fields'].items():
                print(f"    - {subfield}: {subdesc}")

def show_cli_input_examples():
    """Show CLI input examples"""
    print("\n" + "=" * 60)
    print("COMMAND LINE INPUT EXAMPLES")
    print("=" * 60)
    
    examples = [
        {
            "name": "Basic Analysis",
            "command": "python3 rca_hybrid/cli.py my_task_001",
            "description": "Analyze task with default settings"
        },
        {
            "name": "Dropdown-Specific Analysis",
            "command": "python3 rca_hybrid/cli.py dropdown_task --analysis-type dropdown",
            "description": "Force dropdown algorithm"
        },
        {
            "name": "With Input Files",
            "command": """python3 rca_hybrid/cli.py task_001 \\
    --failure-log error_log.txt \\
    --dom-snapshot page_snapshot.html \\
    --output results.json""",
            "description": "Use files as input and save results"
        },
        {
            "name": "Advanced Configuration",
            "command": """python3 rca_hybrid/cli.py advanced_task \\
    --analysis-type auto_detect \\
    --framework selenium \\
    --confidence-threshold 0.8 \\
    --learning-mode aggressive \\
    --verbose""",
            "description": "Custom thresholds and learning mode"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['name'].upper()}:")
        print(f"   {example['description']}")
        print(f"   Command:")
        print(f"   {example['command']}")

async def main():
    """Main demonstration"""
    await example_input_methods()
    show_input_field_details()
    show_cli_input_examples()
    
    print("\n" + "=" * 60)
    print("📋 QUICK START CHECKLIST")
    print("=" * 60)
    print("1. ✓ Import the analyzer: from rca_hybrid.hybrid_analyzer import HybridRootCauseAnalyzer")
    print("2. ✓ Create your task result object with reasoning files and database data")
    print("3. ✓ Build HybridAnalysisRequest with your failure data")
    print("4. ✓ Call analyzer.analyze(request) to get results")
    print("5. ✓ Or use CLI: python3 rca_hybrid/cli.py <task_id> [options]")
    
    print("\n💡 TIP: Start with AUTO_DETECT analysis type - the algorithm will choose the best approach!")

if __name__ == "__main__":
    asyncio.run(main())
