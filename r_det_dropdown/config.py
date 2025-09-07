"""
Configuration and Constants for Deterministic Dropdown Analysis
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
        logging.FileHandler('dropdown_det_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Root Cause Classifications based on the deterministic algorithm
class RootCauseType(Enum):
    DOM_PARSING_FAILURE = "DOM_PARSING_FAILURE"
    ELEMENT_INTERACTION_FAILURE = "ELEMENT_INTERACTION_FAILURE"
    DYNAMIC_CONTENT_FAILURE = "DYNAMIC_CONTENT_FAILURE"
    AGENT_REASONING_FAILURE = "AGENT_REASONING_FAILURE"
    WEBSITE_STATE_FAILURE = "WEBSITE_STATE_FAILURE"
    SUCCESS = "SUCCESS"

# Step definitions for the cascade dropdown workflow
DROPDOWN_STEPS = {
    1: "Initial Element Detection",
    2: "Primary Category Navigation", 
    3: "Subcategory Selection Validation",
    4: "Filter Application Verification",
    5: "Product Analysis and Selection",
    6: "Transaction Completion"
}

# Minimum load time threshold (milliseconds)
MINIMUM_LOAD_TIME = 500

# File processing constants
DB_EXTENSIONS = ['.db', '.sqlite', '.sqlite3', '.db3', '.sql', '.dat']
HIDDEN_CLASSES = ['hidden', 'invisible', 'offscreen', 'sr-only', 'd-none', 'is-hidden']
TEXT_EXTENSIONS = ['.log', '.txt', '.json', '.xml', '.yaml', '.yml', '.cfg', '.ini', '.conf']

# Framework detection patterns
FRAMEWORK_PATTERNS = {
    'react': re.compile(r'react|react-dom'),
    'vue': re.compile(r'vue'),
    'angular': re.compile(r'angular'),
    'jquery': re.compile(r'jquery'),
    'bootstrap': re.compile(r'bootstrap'),
    'tailwind': re.compile(r'tailwind'),
    'vanilla': re.compile(r'vanilla|no-framework'),
}

# Expected dropdown workflow elements
DROPDOWN_ELEMENTS = {
    'dropdown_trigger': ['dropdown', 'select', 'menu', 'nav'],
    'men_option': ['men', 'male', 'mens'],
    'shoes_subcategory': ['shoes', 'footwear'],
    'clothing_subcategory': ['clothing', 'apparel'],
    'nike_filter': ['nike', 'brand-nike'],
    'price_elements': ['price', 'cost', 'amount', '$'],
    'cart_elements': ['cart', 'add-to-cart', 'shopping-cart'],
    'checkout_elements': ['checkout', 'purchase', 'buy-now']
}
