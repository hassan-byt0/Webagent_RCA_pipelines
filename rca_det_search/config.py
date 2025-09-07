"""
Configuration and Constants for Deterministic ArXiv Search Analysis
"""
import re
import logging
from pathlib import Path
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('arxiv_det_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Root Cause Classifications based on Algorithm 2
class RootCauseType(Enum):
    DOM_PARSING_FAILURE = "DOM_PARSING_FAILURE"
    ELEMENT_INTERACTION_FAILURE = "ELEMENT_INTERACTION_FAILURE"
    DYNAMIC_CONTENT_FAILURE = "DYNAMIC_CONTENT_FAILURE"
    AGENT_REASONING_FAILURE = "AGENT_REASONING_FAILURE"
    WEBSITE_STATE_FAILURE = "WEBSITE_STATE_FAILURE"
    SUCCESS = "SUCCESS"

# Step definitions for the ArXiv search workflow
ARXIV_STEPS = {
    1: "Navigation and Page Load Verification",
    2: "Author Input Field Analysis",
    3: "Classification Label Processing",
    4: "Date Input Validation",
    5: "Search Execution and Results Verification"
}

# Author failure classification types
class AuthorFailureType(Enum):
    WRONG_AUTHOR_HALLUCINATION = "wrong_author_hallucination"
    DYNAMIC_RENDERING_ISSUE = "dynamic_rendering_issue"
    INTERACTION_FAILURE = "interaction_failure"

# Date failure classification types
class DateFailureType(Enum):
    HALLUCINATION = "hallucination"
    FORMAT_ERROR = "format_error"
    REASONING_ISSUE = "reasoning_issue"

# File processing constants
DB_EXTENSIONS = ['.db', '.sqlite', '.sqlite3', '.db3', '.sql', '.dat']
HIDDEN_CLASSES = ['hidden', 'invisible', 'offscreen', 'sr-only', 'd-none', 'is-hidden']
TEXT_EXTENSIONS = ['.log', '.txt', '.json', '.xml', '.yaml', '.yml', '.cfg', '.ini', '.conf']

# Framework detection patterns
FRAMEWORK_PATTERNS = {
    'angular': re.compile(r'angular|ng-'),
    'bootstrap': re.compile(r'bootstrap|bs-'),
    'svelte': re.compile(r'svelte'),
    'tailwind': re.compile(r'tailwind|tw-'),
    'vanilla': re.compile(r'vanilla|no-framework'),
    'react': re.compile(r'react'),
    'vue': re.compile(r'vue'),
    'jquery': re.compile(r'jquery|\$\(')
}

# Expected ArXiv search workflow elements
ARXIV_ELEMENTS = {
    'author_input': ['author', 'creator', 'name-field'],
    'author_dropdown': ['author-dropdown', 'autocomplete', 'suggestions'],
    'classification_labels': ['subject-class', 'classification', 'category'],
    'date_input': ['date', 'year', 'time', 'period'],
    'search_button': ['search', 'submit', 'find'],
    'captcha': ['captcha', 'recaptcha', 'challenge'],
    'results': ['result', 'paper', 'article', 'entry']
}

# Expected classification combinations
VALID_CLASSIFICATIONS = [
    'cs+math',
    'cs+stats', 
    'cs+math+stats',
    'computer science',
    'mathematics',
    'statistics'
]

# Date input options
VALID_DATE_OPTIONS = [
    'input_2025_specific_field',
    'selected_last_12_months',
    'input_proper_date_range',
    'selected_all_dates'
]

# Minimum expected search results
MINIMUM_SEARCH_RESULTS = 2
