# Integration Guide: r_det_dropdown with Existing Systems

## Overview

The `r_det_dropdown` package implements a deterministic cascade algorithm for dropdown workflow root cause analysis. It can be used standalone or integrated with existing RCA systems like `rca_pp_2`.

## Quick Start

### 1. Standalone Usage

```bash
# Run on failed dropdown tasks
cd /Users/hassanshaikh/Downloads/webagents/agent-collector
python r_det_dropdown/main.py
```

### 2. Programmatic Usage

```python
from r_det_dropdown.pipeline import DropdownDetPipeline

# Initialize pipeline
pipeline = DropdownDetPipeline(
    parent_folder="data/failed tasks/dropdown",
    output_dir="results/dropdown_analysis"
)

# Run analysis
results = await pipeline.run_pipeline()
```

### 3. Step-by-Step Analysis

```python
from r_det_dropdown.step_parser import DropdownStepParser
from r_det_dropdown.deterministic_analyzer import DeterministicDropdownAnalyzer

# Parse steps from your data format
parser = DropdownStepParser()
steps = parser.parse_steps_from_input(your_step_data)

# Analyze with deterministic algorithm  
analyzer = DeterministicDropdownAnalyzer()
result = analyzer.analyze_task(task_result, failure_log, dom_snapshot, action_sequence, framework)

print(f"Root Cause: {result.root_cause.value}")
```

## Integration with rca_pp_2

### Side-by-Side Comparison

You can run both systems on the same data to compare results:

```python
# Run both analyzers
rca_pp_2_result = run_rca_pp_2_analysis(task_data)
r_det_dropdown_result = run_deterministic_analysis(task_data)

# Compare results
comparison = {
    "task_id": task_data.task_id,
    "rca_pp_2": rca_pp_2_result.root_cause,
    "deterministic": r_det_dropdown_result.root_cause.value,
    "agreement": rca_pp_2_result.root_cause == r_det_dropdown_result.root_cause.value,
    "confidence_rca_pp_2": rca_pp_2_result.confidence,
    "deterministic_logic": "rule-based"
}
```

### Hybrid Approach

Use deterministic analysis for quick screening, ML analysis for complex cases:

```python
def hybrid_analysis(task_data):
    # First, try deterministic analysis
    det_result = run_deterministic_analysis(task_data)
    
    # If confident about the result, use it
    if det_result.root_cause in [RootCauseType.DOM_PARSING_FAILURE, 
                                RootCauseType.AGENT_REASONING_FAILURE]:
        return det_result
    
    # For complex cases, use ML-based analysis
    ml_result = run_rca_pp_2_analysis(task_data)
    return ml_result
```

## Input Data Compatibility

The deterministic analyzer accepts multiple input formats:

### From rca_pp_2 TaskResult

```python
def convert_rca_pp_2_to_deterministic(rca_task_result):
    # Extract steps from rca_pp_2 format
    steps_data = []
    for i, action in enumerate(rca_task_result.actions):
        steps_data.append({
            "step_number": i + 1,
            "action": action.description,
            "success": action.success,
            "timing_ms": action.duration_ms
        })
    
    # Parse with deterministic parser
    parser = DropdownStepParser()
    return parser.parse_steps_from_input(steps_data)
```

### From Log Files

```python
def parse_logs_for_deterministic(log_file_path):
    with open(log_file_path, 'r') as f:
        log_content = f.read()
    
    # Extract step information from logs
    steps_text = extract_dropdown_steps(log_content)
    
    # Parse with deterministic parser
    parser = DropdownStepParser()
    return parser.parse_steps_from_input(steps_text)
```

## Output Format Compatibility

Both systems produce compatible JSON output:

```json
{
  "task_id": "dropdown_task_001",
  "root_cause": "AGENT_REASONING_FAILURE",
  "analysis_method": "deterministic_cascade",
  "framework": "react",
  "failure_step": 3,
  "confidence": "rule_based",
  "timestamp": "2025-09-02T21:00:00Z"
}
```

## Performance Comparison

| Aspect | rca_pp_2 | r_det_dropdown |
|--------|----------|----------------|
| Speed | ~2-5s per task | ~0.1s per task |
| Consistency | Variable | 100% consistent |
| Resource Usage | High (GPU/CPU) | Low (CPU only) |
| Interpretability | Black box | Transparent rules |
| Customization | Model retraining | Code modification |

## Use Case Recommendations

### Use r_det_dropdown when:
- Need fast batch processing
- Require consistent results
- Want transparent reasoning
- Have clear dropdown workflow patterns
- Need low-resource deployment

### Use rca_pp_2 when:
- Analyzing complex, unusual failures
- Need probabilistic confidence scores
- Have diverse task types
- Require learning from new patterns

### Use hybrid approach when:
- Want best of both worlds
- Have mixed complexity tasks
- Need speed + accuracy
- Can invest in dual-system maintenance

## Deployment Options

### 1. Replace rca_pp_2 for Dropdown Tasks

```python
# Route dropdown tasks to deterministic analyzer
if task.task_type == "dropdown_workflow":
    result = run_deterministic_analysis(task)
else:
    result = run_rca_pp_2_analysis(task)
```

### 2. Parallel Analysis with Comparison

```python
# Run both systems and compare
det_result = run_deterministic_analysis(task)
ml_result = run_rca_pp_2_analysis(task)

# Log disagreements for investigation
if det_result.root_cause.value != ml_result.root_cause:
    log_disagreement(task, det_result, ml_result)
```

### 3. Deterministic First, ML Fallback

```python
# Try deterministic first
try:
    result = run_deterministic_analysis(task)
    if result.root_cause != RootCauseType.SUCCESS:
        return result
except Exception:
    pass

# Fallback to ML analysis
return run_rca_pp_2_analysis(task)
```

## Monitoring and Validation

Track the performance of both systems:

```python
metrics = {
    "deterministic_accuracy": calculate_accuracy(det_results, ground_truth),
    "ml_accuracy": calculate_accuracy(ml_results, ground_truth),
    "agreement_rate": calculate_agreement(det_results, ml_results),
    "speed_improvement": calculate_speed_gain(det_times, ml_times),
    "resource_savings": calculate_resource_reduction()
}
```

## Migration Path

1. **Phase 1**: Deploy r_det_dropdown alongside rca_pp_2
2. **Phase 2**: Compare results and validate accuracy
3. **Phase 3**: Route dropdown tasks to deterministic analyzer
4. **Phase 4**: Expand to other workflow types if successful

## Conclusion

The `r_det_dropdown` system provides a fast, consistent, and transparent alternative to ML-based root cause analysis for dropdown workflows. It can be used standalone or integrated with existing systems to provide the best combination of speed, accuracy, and interpretability.
