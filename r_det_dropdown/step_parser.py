"""
Step Parser for Deterministic Dropdown Analysis
Parses workflow steps from various input formats
"""
import json
import re
from typing import List, Dict, Any, Optional
from .models import DropdownStep
from .config import logger, DROPDOWN_STEPS

class DropdownStepParser:
    """
    Parses dropdown workflow steps from different input formats
    """
    
    def __init__(self):
        self.logger = logger
    
    def parse_steps_from_input(self, input_data: Any) -> List[DropdownStep]:
        """
        Parse steps from various input formats
        
        Args:
            input_data: Can be string, dict, list, or file path
            
        Returns:
            List of DropdownStep objects
        """
        if isinstance(input_data, str):
            # Try to parse as JSON first
            try:
                json_data = json.loads(input_data)
                return self._parse_steps_from_dict(json_data)
            except json.JSONDecodeError:
                # Parse as text
                return self._parse_steps_from_text(input_data)
        
        elif isinstance(input_data, dict):
            return self._parse_steps_from_dict(input_data)
        
        elif isinstance(input_data, list):
            return self._parse_steps_from_list(input_data)
        
        else:
            self.logger.warning(f"Unsupported input type: {type(input_data)}")
            return []
    
    def _parse_steps_from_text(self, text: str) -> List[DropdownStep]:
        """Parse steps from plain text"""
        steps = []
        lines = text.split('\n')
        
        step_number = 1
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for step indicators
            step_info = self._extract_step_info_from_line(line, step_number)
            if step_info:
                steps.append(step_info)
                step_number += 1
        
        return steps
    
    def _parse_steps_from_dict(self, data: Dict) -> List[DropdownStep]:
        """Parse steps from dictionary format"""
        steps = []
        
        # Handle different dictionary structures
        if 'steps' in data:
            step_data = data['steps']
        elif 'actions' in data:
            step_data = data['actions']
        elif 'workflow' in data:
            step_data = data['workflow']
        else:
            # Treat the whole dict as step data
            step_data = data
        
        if isinstance(step_data, list):
            return self._parse_steps_from_list(step_data)
        elif isinstance(step_data, dict):
            # Convert dict to list of steps
            for key, value in step_data.items():
                step = self._create_step_from_key_value(key, value)
                if step:
                    steps.append(step)
        
        return steps
    
    def _parse_steps_from_list(self, step_list: List) -> List[DropdownStep]:
        """Parse steps from list format"""
        steps = []
        
        for i, item in enumerate(step_list):
            if isinstance(item, dict):
                step = self._create_step_from_dict(item, i + 1)
            elif isinstance(item, str):
                step = self._extract_step_info_from_line(item, i + 1)
            else:
                continue
            
            if step:
                steps.append(step)
        
        return steps
    
    def _create_step_from_dict(self, step_dict: Dict, step_number: int) -> Optional[DropdownStep]:
        """Create DropdownStep from dictionary"""
        try:
            # Extract common fields
            step_name = (step_dict.get('name') or 
                        step_dict.get('step_name') or 
                        step_dict.get('title') or
                        DROPDOWN_STEPS.get(step_number, f"Step {step_number}"))
            
            action_taken = (step_dict.get('action') or
                           step_dict.get('action_taken') or
                           step_dict.get('description') or
                           "Unknown action")
            
            success = step_dict.get('success', False)
            if isinstance(success, str):
                success = success.lower() in ['true', 'success', 'completed', 'yes']
            
            timing_ms = step_dict.get('timing_ms') or step_dict.get('duration')
            if timing_ms and isinstance(timing_ms, str):
                # Extract number from string
                timing_match = re.search(r'\d+', timing_ms)
                timing_ms = int(timing_match.group()) if timing_match else None
            
            elements_detected = step_dict.get('elements_detected', [])
            if isinstance(elements_detected, str):
                elements_detected = [elements_detected]
            
            error_message = step_dict.get('error') or step_dict.get('error_message')
            
            return DropdownStep(
                step_number=step_dict.get('step_number', step_number),
                step_name=step_name,
                action_taken=action_taken,
                success=success,
                timing_ms=timing_ms,
                elements_detected=elements_detected,
                error_message=error_message
            )
            
        except Exception as e:
            self.logger.warning(f"Error creating step from dict: {e}")
            return None
    
    def _create_step_from_key_value(self, key: str, value: Any) -> Optional[DropdownStep]:
        """Create DropdownStep from key-value pair"""
        try:
            # Try to extract step number from key
            step_match = re.search(r'step[\s_]*(\d+)', key.lower())
            step_number = int(step_match.group(1)) if step_match else 1
            
            if isinstance(value, dict):
                return self._create_step_from_dict(value, step_number)
            elif isinstance(value, str):
                success = any(term in value.lower() for term in ['success', 'completed', 'true'])
                
                return DropdownStep(
                    step_number=step_number,
                    step_name=DROPDOWN_STEPS.get(step_number, key),
                    action_taken=value,
                    success=success
                )
            else:
                return None
                
        except Exception as e:
            self.logger.warning(f"Error creating step from key-value: {e}")
            return None
    
    def _extract_step_info_from_line(self, line: str, step_number: int) -> Optional[DropdownStep]:
        """Extract step information from a single line of text"""
        try:
            # Determine success from keywords
            line_lower = line.lower()
            success_keywords = ['success', 'completed', 'found', 'clicked', 'selected', 'true']
            failure_keywords = ['failed', 'error', 'not found', 'unable', 'timeout', 'false']
            
            success = False
            if any(keyword in line_lower for keyword in success_keywords):
                success = True
            elif any(keyword in line_lower for keyword in failure_keywords):
                success = False
            
            # Extract timing if present
            timing_match = re.search(r'(\d+)\s*ms', line)
            timing_ms = int(timing_match.group(1)) if timing_match else None
            
            # Determine step name based on content
            step_name = self._determine_step_name_from_content(line, step_number)
            
            return DropdownStep(
                step_number=step_number,
                step_name=step_name,
                action_taken=line.strip(),
                success=success,
                timing_ms=timing_ms
            )
            
        except Exception as e:
            self.logger.warning(f"Error extracting step info from line: {e}")
            return None
    
    def _determine_step_name_from_content(self, content: str, step_number: int) -> str:
        """Determine step name based on content keywords"""
        content_lower = content.lower()
        
        # Keyword mapping to step types
        keyword_to_step = {
            'dropdown': "Initial Element Detection",
            'men': "Primary Category Navigation",
            'category': "Primary Category Navigation", 
            'subcategory': "Subcategory Selection Validation",
            'shoes': "Subcategory Selection Validation",
            'clothing': "Subcategory Selection Validation",
            'filter': "Filter Application Verification",
            'nike': "Filter Application Verification",
            'product': "Product Analysis and Selection",
            'price': "Product Analysis and Selection",
            'cart': "Transaction Completion",
            'checkout': "Transaction Completion"
        }
        
        for keyword, step_name in keyword_to_step.items():
            if keyword in content_lower:
                return step_name
        
        # Fallback to default step name
        return DROPDOWN_STEPS.get(step_number, f"Step {step_number}")
    
    def validate_steps(self, steps: List[DropdownStep]) -> List[DropdownStep]:
        """
        Validate and normalize the parsed steps
        
        Args:
            steps: List of parsed steps
            
        Returns:
            List of validated and normalized steps
        """
        validated_steps = []
        
        for step in steps:
            # Ensure step number is within valid range
            if step.step_number < 1 or step.step_number > 6:
                self.logger.warning(f"Invalid step number {step.step_number}, adjusting")
                step.step_number = max(1, min(6, step.step_number))
            
            # Ensure step name matches expected workflow
            expected_name = DROPDOWN_STEPS.get(step.step_number)
            if expected_name and step.step_name != expected_name:
                self.logger.info(f"Normalizing step name from '{step.step_name}' to '{expected_name}'")
                step.step_name = expected_name
            
            validated_steps.append(step)
        
        return validated_steps
