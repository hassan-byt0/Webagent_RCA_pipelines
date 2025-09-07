"""
Data Models for RCA Pipeline
"""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any

@dataclass
class TaskResult:
    """Structure for webagent task results"""
    task_id: str
    timestamp: datetime
    task_type: str
    status: str
    verified_success: bool = False
    reasoning_files: Dict[str, str] = None
    html_files: List[Dict] = None
    script_files: List[Dict] = None
    db_data: Optional[Dict] = None
    other_files: List[Dict] = None
    folder_structure: Dict = None

    def __post_init__(self):
        if self.reasoning_files is None:
            self.reasoning_files = {}
        if self.html_files is None:
            self.html_files = []
        if self.script_files is None:
            self.script_files = []
        if self.other_files is None:
            self.other_files = []
        if self.folder_structure is None:
            self.folder_structure = {}
        if self.db_data is None:
            self.db_data = {}

@dataclass
class RCAResult:
    """Structure for RCA analysis results"""
    task_id: str
    analysis_timestamp: datetime
    root_causes: List[str]
    five_whys: Dict[str, List[str]]
    contributing_factors: List[str]
    recommendations: List[str]
    analysis_summary: str
    framework: str = ""
    element_types: Dict[str, int] = None
    db_issues: List[str] = None

    def __post_init__(self):
        if self.element_types is None:
            self.element_types = {}
        if self.db_issues is None:
            self.db_issues = []