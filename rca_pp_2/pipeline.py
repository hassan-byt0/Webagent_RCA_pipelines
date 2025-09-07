"""
RCA Pipeline Orchestration
"""
import json
import csv
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from dataclasses import asdict
from .models import TaskResult, RCAResult
from .task_collector import TaskResultCollector
#from .rca_analyzer import OpenAIRCAAnalyzer
from .rca_analyzer import GeminiRCAAnalyzer
from .file_processor import FileProcessor
from .config import GEMINI_API_KEY,GEMINI_MODEL

logger = logging.getLogger(__name__)

class RCAPipeline:
    def __init__(self, parent_folder: str, web_folder: str, output_dir: str = "rca_results"):
        self.parent_folder = parent_folder
        self.web_folder = Path(web_folder)
        self.output_dir = Path(output_dir)
        self.collector = TaskResultCollector(parent_folder)
        #self.analyzer = GeminiRCAAnalyzer()
        self.analyzer = GeminiRCAAnalyzer(api_key=GEMINI_API_KEY)
        #self.analyzer = OpenAIRCAAnalyzer()
        self.reference_html_map = self._load_reference_html()
        
        self.results = []
        self.processed_tasks = []
        self.output_dir.mkdir(parents=True, exist_ok=True)
        Path("cache/reasoning").mkdir(parents=True, exist_ok=True)
    
    def _load_reference_html(self) -> dict:
        """Load all reference HTML files with full content"""
        reference_map = {}
        if self.web_folder.exists() and self.web_folder.is_dir():
            for file_path in self.web_folder.glob("*.txt"):
                # Extract task ID from filename
                file_stem = file_path.stem
                if file_stem:
                    task_id = file_stem.split('_')[-1]
                    try:
                        # Get both parsed data and raw content
                        parsed = FileProcessor.parse_html_file(str(file_path))
                        with open(file_path, 'r', encoding='utf-8') as f:
                            raw_content = f.read()
                        # Add full content to parsed data
                        parsed['full_content'] = raw_content
                        reference_map[task_id] = parsed
                        logger.info(f"Loaded reference HTML for task ID: {task_id}")
                    except Exception as e:
                        logger.error(f"Error loading reference HTML for {file_path}: {e}")
        return reference_map

    async def run_pipeline(self) -> list[RCAResult]:
        """Execute pipeline with validation checks"""
        logger.info(f"Starting RCA pipeline: {self.parent_folder}")
        task_folders = self.collector.discover_task_folders()
        
        for task_folder in task_folders:
            try:
                folder_path = Path(task_folder)
                folder_name = folder_path.name
                task_id = folder_name.split('_')[-1]
                
                logger.info(f"Processing task: {folder_name} (ID: {task_id})")
                
                task_result = self.collector.process_task_folder(task_folder)
                self._validate_data_passing(task_result)
                
                # Get reference HTML for this task ID
                reference_html = self.reference_html_map.get(task_id)
                
                rca_result = await self.analyzer.analyze_task(task_result, reference_html)
                self.results.append(rca_result)
                
                self.processed_tasks.append({
                    'task_id': task_id,
                    'folder_name': folder_name,
                    'status': task_result.status,
                    'verified': task_result.verified_success,
                    'folder_path': task_folder,
                    'file_count': task_result.folder_structure.get('total_files'),
                    'reasoning_files': len(task_result.reasoning_files),
                    'html_files': len(task_result.html_files),
                    'db_files': len(task_result.db_data),
                    'reference_available': reference_html is not None
                })
                
            except Exception as e:
                logger.exception(f"Failed processing task {task_folder}: {e}")
                folder_name = Path(task_folder).name
                task_id = folder_name.split('_')[-1] if '_' in folder_name else folder_name
                # Create error result for failed tasks
                self.results.append(self.analyzer._error_result(
                    task_id, 
                    f"Processing error: {str(e)}"
                ))
                self.processed_tasks.append({
                    'task_id': task_id,
                    'folder_name': folder_name,
                    'status': "error",
                    'verified': False,
                    'folder_path': task_folder,
                    'file_count': 0,
                    'reasoning_files': 0,
                    'html_files': 0,
                    'db_files': 0,
                    'reference_available': False
                })
        
        self._save_results()
        logger.info(f"Pipeline completed. Processed {len(self.results)} tasks")
        return self.results

    def _validate_data_passing(self, task_result: TaskResult):
        """Validate critical data passing with better HTML analysis"""
        validation_notes = []
        
        if not task_result.html_files:
            validation_notes.append("No HTML files processed")
        else:
            for html in task_result.html_files:
                if 'error' in html:
                    validation_notes.append(f"HTML error: {html.get('file_path')} - {html['error']}")
                elif html.get('content_length', 0) == 0:
                    validation_notes.append(f"HTML empty: {html.get('file_path')}")
                elif not html.get('detected_frameworks') and not html.get('element_counts'):
                    validation_notes.append(f"HTML analysis found no frameworks/elements: {html.get('file_path')}")
        
        if task_result.db_data:
            for path, data in task_result.db_data.items():
                if 'error' in data:
                    validation_notes.append(f"DB error: {path} - {data['error']}")
        
        if not task_result.reasoning_files:
            validation_notes.append("No reasoning files found")
        
        if validation_notes:
            logger.warning(f"Data validation issues for {task_result.task_id}:")
            for note in validation_notes:
                logger.warning(f"- {note}")

    def _save_results(self):
        """Save results with data validation"""
        # Main JSON output
        json_path = self.output_dir / "rca_results.json"
        with open(json_path, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "tasks": [asdict(r) for r in self.results],
                "processed_tasks": self.processed_tasks
            }, f, indent=2, default=str)
        
        # RCA Analysis CSV
        rca_csv = self.output_dir / "rca_analysis.csv"
        with open(rca_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'task_id', 'status', 'framework', 'element_types', 
                'root_causes', 'five_whys', 'db_issues', 
                'recommendations', 'analysis_summary'
            ])
            writer.writeheader()
            for result in self.results:
                writer.writerow({
                    'task_id': result.task_id,
                    'status': "success" if "success" in result.analysis_summary.lower() else "failure",
                    'framework': result.framework,
                    'element_types': json.dumps(result.element_types),
                    'root_causes': ' | '.join(result.root_causes),
                    'five_whys': json.dumps(result.five_whys),
                    'db_issues': ' | '.join(result.db_issues),
                    'recommendations': ' | '.join(result.recommendations),
                    'analysis_summary': result.analysis_summary
                })
        
        # Data Validation Report
        validation_csv = self.output_dir / "data_validation.csv"
        with open(validation_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'task_id', 'html_files', 'db_files', 'reasoning_files',
                'framework_detected', 'elements_detected', 'validation_notes',
                'reference_available'
            ])
            writer.writeheader()
            for task in self.processed_tasks:
                html_processed = task['html_files'] > 0
                db_processed = task['db_files'] > 0
                reasoning_processed = task['reasoning_files'] > 0
                
                result = next((r for r in self.results if r.task_id == task['task_id']), None)
                
                framework_detected = result.framework != "Unknown" if result else False
                elements_detected = bool(result.element_types) if result else False
                
                validation_status = "OK" if all([
                    html_processed, 
                    db_processed,
                    reasoning_processed
                ]) else "Validation issues"
                
                writer.writerow({
                    'task_id': task['task_id'],
                    'html_files': task['html_files'],
                    'db_files': task['db_files'],
                    'reasoning_files': task['reasoning_files'],
                    'framework_detected': framework_detected,
                    'elements_detected': elements_detected,
                    'validation_notes': validation_status,
                    'reference_available': task['reference_available']
                })
        
        logger.info(f"Results saved to {self.output_dir}")