# Hybrid Root Cause Analysis System

A comprehensive end-to-end system that combines deterministic algorithms with AI-powered analysis and adaptive learning for web automation failure diagnosis.

## 🎯 Overview

The Hybrid Root Cause Analysis System revolutionizes web automation debugging by intelligently combining three powerful approaches:

1. **Deterministic Algorithms** - Fast, rule-based analysis for known patterns (Dropdown & ArXiv)
2. **AI-Powered Analysis** - LLM-based comprehensive analysis for complex cases  
3. **Adaptive Learning** - Continuous improvement through pattern recognition and rule evolution

### Why Hybrid?

- **Speed**: Deterministic algorithms provide instant analysis for known patterns
- **Coverage**: AI analysis handles edge cases and unknown failure modes
- **Intelligence**: Adaptive learning improves accuracy over time
- **Reliability**: Multi-tier fallback ensures analysis always completes

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Hybrid Analyzer                              │
├─────────────────────────────────────────────────────────────────────────┤
│  Input: Web Agent Task Failure Data                                    │
│  │                                                                     │
│  ├─► 1. AUTO-DETECT Failure Type (Dropdown/ArXiv/Unknown)             │
│  │                                                                     │
│  ├─► 2. TRY DETERMINISTIC Algorithm                                    │
│  │    ├─ Parse action_sequence → workflow steps                       │
│  │    ├─ Run specialized algorithm (Algorithm 1 or 2)                 │
│  │    └─ Return if confidence > threshold                             │
│  │                                                                     │
│  ├─► 3. FALLBACK TO AI Analysis                                       │
│  │    ├─ Multi-stage LLM analysis                                     │
│  │    ├─ 5 Whys technique                                             │
│  │    └─ Structured result extraction                                 │
│  │                                                                     │
│  └─► 4. ADAPTIVE LEARNING                                             │
│       ├─ Store failure patterns                                       │
│       ├─ Update deterministic rules                                   │
│       └─ Improve future accuracy                                      │
│                                                                        │
│  Output: Root Cause Category + Confidence + Method Used               │
└─────────────────────────────────────────────────────────────────────────┘
```

### Core Components

- **HybridRootCauseAnalyzer** - Main orchestrator and decision engine
- **AIRootCauseAnalyzer** - LLM-powered analysis with Groq integration
- **AdaptiveLearner** - TF-IDF pattern recognition and rule updates
- **Configuration System** - Flexible analysis modes and thresholds
- **CLI Interface** - Command-line tool for easy integration

## 🔄 How Deterministic Integration Works

### The Challenge: From Steps to Full Context

**Original Deterministic Algorithms** (r_det_dropdown & rca_det_search) only took "steps":
```python
# Original approach - limited input
steps = ["Step 1: Dropdown detected", "Step 2: Click failed"]
result = analyzer.analyze_steps(steps)
```

**Hybrid System** - Enhanced with full context:
```python
# Enhanced approach - rich input data
request = HybridAnalysisRequest(
    task_id="dropdown_failure_001",
    task_result=full_task_data,      # Complete execution context
    failure_log=detailed_error_log,   # Full error information  
    dom_snapshot=html_content,        # Page state at failure
    action_sequence=all_actions,      # Complete action history
    framework="selenium"              # Technical context
)
```

### Step Conversion Process

The hybrid system intelligently converts rich task data back to steps for deterministic algorithms:

```python
# 1. Action Sequence → Workflow Steps
action_sequence = [
    {"action": "click", "element": "#dropdown-trigger", "success": True},
    {"action": "wait", "duration": 5000},
    {"action": "click", "element": "#option-1", "success": False}
]

# 2. Converted to Steps for Deterministic Algorithm
steps = [
    "Step 1: Dropdown trigger clicked successfully",
    "Step 2: Wait completed (5000ms)", 
    "Step 3: Option selection failed - element not found"
]

# 3. Enhanced with Context
enhanced_steps = {
    "steps": steps,
    "dom_context": dom_snapshot,
    "error_context": failure_log,
    "framework_context": framework
}
```

## 🚀 Quick Start

### Installation

```bash
# Install required dependencies
pip install scikit-learn tiktoken beautifulsoup4 langchain-openai langchain-core langchain-google-genai

# Set API keys for AI analysis (choose one or more providers)
export GROQ_API_KEY="your-groq-api-key"           # Fastest provider
export OPENAI_API_KEY="your-openai-api-key"       # High-quality provider  
export GEMINI_API_KEY="your-gemini-api-key"       # Google's advanced AI
```

### Basic Usage

```python
from rca_hybrid.hybrid_analyzer import HybridRootCauseAnalyzer
from rca_hybrid.models import HybridAnalysisRequest
from rca_hybrid.config import HybridAnalysisType, LearningMode

