#!/usr/bin/env python3
"""
ArXiv Search Root Cause Analysis - Usage Examples
Demonstrates various use cases and scenarios for the deterministic ArXiv analyzer
"""

import json
import sqlite3
from pathlib import Path

try:
    from deterministic_analyzer import DeterministicArxivAnalyzer
    from pipeline import ArxivDetPipeline
    from config import RootCauseType, AuthorFailureType, DateFailureType
except ImportError:
    from rca_det_search.deterministic_analyzer import DeterministicArxivAnalyzer
    from rca_det_search.pipeline import ArxivDetPipeline
    from rca_det_search.config import RootCauseType, AuthorFailureType, DateFailureType

def example_1_basic_analysis():
    """Example 1: Basic ArXiv search analysis"""
    print("=" * 60)
    print("EXAMPLE 1: Basic ArXiv Search Analysis")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = DeterministicArxivAnalyzer()
    
    # Sample task data
    task_data = {
        'task_id': 'arxiv_neural_networks_2023',
        'framework': 'selenium',
        'reasoning_files': {
            'reasoning_1.txt': '''
            Human: Search for papers by Geoffrey Hinton about neural networks published in 2023
            AI: I'll search ArXiv for papers by Geoffrey Hinton from 2023.
            Action: navigate to https://arxiv.org/
            Action: click author field
            Action: type "John Smith"  # This is wrong - should be Geoffrey Hinton
            Action: select classification "cs.AI"
            Action: set date range 2023-01-01 to 2023-12-31
            Action: click search
            Result: No results found for John Smith
            '''
        },
        'db_data': None,
        'html_files': []
    }
    
    # Perform analysis
    result = analyzer.analyze_task(**task_data)
    
    print(f"📊 Analysis Results:")
    print(f"  Task ID: {result.task_id}")
    print(f"  Root Cause: {result.root_cause.value}")
    print(f"  Failed Step: {result.failure_step}")
    print(f"  Author Failure: {result.author_failure_type.value if result.author_failure_type else 'None'}")
    print(f"  Confidence: {result.confidence_score:.2f}")
    
    print(f"\n🔍 Step Analysis:")
    for step_id, passed in result.step_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  Step {step_id}: {status}")
    
    return result

def example_2_successful_search():
    """Example 2: Successful ArXiv search"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Successful ArXiv Search")
    print("=" * 60)
    
    analyzer = DeterministicArxivAnalyzer()
    
    task_data = {
        'task_id': 'arxiv_quantum_success',
        'framework': 'playwright',
        'reasoning_files': {
            'reasoning_1.txt': '''
            Human: Search for quantum computing papers by Peter Shor
            AI: I'll search ArXiv for Peter Shor's quantum computing papers.
            Action: navigate to https://arxiv.org/
            Action: click author field
            Action: type "Peter Shor"
            Action: select classification "quant-ph"
            Action: set date range 2020-01-01 to 2025-01-01
            Action: click search button
            Result: Found 15 papers by Peter Shor in quantum physics
            Action: display results list
            Success: Search completed successfully
            '''
        },
        'db_data': None,
        'html_files': []
    }
    
    result = analyzer.analyze_task(**task_data)
    
    print(f"📊 Analysis Results:")
    print(f"  Task ID: {result.task_id}")
    print(f"  Root Cause: {result.root_cause.value}")
    print(f"  Success Rate: {sum(result.step_results.values()) / len(result.step_results) * 100:.1f}%")
    print(f"  Confidence: {result.confidence_score:.2f}")
    
    return result

def example_3_website_blocking():
    """Example 3: Website state failure (CAPTCHA/blocking)"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Website State Failure (CAPTCHA)")
    print("=" * 60)
    
    analyzer = DeterministicArxivAnalyzer()
    
    task_data = {
        'task_id': 'arxiv_captcha_blocked',
        'framework': 'selenium',
        'reasoning_files': {
            'reasoning_1.txt': '''
            Human: Search for machine learning papers
            AI: I'll navigate to ArXiv and search for ML papers.
            Action: navigate to https://arxiv.org/
            Error: Page shows CAPTCHA challenge
            Error: Cannot proceed with automated interaction
            Error: Access blocked by anti-bot protection
            Result: Task failed - unable to access ArXiv interface
            '''
        },
        'db_data': None,
        'html_files': []
    }
    
    result = analyzer.analyze_task(**task_data)
    
    print(f"📊 Analysis Results:")
    print(f"  Task ID: {result.task_id}")
    print(f"  Root Cause: {result.root_cause.value}")
    print(f"  Failed Step: {result.failure_step}")
    print(f"  Issue: Website access blocked")
    
    return result

