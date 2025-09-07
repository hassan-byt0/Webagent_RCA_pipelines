"""
Task Collector for ArXiv Search Deterministic Analysis
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    from .models import TaskResult, ArxivSearchStep
    from .config import logger, TEXT_EXTENSIONS, DB_EXTENSIONS
except ImportError:
    from models import TaskResult, ArxivSearchStep
    from config import logger, TEXT_EXTENSIONS, DB_EXTENSIONS

class ArxivTaskCollector:
    """
    Collects and processes task data for ArXiv search workflow analysis
    """
    
    def __init__(self, parent_folder: str):
        self.parent_folder = Path(parent_folder)
        self.logger = logger
    
    def collect_all_tasks(self) -> List[TaskResult]:
        """
        Collect all tasks from the parent folder
        
        Returns:
            List of TaskResult objects
        """
        tasks = []
        
        if not self.parent_folder.exists():
            self.logger.error(f"Parent folder does not exist: {self.parent_folder}")
            return tasks
        
        # Iterate through all task folders
        for task_folder in self.parent_folder.iterdir():
            if task_folder.is_dir():
                try:
                    task_result = self._process_task_folder(task_folder)
                    if task_result:
                        tasks.append(task_result)
                        self.logger.info(f"Collected task: {task_result.task_id}")
                except Exception as e:
                    self.logger.error(f"Error processing task folder {task_folder}: {e}")
        
        self.logger.info(f"Collected {len(tasks)} tasks total")
        return tasks
    
    def _process_task_folder(self, task_folder: Path) -> Optional[TaskResult]:
        """
        Process a single task folder and extract relevant data
        
        Args:
            task_folder: Path to the task folder
            
        Returns:
            TaskResult object or None if processing fails
        """
        task_id = task_folder.name
        
        # Initialize task result
        task_result = TaskResult(
            task_id=task_id,
            timestamp=datetime.fromtimestamp(task_folder.stat().st_mtime),
            task_type="arxiv_search",
            status="failed"  # Assuming failed tasks folder
        )
        
        # Process files in the task folder
        for file_path in task_folder.rglob("*"):
            if file_path.is_file():
                self._process_file(file_path, task_result, task_folder)
        
        # Extract steps from collected data
        task_result.steps = self._extract_steps_from_task_data(task_result)
        
        return task_result
    
    def _process_file(self, file_path: Path, task_result: TaskResult, task_folder: Path):
        """
        Process a single file and add its data to the task result
        
        Args:
            file_path: Path to the file
            task_result: TaskResult to update
            task_folder: Base task folder path
        """
        try:
            relative_path = file_path.relative_to(task_folder)
            file_info = {
                'path': str(relative_path),
                'full_path': str(file_path),
                'size': file_path.stat().st_size,
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime)
            }
            
            # Categorize file based on type and content
            if file_path.suffix.lower() in TEXT_EXTENSIONS:
                content = self._safe_read_text_file(file_path)
                file_info['content'] = content
                
                # Categorize based on filename and content
                filename_lower = file_path.name.lower()
                if any(term in filename_lower for term in ['reasoning', 'thought', 'plan']):
                    task_result.reasoning_files[str(relative_path)] = content
                elif 'html' in filename_lower or file_path.suffix.lower() == '.html':
                    file_info['type'] = 'html'
                    task_result.html_files.append(file_info)
                elif any(term in filename_lower for term in ['script', 'action', 'step']):
                    file_info['type'] = 'script'
                    task_result.script_files.append(file_info)
                else:
                    file_info['type'] = 'other'
                    task_result.other_files.append(file_info)
            
            elif file_path.suffix.lower() == '.html':
                content = self._safe_read_text_file(file_path)
                file_info['content'] = content
                file_info['type'] = 'html'
                task_result.html_files.append(file_info)
            
            elif file_path.suffix.lower() in DB_EXTENSIONS:
                # Handle database files
                file_info['type'] = 'database'
                # For now, just store the path - could add DB parsing later
                if task_result.db_data is None:
                    task_result.db_data = {}
                task_result.db_data[str(relative_path)] = str(file_path)
            
            else:
                file_info['type'] = 'other'
                task_result.other_files.append(file_info)
                
        except Exception as e:
            self.logger.warning(f"Error processing file {file_path}: {e}")
    
    def _safe_read_text_file(self, file_path: Path) -> str:
        """
        Safely read a text file with encoding detection
        
        Args:
            file_path: Path to the text file
            
        Returns:
            File content as string
        """
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                self.logger.warning(f"Error reading file {file_path} with {encoding}: {e}")
        
        # If all encodings fail, try binary mode and decode with errors='ignore'
        try:
            with open(file_path, 'rb') as f:
                return f.read().decode('utf-8', errors='ignore')
        except Exception as e:
            self.logger.error(f"Failed to read file {file_path}: {e}")
            return ""
    
    def _extract_steps_from_task_data(self, task_result: TaskResult) -> List[ArxivSearchStep]:
        """
        Extract workflow steps from the collected task data
        
        Args:
            task_result: TaskResult with collected file data
            
        Returns:
            List of ArxivSearchStep objects
        """
        steps = []
        
        # Try to extract steps from script files
        for script_file in task_result.script_files:
            content = script_file.get('content', '')
            if content:
                extracted_steps = self._parse_steps_from_content(content)
                steps.extend(extracted_steps)
        
        # Try to extract from reasoning files
        for reasoning_content in task_result.reasoning_files.values():
            if reasoning_content:
                extracted_steps = self._parse_steps_from_content(reasoning_content)
                steps.extend(extracted_steps)
        
        # If no steps found, create default structure
        if not steps:
            steps = self._create_default_steps()
        
        return steps
    
    def _parse_steps_from_content(self, content: str) -> List[ArxivSearchStep]:
        """
        Parse workflow steps from file content
        
        Args:
            content: File content to parse
            
        Returns:
            List of extracted ArxivSearchStep objects
        """
        steps = []
        step_indicators = [
            "navigation", "arxiv", "author", "input", "classification", 
            "subject", "date", "search", "results"
        ]
        
        lines = content.split('\n')
        current_step = 1
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            
            for indicator in step_indicators:
                if indicator in line_lower:
                    # Determine step type and success
                    step_name = self._determine_step_name(current_step, indicator)
                    success = self._determine_step_success(line_lower, lines[i:i+3])
                    
                    step = ArxivSearchStep(
                        step_number=current_step,
                        step_name=step_name,
                        action_taken=line.strip(),
                        success=success
                    )
                    steps.append(step)
                    current_step += 1
                    break
        
        return steps
    
    def _determine_step_name(self, step_number: int, indicator: str) -> str:
        """Determine step name based on step number and indicator"""
        step_names = {
            1: "Navigation and Page Load Verification",
            2: "Author Input Field Analysis",
            3: "Classification Label Processing",
            4: "Date Input Validation",
            5: "Search Execution and Results Verification"
        }
        return step_names.get(step_number, f"Step {step_number}")
    
    def _determine_step_success(self, current_line: str, context_lines: List[str]) -> bool:
        """Determine if a step was successful based on content"""
        success_indicators = ['success', 'completed', 'found', 'clicked', 'selected', 'detected']
        failure_indicators = ['error', 'failed', 'not found', 'unable', 'timeout', 'captcha']
        
        # Check current line and next few lines for success/failure indicators
        text_to_check = ' '.join(context_lines).lower()
        
        has_success = any(indicator in text_to_check for indicator in success_indicators)
        has_failure = any(indicator in text_to_check for indicator in failure_indicators)
        
        if has_failure:
            return False
        elif has_success:
            return True
        else:
            # Default to failed if unclear
            return False
    
    def _create_default_steps(self) -> List[ArxivSearchStep]:
        """Create default ArXiv search workflow steps"""
        default_steps = [
            ArxivSearchStep(1, "Navigation and Page Load Verification", "Navigate to ArXiv", False),
            ArxivSearchStep(2, "Author Input Field Analysis", "Input author information", False),
            ArxivSearchStep(3, "Classification Label Processing", "Select classifications", False),
            ArxivSearchStep(4, "Date Input Validation", "Input date criteria", False),
            ArxivSearchStep(5, "Search Execution and Results Verification", "Execute search", False)
        ]
        return default_steps