# Initialize analyzer
analyzer = HybridRootCauseAnalyzer(
    confidence_threshold=0.75,
    learning_mode=LearningMode.ACTIVE
)

# Create your task result object (from your web agent)
class TaskResult:
    def __init__(self):
        self.reasoning_files = {
            "agent_log.txt": "Failed to click dropdown option",
            "selenium_log.txt": "ElementNotInteractableException"
        }
        self.db_data = {
            "actions": [
                {"type": "click", "element": "#dropdown", "success": True},
                {"type": "click", "element": "#option-1", "success": False}
            ],
            "errors": ["Element not found: #option-1"]
        }

# Create analysis request
request = HybridAnalysisRequest(
    task_id="dropdown_failure_001",
    analysis_type=HybridAnalysisType.AUTO_DETECT,  # Let system choose best method
    task_result=TaskResult(),
    failure_log="""
ERROR: Failed to select dropdown option
- Dropdown opened successfully  
- Target option #option-1 not found
- Operation timed out after 30 seconds
""",
    dom_snapshot="""
<select id="dropdown">
    <option value="">Select option</option>
    <option value="1">Option 1</option>
</select>
""",
    action_sequence=[
        {"action": "click", "element": "#dropdown", "success": True},
        {"action": "click", "element": "#option-1", "success": False}
    ],
    framework="selenium"
)

# Run analysis
result = await analyzer.analyze(request)
print(f"Root cause: {result.final_root_cause}")
print(f"Method used: {result.primary_method}")
print(f"Confidence: {result.final_confidence:.2f}")
```

### Command Line Usage

```bash
# Basic analysis
python3 rca_hybrid/cli.py my_task_001

# Algorithm-specific analysis
python3 rca_hybrid/cli.py dropdown_task --analysis-type dropdown
python3 rca_hybrid/cli.py arxiv_task --analysis-type arxiv_search

# With input files
python3 rca_hybrid/cli.py task_001 \
    --failure-log error_log.txt \
    --dom-snapshot page.html \
    --output results.json

# Advanced configuration
python3 rca_hybrid/cli.py advanced_task \
    --analysis-type auto_detect \
    --confidence-threshold 0.8 \
    --learning-mode aggressive \
    --framework selenium \
    --verbose
```

## 📊 Input Data Formats

### From Web Agent Task Results

Your web agent provides rich execution data that the hybrid system intelligently processes:

```python
# Your existing web agent task result structure
class WebAgentTaskResult:
    def __init__(self):
        # Execution logs and reasoning
        self.reasoning_files = {
            "agent_reasoning.txt": "Attempted to click dropdown...",
            "selenium_log.txt": "WebDriverException: Element not clickable",
            "browser_console.log": "JavaScript error: Uncaught TypeError"
        }
        
        # Database/execution data
        self.db_data = {
            "actions_taken": [
                {"timestamp": "2025-01-15T10:00:00", "action": "navigate", "url": "https://site.com"},
                {"timestamp": "2025-01-15T10:00:05", "action": "click", "element": "#dropdown-trigger", "success": True},
                {"timestamp": "2025-01-15T10:00:10", "action": "wait", "duration": 5000},
                {"timestamp": "2025-01-15T10:00:15", "action": "click", "element": "#option-1", "success": False}
            ],
            "errors_encountered": [
                "ElementNotFoundException: Unable to locate element: #option-1",
                "TimeoutException: Operation timed out after 30 seconds"
            ],
            "page_states": [
                {"step": "initial", "url": "https://site.com", "elements_found": 15},
                {"step": "dropdown_opened", "url": "https://site.com", "elements_found": 18},
                {"step": "failure", "url": "https://site.com", "elements_found": 18}
            ]
        }
        
        # Technical details
        self.framework_used = "selenium"
        self.browser_info = "Chrome 120.0.6099.109"
        self.execution_time = 35000  # ms
```

### Step Conversion Magic ✨

The hybrid system automatically converts your rich data into steps for deterministic algorithms:

**Original Deterministic Input** (what algorithms expected):
```python
# Simple steps array - limited context
steps = [
    "Step 1: Dropdown detection - success",
    "Step 2: Men category navigation - success", 
    "Step 3: Subcategory selection - failed"
]
```

**Hybrid System Conversion** (how we enhanced it):
```python
# Rich context → Enhanced steps for deterministic algorithms
def convert_to_enhanced_steps(action_sequence, failure_log, dom_snapshot):
    enhanced_steps = []
    
    for i, action in enumerate(action_sequence, 1):
        # Convert action to step description
        step_desc = f"Step {i}: {action['action']} on {action.get('element', 'unknown')}"
        
        # Add success/failure status
        if action.get('success', True):
            step_desc += " - success"
        else:
            step_desc += " - failed"
            # Add error context from failure_log
            if 'not found' in failure_log.lower():
                step_desc += " (element not found)"
            elif 'timeout' in failure_log.lower():
                step_desc += " (timeout)"
        
        enhanced_steps.append(step_desc)
    
    # Add DOM context for better analysis
    return {
        "steps": enhanced_steps,
        "dom_context": dom_snapshot,
        "error_details": failure_log,
        "framework": framework
    }