def example_4_date_format_error():
    """Example 4: Date formatting and validation errors"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Date Format Error")
    print("=" * 60)
    
    analyzer = DeterministicArxivAnalyzer()
    
    task_data = {
        'task_id': 'arxiv_date_format_error',
        'framework': 'selenium',
        'reasoning_files': {
            'reasoning_1.txt': '''
            Human: Find papers published in Q1 2024
            AI: I'll search for papers from Q1 2024.
            Action: navigate to https://arxiv.org/
            Action: click author field
            Action: type "Yann LeCun"
            Action: select classification "cs.AI"
            Action: set date range "Q1 2024" to "Q1 2024"  # Invalid format
            Error: Date format not recognized
            Error: Expected YYYY-MM-DD format
            Result: Search failed due to date validation error
            '''
        },
        'db_data': None,
        'html_files': []
    }
    
    result = analyzer.analyze_task(**task_data)
    
    print(f"📊 Analysis Results:")
    print(f"  Task ID: {result.task_id}")
    print(f"  Root Cause: {result.root_cause.value}")
    print(f"  Date Failure: {result.date_failure_type.value if result.date_failure_type else 'None'}")
    print(f"  Failed Step: {result.failure_step}")
    
    return result

def example_5_dynamic_content_failure():
    """Example 5: Dynamic content loading issues"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Dynamic Content Loading Failure")
    print("=" * 60)
    
    analyzer = DeterministicArxivAnalyzer()
    
    task_data = {
        'task_id': 'arxiv_dynamic_content_fail',
        'framework': 'playwright',
        'reasoning_files': {
            'reasoning_1.txt': '''
            Human: Search papers in computer vision category
            AI: I'll search for computer vision papers.
            Action: navigate to https://arxiv.org/
            Action: click author field
            Action: type "Fei-Fei Li"
            Action: click classification dropdown
            Action: wait for classification options to load
            Error: Classification options not loading
            Error: Dynamic content failed to render
            Error: Dropdown remains empty after 10 seconds
            Result: Cannot select classification - task failed
            '''
        },
        'db_data': None,
        'html_files': []
    }
    
    result = analyzer.analyze_task(**task_data)
    
    print(f"📊 Analysis Results:")
    print(f"  Task ID: {result.task_id}")
    print(f"  Root Cause: {result.root_cause.value}")
    print(f"  Failed Step: {result.failure_step} (Classification processing)")
    print(f"  Issue: Dynamic content loading failure")
    
    return result

