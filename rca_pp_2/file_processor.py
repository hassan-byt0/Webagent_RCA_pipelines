"""
File Processing Utilities
"""
import os
import re
import logging
from pathlib import Path
from bs4 import BeautifulSoup
from .config import DB_EXTENSIONS, HIDDEN_CLASSES, FRAMEWORK_PATTERNS, TEXT_EXTENSIONS

logger = logging.getLogger(__name__)

class FileProcessor:
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
    def parse_html_file(file_path: str) -> dict[str, any]:
        """Parse HTML files with enhanced framework detection and error recovery"""
        try:
            content = FileProcessor.read_text_file(file_path)
            if not content:
                return {
                    'file_path': str(file_path),
                    'error': 'Empty content',
                    'primary_framework': 'Unknown',
                    'full_content': ''
                }
            
            soup = BeautifulSoup(content, 'html.parser')
            result = {
                'file_path': str(file_path),
                'title': soup.title.string if soup.title else "No title",
                'content_length': len(content),
                'detected_frameworks': [],
                'ui_elements': [],
                'primary_framework': 'Unknown',
                'full_content': content  # Store full HTML content
            }
            
            # Detect frameworks and UI elements
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
                'primary_framework': 'Unknown',
                'full_content': ''
            }
    
    @staticmethod
    def _detect_framework_elements(soup, result):
        """Enhanced framework detection with multiple methods"""
        framework_counts = {}
        
        # Script-based detection
        for script in soup.find_all('script'):
            src = script.get('src', '').lower()
            content = script.string or ''
            for fw, pattern in FRAMEWORK_PATTERNS.items():
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
            for fw, pattern in FRAMEWORK_PATTERNS.items():
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
        if any(hc in classes for hc in HIDDEN_CLASSES):
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
    def read_script_file(file_path: str) -> dict[str, any]:
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
    def process_other_file(file_path: str) -> dict[str, any]:
        """Process other file types with validation"""
        try:
            file_ext = Path(file_path).suffix.lower()
            file_info = {
                'file_path': str(file_path),
                'file_name': os.path.basename(file_path),
                'extension': file_ext,
                'size': os.path.getsize(file_path) if os.path.exists(file_path) else 0
            }

            if file_ext in TEXT_EXTENSIONS:
                content = FileProcessor.read_text_file(file_path)
                file_info['content'] = content[:5000] if content else ''
            return file_info
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return {'file_path': str(file_path), 'error': str(e)}