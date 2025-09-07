"""
Configuration and Constants for Hybrid Root Cause Analysis
"""
import logging
from enum import Enum
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('hybrid_rca_analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Hybrid analysis types
class HybridAnalysisType(Enum):
    DROPDOWN = "dropdown"
    ARXIV_SEARCH = "arxiv_search"
    AUTO_DETECT = "auto_detect"

# Learning modes for adaptive enhancement
class LearningMode(Enum):
    PASSIVE = "passive"          # Only learn, don't update deterministic rules
    ACTIVE = "active"            # Learn and update deterministic rules
    AGGRESSIVE = "aggressive"    # Proactively update rules based on patterns

# Confidence thresholds for decision making
class ConfidenceThreshold(Enum):
    LOW = 0.6       # Use AI if deterministic confidence below 60%
    MEDIUM = 0.75   # Use AI if deterministic confidence below 75%
    HIGH = 0.9      # Use AI if deterministic confidence below 90%

# AI Model Configurations - Multiple Provider Support
AI_MODEL_CONFIGS = {
    'gpt': {
        'provider': 'openai',
        'model': 'gpt-4o',
        'api_key_env': 'OPENAI_API_KEY',
        'base_url': 'https://api.openai.com/v1',
        'temperature': 0.1,
        'max_tokens': 2048,
        'timeout': 30
    },
    'groq': {
        'provider': 'groq',
        'model': 'meta-llama/llama-4-maverick-17b-128e-instruct',
        'api_key_env': 'GROQ_API_KEY',
        'base_url': 'https://api.groq.com/openai/v1',
        'temperature': 0.1,
        'max_tokens': 2048,
        'timeout': 30
    },
    'gemini': {
        'provider': 'google',
        'model': 'gemini-2.0-flash-exp',  # Using available model
        'api_key_env': 'GEMINI_API_KEY',
        'temperature': 0.1,
        'max_tokens': 2048,
        'timeout': 30
    }
}

# Default AI Model Configuration (can be overridden)
DEFAULT_AI_PROVIDER = 'gpt'  # Options: 'gpt', 'groq', 'gemini'
AI_MODEL_CONFIG = AI_MODEL_CONFIGS[DEFAULT_AI_PROVIDER]

# Fallback strategies
FALLBACK_STRATEGIES = {
    'deterministic_failure': 'use_ai',
    'ai_failure': 'use_heuristic',
    'both_failure': 'return_unknown'
}

# Learning database configuration
LEARNING_DB_CONFIG = {
    'db_path': Path('rca_hybrid/learning_database.sqlite'),
    'backup_frequency': 100,  # Backup every 100 new cases
    'max_cases_per_type': 10000  # Maximum cases to store per failure type
}

# Pattern recognition thresholds
PATTERN_RECOGNITION = {
    'min_occurrences': 5,      # Minimum times a pattern must occur
    'confidence_boost': 0.1,   # How much to boost confidence for known patterns
    'similarity_threshold': 0.8 # Threshold for considering patterns similar
}

# Deterministic algorithm enhancement settings
ENHANCEMENT_SETTINGS = {
    'auto_update_rules': True,
    'validation_required': True,  # Require validation before updating rules
    'backup_before_update': True,
    'rollback_on_failure': True
}

# Root cause mapping between systems
ROOT_CAUSE_MAPPING = {
    # Dropdown analyzer root causes
    'DOM_PARSING_FAILURE': 'DOM_PARSING_FAILURE',
    'ELEMENT_INTERACTION_FAILURE': 'ELEMENT_INTERACTION_FAILURE', 
    'DYNAMIC_CONTENT_FAILURE': 'DYNAMIC_CONTENT_FAILURE',
    'AGENT_REASONING_FAILURE': 'AGENT_REASONING_FAILURE',
    'SUCCESS': 'SUCCESS',
    
    # ArXiv analyzer root causes
    'WEBSITE_STATE_FAILURE': 'WEBSITE_STATE_FAILURE',
    
    # AI-discovered root causes (will be added dynamically)
    'UNKNOWN': 'UNKNOWN'
}

# Analysis pipeline timeouts (in seconds)
TIMEOUTS = {
    'deterministic_analysis': 5,
    'ai_analysis': 30,
    'learning_update': 10,
    'total_pipeline': 60
}

# File paths
PATHS = {
    'learning_db': 'rca_hybrid/learning_database.sqlite',
    'rule_updates': 'rca_hybrid/rule_updates/',
    'backups': 'rca_hybrid/backups/',
    'logs': 'rca_hybrid/logs/'
}

# Create directories if they don't exist
for path_key, path_value in PATHS.items():
    Path(path_value).parent.mkdir(parents=True, exist_ok=True)
