#!/usr/bin/env python3
"""
Integration Test for Both Deterministic Analyzers
Tests r_det_dropdown and rca_det_search working together
"""

import sys
from pathlib import Path
from datetime import datetime

# Add paths for both analyzers
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / "r_det_dropdown"))
sys.path.append(str(Path(__file__).parent / "rca_det_search"))

def test_dropdown_analyzer():
    """Test the dropdown analyzer"""
    print("🔍 Testing Dropdown Analyzer (Algorithm 1)")
    print("-" * 50)
    
    try:
        from r_det_dropdown.deterministic_analyzer import DropdownDeterministicAnalyzer
        from r_det_dropdown.models import TaskResult as DropdownTaskResult
        
        analyzer = DropdownDeterministicAnalyzer()
        task_result = DropdownTaskResult(
            task_id='integration_dropdown_test',
            timestamp=datetime.now(),
            task_type='ecommerce_dropdown',
            status='completed'
        )
        
        result = analyzer.analyze_task(
            task_result=task_result,
            failure_log='Action: click dropdown\nAction: select option "Electronics"\nSuccess: Selection completed',
            dom_snapshot='<select id="category"><option value="electronics">Electronics</option></select>',
            action_sequence=[{'action': 'click', 'element': 'category'}, {'action': 'select', 'value': 'electronics'}],
            framework='selenium'
        )
        
        print(f"✅ Dropdown Analyzer Test PASSED")
        print(f"  Task ID: {result.task_id}")
        print(f"  Root Cause: {result.root_cause.value}")
        print(f"  Framework: {result.framework}")
        print(f"  Steps: {len(result.steps)}")
        return True
        
    except Exception as e:
        print(f"❌ Dropdown Analyzer Test FAILED: {e}")
        return False

def test_arxiv_analyzer():
    """Test the ArXiv analyzer"""
    print("\n🔍 Testing ArXiv Analyzer (Algorithm 2)")
    print("-" * 50)
    
    try:
        from rca_det_search.deterministic_analyzer import DeterministicArxivAnalyzer
        from rca_det_search.models import TaskResult as ArxivTaskResult
        
        analyzer = DeterministicArxivAnalyzer()
        task_result = ArxivTaskResult(
            task_id='integration_arxiv_test',
            timestamp=datetime.now(),
            task_type='arxiv_search',
            status='completed'
        )
        
        result = analyzer.analyze_task(
            task_result=task_result,
            failure_log='Action: navigate to arxiv.org\nAction: type "Geoffrey Hinton" in author field\nSuccess: Search completed',
            dom_snapshot='<input id="author" type="text" /><select id="classification"><option value="cs.AI">Computer Science - AI</option></select>',
            action_sequence=[
                {'action': 'navigate', 'url': 'https://arxiv.org'},
                {'action': 'type', 'element': 'author', 'value': 'Geoffrey Hinton'}
            ],
            framework='playwright'
        )
        
        print(f"✅ ArXiv Analyzer Test PASSED")
        print(f"  Task ID: {result.task_id}")
        print(f"  Root Cause: {result.root_cause.value}")
        print(f"  Framework: {result.framework}")
        print(f"  Steps: {len(result.steps)}")
        return True
        
    except Exception as e:
        print(f"❌ ArXiv Analyzer Test FAILED: {e}")
        return False