```

**Result for Deterministic Algorithms**:
```python
# Enhanced input maintains compatibility while adding context
enhanced_input = {
    "steps": [
        "Step 1: click on #dropdown-trigger - success",
        "Step 2: wait for 5000ms - success", 
        "Step 3: click on #option-1 - failed (element not found)"
    ],
    "dom_context": "<select id='dropdown-trigger'>...</select>",
    "error_details": "ElementNotFoundException: Unable to locate element: #option-1",
    "framework": "selenium"
}
```

## 🔧 Analysis Modes & Configuration

### Analysis Types

| Type | Description | Use Case | Algorithm Used |
|------|-------------|----------|----------------|
| `AUTO_DETECT` | Automatic detection | General purpose | System chooses best fit |
| `DROPDOWN` | Cascade dropdown analysis | E-commerce dropdown flows | Algorithm 1: Dropdown RCA |
| `ARXIV_SEARCH` | Academic search analysis | ArXiv search forms | Algorithm 2: ArXiv RCA |

### Learning Modes

| Mode | Aggressiveness | Pattern Recognition | Rule Updates |
|------|----------------|-------------------|--------------|
| `PASSIVE` | Low | Log patterns only | No automatic updates |
| `ACTIVE` | Medium | Learn from high-confidence cases | Moderate updates |
| `AGGRESSIVE` | High | Learn from all cases | Frequent updates |

### Confidence Thresholds

```python
# Conservative - higher confidence required for deterministic acceptance
analyzer = HybridRootCauseAnalyzer(confidence_threshold=0.85)

# Balanced - default threshold (recommended)
analyzer = HybridRootCauseAnalyzer(confidence_threshold=0.75)

