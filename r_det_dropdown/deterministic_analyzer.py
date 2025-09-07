"""
Deterministic Dropdown Root Cause Analyzer
Implementation of Algorithm 1: Cascade Dropdown Root Cause Analysis
"""
import json
import re
from typing import List, Dict, Optional, Any
from .models import DropdownStep, DropdownAnalysisResult, TaskResult
from .config import RootCauseType, MINIMUM_LOAD_TIME, DROPDOWN_ELEMENTS, logger

class DeterministicDropdownAnalyzer:
    """
    Implements the deterministic cascade dropdown root cause analysis algorithm
    """
    
    def __init__(self):
        self.logger = logger
    
    def analyze_task(self, task_result: TaskResult, failure_log: str, 
                    dom_snapshot: str, action_sequence: List[Dict], 
                    framework: str) -> DropdownAnalysisResult:
        """
        Main analysis method implementing Algorithm 1
        
        Args:
            task_result: The task result data
            failure_log: Log data (L)
            dom_snapshot: DOM snapshot data (D) 
            action_sequence: Sequence of actions taken (A)
            framework: Framework used (F)
            
        Returns:
            DropdownAnalysisResult with root cause classification
        """
        self.logger.info(f"Starting deterministic analysis for task {task_result.task_id}")
        
        # Parse steps from action sequence and logs
        steps = self._parse_steps_from_data(action_sequence, failure_log, dom_snapshot)
        
        # Apply deterministic algorithm
        root_cause = self._apply_cascade_algorithm(steps, failure_log, dom_snapshot, 
                                                 action_sequence, framework)
        
        # Determine failure step
        failure_step = self._identify_failure_step(steps, root_cause)
        
        analysis_details = {
            "algorithm_version": "1.0",
            "total_steps_analyzed": len(steps),
            "framework_detected": framework,
            "analysis_method": "deterministic_cascade"
        }
        
        return DropdownAnalysisResult(
            task_id=task_result.task_id,
            framework=framework,
            steps=steps,
            root_cause=root_cause,
            failure_step=failure_step,
            analysis_details=analysis_details
        )
    
    def _parse_steps_from_data(self, action_sequence: List[Dict], 
                              failure_log: str, dom_snapshot: str) -> List[DropdownStep]:
        """Parse dropdown workflow steps from the provided data"""
        steps = []
        
        # Step 1: Initial Element Detection
        dropdown_detected = self._check_dropdown_detection(dom_snapshot)
        interaction_success = self._check_dropdown_interaction(action_sequence)
        
        steps.append(DropdownStep(
            step_number=1,
            step_name="Initial Element Detection",
            action_taken="Detect and interact with dropdown",
            success=dropdown_detected and interaction_success,
            elements_detected=self._extract_dropdown_elements(dom_snapshot)
        ))
        
        # Step 2: Primary Category Navigation
        men_clicked, timing = self._check_men_option_clicked(action_sequence)
        searched_instead = self._check_agent_searched_instead(failure_log)
        
        steps.append(DropdownStep(
            step_number=2,
            step_name="Primary Category Navigation", 
            action_taken="Click Men option",
            success=men_clicked and not searched_instead,
            timing_ms=timing,
            elements_detected=self._extract_category_elements(dom_snapshot)
        ))
        
        # Step 3: Subcategory Selection Validation
        clothing_clicked = self._check_clothing_instead_shoes(action_sequence)
        subcategory_loaded = self._check_subcategory_options_loaded(dom_snapshot)
        
        steps.append(DropdownStep(
            step_number=3,
            step_name="Subcategory Selection Validation",
            action_taken="Select subcategory",
            success=not clothing_clicked and subcategory_loaded,
            elements_detected=self._extract_subcategory_elements(dom_snapshot)
        ))
        
        # Step 4: Filter Application Verification  
        nike_applied = self._check_nike_filter_applied(action_sequence)
        grid_updated = self._check_grid_updated(dom_snapshot)
        server_error = self._check_server_response_error(failure_log)
        
        steps.append(DropdownStep(
            step_number=4,
            step_name="Filter Application Verification",
            action_taken="Apply Nike filter",
            success=nike_applied and grid_updated,
            elements_detected=self._extract_filter_elements(dom_snapshot),
            error_message="Server error detected" if server_error else None
        ))
        
        # Step 5: Product Analysis and Selection
        price_parsed = self._check_price_elements_parsed(dom_snapshot)
        correct_cheapest = self._check_correct_cheapest_identified(action_sequence)
        
        steps.append(DropdownStep(
            step_number=5,
            step_name="Product Analysis and Selection",
            action_taken="Analyze and select product",
            success=price_parsed and correct_cheapest,
            elements_detected=self._extract_product_elements(dom_snapshot)
        ))
        
        # Step 6: Transaction Completion
        correct_item_added = self._check_correct_item_added(action_sequence)
        checkout_success = self._check_checkout_interaction(action_sequence, dom_snapshot)
        
        steps.append(DropdownStep(
            step_number=6,
            step_name="Transaction Completion",
            action_taken="Add to cart and checkout",
            success=correct_item_added and checkout_success,
            elements_detected=self._extract_checkout_elements(dom_snapshot)
        ))
        
        return steps
    
    def _apply_cascade_algorithm(self, steps: List[DropdownStep], failure_log: str,
                               dom_snapshot: str, action_sequence: List[Dict], 
                               framework: str) -> RootCauseType:
        """
        Apply the deterministic cascade algorithm from the specification
        """
        # Step 1: Initial Element Detection
        dropdown_detected = self._check_dropdown_detection(dom_snapshot)
        if not dropdown_detected:
            return RootCauseType.DOM_PARSING_FAILURE
            
        dropdown_interaction = self._check_dropdown_interaction(action_sequence)
        if dropdown_detected and not dropdown_interaction:
            return RootCauseType.ELEMENT_INTERACTION_FAILURE
        
        # Step 2: Primary Category Navigation
        men_clicked, timing = self._check_men_option_clicked(action_sequence)
        if men_clicked:
            if timing and timing < MINIMUM_LOAD_TIME:
                return RootCauseType.DYNAMIC_CONTENT_FAILURE
        else:
            if self._check_agent_searched_instead(failure_log):
                return RootCauseType.DYNAMIC_CONTENT_FAILURE
        
        # Step 3: Subcategory Selection Validation
        if self._check_clothing_instead_shoes(action_sequence):
            return RootCauseType.AGENT_REASONING_FAILURE
            
        if not self._check_subcategory_options_loaded(dom_snapshot):
            return RootCauseType.DYNAMIC_CONTENT_FAILURE
        
        # Step 4: Filter Application Verification
        nike_applied = self._check_nike_filter_applied(action_sequence)
        grid_updated = self._check_grid_updated(dom_snapshot)
        if nike_applied and not grid_updated:
            if self._check_server_response_error(failure_log):
                return RootCauseType.WEBSITE_STATE_FAILURE
            else:
                return RootCauseType.DYNAMIC_CONTENT_FAILURE
        
        # Step 5: Product Analysis and Selection
        price_elements_detected = self._check_price_elements_detected(dom_snapshot)
        price_parsed = self._check_price_elements_parsed(dom_snapshot)
        if price_elements_detected and not price_parsed:
            return RootCauseType.DOM_PARSING_FAILURE
            
        if self._check_wrong_product_identified_cheapest(action_sequence):
            return RootCauseType.AGENT_REASONING_FAILURE
        
        # Step 6-7: Transaction Completion
        if self._check_wrong_item_added_to_cart(action_sequence):
            return RootCauseType.AGENT_REASONING_FAILURE
            
        checkout_elements_detected = self._check_checkout_elements_detected(dom_snapshot)
        checkout_interaction_success = self._check_checkout_interaction_success(action_sequence)
        if checkout_elements_detected and not checkout_interaction_success:
            return RootCauseType.ELEMENT_INTERACTION_FAILURE
        
        return RootCauseType.SUCCESS
    
    def _identify_failure_step(self, steps: List[DropdownStep], root_cause: RootCauseType) -> Optional[int]:
        """Identify which step failed based on the analysis"""
        if root_cause == RootCauseType.SUCCESS:
            return None
            
        for step in steps:
            if not step.success:
                return step.step_number
        
        return None
    
    # Helper methods for checking specific conditions
    def _check_dropdown_detection(self, dom_snapshot: str) -> bool:
        """Check if dropdown element was detected in DOM"""
        if not dom_snapshot:
            return False
        return any(element in dom_snapshot.lower() for element in DROPDOWN_ELEMENTS['dropdown_trigger'])
    
    def _check_dropdown_interaction(self, action_sequence: List[Dict]) -> bool:
        """Check if dropdown interaction was successful"""
        for action in action_sequence:
            if action.get('type') == 'click' and 'dropdown' in action.get('target', '').lower():
                return action.get('success', False)
        return False
    
    def _check_men_option_clicked(self, action_sequence: List[Dict]) -> tuple[bool, Optional[int]]:
        """Check if Men option was clicked successfully and return timing"""
        for action in action_sequence:
            if (action.get('type') == 'click' and 
                any(men_term in action.get('target', '').lower() for men_term in DROPDOWN_ELEMENTS['men_option'])):
                return action.get('success', False), action.get('timing_ms')
        return False, None
    
    def _check_agent_searched_instead(self, failure_log: str) -> bool:
        """Check if agent searched instead of clicking"""
        if not failure_log:
            return False
        return 'search' in failure_log.lower() and 'click' not in failure_log.lower()
    
    def _check_clothing_instead_shoes(self, action_sequence: List[Dict]) -> bool:
        """Check if Clothing was clicked instead of Shoes"""
        for action in action_sequence:
            if action.get('type') == 'click':
                target = action.get('target', '').lower()
                if any(clothing_term in target for clothing_term in DROPDOWN_ELEMENTS['clothing_subcategory']):
                    return True
        return False
    
    def _check_subcategory_options_loaded(self, dom_snapshot: str) -> bool:
        """Check if subcategory options were loaded"""
        if not dom_snapshot:
            return False
        return (any(shoe_term in dom_snapshot.lower() for shoe_term in DROPDOWN_ELEMENTS['shoes_subcategory']) or
                any(clothing_term in dom_snapshot.lower() for clothing_term in DROPDOWN_ELEMENTS['clothing_subcategory']))
    
    def _check_nike_filter_applied(self, action_sequence: List[Dict]) -> bool:
        """Check if Nike filter was applied"""
        for action in action_sequence:
            if (action.get('type') in ['click', 'select'] and
                any(nike_term in action.get('target', '').lower() for nike_term in DROPDOWN_ELEMENTS['nike_filter'])):
                return action.get('success', False)
        return False
    
    def _check_grid_updated(self, dom_snapshot: str) -> bool:
        """Check if product grid was updated after filter"""
        # This would need more sophisticated logic in real implementation
        return 'nike' in dom_snapshot.lower() if dom_snapshot else False
    
    def _check_server_response_error(self, failure_log: str) -> bool:
        """Check for server response errors in log"""
        if not failure_log:
            return False
        error_indicators = ['500', '502', '503', '504', 'server error', 'timeout']
        return any(error in failure_log.lower() for error in error_indicators)
    
    def _check_price_elements_detected(self, dom_snapshot: str) -> bool:
        """Check if price elements were detected"""
        if not dom_snapshot:
            return False
        return any(price_term in dom_snapshot.lower() for price_term in DROPDOWN_ELEMENTS['price_elements'])
    
    def _check_price_elements_parsed(self, dom_snapshot: str) -> bool:
        """Check if price elements were successfully parsed"""
        if not dom_snapshot:
            return False
        # Look for price patterns like $XX.XX
        price_pattern = r'\$\d+\.?\d*'
        return bool(re.search(price_pattern, dom_snapshot))
    
    def _check_wrong_product_identified_cheapest(self, action_sequence: List[Dict]) -> bool:
        """Check if wrong product was identified as cheapest"""
        # This would need more sophisticated logic based on actual product data
        return False
    
    def _check_correct_cheapest_identified(self, action_sequence: List[Dict]) -> bool:
        """Check if correct cheapest product was identified"""
        return not self._check_wrong_product_identified_cheapest(action_sequence)
    
    def _check_wrong_item_added_to_cart(self, action_sequence: List[Dict]) -> bool:
        """Check if wrong item was added to cart"""
        # This would need logic to compare selected vs added items
        return False
    
    def _check_correct_item_added(self, action_sequence: List[Dict]) -> bool:
        """Check if correct item was added to cart"""
        return not self._check_wrong_item_added_to_cart(action_sequence)
    
    def _check_checkout_elements_detected(self, dom_snapshot: str) -> bool:
        """Check if checkout elements were detected"""
        if not dom_snapshot:
            return False
        return any(checkout_term in dom_snapshot.lower() for checkout_term in DROPDOWN_ELEMENTS['checkout_elements'])
    
    def _check_checkout_interaction_success(self, action_sequence: List[Dict]) -> bool:
        """Check if checkout interaction was successful"""
        for action in action_sequence:
            if (action.get('type') == 'click' and
                any(checkout_term in action.get('target', '').lower() for checkout_term in DROPDOWN_ELEMENTS['checkout_elements'])):
                return action.get('success', False)
        return False
    
    def _check_checkout_interaction(self, action_sequence: List[Dict], dom_snapshot: str) -> bool:
        """Check overall checkout interaction success"""
        return (self._check_checkout_elements_detected(dom_snapshot) and 
                self._check_checkout_interaction_success(action_sequence))
    
    # Element extraction methods
    def _extract_dropdown_elements(self, dom_snapshot: str) -> List[str]:
        """Extract dropdown-related elements from DOM"""
        elements = []
        if dom_snapshot:
            for element_type in DROPDOWN_ELEMENTS['dropdown_trigger']:
                if element_type in dom_snapshot.lower():
                    elements.append(element_type)
        return elements
    
    def _extract_category_elements(self, dom_snapshot: str) -> List[str]:
        """Extract category elements from DOM"""
        elements = []
        if dom_snapshot:
            for element_type in DROPDOWN_ELEMENTS['men_option']:
                if element_type in dom_snapshot.lower():
                    elements.append(element_type)
        return elements
    
    def _extract_subcategory_elements(self, dom_snapshot: str) -> List[str]:
        """Extract subcategory elements from DOM"""
        elements = []
        if dom_snapshot:
            for element_list in [DROPDOWN_ELEMENTS['shoes_subcategory'], DROPDOWN_ELEMENTS['clothing_subcategory']]:
                for element_type in element_list:
                    if element_type in dom_snapshot.lower():
                        elements.append(element_type)
        return elements
    
    def _extract_filter_elements(self, dom_snapshot: str) -> List[str]:
        """Extract filter elements from DOM"""
        elements = []
        if dom_snapshot:
            for element_type in DROPDOWN_ELEMENTS['nike_filter']:
                if element_type in dom_snapshot.lower():
                    elements.append(element_type)
        return elements
    
    def _extract_product_elements(self, dom_snapshot: str) -> List[str]:
        """Extract product elements from DOM"""
        elements = []
        if dom_snapshot:
            for element_type in DROPDOWN_ELEMENTS['price_elements']:
                if element_type in dom_snapshot.lower():
                    elements.append(element_type)
        return elements
    
    def _extract_checkout_elements(self, dom_snapshot: str) -> List[str]:
        """Extract checkout elements from DOM"""
        elements = []
        if dom_snapshot:
            for element_list in [DROPDOWN_ELEMENTS['cart_elements'], DROPDOWN_ELEMENTS['checkout_elements']]:
                for element_type in element_list:
                    if element_type in dom_snapshot.lower():
                        elements.append(element_type)
        return elements
