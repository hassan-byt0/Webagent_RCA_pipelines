#!/usr/bin/env python3
"""
Comprehensive WebAgent RCA Pipeline with Hierarchical Processing
- Multi-stage summarization for large reasoning files
- Strict token budgeting with request validation
- Hierarchical RCA analysis
- Enhanced HTML analysis with fallbacks
"""

import os
import json
import sqlite3
import logging
import asyncio
import re
import csv
import hashlib
import time
import tiktoken
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rca_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Token estimation function
def estimate_tokens(text: str, model: str) -> int:
    """Estimate tokens using tiktoken or fallback method"""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        return len(text) // 4 + 1

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

class FileProcessor:
    """Handles file processing with enhanced framework detection"""
    
    DB_EXTENSIONS = ['.db', '.sqlite', '.sqlite3', '.db3', '.sql', '.dat']
    HIDDEN_CLASSES = ['hidden', 'invisible', 'offscreen', 'sr-only', 'd-none', 'is-hidden']
    FRAMEWORK_PATTERNS = {
        'react': re.compile(r'react|react-dom'),
        'vue': re.compile(r'vue'),
        'angular': re.compile(r'angular'),
        'jquery': re.compile(r'jquery'),
        'antd': re.compile(r'ant-'),
        'material_ui': re.compile(r'Mui'),
        'bootstrap': re.compile(r'bs-|bootstrap|btn-'),
        'chakra': re.compile(r'chakra-'),
        'tailwind': re.compile(r'tw-|tailwind'),
    }
    
    @staticmethod
    def read_text_file(file_path: str) -> str:
        """Read text files with robust encoding handling"""
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.error(f"Error reading file {file_path}: {e}")
                break
        return ""

    @staticmethod
    def parse_html_file(file_path: str) -> Dict[str, Any]:
        """Parse HTML files with enhanced framework detection and error recovery"""
        try:
            content = FileProcessor.read_text_file(file_path)
            if not content:
                return {
                    'file_path': str(file_path),
                    'error': 'Empty content',
                    'primary_framework': 'Unknown'
                }
            
            soup = BeautifulSoup(content, 'html.parser')
            result = {
                'file_path': str(file_path),
                'title': soup.title.string if soup.title else "No title",
                'content_length': len(content),
                'detected_frameworks': [],
                'ui_elements': [],
                'primary_framework': 'Unknown'  # Default value
            }
            
            # Detect frameworks and UI elements with error handling
            try:
                FileProcessor._detect_framework_elements(soup, result)
                FileProcessor._detect_ui_elements(soup, result)
            except Exception as e:
                logger.error(f"Error analyzing HTML: {e}")
                result['error'] = str(e)
            
            return result
        except Exception as e:
            logger.exception(f"Error parsing HTML file {file_path}")
            return {
                'file_path': str(file_path),
                'error': str(e),
                'primary_framework': 'Unknown'
            }
    
    @staticmethod
    def _detect_framework_elements(soup, result):
        """Enhanced framework detection with multiple methods"""
        framework_counts = {}
        
        # Script-based detection
        for script in soup.find_all('script'):
            src = script.get('src', '').lower()
            content = script.string or ''
            for fw, pattern in FileProcessor.FRAMEWORK_PATTERNS.items():
                if pattern.search(src) or pattern.search(content):
                    framework_counts[fw] = framework_counts.get(fw, 0) + 1
        
        # Attribute-based detection
        if soup.find(attrs={'v-bind': True}):
            framework_counts['vue'] = framework_counts.get('vue', 0) + 1
        if soup.find(attrs={'ng-app': True}):
            framework_counts['angular'] = framework_counts.get('angular', 0) + 1
        if soup.find(attrs={'data-reactroot': True}):
            framework_counts['react'] = framework_counts.get('react', 0) + 1
        
        # Class-based detection
        for element in soup.find_all(class_=True):
            classes = ' '.join(element.get('class', []))
            for fw, pattern in FileProcessor.FRAMEWORK_PATTERNS.items():
                if pattern.search(classes):
                    framework_counts[fw] = framework_counts.get(fw, 0) + 1
        
        # Determine primary framework
        if framework_counts:
            sorted_frameworks = sorted(framework_counts.items(), key=lambda x: x[1], reverse=True)
            result['detected_frameworks'] = [fw for fw, count in sorted_frameworks]
            result['primary_framework'] = sorted_frameworks[0][0]
    
    @staticmethod
    def _detect_ui_elements(soup, result):
        """Enhanced UI element detection with role-based classification"""
        element_counts = {}
        role_mapping = {
            'button': ['button', 'menuitem'],
            'dropdown': ['combobox', 'listbox'],
            'input': ['textbox', 'searchbox'],
            'checkbox': ['checkbox'],
            'radio': ['radio'],
            'slider': ['slider'],
            'modal': ['dialog'],
            'tab': ['tab'],
            'accordion': ['region', 'group'],
            'datepicker': ['grid']
        }
        
        # Process all elements
        for element in soup.find_all():
            element_type = None
            
            # Detect by ARIA role
            role = element.get('role', '')
            for elem_type, roles in role_mapping.items():
                if role in roles:
                    element_type = elem_type
                    break
            
            # Detect by common patterns
            if not element_type:
                classes = ' '.join(element.get('class', []))
                if 'dropdown' in classes or 'select' in classes:
                    element_type = 'dropdown'
                elif 'modal' in classes or 'dialog' in classes:
                    element_type = 'modal'
                elif 'date' in classes or 'calendar' in classes:
                    element_type = 'datepicker'
                elif 'tab' in classes:
                    element_type = 'tab'
                elif 'accordion' in classes or 'collapse' in classes:
                    element_type = 'accordion'
            
            # Detect by tag name
            if not element_type:
                if element.name == 'select':
                    element_type = 'dropdown'
                elif element.name == 'input' and element.get('type') == 'date':
                    element_type = 'datepicker'
                elif element.name == 'dialog':
                    element_type = 'modal'
            
            # Record element if classified
            if element_type:
                element_counts[element_type] = element_counts.get(element_type, 0) + 1
                result['ui_elements'].append({
                    'element_type': element_type,
                    'tag': element.name,
                    'id': element.get('id'),
                    'classes': element.get('class', []),
                    'role': role,
                    'aria_attributes': {k:v for k,v in element.attrs.items() if k.startswith('aria-')},
                    'visible': FileProcessor._is_element_visible(element),
                    'text_content': (element.text or '').strip()[:100]
                })
        
        # Add element counts
        result['element_counts'] = element_counts
    
    @staticmethod
    def _is_element_visible(element) -> bool:
        """Comprehensive visibility detection"""
        # Check hidden attribute
        if element.get('hidden') == 'hidden' or element.get('aria-hidden') == 'true':
            return False
            
        # Check inline styles
        style = element.get('style', '').lower()
        if 'display:none' in style or 'visibility:hidden' in style or 'opacity:0' in style:
            return False
            
        # Check CSS classes
        classes = element.get('class', [])
        if any(hc in classes for hc in FileProcessor.HIDDEN_CLASSES):
            return False
            
        # Check dimensions
        if element.get('width') == '0' or element.get('height') == '0':
            return False
            
        # Check off-screen positioning
        if 'position:absolute' in style and ('left:-9999px' in style or 'top:-9999px' in style):
            return False
            
        # Check visibility property
        if 'visibility:hidden' in style:
            return False
            
        return True

    @staticmethod
    def read_script_file(file_path: str) -> Dict[str, Any]:
        """Read and analyze script files"""
        try:
            content = FileProcessor.read_text_file(file_path)
            return {
                'file_path': str(file_path),
                'file_name': os.path.basename(file_path),
                'extension': Path(file_path).suffix,
                'size': len(content),
                'line_count': len(content.splitlines()),
                'has_async': 'async' in content or 'await' in content,
                'has_imports': 'import' in content or 'require' in content,
                'content_snippet': content[:1000] if content else ''
            }
        except Exception as e:
            logger.error(f"Error reading script file {file_path}: {e}")
            return {'file_path': str(file_path), 'error': str(e)}
    
    @staticmethod
    def process_other_file(file_path: str) -> Dict[str, Any]:
        """Process other file types with validation"""
        try:
            file_ext = Path(file_path).suffix.lower()
            file_info = {
                'file_path': str(file_path),
                'file_name': os.path.basename(file_path),
                'extension': file_ext,
                'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
            }

            text_extensions = ['.log', '.txt', '.json', '.xml', '.yaml', '.yml', '.cfg', '.ini', '.conf']
            if file_ext in text_extensions:
                content = FileProcessor.read_text_file(file_path)
                file_info['content'] = content[:5000] if content else ''
            return file_info
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return {'file_path': str(file_path), 'error': str(e)}