# Aggressive - lower threshold, prefer deterministic over AI
analyzer = HybridRootCauseAnalyzer(confidence_threshold=0.60)
```

## 📈 Analysis Workflow

### Step-by-Step Process

1. **Input Processing & Validation**
   ```python
   # Validate required fields
   ✓ task_id, analysis_type, task_result
   ✓ failure_log, dom_snapshot, action_sequence
   ✓ framework information
   ```

2. **Type Detection** (if AUTO_DETECT)
   ```python
   # Pattern matching for algorithm selection
   if detect_dropdown_patterns(action_sequence, dom_snapshot):
       algorithm = "dropdown"
   elif detect_search_patterns(action_sequence, dom_snapshot):
       algorithm = "arxiv_search"
   else:
       algorithm = "ai_only"
   ```

3. **Step Conversion for Deterministic Analysis**
   ```python
   # Convert rich data to algorithm-compatible format
   enhanced_steps = convert_actions_to_steps(
       action_sequence=request.action_sequence,
       failure_log=request.failure_log,
       dom_snapshot=request.dom_snapshot
   )
   ```

4. **Deterministic Analysis Execution**
   ```python
   # Run appropriate algorithm
   det_result = deterministic_analyzer.analyze_task(
       task_result=request.task_result,
       failure_log=request.failure_log,
       dom_snapshot=request.dom_snapshot,
       action_sequence=enhanced_steps,
       framework=request.framework
   )
   
   # Check confidence threshold
   if det_result.confidence_score >= confidence_threshold:
       return det_result  # Success!
   ```

5. **AI Fallback** (if deterministic fails or low confidence)
   ```python
   # Prepare comprehensive context for LLM
   ai_context = {
       "failure_description": failure_log,
       "dom_analysis": dom_snapshot,
       "action_history": action_sequence,
       "deterministic_attempt": det_result,
       "framework_info": framework
   }
   
   # Multi-stage AI analysis
   ai_result = ai_analyzer.analyze(ai_context)
   ```

6. **Adaptive Learning**
   ```python
   # Store case for learning
   learning_case = {
       "input_patterns": extract_patterns(request),
       "deterministic_success": det_result.success,
       "final_root_cause": final_result.root_cause,
       "confidence": final_result.confidence
   }
   
   # Update rules if learning mode allows
   adaptive_learner.learn_from_case(learning_case)
   ```

## 📋 Comprehensive Result Structure

```json
{
  "task_id": "dropdown_failure_001",
  "analysis_type": "auto_detect",
  "timestamp": "2025-09-02T15:30:00Z",
  
  "execution_summary": {
    "primary_method": "deterministic",
    "deterministic_success": true,
    "ai_fallback_used": false,
    "total_analysis_time_ms": 1250.5
  },
  
  "final_results": {
    "root_cause": "Dropdown toggle function incomplete",
    "confidence": 0.85,
    "category": "DOM_PARSING_FAILURE",
    "framework": "selenium"
  },
  
  "deterministic_analysis": {
    "analyzer_type": "dropdown",
    "algorithm": "Algorithm 1: Cascade Dropdown RCA",
    "root_cause": "JavaScript function toggleDropdown() incomplete",
    "confidence_score": 0.87,
    "failure_step": 2,
    "step_analysis": {
      "step_1": {"name": "Initial Element Detection", "success": true, "timing_ms": 250},
      "step_2": {"name": "Primary Category Navigation", "success": false, "error": "dropdown not expanding"},
      "step_3": {"name": "Subcategory Selection", "success": false, "skipped": true}
    },
    "analysis_time_ms": 45.2,
    "success": true
  },
  
  "ai_analysis": null,
  
  "learning_results": {
    "pattern_stored": true,
    "similar_cases_found": 3,
    "new_rules_generated": [],
    "learning_confidence": 0.78,
    "learning_mode": "active"
  },
  
  "metadata": {
    "analyzer_version": "1.0.0",
    "deterministic_version": "1.2.1",
    "ai_model": "llama-3.1-70b-versatile",
    "learning_database_size": 1247
  }
}
```

## 🔍 Algorithm Details

### Algorithm 1: Cascade Dropdown Analysis (r_det_dropdown)

**Workflow Steps:**
1. Initial Element Detection - Detect dropdown trigger elements
2. Primary Category Navigation - Navigate to main categories (e.g., Men)
3. Subcategory Selection Validation - Select appropriate subcategories
4. Filter Application Verification - Apply product filters
5. Product Analysis and Selection - Analyze and select products
6. Transaction Completion - Complete purchase flow

**Root Cause Categories:**
- `DOM_PARSING_FAILURE` - Elements not detected in DOM
- `ELEMENT_INTERACTION_FAILURE` - Elements found but interaction failed
- `DYNAMIC_CONTENT_FAILURE` - Dynamic content loading issues
- `AGENT_REASONING_FAILURE` - Incorrect agent decision making
- `WEBSITE_STATE_FAILURE` - Server/website state issues

### Algorithm 2: ArXiv Search Analysis (rca_det_search)

**Workflow Steps:**
1. Navigation and Page Load Verification - Validate ArXiv accessibility
2. Author Input Field Analysis - Author field interactions and validation
3. Classification Label Processing - Academic classification handling
4. Date Input Validation - Date range input and validation
5. Search Execution and Results Verification - Search functionality validation

**Root Cause Categories:**
- `NAVIGATION_FAILURE` - Site accessibility issues
- `AUTHOR_INPUT_FAILURE` - Author field problems
- `CLASSIFICATION_FAILURE` - Academic classification issues
- `DATE_VALIDATION_FAILURE` - Date input problems
- `SEARCH_EXECUTION_FAILURE` - Search functionality issues

## 🤖 AI Analysis Component

### 🌟 Multi-Provider AI Support

The system now supports three AI providers for maximum flexibility and performance:

#### Available Providers

| Provider | Model | Avg Response Time | Reliability | Best Use Case |
|----------|-------|-------------------|-------------|---------------|
| **GPT-4o** | gpt-4o | ~19.1s | ⭐⭐⭐⭐⭐ | High-quality analysis |
| **Groq** | meta-llama/llama-4-maverick-17b-128e-instruct | ~4.3s | ⭐⭐⭐⭐⭐ | Speed-critical applications |
| **Gemini** | gemini-2.0-flash-exp | ~60s | ⭐⭐⭐⭐ | Complex reasoning tasks |

#### Provider Configuration

```python
# Multi-provider configuration in config.py
AI_MODEL_CONFIGS = {
    'gpt': {
        'provider': 'openai',
        'model': 'gpt-4o',
        'api_key_env': 'OPENAI_API_KEY',
        'base_url': 'https://api.openai.com/v1',
        'temperature': 0.1,
        'max_tokens': 2048,
        'timeout': 30
    },
    'groq': {
        'provider': 'groq',
        'model': 'meta-llama/llama-4-maverick-17b-128e-instruct',
        'api_key_env': 'GROQ_API_KEY',
        'base_url': 'https://api.groq.com/openai/v1',
        'temperature': 0.1,
        'max_tokens': 2048,
        'timeout': 30
    },
    'gemini': {
        'provider': 'google',
        'model': 'gemini-2.0-flash-exp',
        'api_key_env': 'GEMINI_API_KEY',
        'temperature': 0.1,
        'max_tokens': 2048,
        'timeout': 30
    }
}
```

#### Usage with Different Providers

```python
# Initialize with specific AI provider
analyzer_gpt = HybridRootCauseAnalyzer(ai_provider='gpt')
analyzer_groq = HybridRootCauseAnalyzer(ai_provider='groq')  # Fastest
analyzer_gemini = HybridRootCauseAnalyzer(ai_provider='gemini')

