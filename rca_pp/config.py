"""
Configuration and Constants
"""
import re
import logging
from pathlib import Path

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
    'antd': re.compile(r'ant-'),
    'material_ui': re.compile(r'Mui'),
    'bootstrap': re.compile(r'bs-|bootstrap|btn-'),
    'chakra': re.compile(r'chakra-'),
    'tailwind': re.compile(r'tw-|tailwind'),
}

# API Configuration - OPENAI VERSION
OPENAI_API_KEY = "sk-proj-XsGOYBghOsmhy2s1f36yT3BlbkFJcGUUUYTH3mzb2tUqO9vW"  # Replace with your OpenAI key
OPENAI_MODEL = "gpt-4-turbo"  # Or another OpenAI model

# Token limits - OPENAI VERSION
MAX_TOKENS_PER_REQUEST = 128000  # Increased for OpenAI's larger context
MIN_TOKENS_FOR_RESPONSE = 1000
MAX_CHUNK_SIZE = 30000

# GROQ VERSION (COMMENTED OUT)
# GROQ_API_KEY = "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"
# GROQ_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"
# MAX_TOKENS_PER_REQUEST = 5000
# MIN_TOKENS_FOR_RESPONSE = 500
# MAX_CHUNK_SIZE = 3000