"""
Main Pipeline for Deterministic Dropdown Analysis
"""
import json
import asyncio
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from .task_collector import DropdownTaskCollector
from .deterministic_analyzer import DeterministicDropdownAnalyzer
from .models import TaskResult, DropdownAnalysisResult
from .config import logger, FRAMEWORK_PATTERNS

class DropdownDetPipeline:
    """
    Main pipeline for running deterministic dropdown root cause analysis
    """
    
    def __init__(self, parent_folder: str, output_dir: str):
        """
        Initialize the pipeline
        
        Args:
            parent_folder: Path to folder containing failed task data
            output_dir: Directory to save analysis results
        """
        self.parent_folder = parent_folder
        self.output_dir = Path(output_dir)
        self.task_collector = DropdownTaskCollector(parent_folder)
        self.analyzer = DeterministicDropdownAnalyzer()
        self.logger = logger
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def run_pipeline(self) -> Dict[str, Any]:
        """
        Run the complete analysis pipeline
        
        Returns:
            Dictionary with pipeline results and statistics
        """
        self.logger.info("Starting deterministic dropdown analysis pipeline")
        start_time = datetime.now()
        
        # Step 1: Collect all tasks
        self.logger.info("Step 1: Collecting tasks...")
        tasks = self.task_collector.collect_all_tasks()
        
        if not tasks:
            self.logger.warning("No tasks found to analyze")
            return {"error": "No tasks found", "task_count": 0}
        
        # Step 2: Analyze each task
        self.logger.info(f"Step 2: Analyzing {len(tasks)} tasks...")
        results = []
        
        for i, task in enumerate(tasks):
            try:
                self.logger.info(f"Analyzing task {i+1}/{len(tasks)}: {task.task_id}")
                result = await self._analyze_single_task(task)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Error analyzing task {task.task_id}: {e}")
                # Create error result
                error_result = DropdownAnalysisResult(
                    task_id=task.task_id,
                    framework="unknown",
                    steps=[],
                    root_cause=None,
                    analysis_details={"error": str(e)}
                )
                results.append(error_result)
        
        # Step 3: Generate reports
        self.logger.info("Step 3: Generating reports...")
        pipeline_stats = await self._generate_reports(results, start_time)
        
        self.logger.info(f"Pipeline completed in {pipeline_stats['duration_seconds']:.2f} seconds")
        return pipeline_stats
    
    async def _analyze_single_task(self, task: TaskResult) -> DropdownAnalysisResult:
        """
        Analyze a single task using the deterministic algorithm
        
        Args:
            task: TaskResult to analyze
            
        Returns:
            DropdownAnalysisResult with root cause analysis
        """
        # Extract data for analysis
        failure_log = self._extract_failure_log(task)
        dom_snapshot = self._extract_dom_snapshot(task)
        action_sequence = self._extract_action_sequence(task)
        framework = self._detect_framework(task)
        
        # Run deterministic analysis
        result = self.analyzer.analyze_task(
            task_result=task,
            failure_log=failure_log,
            dom_snapshot=dom_snapshot,
            action_sequence=action_sequence,
            framework=framework
        )
        
        return result
    
    def _extract_failure_log(self, task: TaskResult) -> str:
        """Extract failure log from task data"""
        log_content = ""
        
        # Check reasoning files for logs
        for file_path, content in task.reasoning_files.items():
            if any(term in file_path.lower() for term in ['log', 'error', 'failure']):
                log_content += content + "\n"
        
        # Check other files for logs
        for file_info in task.other_files:
            if (file_info.get('type') == 'other' and 
                any(term in file_info['path'].lower() for term in ['log', 'error'])):
                log_content += file_info.get('content', '') + "\n"
        
        return log_content.strip()
    
    def _extract_dom_snapshot(self, task: TaskResult) -> str:
        """Extract DOM snapshot from task data"""
        dom_content = ""
        
        # Get HTML content from HTML files
        for html_file in task.html_files:
            dom_content += html_file.get('content', '') + "\n"
        
        # Check reasoning files for DOM references
        for file_path, content in task.reasoning_files.items():
            if 'html' in file_path.lower() or 'dom' in file_path.lower():
                dom_content += content + "\n"
        
        return dom_content.strip()
    
    def _extract_action_sequence(self, task: TaskResult) -> List[Dict]:
        """Extract action sequence from task data"""
        actions = []
        
        # Parse steps from task
        for step in task.steps:
            action = {
                'type': 'step',
                'step_number': step.step_number,
                'action': step.action_taken,
                'success': step.success,
                'target': step.step_name,
                'timing_ms': step.timing_ms
            }
            actions.append(action)
        
        # Try to parse additional actions from script files
        for script_file in task.script_files:
            content = script_file.get('content', '')
            parsed_actions = self._parse_actions_from_script(content)
            actions.extend(parsed_actions)
        
        return actions
    
    def _parse_actions_from_script(self, script_content: str) -> List[Dict]:
        """Parse actions from script file content"""
        actions = []
        
        # Simple parsing - look for common action patterns
        lines = script_content.split('\n')
        for line in lines:
            line_lower = line.lower().strip()
            
            if 'click' in line_lower:
                actions.append({
                    'type': 'click',
                    'target': line.strip(),
                    'success': 'success' in line_lower or 'clicked' in line_lower
                })
            elif 'select' in line_lower:
                actions.append({
                    'type': 'select', 
                    'target': line.strip(),
                    'success': 'success' in line_lower or 'selected' in line_lower
                })
            elif 'type' in line_lower or 'input' in line_lower:
                actions.append({
                    'type': 'input',
                    'target': line.strip(),
                    'success': 'success' in line_lower
                })
        
        return actions
    
    def _detect_framework(self, task: TaskResult) -> str:
        """Detect framework used based on task data"""
        all_content = ""
        
        # Combine all text content
        for content in task.reasoning_files.values():
            all_content += content + " "
        
        for html_file in task.html_files:
            all_content += html_file.get('content', '') + " "
        
        all_content = all_content.lower()
        
        # Check for framework patterns
        for framework, pattern in FRAMEWORK_PATTERNS.items():
            if pattern.search(all_content):
                return framework
        
        return "unknown"
    
    async def _generate_reports(self, results: List[DropdownAnalysisResult], 
                              start_time: datetime) -> Dict[str, Any]:
        """
        Generate analysis reports and statistics
        
        Args:
            results: List of analysis results
            start_time: Pipeline start time
            
        Returns:
            Dictionary with pipeline statistics
        """
        end_time = datetime.now()
        duration = end_time - start_time
        
        # Calculate statistics
        total_tasks = len(results)
        successful_analyses = len([r for r in results if r.root_cause is not None])
        
        # Count root causes
        root_cause_counts = {}
        framework_counts = {}
        
        for result in results:
            if result.root_cause:
                cause = result.root_cause.value
                root_cause_counts[cause] = root_cause_counts.get(cause, 0) + 1
            
            framework = result.framework
            framework_counts[framework] = framework_counts.get(framework, 0) + 1
        
        # Save detailed results
        detailed_results_path = self.output_dir / "detailed_results.json"
        with open(detailed_results_path, 'w') as f:
            results_data = [result.to_dict() for result in results]
            json.dump(results_data, f, indent=2, default=str)
        
        # Save summary statistics
        stats = {
            "pipeline_info": {
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration_seconds": duration.total_seconds(),
                "algorithm_version": "deterministic_cascade_v1.0"
            },
            "task_statistics": {
                "total_tasks": total_tasks,
                "successful_analyses": successful_analyses,
                "failed_analyses": total_tasks - successful_analyses
            },
            "root_cause_distribution": root_cause_counts,
            "framework_distribution": framework_counts,
            "output_files": {
                "detailed_results": str(detailed_results_path),
                "summary_stats": str(self.output_dir / "summary_statistics.json")
            }
        }
        
        # Save summary statistics
        summary_path = self.output_dir / "summary_statistics.json"
        with open(summary_path, 'w') as f:
            json.dump(stats, f, indent=2, default=str)
        
        self.logger.info(f"Results saved to {self.output_dir}")
        self.logger.info(f"Root cause distribution: {root_cause_counts}")
        
        return stats