# CLI usage with provider selection
python3 rca_hybrid/cli.py task_001 --ai-provider groq
python3 rca_hybrid/cli.py task_001 --ai-provider gpt
python3 rca_hybrid/cli.py task_001 --ai-provider gemini
```

#### Environment Setup

```bash
# Set up all three providers
export OPENAI_API_KEY="your_openai_api_key"
export GROQ_API_KEY="your_groq_api_key"
export GEMINI_API_KEY="your_gemini_api_key"

# Test all providers
python test_ai_providers.py
```

#### Automatic Fallback

The system includes intelligent fallback mechanisms:

```python
# Provider selection logic
class HybridRootCauseAnalyzer:
    def __init__(self, ai_provider=None):
        # Select provider with fallback
        if ai_provider and ai_provider in AI_MODEL_CONFIGS:
            self.selected_config = AI_MODEL_CONFIGS[ai_provider]
        else:
            self.selected_config = AI_MODEL_CONFIG  # Default
        
        # Initialize with provider-specific settings
        self.ai_analyzer = AIRootCauseAnalyzer(
            model_config=self.selected_config
        )
```

### Multi-Stage Analysis Process

1. **Primary Analysis**
   ```python
   # Initial problem assessment
   primary_prompt = f"""
   Analyze this web automation failure:
   
   Failure Log: {failure_log}
   DOM State: {dom_snapshot}
   Actions: {action_sequence}
   Framework: {framework}
   
   Provide initial root cause assessment.
   """
   ```

2. **Detailed Analysis with 5 Whys**
   ```python
   # Deep dive using 5 Whys technique
   detailed_prompt = f"""
   Based on primary analysis: {primary_result}
   
   Apply 5 Whys technique:
   1. Why did the automation fail?
   2. Why did that underlying issue occur?
   3. Why was that condition present?
   4. Why wasn't this prevented?
   5. Why is this the root cause?
   """
   ```

3. **Structured Result Extraction**
   ```python
   # Extract actionable results
   extraction_prompt = f"""
   Extract structured results:
   - Root cause category
   - Confidence level (0.0-1.0)
   - Technical explanation
   - Recommended fixes
   """
   ```

### AI Model Configuration

```python
AI_MODEL_CONFIG = {
    'model': 'llama-3.1-70b-versatile',  # Groq model
    'temperature': 0.1,                   # Low randomness for consistency
    'max_tokens': 2000,                   # Sufficient for detailed analysis
    'timeout': 30.0,                      # 30 second timeout
    'base_url': 'https://api.groq.com/openai/v1'
}
```

## 🧠 Adaptive Learning System

### Pattern Recognition

```python
# TF-IDF vectorization for similarity detection
vectorizer = TfidfVectorizer(
    max_features=1000,
    stop_words='english',
    ngram_range=(1, 2)
)

# Extract patterns from failure data
patterns = [
    failure_log,
    dom_snapshot_text,
    action_sequence_text,
    error_messages
]

# Find similar cases
similarity_scores = cosine_similarity(
    new_case_vector,
    existing_cases_matrix
)
```

### Learning Database Schema

```sql
-- SQLite database structure
CREATE TABLE learning_cases (
    id INTEGER PRIMARY KEY,
    case_id TEXT UNIQUE,
    input_patterns TEXT,
    failure_type TEXT,
    root_cause TEXT,
    confidence REAL,
    method_used TEXT,
    timestamp DATETIME,
    framework TEXT
);

CREATE TABLE pattern_rules (
    id INTEGER PRIMARY KEY,
    pattern_hash TEXT UNIQUE,
    pattern_description TEXT,
    recommended_algorithm TEXT,
    confidence_threshold REAL,
    success_count INTEGER,
    failure_count INTEGER,
    last_updated DATETIME
);
```

### Rule Update Process

```python
def update_rules_from_patterns(self, new_case):
    # Find similar patterns
    similar_cases = self.find_similar_cases(new_case, threshold=0.7)
    
    if len(similar_cases) >= 3:  # Sufficient evidence
        # Generate new rule
        new_rule = {
            'pattern': extract_common_pattern(similar_cases),
            'algorithm': determine_best_algorithm(similar_cases),
            'confidence': calculate_rule_confidence(similar_cases)
        }
        
        # Validate rule before adding
        if self.validate_rule(new_rule):
            self.add_rule(new_rule)
            logger.info(f"New rule added: {new_rule['pattern']}")
