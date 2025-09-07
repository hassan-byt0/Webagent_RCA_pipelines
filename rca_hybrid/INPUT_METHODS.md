# Hybrid Root Cause Analysis - Input Methods Guide

This guide shows all the different ways to provide input to the hybrid root cause analysis algorithm.

## Table of Contents
1. [Programmatic API Input](#programmatic-api-input)
2. [Command Line Interface (CLI)](#command-line-interface-cli)
3. [File-Based Input](#file-based-input)
4. [Input Field Descriptions](#input-field-descriptions)
5. [Quick Start Examples](#quick-start-examples)

---

## Programmatic API Input

### Method 1: Complete Input Structure

```python
import asyncio
from rca_hybrid.hybrid_analyzer import HybridRootCauseAnalyzer
from rca_hybrid.models import HybridAnalysisRequest
from rca_hybrid.config import HybridAnalysisType, LearningMode

async def analyze_failure():
    # Initialize analyzer
    analyzer = HybridRootCauseAnalyzer(
        confidence_threshold=0.75,
        learning_mode=LearningMode.ACTIVE
    )
    
    # Create your task result object
    class TaskResult:
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
    
    # Create analysis request
    request = HybridAnalysisRequest(
        task_id="dropdown_failure_001",
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
    
    # Run analysis
    result = await analyzer.analyze(request)
    print(f"Root cause: {result.final_root_cause}")
    print(f"Confidence: {result.final_confidence}")
    return result

# Run the analysis
asyncio.run(analyze_failure())
```

### Method 2: Minimal Input (Required Fields Only)

```python
# Minimal example with only required fields
request = HybridAnalysisRequest(
    task_id="minimal_example",
    analysis_type=HybridAnalysisType.AUTO_DETECT,
    task_result=your_task_result,  # Your existing task result object
    failure_log="Element not clickable",
    dom_snapshot="<button id='btn'>Click me</button>",
    action_sequence=[{"action": "click", "element": "#btn"}],
    framework="selenium"
)

analyzer = HybridRootCauseAnalyzer()
result = await analyzer.analyze(request)
```

### Method 3: Algorithm-Specific Input

```python
# Force dropdown algorithm
dropdown_request = HybridAnalysisRequest(
    task_id="dropdown_specific",
    analysis_type=HybridAnalysisType.DROPDOWN,  # Force dropdown algorithm
    task_result=your_task_result,
    failure_log="Dropdown cascade failure",
    dom_snapshot="<select><option>Item 1</option></select>",
    action_sequence=[{"action": "select", "element": "select"}],
    framework="selenium"
)

# Force ArXiv search algorithm
arxiv_request = HybridAnalysisRequest(
    task_id="arxiv_specific", 
    analysis_type=HybridAnalysisType.ARXIV_SEARCH,  # Force ArXiv algorithm
    task_result=your_task_result,
    failure_log="Search form submission failed",
    dom_snapshot="<form><input name='query'><button>Search</button></form>",
    action_sequence=[{"action": "submit", "form": "search_form"}],
    framework="selenium"
)
```

---

## Command Line Interface (CLI)

### Basic Usage

```bash
# Basic analysis with default settings
python3 rca_hybrid/cli.py my_task_001

# Show help
python3 rca_hybrid/cli.py --help
```

### Complete CLI Options

```bash
python3 rca_hybrid/cli.py TASK_ID [OPTIONS]

Options:
  --analysis-type {dropdown,arxiv_search,auto_detect}
                        Type of analysis to perform (default: auto_detect)
  --framework FRAMEWORK
                        Web automation framework used (default: unknown)
  --confidence-threshold CONFIDENCE_THRESHOLD
                        Confidence threshold for deterministic analysis (default: 0.75)
  --learning-mode {passive,active,aggressive}
                        Learning mode for adaptive system (default: active)
  --failure-log FAILURE_LOG
                        Failure log content or path to log file
  --dom-snapshot DOM_SNAPSHOT
                        DOM snapshot content or path to HTML file
  --output, -o OUTPUT   Output file for results (JSON format)
  --verbose, -v         Enable verbose output
```

### CLI Examples

```bash
# 1. Basic analysis
python3 rca_hybrid/cli.py my_task_001

# 2. Dropdown-specific analysis
python3 rca_hybrid/cli.py dropdown_task --analysis-type dropdown

# 3. With input files
python3 rca_hybrid/cli.py task_001 \
    --failure-log error_log.txt \
    --dom-snapshot page_snapshot.html \
    --output results.json

# 4. Advanced configuration
python3 rca_hybrid/cli.py advanced_task \
    --analysis-type auto_detect \
    --framework selenium \
    --confidence-threshold 0.8 \
    --learning-mode aggressive \
    --verbose

# 5. ArXiv search analysis with custom threshold
python3 rca_hybrid/cli.py arxiv_task \
    --analysis-type arxiv_search \
    --framework playwright \
    --confidence-threshold 0.9 \
    --output arxiv_results.json
```

---

## File-Based Input

### Input Files

You can provide input through files:

```bash
# Create input files
echo "ElementNotInteractableException: Element not clickable" > error_log.txt
echo "<button id='btn' disabled>Click me</button>" > page_snapshot.html

# Use files as input
python3 rca_hybrid/cli.py file_task \
    --failure-log error_log.txt \
    --dom-snapshot page_snapshot.html \
    --output results.json
```

### JSON Configuration File

Create a JSON configuration file:

```json
{
    "task_id": "json_config_task",
    "analysis_type": "auto_detect",
    "framework": "selenium",
    "confidence_threshold": 0.8,
    "learning_mode": "active",
    "failure_log": "Element selection failed after multiple retries",
    "dom_snapshot": "<div><select id='dropdown'><option>Item 1</option></select></div>",
    "action_sequence": [
        {"action": "click", "element": "#dropdown"},
        {"action": "select", "option": "Item 2", "failed": true}
    ]
}
```

Then load and use it programmatically:

```python
import json
from rca_hybrid.models import HybridAnalysisRequest
from rca_hybrid.config import HybridAnalysisType, LearningMode

# Load from JSON
with open('config.json') as f:
    config = json.load(f)

# Convert to request object
request = HybridAnalysisRequest(
    task_id=config['task_id'],
    analysis_type=HybridAnalysisType(config['analysis_type'].upper()),
    task_result=your_task_result,
    failure_log=config['failure_log'],
    dom_snapshot=config['dom_snapshot'],
    action_sequence=config['action_sequence'],
    framework=config['framework']
)
```

---

## Input Field Descriptions

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `task_id` | string | Unique identifier for analysis | `"dropdown_failure_001"` |
| `analysis_type` | HybridAnalysisType | Analysis type to perform | `AUTO_DETECT`, `DROPDOWN`, `ARXIV_SEARCH` |
| `task_result` | Object | Your task execution result | Object with `reasoning_files` and `db_data` |
| `failure_log` | string | Detailed failure log or error message | `"ElementNotInteractableException: Element not clickable"` |
| `dom_snapshot` | string | HTML snapshot at time of failure | `"<div><button id='btn'>Click</button></div>"` |
| `action_sequence` | List[Dict] | Actions that led to failure | `[{"action": "click", "element": "#btn"}]` |
| `framework` | string | Web automation framework | `"selenium"`, `"playwright"`, `"puppeteer"` |

### Optional Configuration Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `confidence_threshold` | float | 0.75 | Minimum confidence for deterministic analysis (0.0-1.0) |
| `learning_mode` | LearningMode | ACTIVE | Learning aggressiveness: `PASSIVE`, `ACTIVE`, `AGGRESSIVE` |

### Task Result Object Structure

Your `task_result` object should contain:

```python
class TaskResult:
    def __init__(self):
        self.reasoning_files = {
            # Dictionary of log files with failure information
            "agent_log.txt": "Agent execution log content",
            "selenium_log.txt": "WebDriver log content",
            "browser_console.log": "Browser console errors"
        }
        self.db_data = {
            # Database information about actions taken
            "actions": [
                {"type": "click", "element": "#btn", "success": True},
                {"type": "wait", "duration": 5000},
                {"type": "click", "element": "#missing", "success": False}
            ],
            "errors": ["Element not found: #missing"],
            "timeouts": [{"element": "#missing", "duration": 30000}]
        }
```

---

## Quick Start Examples

### 1. From Your Web Agent Code

```python
# In your web agent failure handling
async def handle_task_failure(task_result):
    from rca_hybrid.hybrid_analyzer import HybridRootCauseAnalyzer
    from rca_hybrid.models import HybridAnalysisRequest
    from rca_hybrid.config import HybridAnalysisType
    
    analyzer = HybridRootCauseAnalyzer()
    
    request = HybridAnalysisRequest(
        task_id=f"task_{datetime.now().isoformat()}",
        analysis_type=HybridAnalysisType.AUTO_DETECT,
        task_result=task_result,  # Your existing task result
        failure_log=str(task_result.error),
        dom_snapshot=task_result.page_source,
        action_sequence=task_result.actions_taken,
        framework="selenium"  # or your framework
    )
    
    result = await analyzer.analyze(request)
    print(f"Root cause identified: {result.final_root_cause}")
    return result
```

### 2. Quick CLI Test

```bash
# Quick test with minimal input
python3 rca_hybrid/cli.py test_task_001 \
    --failure-log "Button not clickable" \
    --dom-snapshot "<button disabled>Click me</button>" \
    --framework selenium \
    --verbose
```

### 3. Batch Analysis

```python
# Analyze multiple failures
async def batch_analyze(failures):
    analyzer = HybridRootCauseAnalyzer()
    results = []
    
    for failure_data in failures:
        request = HybridAnalysisRequest(
            task_id=failure_data['id'],
            analysis_type=HybridAnalysisType.AUTO_DETECT,
            task_result=failure_data['result'],
            failure_log=failure_data['log'],
            dom_snapshot=failure_data['dom'],
            action_sequence=failure_data['actions'],
            framework=failure_data['framework']
        )
        
        result = await analyzer.analyze(request)
        results.append(result)
    
    return results
```

---

## Analysis Types

- **AUTO_DETECT**: Let the algorithm automatically choose the best analysis method
- **DROPDOWN**: Force analysis using dropdown-specific algorithms
- **ARXIV_SEARCH**: Force analysis using ArXiv search-specific algorithms

## Learning Modes

- **PASSIVE**: Only learn from high-confidence cases
- **ACTIVE**: Learn from medium to high-confidence cases (recommended)
- **AGGRESSIVE**: Learn from all cases, including low-confidence ones

---

## Environment Setup

Make sure you have the required environment variables set:

```bash
# For AI-powered analysis (optional but recommended)
export GROQ_API_KEY="your_groq_api_key_here"

# For enhanced analysis
export OPENAI_API_KEY="your_openai_api_key_here"  # Alternative to Groq
```

---

## Error Handling

```python
try:
    result = await analyzer.analyze(request)
    print(f"Analysis successful: {result.final_root_cause}")
except Exception as e:
    print(f"Analysis failed: {e}")
    # Fallback to basic error logging
```

---

💡 **Pro Tip**: Start with `AUTO_DETECT` analysis type - the algorithm will automatically choose the best approach based on your input data!