class DatabaseProcessor:
    """Enhanced database processing with validation and retries"""
    
    MAX_RETRIES = 3
    RETRY_DELAY = 1

    @staticmethod
    def extract_db_data(db_path: str) -> Dict[str, Any]:
        """Robust database extraction with retries"""
        for attempt in range(DatabaseProcessor.MAX_RETRIES):
            try:
                return DatabaseProcessor._extract_data(db_path)
            except sqlite3.OperationalError as e:
                if "locked" in str(e) and attempt < DatabaseProcessor.MAX_RETRIES - 1:
                    logger.warning(f"Database locked, retrying ({attempt+1}/{DatabaseProcessor.MAX_RETRIES})")
                    time.sleep(DatabaseProcessor.RETRY_DELAY * (attempt + 1))
                else:
                    logger.error(f"Database error after {attempt+1} attempts: {e}")
                    return {'db_path': str(db_path), 'error': str(e)}
            except Exception as e:
                logger.exception(f"Critical database error: {e}")
                return {'db_path': str(db_path), 'error': str(e)}
        return {'db_path': str(db_path), 'error': "Max retries exceeded"}

    @staticmethod
    def _extract_data(db_path: str) -> Dict[str, Any]:
        """Actual database extraction logic"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in cursor.fetchall()]
            db_data = {
                'db_path': str(db_path),
                'tables': {},
                'total_tables': len(tables)
            }
            
            for table in tables:
                try:
                    cursor.execute(f"PRAGMA table_info([{table}])")
                    columns = [col[1] for col in cursor.fetchall()]
                    
                    cursor.execute(f"SELECT COUNT(*) FROM [{table}]")
                    row_count = cursor.fetchone()[0]
                    
                    sample_data = []
                    if row_count > 0:
                        cursor.execute(f"SELECT * FROM [{table}] LIMIT 5")
                        sample_data = cursor.fetchall()
                    
                    cursor.execute(f"PRAGMA index_list([{table}])")
                    indexes = [idx[1] for idx in cursor.fetchall()]
                    
                    db_data['tables'][table] = {
                        'columns': columns,
                        'row_count': row_count,
                        'indexes': indexes,
                        'sample_data_count': len(sample_data),
                        'sample_data': sample_data if row_count <= 100 else []
                    }
                except Exception as e:
                    logger.error(f"Error processing table {table}: {e}")
                    db_data['tables'][table] = {'error': str(e)}
            return db_data
        finally:
            conn.close()

class TaskValidator:
    """Task-specific validation system"""
    
    VALIDATORS = {
        "shopping": "validate_shopping_task",
        "login": "validate_login_task",
        "form_submission": "validate_form_submission"
    }
    
    @staticmethod
    def validate_shopping_task(task_result: TaskResult) -> bool:
        """Validate shopping task success criteria"""
        for content in task_result.reasoning_files.values():
            content_lower = content.lower()
            if "order confirmed" in content_lower or "purchase successful" in content_lower:
                return True
            if "successfully added to cart" in content_lower and "payment processed" in content_lower:
                return True
        
        for html_data in task_result.html_files:
            content = html_data.get('content', '').lower()
            if "thank you for your order" in content:
                return True
            if "order-confirmation" in content:
                return True
        
        for db_path, db_data in task_result.db_data.items():
            if 'orders' in db_data.get('tables', {}):
                orders = db_data['tables']['orders']
                if orders.get('row_count', 0) > 0:
                    return True
            if 'cart' in db_data.get('tables', {}):
                cart = db_data['tables']['cart']
                if cart.get('row_count', 0) >= 2:
                    return True
        
        return False

    @staticmethod
    def validate_task(task_result: TaskResult) -> bool:
        """Main validation entry point"""
        validator_name = TaskValidator.VALIDATORS.get(task_result.task_type)
        if validator_name:
            validator = getattr(TaskValidator, validator_name, None)
            if validator:
                logger.info(f"Running {validator_name} validation for {task_result.task_id}")
                return validator(task_result)
        
        return any(
            "success" in content.lower() and "failed" not in content.lower()
            for content in task_result.reasoning_files.values()
        )

class TaskResultCollector:
    """Collects and processes task results with enhanced validation"""

    def __init__(self, parent_folder: str):
        self.parent_folder = Path(parent_folder)
        self.file_processor = FileProcessor()
        self.db_processor = DatabaseProcessor()

    def discover_task_folders(self) -> List[str]:
        """Discover all task folders in the parent directory"""
        if not self.parent_folder.exists():
            logger.error(f"Parent folder does not exist: {self.parent_folder}")
            return []
        return [str(item) for item in self.parent_folder.iterdir() if item.is_dir()]

    def analyze_folder_structure(self, task_folder: Path) -> Dict[str, Any]:
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
            
            if file_ext in FileProcessor.DB_EXTENSIONS:
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

class GroqRCAAnalyzer:
    """Performs RCA with hierarchical processing"""
    
    def __init__(self, api_key: str = "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",
                 model: str = "meta-llama/llama-4-maverick-17b-128e-instruct"):
        self.llm = ChatOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key,
            model=model,
            temperature=0.1,
            max_tokens=4096
        )
        self.model_name = model
        self.MAX_TOKENS_PER_REQUEST = 5000  # Strict limit to avoid 413 errors
        self.MIN_TOKENS_FOR_RESPONSE = 500
        self.MAX_CHUNK_SIZE = 3000  # Tokens per chunk

    def _get_cache_path(self, task_id: str, file_name: str) -> Path:
        """Get cache path for processed reasoning files"""
        cache_dir = Path("cache/reasoning") / task_id
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir / f"{hashlib.md5(file_name.encode()).hexdigest()}.json"

    def extract_critical_sections(self, content: str) -> List[str]:
        """Extract key sections to preserve verbatim"""
        critical = []
        
        # Preserve final outcome
        final_answer = re.search(r"Final Answer:.+", content, re.DOTALL)
        if final_answer:
            critical.append(final_answer.group(0)[:1000])  # Limit length
        
        # Preserve error messages
        errors = re.findall(r"Error:.+|Exception:.+|Failed:.+", content)
        critical.extend(errors[:3])  # Limit to 3 errors
        
        # Preserve tool responses with failure
        tool_failures = re.findall(r"Tool:.+\nResult:.+(error|fail|invalid|denied)", content, re.IGNORECASE)
        critical.extend(tool_failures[:2])  # Limit to 2 failures
        
        return critical

    def remove_boilerplate(self, content: str) -> str:
        """Remove unnecessary boilerplate from reasoning files"""
        # Remove system prompts and formatting instructions
        cleaned = re.sub(r"# Input Format.*?---", "", content, flags=re.DOTALL)
        cleaned = re.sub(r"RESPONSE FORMAT.*?---", "", cleaned, flags=re.DOTALL)
        cleaned = re.sub(r"SystemMessage.*?\)", "", cleaned, flags=re.DOTALL)
        cleaned = re.sub(r"HumanMessage.*?\)", "", cleaned, flags=re.DOTALL)
        cleaned = re.sub(r"AIMessage.*?\)", "", cleaned, flags=re.DOTALL)
        return cleaned.strip()

    async def summarize_to_token_limit(self, content: str, max_tokens: int) -> str:
        """Hierarchical summarization to fit token limits"""
        if estimate_tokens(content, self.model_name) <= max_tokens:
            return content
        
        # First-level summarization
        summary = await self._summarize_content(content)
        if estimate_tokens(summary, self.model_name) <= max_tokens:
            return summary
        
        # Second-level summarization (more aggressive)
        return await self._summarize_content(summary, aggressive=True)

    async def _summarize_content(self, content: str, aggressive: bool = False) -> str:
        """Summarize content with adjustable aggressiveness"""
        if len(content) < 500:
            return content
        
        prompt = f"""