```

## 🛠️ Integration Examples

### With Existing Web Automation

```python
# In your web automation failure handler
class WebAutomationAgent:
    def __init__(self):
        self.rca_analyzer = HybridRootCauseAnalyzer(
            confidence_threshold=0.75,
            learning_mode=LearningMode.ACTIVE
        )
    
    async def handle_task_failure(self, task_result):
        # Create analysis request from your task data
        rca_request = HybridAnalysisRequest(
            task_id=task_result.task_id,
            analysis_type=HybridAnalysisType.AUTO_DETECT,
            task_result=task_result,
            failure_log=str(task_result.last_error),
            dom_snapshot=task_result.page_source,
            action_sequence=task_result.action_history,
            framework=self.framework_name
        )
        
        # Get root cause analysis
        rca_result = await self.rca_analyzer.analyze(rca_request)
        
        # Log results
        logger.info(f"RCA completed: {rca_result.final_root_cause}")
        logger.info(f"Method: {rca_result.primary_method}")
        logger.info(f"Confidence: {rca_result.final_confidence}")
        
        # Take corrective action based on root cause
        await self.handle_root_cause(rca_result)
        
        return rca_result
```

### Batch Processing

```python
# Analyze multiple failures
async def batch_analyze_failures(failure_data_list):
    analyzer = HybridRootCauseAnalyzer()
    results = []
    
    for failure_data in failure_data_list:
        request = HybridAnalysisRequest(
            task_id=failure_data['task_id'],
            analysis_type=HybridAnalysisType.AUTO_DETECT,
            task_result=failure_data['task_result'],
            failure_log=failure_data['error_log'],
            dom_snapshot=failure_data['page_html'],
            action_sequence=failure_data['actions'],
            framework=failure_data['framework']
        )
        
        result = await analyzer.analyze(request)
        results.append(result)
        
        # Optional: Add delay to avoid rate limiting
        await asyncio.sleep(0.1)
    
    return results
```

## 📊 Monitoring & Statistics

### Performance Metrics

```python
# Get analysis statistics
stats = analyzer.get_statistics()
print(f"Total analyses: {stats['total_analyses']}")
print(f"Deterministic success rate: {stats['deterministic_success_rate']:.2%}")
print(f"Average analysis time: {stats['avg_analysis_time_ms']:.1f}ms")
print(f"Learning cases stored: {stats['learning_cases_count']}")
```

### Learning Effectiveness

```python
# Monitor learning progress
learning_stats = adaptive_learner.get_learning_statistics()
print(f"Rules generated: {learning_stats['rules_generated']}")
print(f"Pattern recognition accuracy: {learning_stats['pattern_accuracy']:.2%}")
print(f"Recent improvements: {learning_stats['recent_improvements']}")
```

## 🔧 Advanced Configuration

### Custom Confidence Strategies

```python
# Custom confidence calculation
class CustomConfidenceStrategy:
    def calculate_confidence(self, deterministic_result, context):
        base_confidence = deterministic_result.confidence_score
        
        # Boost confidence for known patterns
        if self.is_known_pattern(context):
            base_confidence *= 1.1
        
        # Reduce confidence for edge cases
        if self.is_edge_case(context):
            base_confidence *= 0.9
            
        return min(base_confidence, 1.0)

# Use custom strategy
analyzer = HybridRootCauseAnalyzer(
    confidence_strategy=CustomConfidenceStrategy()
)
```

### Framework-Specific Adaptations

```python
# Framework-specific configuration
FRAMEWORK_CONFIGS = {
    'selenium': {
        'timeout_multiplier': 1.0,
        'dom_parser': 'html.parser',
        'error_patterns': ['ElementNotInteractableException', 'TimeoutException']
    },
    'playwright': {
        'timeout_multiplier': 0.8,
        'dom_parser': 'lxml',
        'error_patterns': ['TimeoutError', 'ElementHandleError']
    },
    'puppeteer': {
        'timeout_multiplier': 1.2,
        'dom_parser': 'html.parser',
        'error_patterns': ['TimeoutError', 'ElementNotFoundError']
    }
}
```

## 🧪 Testing & Validation

### Component Testing

```bash
# Test individual components
cd /path/to/agent-collector

# Test hybrid analyzer
python3 -c "
from rca_hybrid.hybrid_analyzer import HybridRootCauseAnalyzer
print('✓ Hybrid analyzer initialized')
"

# Test AI analyzer
python3 -c "
from rca_hybrid.ai_analyzer import AIRootCauseAnalyzer
print('✓ AI analyzer initialized')
"

