"""
Data Models for Deterministic Dropdown Analysis
"""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any
from .config import RootCauseType

@dataclass
class DropdownStep:
    """Structure for individual dropdown workflow steps"""
    step_number: int
    step_name: str
    action_taken: str
    success: bool
    timing_ms: Optional[int] = None
    elements_detected: List[str] = None
    error_message: Optional[str] = None
    dom_snapshot: Optional[str] = None

    def __post_init__(self):
        if self.elements_detected is None:
            self.elements_detected = []

@dataclass
class DropdownAnalysisResult:
    """Structure for dropdown analysis results"""
    task_id: str
    framework: str
    steps: List[DropdownStep]
    root_cause: RootCauseType
    failure_step: Optional[int] = None
    analysis_details: Dict[str, Any] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.analysis_details is None:
            self.analysis_details = {}
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        result['root_cause'] = self.root_cause.value
        result['timestamp'] = self.timestamp.isoformat()
        return result

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
    steps: List[DropdownStep] = None

    def __post_init__(self):
        if self.reasoning_files is None:
            self.reasoning_files = {}
        if self.html_files is None:
            self.html_files = []
        if self.script_files is None:
            self.script_files = []
        if self.other_files is None:
            self.other_files = []
        if self.steps is None:
            self.steps = []

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        return result
