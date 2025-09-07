"""
Deterministic ArXiv Search Root Cause Analyzer
Implementation of Algorithm 2: ArXiv Advanced Search Root Cause Analysis
"""
import json
import re
from typing import List, Dict, Optional, Any

try:
    from .models import ArxivSearchStep, ArxivAnalysisResult, TaskResult
    from .config import (RootCauseType, AuthorFailureType, DateFailureType, 
                        ARXIV_ELEMENTS, VALID_CLASSIFICATIONS, VALID_DATE_OPTIONS,
                        MINIMUM_SEARCH_RESULTS, logger)
except ImportError:
    from models import ArxivSearchStep, ArxivAnalysisResult, TaskResult
    from config import (RootCauseType, AuthorFailureType, DateFailureType, 
                       ARXIV_ELEMENTS, VALID_CLASSIFICATIONS, VALID_DATE_OPTIONS,
                       MINIMUM_SEARCH_RESULTS, logger)

class DeterministicArxivAnalyzer:
    """
    Implements the deterministic ArXiv search root cause analysis algorithm
    """
    
    def __init__(self):
        self.logger = logger
    
    def analyze_task(self, task_result: TaskResult, failure_log: str, 
                    dom_snapshot: str, action_sequence: List[Dict], 
                    framework: str) -> ArxivAnalysisResult:
        """
        Main analysis method implementing Algorithm 2
        
        Args:
            task_result: The task result data
            failure_log: Log data (L)
            dom_snapshot: DOM snapshot data (D) 
            action_sequence: Sequence of actions taken (A)
            framework: Framework used (F)
            
        Returns:
            ArxivAnalysisResult with root cause classification
        """
        self.logger.info(f"Starting ArXiv deterministic analysis for task {task_result.task_id}")
        
        # Parse steps from action sequence and logs
        steps = self._parse_steps_from_data(action_sequence, failure_log, dom_snapshot)
        
        # Apply deterministic algorithm
        root_cause, author_failure, date_failure = self._apply_arxiv_algorithm(
            steps, failure_log, dom_snapshot, action_sequence, framework)
        
        # Determine failure step
        failure_step = self._identify_failure_step(steps, root_cause)
        
        analysis_details = {
            "algorithm_version": "2.0",
            "total_steps_analyzed": len(steps),
            "framework_detected": framework,
            "analysis_method": "deterministic_arxiv_search"
        }
        
        return ArxivAnalysisResult(
            task_id=task_result.task_id,
            framework=framework,
            steps=steps,
            root_cause=root_cause,
            failure_step=failure_step,
            author_failure_type=author_failure,
            date_failure_type=date_failure,
            analysis_details=analysis_details
        )
    
    def _parse_steps_from_data(self, action_sequence: List[Dict], 
                              failure_log: str, dom_snapshot: str) -> List[ArxivSearchStep]:
        """Parse ArXiv search workflow steps from the provided data"""
        steps = []
        
        # Step 1: Navigation and Page Load Verification
        page_loaded = self._check_arxiv_page_loaded(failure_log)
        captcha_detected = self._check_captcha_detected(dom_snapshot)
        
        steps.append(ArxivSearchStep(
            step_number=1,
            step_name="Navigation and Page Load Verification",
            action_taken="Navigate to ArXiv search page",
            success=page_loaded,
            elements_detected=self._extract_page_elements(dom_snapshot),
            failure_classification="captcha" if captcha_detected else None
        ))
        
        # Step 2: Author Input Field Analysis
        author_input_detected = self._check_author_input_detected(dom_snapshot)
        author_dropdown_detected = self._check_author_dropdown_detected(dom_snapshot)
        author_interaction_success = self._check_author_interaction(action_sequence)
        
        steps.append(ArxivSearchStep(
            step_number=2,
            step_name="Author Input Field Analysis",
            action_taken="Detect and interact with author fields",
            success=author_input_detected and author_dropdown_detected and author_interaction_success,
            elements_detected=self._extract_author_elements(dom_snapshot)
        ))
        
        # Step 3: Classification Label Processing
        classification_detected = self._check_classification_labels_detected(dom_snapshot)
        correct_classification = self._check_correct_classification_selected(action_sequence)
        
        steps.append(ArxivSearchStep(
            step_number=3,
            step_name="Classification Label Processing",
            action_taken="Select classification labels",
            success=classification_detected and correct_classification,
            elements_detected=self._extract_classification_elements(dom_snapshot)
        ))
        
        # Step 4: Date Input Validation
        date_elements_detected = self._check_date_input_detected(dom_snapshot)
        valid_date_input = self._check_valid_date_input(action_sequence)
        
        steps.append(ArxivSearchStep(
            step_number=4,
            step_name="Date Input Validation",
            action_taken="Input date criteria",
            success=date_elements_detected and valid_date_input,
            elements_detected=self._extract_date_elements(dom_snapshot)
        ))
        
        # Step 5: Search Execution and Results Verification
        search_button_detected = self._check_search_button_detected(dom_snapshot)
        search_button_clicked = self._check_search_button_clicked(action_sequence)
        sufficient_results = self._check_sufficient_search_results(dom_snapshot, failure_log)
        
        steps.append(ArxivSearchStep(
            step_number=5,
            step_name="Search Execution and Results Verification",
            action_taken="Execute search and verify results",
            success=search_button_detected and search_button_clicked and sufficient_results,
            elements_detected=self._extract_search_elements(dom_snapshot)
        ))
        
        return steps
    
    def _apply_arxiv_algorithm(self, steps: List[ArxivSearchStep], failure_log: str,
                              dom_snapshot: str, action_sequence: List[Dict], 
                              framework: str) -> tuple[RootCauseType, Optional[AuthorFailureType], Optional[DateFailureType]]:
        """
        Apply the deterministic ArXiv algorithm from Algorithm 2
        """
        author_failure_type = None
        date_failure_type = None
        
        # Step 1: Navigation and Page Load Verification
        if not self._check_arxiv_page_loaded(failure_log):
            if self._check_captcha_detected(dom_snapshot):
                return RootCauseType.WEBSITE_STATE_FAILURE, author_failure_type, date_failure_type
            else:
                return RootCauseType.WEBSITE_STATE_FAILURE, author_failure_type, date_failure_type
        
        # Step 2: Author Input Field Analysis
        if not self._check_author_input_detected(dom_snapshot):
            return RootCauseType.DOM_PARSING_FAILURE, author_failure_type, date_failure_type
        
        if not self._check_author_dropdown_detected(dom_snapshot):
            return RootCauseType.DOM_PARSING_FAILURE, author_failure_type, date_failure_type
        
        if not self._check_author_interaction(action_sequence):
            failure_type = self._classify_author_failure(action_sequence, failure_log)
            author_failure_type = failure_type
            
            if failure_type == AuthorFailureType.WRONG_AUTHOR_HALLUCINATION:
                return RootCauseType.AGENT_REASONING_FAILURE, author_failure_type, date_failure_type
            elif failure_type == AuthorFailureType.DYNAMIC_RENDERING_ISSUE:
                return RootCauseType.DYNAMIC_CONTENT_FAILURE, author_failure_type, date_failure_type
            else:
                return RootCauseType.DYNAMIC_CONTENT_FAILURE, author_failure_type, date_failure_type
        
        # Step 3: Classification Label Processing
        if not self._check_classification_labels_detected(dom_snapshot):
            return RootCauseType.DOM_PARSING_FAILURE, author_failure_type, date_failure_type
        
        if not self._check_correct_classification_selected(action_sequence):
            return RootCauseType.DYNAMIC_CONTENT_FAILURE, author_failure_type, date_failure_type
        
        # Step 4: Date Input Validation
        if not self._check_date_input_detected(dom_snapshot):
            return RootCauseType.DOM_PARSING_FAILURE, author_failure_type, date_failure_type
        
        if not self._check_valid_date_input(action_sequence):
            date_failure = self._classify_date_failure(action_sequence, failure_log)
            date_failure_type = date_failure
            
            if date_failure in [DateFailureType.HALLUCINATION, DateFailureType.FORMAT_ERROR, DateFailureType.REASONING_ISSUE]:
                return RootCauseType.AGENT_REASONING_FAILURE, author_failure_type, date_failure_type
        
        # Step 5: Search Execution and Results Verification
        if not self._check_search_button_detected(dom_snapshot):
            return RootCauseType.DOM_PARSING_FAILURE, author_failure_type, date_failure_type
        
        if self._check_search_button_detected(dom_snapshot) and not self._check_search_button_clicked(action_sequence):
            return RootCauseType.ELEMENT_INTERACTION_FAILURE, author_failure_type, date_failure_type
        
        if not self._check_sufficient_search_results(dom_snapshot, failure_log):
            return RootCauseType.WEBSITE_STATE_FAILURE, author_failure_type, date_failure_type
        
        return RootCauseType.SUCCESS, author_failure_type, date_failure_type
    
    def _identify_failure_step(self, steps: List[ArxivSearchStep], root_cause: RootCauseType) -> Optional[int]:
        """Identify which step failed based on the analysis"""
        if root_cause == RootCauseType.SUCCESS:
            return None
            
        for step in steps:
            if not step.success:
                return step.step_number
        
        return None
    
    # Helper methods for checking specific conditions
    def _check_arxiv_page_loaded(self, failure_log: str) -> bool:
        """Check if ArXiv page loaded successfully"""
        if not failure_log:
            return True  # Assume success if no log
        
        failure_indicators = ['failed to load', 'page not found', 'connection error', 'timeout']
        return not any(indicator in failure_log.lower() for indicator in failure_indicators)
    
    def _check_captcha_detected(self, dom_snapshot: str) -> bool:
        """Check if captcha is detected in DOM"""
        if not dom_snapshot:
            return False
        return any(captcha_term in dom_snapshot.lower() for captcha_term in ARXIV_ELEMENTS['captcha'])
    
    def _check_author_input_detected(self, dom_snapshot: str) -> bool:
        """Check if author input field is detected"""
        if not dom_snapshot:
            return False
        return any(author_term in dom_snapshot.lower() for author_term in ARXIV_ELEMENTS['author_input'])
    
    def _check_author_dropdown_detected(self, dom_snapshot: str) -> bool:
        """Check if author dropdown is detected"""
        if not dom_snapshot:
            return False
        return any(dropdown_term in dom_snapshot.lower() for dropdown_term in ARXIV_ELEMENTS['author_dropdown'])
    
    def _check_author_interaction(self, action_sequence: List[Dict]) -> bool:
        """Check if author interaction was successful"""
        for action in action_sequence:
            if (action.get('type') in ['input', 'type', 'select'] and
                any(author_term in action.get('target', '').lower() for author_term in ARXIV_ELEMENTS['author_input'])):
                return action.get('success', False)
        return False
    
    def _classify_author_failure(self, action_sequence: List[Dict], failure_log: str) -> AuthorFailureType:
        """Classify the type of author interaction failure"""
        # Check for hallucination indicators
        hallucination_indicators = ['wrong author', 'hallucination', 'incorrect name', 'made up']
        if any(indicator in failure_log.lower() for indicator in hallucination_indicators):
            return AuthorFailureType.WRONG_AUTHOR_HALLUCINATION
        
        # Check for dynamic rendering issues
        dynamic_indicators = ['dropdown not loaded', 'suggestions not appearing', 'timing issue']
        if any(indicator in failure_log.lower() for indicator in dynamic_indicators):
            return AuthorFailureType.DYNAMIC_RENDERING_ISSUE
        
        return AuthorFailureType.INTERACTION_FAILURE
    
    def _check_classification_labels_detected(self, dom_snapshot: str) -> bool:
        """Check if classification labels are detected"""
        if not dom_snapshot:
            return False
        return any(class_term in dom_snapshot.lower() for class_term in ARXIV_ELEMENTS['classification_labels'])
    
    def _check_correct_classification_selected(self, action_sequence: List[Dict]) -> bool:
        """Check if correct classification combination was selected"""
        for action in action_sequence:
            if action.get('type') in ['click', 'select']:
                target = action.get('target', '').lower()
                # Check if any valid classification was selected
                if any(valid_class in target for valid_class in VALID_CLASSIFICATIONS):
                    return action.get('success', False)
        return False
    
    def _check_date_input_detected(self, dom_snapshot: str) -> bool:
        """Check if date input elements are detected"""
        if not dom_snapshot:
            return False
        return any(date_term in dom_snapshot.lower() for date_term in ARXIV_ELEMENTS['date_input'])
    
    def _check_valid_date_input(self, action_sequence: List[Dict]) -> bool:
        """Check if valid date input was provided"""
        for action in action_sequence:
            if action.get('type') in ['input', 'select', 'type']:
                target = action.get('target', '').lower()
                if any(date_term in target for date_term in ARXIV_ELEMENTS['date_input']):
                    # Check if action value matches valid date options
                    action_value = action.get('value', '').lower()
                    if any(valid_option.replace('_', ' ') in action_value for valid_option in VALID_DATE_OPTIONS):
                        return action.get('success', False)
        return False
    
    def _classify_date_failure(self, action_sequence: List[Dict], failure_log: str) -> DateFailureType:
        """Classify the type of date input failure"""
        # Check for hallucination
        if 'hallucination' in failure_log.lower() or 'wrong date' in failure_log.lower():
            return DateFailureType.HALLUCINATION
        
        # Check for format error
        if 'format' in failure_log.lower() or 'invalid date' in failure_log.lower():
            return DateFailureType.FORMAT_ERROR
        
        # Check for reasoning issue
        if 'reasoning' in failure_log.lower() or 'logic' in failure_log.lower():
            return DateFailureType.REASONING_ISSUE
        
        return DateFailureType.REASONING_ISSUE  # Default
    
    def _check_search_button_detected(self, dom_snapshot: str) -> bool:
        """Check if search button is detected"""
        if not dom_snapshot:
            return False
        return any(search_term in dom_snapshot.lower() for search_term in ARXIV_ELEMENTS['search_button'])
    
    def _check_search_button_clicked(self, action_sequence: List[Dict]) -> bool:
        """Check if search button was clicked successfully"""
        for action in action_sequence:
            if (action.get('type') == 'click' and
                any(search_term in action.get('target', '').lower() for search_term in ARXIV_ELEMENTS['search_button'])):
                return action.get('success', False)
        return False
    
    def _check_sufficient_search_results(self, dom_snapshot: str, failure_log: str) -> bool:
        """Check if sufficient search results were returned"""
        # Check failure log for insufficient results
        if failure_log:
            insufficient_indicators = ['no results', 'insufficient results', 'less than', 'only found']
            if any(indicator in failure_log.lower() for indicator in insufficient_indicators):
                return False
        
        # Check DOM for result elements
        if dom_snapshot:
            result_count = 0
            for result_term in ARXIV_ELEMENTS['results']:
                result_count += dom_snapshot.lower().count(result_term)
            
            return result_count >= MINIMUM_SEARCH_RESULTS
        
        return True  # Assume success if no clear indication of failure
    
    # Element extraction methods
    def _extract_page_elements(self, dom_snapshot: str) -> List[str]:
        """Extract page-level elements from DOM"""
        elements = []
        if dom_snapshot:
            # Check for ArXiv-specific elements
            arxiv_indicators = ['arxiv', 'advanced search', 'search form']
            for indicator in arxiv_indicators:
                if indicator in dom_snapshot.lower():
                    elements.append(indicator)
        return elements
    
    def _extract_author_elements(self, dom_snapshot: str) -> List[str]:
        """Extract author-related elements from DOM"""
        elements = []
        if dom_snapshot:
            for element_list in [ARXIV_ELEMENTS['author_input'], ARXIV_ELEMENTS['author_dropdown']]:
                for element_type in element_list:
                    if element_type in dom_snapshot.lower():
                        elements.append(element_type)
        return elements
    
    def _extract_classification_elements(self, dom_snapshot: str) -> List[str]:
        """Extract classification elements from DOM"""
        elements = []
        if dom_snapshot:
            for element_type in ARXIV_ELEMENTS['classification_labels']:
                if element_type in dom_snapshot.lower():
                    elements.append(element_type)
        return elements
    
    def _extract_date_elements(self, dom_snapshot: str) -> List[str]:
        """Extract date elements from DOM"""
        elements = []
        if dom_snapshot:
            for element_type in ARXIV_ELEMENTS['date_input']:
                if element_type in dom_snapshot.lower():
                    elements.append(element_type)
        return elements
    
    def _extract_search_elements(self, dom_snapshot: str) -> List[str]:
        """Extract search elements from DOM"""
        elements = []
        if dom_snapshot:
            for element_list in [ARXIV_ELEMENTS['search_button'], ARXIV_ELEMENTS['results']]:
                for element_type in element_list:
                    if element_type in dom_snapshot.lower():
                        elements.append(element_type)
        return elements