# Test adaptive learner
python3 -c "
from rca_hybrid.adaptive_learner import AdaptiveLearner
learner = AdaptiveLearner()
print(f'✓ Learning database has {learner.get_case_count()} cases')
"
```

### Integration Testing

```bash
# Run comprehensive demo
python3 rca_hybrid/final_demo.py

# Test all AI providers
python3 test_ai_providers.py

# CLI integration test with specific provider
python3 rca_hybrid/cli.py test_integration \
    --analysis-type auto_detect \
    --ai-provider groq \
    --framework selenium \
    --verbose \
    --output integration_test_results.json

# Performance test across providers
python3 -c "
import asyncio
from rca_hybrid.test_performance import run_performance_test
asyncio.run(run_performance_test(num_cases=100))
"

# Provider-specific testing
python3 rca_hybrid/cli.py task_001 --ai-provider gpt --verbose
python3 rca_hybrid/cli.py task_001 --ai-provider groq --verbose  
python3 rca_hybrid/cli.py task_001 --ai-provider gemini --verbose
```

### Multi-Provider Testing

```python
# Test all providers systematically
def test_all_providers():
    providers = ['gpt', 'groq', 'gemini']
    results = {}
    
    for provider in providers:
        try:
            analyzer = HybridRootCauseAnalyzer(ai_provider=provider)
            result = analyzer.analyze(test_case)
            results[provider] = {
                'status': 'success',
                'confidence': result.final_confidence,
                'time_ms': result.total_analysis_time_ms
            }
        except Exception as e:
            results[provider] = {
                'status': 'failed',
                'error': str(e)
            }
    
    return results

# Run provider comparison
results = test_all_providers()
for provider, result in results.items():
    print(f"{provider}: {result}")
```

### Validation Scripts

```python
# Validate system health
async def validate_system():
    checks = {
        'imports': test_imports(),
        'database': test_database_connection(),
        'ai_connection': test_ai_api(),
        'deterministic': test_deterministic_analyzers(),
        'learning': test_learning_system()
    }
    
    for check, result in checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check}: {'PASS' if result else 'FAIL'}")
    
    return all(checks.values())
```

## 🚨 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Missing dependencies for multi-provider support
pip install scikit-learn tiktoken beautifulsoup4 langchain-openai langchain-core langchain-google-genai

# Python path issues
export PYTHONPATH="/path/to/agent-collector:$PYTHONPATH"
```

**2. Multi-Provider API Issues**
```bash
# Check all provider API keys
echo "OpenAI: $([ -n "$OPENAI_API_KEY" ] && echo "✓ Set" || echo "✗ Missing")"
echo "Groq: $([ -n "$GROQ_API_KEY" ] && echo "✓ Set" || echo "✗ Missing")"
echo "Gemini: $([ -n "$GEMINI_API_KEY" ] && echo "✓ Set" || echo "✗ Missing")"

# Test specific provider connection
python3 -c "
from rca_hybrid.hybrid_analyzer import HybridRootCauseAnalyzer
analyzer = HybridRootCauseAnalyzer(ai_provider='groq')
print('✓ Groq provider ready')
"

# Test all providers
python3 test_ai_providers.py
```

**3. Provider Selection Issues**
```python
# Check available providers
from rca_hybrid.config import AI_MODEL_CONFIGS
print(f"Available providers: {list(AI_MODEL_CONFIGS.keys())}")

# Test provider fallback
analyzer = HybridRootCauseAnalyzer(ai_provider='invalid_provider')
# Should fallback to default provider
```

**4. Database Issues**
```python
# Reset learning database
from rca_hybrid.adaptive_learner import AdaptiveLearner
learner = AdaptiveLearner()
learner.reset_database()
print("✓ Database reset complete")
```

