"""
Task Collection and Processing
"""
import os
import logging
from pathlib import Path
from datetime import datetime
from .models import TaskResult
from .file_processor import FileProcessor
from .db_processor import DatabaseProcessor
from .task_validator import TaskValidator
from .config import DB_EXTENSIONS

logger = logging.getLogger(__name__)

class TaskResultCollector:
    def __init__(self, parent_folder: str):
        self.parent_folder = Path(parent_folder)
        self.file_processor = FileProcessor()
        self.db_processor = DatabaseProcessor()

    def discover_task_folders(self) -> list[str]:
        """Discover all task folders in the parent directory"""
        if not self.parent_folder.exists():
            logger.error(f"Parent folder does not exist: {self.parent_folder}")
            return []
        return [str(item) for item in self.parent_folder.iterdir() if item.is_dir()]

    def analyze_folder_structure(self, task_folder: Path) -> dict[str, any]:
        """Analyze folder structure with validation"""
        structure = {
            'total_files': 0,
            'total_folders': 0,
            'file_types': {},
            'folder_names': []
        }
        
        try:
            for item in task_folder.rglob("*"):
                if item.is_file():
                    structure['total_files'] += 1
                    ext = item.suffix.lower() or 'no_extension'
                    structure['file_types'][ext] = structure['file_types'].get(ext, 0) + 1
                elif item.is_dir() and item != task_folder:
                    structure['total_folders'] += 1
                    structure['folder_names'].append(str(item.relative_to(task_folder)))
        except Exception as e:
            logger.error(f"Error analyzing folder structure: {e}")
        return structure

    def process_task_folder(self, task_folder_path: str) -> TaskResult:
        """Process task folder with data validation"""
        task_folder = Path(task_folder_path)
        task_id = task_folder.name
        logger.info(f"Processing task: {task_id}")
        
        task_result = TaskResult(
            task_id=task_id,
            timestamp=datetime.now(),
            task_type=self.detect_task_type(task_folder),
            status="unknown"
        )

        task_result.folder_structure = self.analyze_folder_structure(task_folder)

        for file_path in task_folder.rglob("*"):
            if file_path.is_file():
                self._process_individual_file(file_path, task_result, task_folder)

        task_result.verified_success = TaskValidator.validate_task(task_result)
        task_result.status = "successful" if task_result.verified_success else "unsuccessful"
        
        logger.info(f"Task processed: {task_id} | Status: {task_result.status} | Verified: {task_result.verified_success}")
        return task_result

    def detect_task_type(self, task_folder: Path) -> str:
        """Detect task type based on folder name and content"""
        folder_name = task_folder.name.lower()
        
        if "login" in folder_name:
            return "login"
        if "shop" in folder_name or "cart" in folder_name or "buy" in folder_name:
            return "shopping"
        if "form" in folder_name or "submit" in folder_name:
            return "form_submission"
        
        for file_path in task_folder.glob("*.txt"):
            if "reasoning" in file_path.name.lower():
                content = FileProcessor.read_text_file(str(file_path)).lower()
                if "add to cart" in content:
                    return "shopping"
                if "login" in content:
                    return "login"
        
        return "web_task"

    def _process_individual_file(self, file_path: Path, task_result: TaskResult, task_folder: Path):
        """Process file with enhanced validation"""
        try:
            file_ext = file_path.suffix.lower()
            relative_path = file_path.relative_to(task_folder)
            
            if file_ext in DB_EXTENSIONS:
                db_data = self.db_processor.extract_db_data(str(file_path))
                task_result.db_data[str(relative_path)] = db_data
            
            elif file_ext in ['.html', '.htm']:
                html_data = self.file_processor.parse_html_file(str(file_path))
                html_data['content'] = self.file_processor.read_text_file(str(file_path))[:5000]
                task_result.html_files.append(html_data)
            
            elif file_ext == '.txt' and 'reasoning' in file_path.name.lower():
                content = self.file_processor.read_text_file(str(file_path))
                task_result.reasoning_files[str(relative_path)] = content
            
            elif file_ext in ['.js', '.py', '.sh', '.bat', '.ps1']:
                script_data = self.file_processor.read_script_file(str(file_path))
                task_result.script_files.append(script_data)
            
            else:
                other_data = self.file_processor.process_other_file(str(file_path))
                task_result.other_files.append(other_data)
        
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")