def example_6_batch_analysis():
    """Example 6: Batch analysis using pipeline"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Batch Analysis Pipeline")
    print("=" * 60)
    
    # Create sample task data
    sample_tasks = [
        {
            'task_id': 'batch_task_1',
            'framework': 'selenium',
            'reasoning_files': {'reasoning.txt': 'Successful search for ML papers'},
            'result_expected': RootCauseType.SUCCESS
        },
        {
            'task_id': 'batch_task_2', 
            'framework': 'playwright',
            'reasoning_files': {'reasoning.txt': 'Wrong author hallucination detected'},
            'result_expected': RootCauseType.AGENT_REASONING_FAILURE
        },
        {
            'task_id': 'batch_task_3',
            'framework': 'selenium', 
            'reasoning_files': {'reasoning.txt': 'CAPTCHA blocking access'},
            'result_expected': RootCauseType.WEBSITE_STATE_FAILURE
        }
    ]
    
    analyzer = DeterministicArxivAnalyzer()
    results = []
    
    print(f"🔄 Processing {len(sample_tasks)} tasks...")
    
    for i, task in enumerate(sample_tasks, 1):
        result = analyzer.analyze_task(
            task_id=task['task_id'],
            framework=task['framework'],
            reasoning_files=task['reasoning_files']
        )
        results.append(result)
        
        print(f"  Task {i}: {result.task_id}")
        print(f"    Root Cause: {result.root_cause.value}")
        print(f"    Expected: {task['result_expected'].value}")
        print(f"    Match: {'✅' if result.root_cause == task['result_expected'] else '❌'}")
    
    # Summary statistics
    success_rate = sum(1 for r in results if r.root_cause == RootCauseType.SUCCESS) / len(results) * 100
    avg_confidence = sum(r.confidence_score for r in results) / len(results)
    
    print(f"\n📈 Batch Analysis Summary:")
    print(f"  Total Tasks: {len(results)}")
    print(f"  Success Rate: {success_rate:.1f}%")
    print(f"  Average Confidence: {avg_confidence:.2f}")
    
    return results

def example_7_real_world_scenario():
    """Example 7: Real-world ArXiv search scenario"""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Real-World ArXiv Search Scenario")
    print("=" * 60)
    
    analyzer = DeterministicArxivAnalyzer()
    
    # Simulate a complex real-world search task
    task_data = {
        'task_id': 'real_world_transformer_search',
        'framework': 'selenium',
        'reasoning_files': {
            'reasoning_1.txt': '''
            Human: Find papers about transformer architectures published in 2023 by Ashish Vaswani
            AI: I need to search ArXiv for transformer papers by Ashish Vaswani from 2023.
            
            Step 1: Navigate to ArXiv
            Action: open https://arxiv.org/
            Result: ArXiv homepage loaded successfully
            
            Step 2: Access advanced search
            Action: click "Advanced Search" link
            Result: Advanced search form displayed
            
            Step 3: Set search criteria
            Action: enter "transformer architecture" in title field
            Action: enter "Ashish Vaswani" in author field
            Action: select category "Computer Science > Machine Learning"
            Action: set date range from 2023-01-01 to 2023-12-31
            
            Step 4: Execute search
            Action: click "Search" button
            Result: Search executed successfully
            
            Step 5: Analyze results
            Result: Found 3 papers matching criteria
            Result: All papers are by Ashish Vaswani about transformers in 2023
            Success: Task completed successfully
            ''',
            'reasoning_2.txt': '''
            Additional context:
            - Search parameters properly validated
            - All form fields correctly filled
            - Results page loaded without errors
            - Papers matched search criteria exactly
            '''
        },
        'db_data': {
            'events': [
                {'action': 'navigate', 'url': 'https://arxiv.org/', 'success': True},
                {'action': 'click', 'element': 'advanced_search_link', 'success': True},
                {'action': 'input', 'field': 'title', 'value': 'transformer architecture', 'success': True},
                {'action': 'input', 'field': 'author', 'value': 'Ashish Vaswani', 'success': True},
                {'action': 'select', 'field': 'category', 'value': 'cs.LG', 'success': True},
                {'action': 'input', 'field': 'date_from', 'value': '2023-01-01', 'success': True},
                {'action': 'input', 'field': 'date_to', 'value': '2023-12-31', 'success': True},
                {'action': 'click', 'element': 'search_button', 'success': True},
                {'action': 'verify', 'element': 'results_list', 'count': 3, 'success': True}
            ]
        },
        'html_files': []
    }
    
    result = analyzer.analyze_task(**task_data)
    
    print(f"📊 Comprehensive Analysis Results:")
    print(f"  Task ID: {result.task_id}")
    print(f"  Framework: {result.framework}")
    print(f"  Root Cause: {result.root_cause.value}")
    print(f"  Confidence Score: {result.confidence_score:.2f}")
    
    print(f"\n🎯 Search Parameters:")
    for param, value in result.search_parameters.items():
        print(f"  {param}: {value}")
    
    print(f"\n📋 Step-by-Step Results:")
    step_names = {
        1: "Navigation and Page Load",
        2: "Author Input Analysis", 
        3: "Classification Processing",
        4: "Date Validation",
        5: "Search Execution"
    }
    
    for step_id, passed in result.step_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  Step {step_id} ({step_names.get(step_id, 'Unknown')}): {status}")
    
    if result.root_cause == RootCauseType.SUCCESS:
        print(f"\n🎉 Analysis Classification: SUCCESSFUL EXECUTION")
        print(f"   All steps completed without errors")
        print(f"   Search criteria properly applied")
        print(f"   Results successfully retrieved")
    
    return result

def example_8_comparative_analysis():
    """Example 8: Compare different failure types"""
    print("\n" + "=" * 60)
    print("EXAMPLE 8: Comparative Failure Analysis")
    print("=" * 60)
    
    analyzer = DeterministicArxivAnalyzer()
    
    # Different failure scenarios for comparison
    scenarios = {
        'DOM Parsing Failure': {
            'reasoning': 'Error: Cannot find author input field\nError: Element not in DOM',
            'expected': RootCauseType.DOM_PARSING_FAILURE
        },
        'Agent Reasoning Failure': {
            'reasoning': 'Action: type "Wrong Author Name"\nNote: Should have been "Correct Author"',
            'expected': RootCauseType.AGENT_REASONING_FAILURE
        },
        'Dynamic Content Failure': {
            'reasoning': 'Error: Classification dropdown not loading\nError: AJAX content timeout',
            'expected': RootCauseType.DYNAMIC_CONTENT_FAILURE
        },
        'Element Interaction Failure': {
            'reasoning': 'Error: Cannot click search button\nError: Element not clickable',
            'expected': RootCauseType.ELEMENT_INTERACTION_FAILURE
        }
    }
    
    print("🔍 Analyzing Different Failure Patterns:")
    print("-" * 50)
    
    for scenario_name, scenario_data in scenarios.items():
        result = analyzer.analyze_task(
            task_id=f"comparative_{scenario_name.lower().replace(' ', '_')}",
            framework='selenium',
            reasoning_files={'reasoning.txt': scenario_data['reasoning']}
        )
        
        match = result.root_cause == scenario_data['expected']
        print(f"\n📊 {scenario_name}:")
        print(f"  Expected: {scenario_data['expected'].value}")
        print(f"  Detected: {result.root_cause.value}")
        print(f"  Accuracy: {'✅ CORRECT' if match else '❌ INCORRECT'}")
        print(f"  Confidence: {result.confidence_score:.2f}")
    
    return scenarios

def save_example_results():
    """Save example results to JSON for React component"""
    print("\n" + "=" * 60)
    print("SAVING EXAMPLE RESULTS FOR REACT COMPONENT")
    print("=" * 60)
    
    analyzer = DeterministicArxivAnalyzer()
    
    # Generate sample data for React component
    sample_results = {
        'tasks': [],
        'summary': {
            'totalTasks': 0,
            'successRate': 0,
            'commonFailures': [],
            'avgConfidence': 0
        }
    }
    
    # Create diverse sample tasks
    sample_tasks = [
        {
            'id': 'arxiv_neural_networks_2023',
            'reasoning': 'Action: type "John Smith" instead of "Geoffrey Hinton"',
            'framework': 'selenium',
            'expected': RootCauseType.AGENT_REASONING_FAILURE
        },
        {
            'id': 'arxiv_quantum_computing_success',
            'reasoning': 'Success: Search completed, found 15 papers by Peter Shor',
            'framework': 'playwright', 
            'expected': RootCauseType.SUCCESS
        },
        {
            'id': 'arxiv_captcha_blocked',
            'reasoning': 'Error: CAPTCHA challenge blocking access',
            'framework': 'selenium',
            'expected': RootCauseType.WEBSITE_STATE_FAILURE
        }
    ]
    
    confidences = []
    failure_counts = {}
    
    for task_data in sample_tasks:
        result = analyzer.analyze_task(
            task_id=task_data['id'],
            framework=task_data['framework'],
            reasoning_files={'reasoning.txt': task_data['reasoning']}
        )
        
        # Convert to React-compatible format
        task_result = {
            'id': result.task_id,
            'framework': result.framework,
            'status': 'success' if result.root_cause == RootCauseType.SUCCESS else 'failed',
            'rootCause': result.root_cause.value,
            'failureStep': result.failure_step,
            'authorFailureType': result.author_failure_type.value if result.author_failure_type else None,
            'dateFailureType': result.date_failure_type.value if result.date_failure_type else None,
            'confidence': result.confidence_score,
            'steps': [
                {
                    'id': i,
                    'name': f"Step {i}",
                    'status': 'success' if passed else 'failed'
                } for i, passed in result.step_results.items()
            ],
            'searchQuery': result.search_parameters.get('query', 'Sample Query'),
            'targetAuthor': result.search_parameters.get('author', 'Sample Author'),
            'actualInput': result.search_parameters.get('actual_author_input', 'Sample Input'),
            'dateRange': f"{result.search_parameters.get('date_from', '2023-01-01')} to {result.search_parameters.get('date_to', '2023-12-31')}",
            'classification': result.search_parameters.get('classification', 'cs.AI'),
            'timestamp': '2025-09-02T22:03:19Z'
        }
        
        sample_results['tasks'].append(task_result)
        confidences.append(result.confidence_score)
        
        failure_type = result.root_cause.value
        failure_counts[failure_type] = failure_counts.get(failure_type, 0) + 1
    
    # Calculate summary statistics
    total_tasks = len(sample_results['tasks'])
    success_count = sum(1 for task in sample_results['tasks'] if task['status'] == 'success')
    
    sample_results['summary'] = {
        'totalTasks': total_tasks,
        'successRate': (success_count / total_tasks * 100) if total_tasks > 0 else 0,
        'commonFailures': [
            {'type': failure_type, 'count': count, 'percentage': count/total_tasks*100}
            for failure_type, count in failure_counts.items()
        ],
        'avgConfidence': sum(confidences) / len(confidences) if confidences else 0
    }
    
    # Save to file
    output_path = Path('sample_react_data.json')
    with open(output_path, 'w') as f:
        json.dump(sample_results, f, indent=2)
    
    print(f"📁 Sample React data saved to: {output_path}")
    print(f"📊 Generated {total_tasks} sample tasks")
    print(f"📈 Success rate: {sample_results['summary']['successRate']:.1f}%")
    
    return sample_results

def main():
    """Run all usage examples"""
    print("🚀 ArXiv Search Root Cause Analysis - Usage Examples")
    print("=" * 60)
    
    # Run all examples
    examples = [
        example_1_basic_analysis,
        example_2_successful_search,
        example_3_website_blocking,
        example_4_date_format_error,
        example_5_dynamic_content_failure,
        example_6_batch_analysis,
        example_7_real_world_scenario,
        example_8_comparative_analysis
    ]
    
    results = []
    for example_func in examples:
        try:
            result = example_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error in {example_func.__name__}: {e}")
    
    # Save example data for React component
    save_example_results()
    
    print("\n" + "=" * 60)
    print("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(f"📊 Total examples run: {len(examples)}")
    print(f"📁 Results saved for React component integration")
    print(f"🎯 Ready for production use!")

if __name__ == "__main__":
    main()