**5. Performance Issues**
```python
# Check analysis times
analyzer = HybridRootCauseAnalyzer(
    confidence_threshold=0.8,  # Higher threshold = less AI usage
    learning_mode=LearningMode.PASSIVE  # Reduce learning overhead
)
```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Verbose analysis
analyzer = HybridRootCauseAnalyzer(debug=True)
result = await analyzer.analyze(request)
```

## 📚 API Reference

### Main Classes

#### HybridRootCauseAnalyzer

```python
class HybridRootCauseAnalyzer:
    def __init__(
        self,
        confidence_threshold: float = 0.75,
        learning_mode: LearningMode = LearningMode.ACTIVE,
        debug: bool = False
    ):
        """Initialize hybrid analyzer"""
    
    async def analyze(
        self, 
        request: HybridAnalysisRequest
    ) -> HybridAnalysisResult:
        """Perform hybrid root cause analysis"""
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get analysis statistics"""
```

#### HybridAnalysisRequest

```python
@dataclass
class HybridAnalysisRequest:
    task_id: str
    analysis_type: HybridAnalysisType
    task_result: Any
    failure_log: str
    dom_snapshot: str
    action_sequence: List[Dict[str, Any]]
    framework: str
    confidence_threshold: Optional[float] = None
    learning_mode: Optional[LearningMode] = None
```

#### HybridAnalysisResult

```python
@dataclass
class HybridAnalysisResult:
    task_id: str
    analysis_type: HybridAnalysisType
    timestamp: datetime
    primary_method: str
    final_root_cause: str
    final_confidence: float
    deterministic_success: bool
    ai_used: bool
    learning_applied: bool
    total_analysis_time_ms: float
    deterministic_result: Optional[DeterministicResult]
    ai_result: Optional[AIAnalysisResult]
```

### Enums

```python
class HybridAnalysisType(Enum):
    DROPDOWN = "dropdown"
    ARXIV_SEARCH = "arxiv_search"
    AUTO_DETECT = "auto_detect"

class LearningMode(Enum):
    PASSIVE = "passive"      # Log only
    ACTIVE = "active"        # Moderate learning
    AGGRESSIVE = "aggressive" # Maximum learning
```

## 🤝 Contributing

### Development Setup

```bash
# Clone and setup
git clone <repository>
cd agent-collector
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio black flake8

# Set up pre-commit hooks
pre-commit install
```

### Adding New Features

1. **New Deterministic Analyzer**
   ```python
   # Create analyzer in new module
   class MyDeterministicAnalyzer:
       def analyze_task(self, task_result, failure_log, dom_snapshot, action_sequence, framework):
           # Implementation
           pass
   
   # Add to hybrid analyzer
   # In hybrid_analyzer.py:_init_deterministic_analyzers()
   try:
       from my_analyzer import MyDeterministicAnalyzer
       self.my_analyzer = MyDeterministicAnalyzer()
   except ImportError:
       self.my_analyzer = None
   ```

2. **Enhanced AI Analysis**
   ```python
   # Extend AI analyzer
   class EnhancedAIAnalyzer(AIRootCauseAnalyzer):
       async def _perform_specialized_analysis(self, context):
           # Add specialized analysis logic
           pass
   ```

3. **Custom Learning Strategies**
   ```python
   # Implement custom learning
   class CustomLearningStrategy:
       def should_learn(self, case):
           # Custom learning criteria
           pass
   ```

### Code Standards

- Follow PEP 8 style guidelines
- Add type hints for all functions
- Include comprehensive docstrings
- Write unit tests for new features
- Update documentation

### Testing Requirements

```bash
# Run all tests
pytest rca_hybrid/tests/

# Run specific test categories
pytest rca_hybrid/tests/test_hybrid_analyzer.py
pytest rca_hybrid/tests/test_ai_analyzer.py
pytest rca_hybrid/tests/test_adaptive_learner.py

# Run with coverage
pytest --cov=rca_hybrid --cov-report=html
```

## 📄 License

MIT License - see LICENSE file for details.

## 🔗 Related Projects

- **r_det_dropdown** - Deterministic dropdown cascade analysis
- **rca_det_search** - Deterministic ArXiv search analysis  
- **rca_pipeline.py** - Original AI-powered RCA system
- **agent-collector** - Web automation testing framework

## 📞 Support

For issues and questions:

1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with:
   - Error messages and logs
   - Input data examples
   - Environment details
   - Steps to reproduce

## 🚀 Future Roadmap

### ✅ Recently Completed
- **Multi-Provider AI Support** - GPT-4o, Groq Llama, and Gemini integration
- **Provider Selection & Fallback** - Intelligent provider routing and backup
- **Performance Optimization** - Provider-specific performance tuning
- **Comprehensive Testing** - Multi-provider validation and testing framework

### 🔮 Upcoming Features
- **Additional AI Providers** - Claude, PaLM, and other emerging models
- **Enhanced Deterministic Analyzers** - Support for more specialized workflows
- **Advanced Learning Models** - Neural network-based pattern recognition
- **Real-time Learning** - Streaming updates to learning system
- **Web Dashboard** - Visual interface for analysis results and provider comparison
- **API Server** - REST API for remote analysis with provider selection
- **Cloud Integration** - Scalable cloud-based analysis with auto-scaling providers
- **Cost Optimization** - Intelligent provider selection based on cost vs quality
- **Provider Analytics** - Detailed performance and accuracy metrics per provider

---

**Built with ❤️ for robust web automation failure analysis**

*This system represents the evolution from simple rule-based analysis to intelligent hybrid approaches that combine the best of deterministic algorithms, AI reasoning, and adaptive learning.*