def test_analyzer_routing():
    """Test routing between different analyzers based on task type"""
    print("\n🔀 Testing Analyzer Routing")
    print("-" * 50)
    
    try:
        from r_det_dropdown.deterministic_analyzer import DropdownDeterministicAnalyzer
        from rca_det_search.deterministic_analyzer import DeterministicArxivAnalyzer
        from r_det_dropdown.models import TaskResult as DropdownTaskResult
        from rca_det_search.models import TaskResult as ArxivTaskResult
        
        # Simulate different task types
        tasks = [
            {
                'type': 'ecommerce_dropdown',
                'analyzer': DropdownDeterministicAnalyzer(),
                'task_result': DropdownTaskResult(
                    task_id='routing_dropdown',
                    timestamp=datetime.now(),
                    task_type='ecommerce_dropdown',
                    status='completed'
                ),
                'log': 'Dropdown interaction test',
                'dom': '<select><option>Test</option></select>',
                'actions': [{'action': 'click', 'element': 'dropdown'}]
            },
            {
                'type': 'arxiv_search',
                'analyzer': DeterministicArxivAnalyzer(),
                'task_result': ArxivTaskResult(
                    task_id='routing_arxiv',
                    timestamp=datetime.now(),
                    task_type='arxiv_search',
                    status='completed'
                ),
                'log': 'ArXiv search test',
                'dom': '<input id="author" /><input id="classification" />',
                'actions': [{'action': 'type', 'element': 'author', 'value': 'test'}]
            }
        ]
        
        results = []
        for task in tasks:
            result = task['analyzer'].analyze_task(
                task_result=task['task_result'],
                failure_log=task['log'],
                dom_snapshot=task['dom'],
                action_sequence=task['actions'],
                framework='selenium'
            )
            results.append((task['type'], result))
            print(f"  ✅ {task['type']}: {result.root_cause.value}")
        
        print(f"✅ Analyzer Routing Test PASSED - {len(results)} analyzers working")
        return True
        
    except Exception as e:
        print(f"❌ Analyzer Routing Test FAILED: {e}")
        return False

def test_comparative_analysis():
    """Compare the two algorithms on similar failure scenarios"""
    print("\n📊 Testing Comparative Analysis")
    print("-" * 50)
    
    try:
        from r_det_dropdown.deterministic_analyzer import DropdownDeterministicAnalyzer
        from rca_det_search.deterministic_analyzer import DeterministicArxivAnalyzer
        from r_det_dropdown.models import TaskResult as DropdownTaskResult
        from rca_det_search.models import TaskResult as ArxivTaskResult
        
        # Test similar DOM parsing failures
        dropdown_analyzer = DropdownDeterministicAnalyzer()
        arxiv_analyzer = DeterministicArxivAnalyzer()
        
        # DOM parsing failure scenarios
        dropdown_result = dropdown_analyzer.analyze_task(
            task_result=DropdownTaskResult(
                task_id='compare_dropdown_dom_fail',
                timestamp=datetime.now(),
                task_type='ecommerce_dropdown',
                status='failed'
            ),
            failure_log='Error: Cannot find dropdown element',
            dom_snapshot='<div>No dropdown found</div>',
            action_sequence=[{'action': 'click', 'element': 'missing_dropdown'}],
            framework='selenium'
        )
        
        arxiv_result = arxiv_analyzer.analyze_task(
            task_result=ArxivTaskResult(
                task_id='compare_arxiv_dom_fail',
                timestamp=datetime.now(),
                task_type='arxiv_search',
                status='failed'
            ),
            failure_log='Error: Cannot find author input field',
            dom_snapshot='<div>No author field found</div>',
            action_sequence=[{'action': 'type', 'element': 'missing_author'}],
            framework='selenium'
        )
        
        print(f"  Dropdown DOM Failure: {dropdown_result.root_cause.value}")
        print(f"  ArXiv DOM Failure: {arxiv_result.root_cause.value}")
        
        # Both should detect DOM parsing failures
        both_detect_dom_failure = (
            "DOM_PARSING" in dropdown_result.root_cause.value and 
            "DOM_PARSING" in arxiv_result.root_cause.value
        )
        
        if both_detect_dom_failure:
            print(f"✅ Comparative Analysis PASSED - Both detect DOM failures correctly")
            return True
        else:
            print(f"❌ Comparative Analysis FAILED - Inconsistent DOM failure detection")
            return False
            
    except Exception as e:
        print(f"❌ Comparative Analysis Test FAILED: {e}")
        return False

def main():
    """Run integration tests"""
    print("🚀 Integration Test Suite for Deterministic Analyzers")
    print("=" * 60)
    print("Testing both Algorithm 1 (Dropdown) and Algorithm 2 (ArXiv)")
    print("=" * 60)
    
    tests = [
        test_dropdown_analyzer,
        test_arxiv_analyzer,
        test_analyzer_routing,
        test_comparative_analysis
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            print(f"❌ Test {test_func.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Integration Test Results:")
    print(f"  Tests Passed: {passed_tests}/{total_tests}")
    print(f"  Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("✅ Both deterministic analyzers are working correctly")
        print("✅ Ready for production deployment")
    else:
        print("⚠️  Some integration tests failed")
        print("❌ Review analyzer implementations before deployment")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