Summarize the following technical content while preserving:
- Error messages
- Key decisions
- Action sequences
- Status changes

{'Provide only the most critical points in 2-3 bullet points' if aggressive else 'Provide 3-5 key bullet points'}

Content:
{content[:5000] if aggressive else content[:10000]}
"""
        messages = [
            SystemMessage(content="You are a technical summarizer focusing on key details"),
            HumanMessage(content=prompt)
        ]
        try:
            response = await self._analyze_with_retry(messages)
            return response.strip()
        except Exception as e:
            logger.error(f"Content summarization failed: {e}")
            # Fallback truncation
            return content[:1000] if aggressive else content[:2000]

    async def process_reasoning_file(self, task_id: str, file_name: str, content: str) -> str:
        """Process reasoning files with hierarchical summarization"""
        cache_path = self._get_cache_path(task_id, file_name)
        if cache_path.exists():
            return json.load(open(cache_path, 'r', encoding='utf-8'))
        
        logger.info(f"Processing reasoning file: {file_name}")
        
        # Step 1: Remove boilerplate content
        cleaned_content = self.remove_boilerplate(content)
        
        # Step 2: Extract critical sections
        critical_sections = self.extract_critical_sections(cleaned_content)
        
        # Step 3: Process remaining content
        remaining_content = cleaned_content
        for section in critical_sections:
            remaining_content = remaining_content.replace(section, "")
        
        # Step 4: Create combined content with token budget
        token_budget = 1500  # Tokens for this file in the final prompt
        critical_str = "\n".join(critical_sections)
        combined = f"CRITICAL SECTIONS:\n{critical_str}\n\nOTHER CONTENT:\n{remaining_content}"
        
        # Summarize to fit token budget
        processed = await self.summarize_to_token_limit(combined, token_budget)
        
        # Save to cache
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(processed, f)
        return processed

    def _truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to a specific token count"""
        try:
            encoding = tiktoken.encoding_for_model(self.model_name)
            tokens = encoding.encode(text)
            if len(tokens) <= max_tokens:
                return text
            return encoding.decode(tokens[:max_tokens])
        except:
            # Fallback: truncate by characters
            return text[:max_tokens * 4]

    async def generate_compact_prompt(self, task_result: TaskResult) -> Tuple[str, int]:
        """Generate RCA prompt with strict token budgeting"""
        # Get core task info with defaults
        primary_framework = "Unknown"
        element_counts = {}
        if task_result.html_files:
            for html_data in task_result.html_files:
                if html_data.get('primary_framework'):
                    primary_framework = html_data['primary_framework']
                if html_data.get('element_counts'):
                    element_counts = html_data['element_counts']
        
        # Build base prompt with token budget
        base_prompt = f"""
## TASK CONTEXT
- ID: {task_result.task_id}
- Status: {task_result.status} {'(Verified)' if task_result.verified_success else '(Unverified)'}
- Type: {task_result.task_type}

## UI FRAMEWORK ANALYSIS
- Primary Framework: {primary_framework}
- Element Distribution: {json.dumps(element_counts) or 'No elements detected'}

## REASONING ANALYSIS
"""
        token_count = estimate_tokens(base_prompt, self.model_name)
        reasoning_content = ""
        
        # Process reasoning files with strict token budget
        reason_budget = 2000  # Total tokens for all reasoning files
        for file_path, content in task_result.reasoning_files.items():
            if token_count >= self.MAX_TOKENS_PER_REQUEST - self.MIN_TOKENS_FOR_RESPONSE:
                break
                
            processed = await self.process_reasoning_file(task_result.task_id, file_path, content)
            file_content = f"\n\n### {file_path}\n{processed}"
            file_tokens = estimate_tokens(file_content, self.model_name)
            
            if token_count + file_tokens > self.MAX_TOKENS_PER_REQUEST - self.MIN_TOKENS_FOR_RESPONSE:
                # Summarize further to fit
                file_content = await self.summarize_to_token_limit(file_content, 500)
                file_tokens = estimate_tokens(file_content, self.model_name)
            
            if token_count + file_tokens <= self.MAX_TOKENS_PER_REQUEST - self.MIN_TOKENS_FOR_RESPONSE:
                reasoning_content += file_content
                token_count += file_tokens
        
        # Add database information
        db_content = "\n\n## DATABASE SUMMARY"
        if task_result.db_data:
            db_summary = []
            for db_path, db_info in task_result.db_data.items():
                db_summary.append(f"- {db_path}: {db_info.get('total_tables', 0)} tables")
                for table, details in db_info.get('tables', {}).items():
                    db_summary.append(f"  - {table}: {details.get('row_count', 0)} rows")
                    if len(db_summary) > 5:  # Limit database details
                        break
            db_content += "\n" + "\n".join(db_summary[:5])
        else:
            db_content += "\nNo databases found"
        
        db_tokens = estimate_tokens(db_content, self.model_name)
        if token_count + db_tokens > self.MAX_TOKENS_PER_REQUEST - self.MIN_TOKENS_FOR_RESPONSE:
            db_content = "\n\n## DATABASE SUMMARY\n[Summary truncated]"
            db_tokens = estimate_tokens(db_content, self.model_name)
        token_count += db_tokens
        
        # Add analysis directives
        directives = f"""
        
## ROOT CAUSE ANALYSIS DIRECTIVES
1. Focus on critical sections from reasoning analysis
2. Analyze failures in relation to UI framework
3. Use 5 Whys methodology
4. Provide specific technical recommendations
5. Include database issues if applicable

## RESPONSE FORMAT
{{
  "root_causes": ["..."],
  "five_whys": {{"Cause": ["Why1", "Why2", ...]}},
  "contributing_factors": ["..."],
  "recommendations": ["..."],
  "analysis_summary": "...",
  "framework": "{primary_framework}",
  "element_types": {json.dumps(element_counts)},
  "db_issues": ["..."]
}}
"""
        # Combine all parts
        full_prompt = base_prompt + reasoning_content + db_content + directives
        token_count = estimate_tokens(full_prompt, self.model_name)
        
        # Final truncation if needed
        if token_count > self.MAX_TOKENS_PER_REQUEST - self.MIN_TOKENS_FOR_RESPONSE:
            full_prompt = self._truncate_to_tokens(
                full_prompt, 
                self.MAX_TOKENS_PER_REQUEST - self.MIN_TOKENS_FOR_RESPONSE
            )
            token_count = estimate_tokens(full_prompt, self.model_name)
        
        return full_prompt, token_count

    async def hierarchical_rca_analysis(self, task_result: TaskResult) -> RCAResult:
        """Perform RCA in stages to handle large inputs"""
        # Stage 1: Analyze reasoning files
        reasoning_analysis = await self.analyze_reasoning_files(task_result)
        
        # Stage 2: Analyze UI framework
        framework_analysis = await self.analyze_ui_framework(task_result)
        
        # Stage 3: Analyze database
        db_analysis = await self.analyze_database(task_result)
        
        # Stage 4: Final RCA synthesis
        return await self.synthesize_rca(
            task_result, 
            reasoning_analysis, 
            framework_analysis, 
            db_analysis
        )

    async def analyze_reasoning_files(self, task_result: TaskResult) -> str:
        """Analyze reasoning files in a focused way"""
        analysis = []
        for file_path, content in task_result.reasoning_files.items():
            processed = await self.process_reasoning_file(task_result.task_id, file_path, content)
            analysis.append(f"### {file_path}\n{processed}")
        
        prompt = f"""
Analyze the following reasoning files to identify critical failures and decision points:

{"".join(analysis)}

Respond with a concise summary of:
- Key errors
- Critical decision points
- Final outcomes
"""
        messages = [
            SystemMessage(content="You are an analyst identifying critical issues in task execution logs"),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = await self._analyze_with_retry(messages)
            return response.strip()
        except Exception as e:
            logger.error(f"Reasoning analysis failed: {e}")
            return "Reasoning analysis incomplete"

    async def analyze_ui_framework(self, task_result: TaskResult) -> str:
        """Analyze UI framework and elements"""
        if not task_result.html_files:
            return "No UI analysis performed"
        
        primary_framework = "Unknown"
        element_counts = {}
        for html_data in task_result.html_files:
            if html_data.get('primary_framework'):
                primary_framework = html_data['primary_framework']
            if html_data.get('element_counts'):
                element_counts = html_data['element_counts']
        
        prompt = f"""
Analyze the UI framework and element distribution for potential issues:

- Primary Framework: {primary_framework}
- Element Distribution: {json.dumps(element_counts)}

Consider common failure patterns for this framework and element types.
"""
        messages = [
            SystemMessage(content="You are a UI expert analyzing potential failure points"),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = await self._analyze_with_retry(messages)
            return response.strip()
        except Exception as e:
            logger.error(f"UI analysis failed: {e}")
            return "UI analysis incomplete"

    async def analyze_database(self, task_result: TaskResult) -> str:
        """Analyze database state for issues"""
        if not task_result.db_data:
            return "No database analysis performed"
        
        db_summary = []
        for db_path, db_info in task_result.db_data.items():
            db_summary.append(f"- {db_path}: {db_info.get('total_tables', 0)} tables")
            for table, details in db_info.get('tables', {}).items():
                db_summary.append(f"  - {table}: {details.get('row_count', 0)} rows")
                if len(db_summary) > 10:  # Limit details
                    break
        
        prompt = f"""
Review the database state for potential issues:

{"".join(db_summary)}

Identify any anomalies or inconsistencies.
"""
        messages = [
            SystemMessage(content="You are a database analyst identifying potential data issues"),
            HumanMessage(content=prompt)
        ]
        
        try:
            response = await self._analyze_with_retry(messages)
            return response.strip()
        except Exception as e:
            logger.error(f"Database analysis failed: {e}")
            return "Database analysis incomplete"

    async def synthesize_rca(self, task_result: TaskResult, reasoning_analysis: str, 
                             framework_analysis: str, db_analysis: str) -> RCAResult:
        """Synthesize final RCA from component analyses"""
        # Get core task info with defaults
        primary_framework = "Unknown"
        element_counts = {}
        if task_result.html_files:
            for html_data in task_result.html_files:
                if html_data.get('primary_framework'):
                    primary_framework = html_data['primary_framework']
                if html_data.get('element_counts'):
                    element_counts = html_data['element_counts']
        
        prompt = f"""
## TASK CONTEXT
- ID: {task_result.task_id}
- Status: {task_result.status} {'(Verified)' if task_result.verified_success else '(Unverified)'}
- Type: {task_result.task_type}

## REASONING ANALYSIS SUMMARY
{reasoning_analysis}

## UI FRAMEWORK ANALYSIS SUMMARY
{framework_analysis}

## DATABASE ANALYSIS SUMMARY
{db_analysis}

## ROOT CAUSE ANALYSIS SYNTHESIS
Perform a comprehensive root cause analysis by integrating the above analyses.
Use the 5 Whys methodology to identify root causes and provide specific recommendations.

## RESPONSE FORMAT
{{
  "root_causes": ["..."],
  "five_whys": {{"Cause": ["Why1", "Why2", ...]}},
  "contributing_factors": ["..."],
  "recommendations": ["..."],
  "analysis_summary": "...",
  "framework": "{primary_framework}",
  "element_types": {json.dumps(element_counts)},
  "db_issues": ["..."]
}}
"""
        # Validate token count before sending
        token_count = estimate_tokens(prompt, self.model_name)
        if token_count > self.MAX_TOKENS_PER_REQUEST - self.MIN_TOKENS_FOR_RESPONSE:
            logger.warning(f"RCA synthesis prompt too large ({token_count} tokens), truncating")
            prompt = self._truncate_to_tokens(prompt, self.MAX_TOKENS_PER_REQUEST - self.MIN_TOKENS_FOR_RESPONSE)
        
        messages = [
            SystemMessage(content="You are an RCA synthesis expert"),
            HumanMessage(content=prompt)
        ]
        
        response_content = await self._analyze_with_retry(messages)
        return self._parse_response(task_result.task_id, response_content)

    async def analyze_task(self, task_result: TaskResult) -> RCAResult:
        """Perform RCA with strict token management"""
        try:
            # First try compact analysis
            prompt, token_count = await self.generate_compact_prompt(task_result)
            if token_count <= self.MAX_TOKENS_PER_REQUEST - self.MIN_TOKENS_FOR_RESPONSE:
                logger.info(f"Using compact prompt ({token_count} tokens) for {task_result.task_id}")
                return await self._analyze_single_prompt(prompt, task_result.task_id)
            else:
                # Fall back to hierarchical analysis
                logger.warning(f"Compact prompt too large ({token_count} tokens), using hierarchical RCA")
                return await self.hierarchical_rca_analysis(task_result)
        except Exception as e:
            logger.exception(f"RCA analysis failed: {e}")
            return self._error_result(task_result.task_id, str(e))

    async def _analyze_single_prompt(self, prompt: str, task_id: str) -> RCAResult:
        """Process normal-sized prompt with validation"""
        # Validate token count before sending
        token_count = estimate_tokens(prompt, self.model_name)
        if token_count > self.MAX_TOKENS_PER_REQUEST - self.MIN_TOKENS_FOR_RESPONSE:
            logger.warning(f"Prompt too large ({token_count} tokens), truncating")
            prompt = self._truncate_to_tokens(prompt, self.MAX_TOKENS_PER_REQUEST - self.MIN_TOKENS_FOR_RESPONSE)
        
        messages = [
            SystemMessage(content="You are an expert in root cause analysis for automated web agents."),
            HumanMessage(content=prompt)
        ]
        
        response_content = await self._analyze_with_retry(messages)
        return self._parse_response(task_id, response_content)

    async def _analyze_with_retry(self, messages: List, max_retries: int = 5) -> str:
        """Send request with exponential backoff and rate limit handling"""
        # First validate message size
        content = "".join([msg.content for msg in messages if isinstance(msg, HumanMessage)])
        token_count = estimate_tokens(content, self.model_name)
        if token_count > 6000:  # Groq's hard limit for this model
            logger.error(f"Request too large ({token_count} tokens), cannot proceed")
            raise ValueError(f"Request exceeds maximum size (6000 tokens)")
        
        for attempt in range(max_retries):
            try:
                return (await asyncio.to_thread(self.llm.invoke, messages)).content
            except Exception as e:
                if "413" in str(e):
                    # Request too large - we can't recover from this
                    logger.error("Request too large, aborting")
                    raise
                elif "429" in str(e):
                    wait_time = min(2 ** (attempt + 1) + 5, 60)  # Exponential backoff with min 5s
                    logger.warning(f"Rate limited (attempt {attempt+1}/{max_retries}), waiting {wait_time}s")
                    await asyncio.sleep(wait_time)
                else:
                    wait_time = min(2 ** (attempt + 1), 30)
                    logger.warning(f"API error (attempt {attempt+1}/{max_retries}): {e} - waiting {wait_time}s")
                    await asyncio.sleep(wait_time)
        raise RuntimeError(f"Failed after {max_retries} retries")

    def _parse_response(self, task_id: str, response_content: str) -> RCAResult:
        """Parse response with enhanced validation and multiple JSON extraction methods"""
        # Try to find JSON in various formats
        json_match = None
        patterns = [
            r'```json\s*({.*?})\s*```',  # JSON code block
            r'```\s*({.*?})\s*```',      # Generic code block
            r'({.*})'                     # Bare JSON
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response_content, re.DOTALL)
            if match:
                json_match = match.group(1)
                try:
                    data = json.loads(json_match)
                    break
                except json.JSONDecodeError:
                    continue
        
        # If no match found, try to parse the whole response
        if not json_match:
            try:
                data = json.loads(response_content)
            except json.JSONDecodeError:
                logger.error(f"Response parsing failed: No JSON found in response")
                logger.error(f"Response content (truncated): {response_content[:1000]}")
                return self._error_result(task_id, "No valid JSON found in response")
        
        # Set default values for required fields
        required_fields = ['root_causes', 'five_whys', 'recommendations', 'analysis_summary']
        defaults = {
            'root_causes': ["Root cause analysis incomplete: missing field"],
            'five_whys': {"Cause": ["Analysis incomplete"]},
            'recommendations': ["Review the model response for technical issues"],
            'analysis_summary': "Analysis summary missing due to model response format issues"
        }
        
        # Ensure required fields exist
        for field in required_fields:
            if field not in data:
                logger.warning(f"Response missing required field: {field}")
                data[field] = defaults[field]
        
        # Ensure framework has a default value
        framework = data.get('framework', 'Unknown')
        
        return RCAResult(
            task_id=task_id,
            analysis_timestamp=datetime.now(),
            root_causes=data.get('root_causes', []),
            five_whys=data.get('five_whys', {}),
            contributing_factors=data.get('contributing_factors', []),
            recommendations=data.get('recommendations', []),
            analysis_summary=data.get('analysis_summary', ''),
            framework=framework,
            element_types=data.get('element_types', {}),
            db_issues=data.get('db_issues', [])
        )
    
    def _error_result(self, task_id: str, error: str) -> RCAResult:
        """Create error result"""
        return RCAResult(
            task_id=task_id,
            analysis_timestamp=datetime.now(),
            root_causes=[f"Analysis error: {error}"],
            five_whys={"Cause": [f"Technical failure: {error}"]},
            contributing_factors=["Technical failure"],
            recommendations=["Check logs", "Verify configuration"],
            analysis_summary="RCA failed due to technical error",
            framework="Unknown"
        )

class RCAPipeline:
    """Orchestrates RCA process with data validation"""

    def __init__(self, parent_folder: str, output_dir: str = "rca_results"):
        self.parent_folder = parent_folder
        self.output_dir = Path(output_dir)
        self.collector = TaskResultCollector(parent_folder)
        self.analyzer = GroqRCAAnalyzer()
        self.results = []
        self.processed_tasks = []
        self.output_dir.mkdir(parents=True, exist_ok=True)
        Path("cache/reasoning").mkdir(parents=True, exist_ok=True)

    async def run_pipeline(self) -> List[RCAResult]:
        """Execute pipeline with validation checks"""
        logger.info(f"Starting RCA pipeline: {self.parent_folder}")
        task_folders = self.collector.discover_task_folders()
        
        for task_folder in task_folders:
            try:
                task_id = Path(task_folder).name
                logger.info(f"Processing task: {task_id}")
                
                task_result = self.collector.process_task_folder(task_folder)
                self._validate_data_passing(task_result)
                
                rca_result = await self.analyzer.analyze_task(task_result)
                self.results.append(rca_result)
                
                self.processed_tasks.append({
                    'task_id': task_id,
                    'status': task_result.status,
                    'verified': task_result.verified_success,
                    'folder_path': task_folder,
                    'file_count': task_result.folder_structure.get('total_files'),
                    'reasoning_files': len(task_result.reasoning_files),
                    'html_files': len(task_result.html_files),
                    'db_files': len(task_result.db_data)
                })
                
            except Exception as e:
                logger.exception(f"Failed processing task {task_folder}: {e}")
                # Create error result for failed tasks
                self.results.append(self.analyzer._error_result(
                    Path(task_folder).name, 
                    f"Processing error: {str(e)}"
                ))
                self.processed_tasks.append({
                    'task_id': Path(task_folder).name,
                    'status': "error",
                    'verified': False,
                    'folder_path': task_folder,
                    'file_count': 0,
                    'reasoning_files': 0,
                    'html_files': 0,
                    'db_files': 0
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
                # Only report as incomplete if there's an error or no content
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
                'framework_detected', 'elements_detected', 'validation_notes'
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
                    'validation_notes': validation_status
                })
        
        logger.info(f"Results saved to {self.output_dir}")

# Main execution
if __name__ == "__main__":
    pipeline = RCAPipeline(
        parent_folder="data/db/browseruse/dropdown_com",
        output_dir="rca_results"
    )
    asyncio.run(pipeline.run_pipeline())#;;;;;;;;;;;8888