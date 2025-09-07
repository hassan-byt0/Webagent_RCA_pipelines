# 🔍 Hybrid Root Cause Analysis (RCA) System

A sophisticated multi-provider AI-powered root cause analysis system that combines deterministic algorithms with artificial intelligence to diagnose web automation task failures.

## 🚀 Features

### 🤖 Multi-Provider AI Support
- **GPT-4o (OpenAI)**: High-quality analysis with consistent performance
- **Groq Llama**: Ultra-fast analysis with meta-llama/llama-4-maverick-17b-128e-instruct
- **Gemini**: Google's advanced AI with gemini-2.0-flash-exp model
- **Automatic Fallback**: Seamless switching between providers on failure

### 🧠 Hybrid Analysis Engine
- **Deterministic Analyzers**: Fast, rule-based analysis for known patterns
  - Dropdown interaction failure detection
  - ArXiv search failure analysis
- **AI-Powered Analysis**: Deep contextual analysis using large language models
- **Adaptive Learning**: System learns from past analyses to improve accuracy
- **Confidence-Based Routing**: Automatically chooses best analysis method

### 📊 Advanced Learning & Adaptation
- **Pattern Recognition**: Identifies recurring failure patterns
- **Rule Enhancement**: Automatically improves deterministic algorithms
- **Learning Database**: SQLite-based storage for historical analysis data
- **Feedback Loop**: Continuous improvement based on analysis results

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Required API keys (see Configuration section)

### Install Dependencies
```bash
cd rca_hybrid
pip install -r requirements.txt
```

### Required Packages
```bash
pip install langchain-openai langchain-google-genai langchain-core sqlite3 pandas numpy
```

## ⚙️ Configuration

### Environment Variables
Create a `.env` file or set the following environment variables:

```bash
# OpenAI Configuration
OPENAI_API_KEY="your_openai_api_key_here"

# Groq Configuration  
GROQ_API_KEY="your_groq_api_key_here"

# Google Gemini Configuration
GEMINI_API_KEY="your_gemini_api_key_here"
```

### AI Provider Configuration
The system supports three AI providers configured in `config.py`:

```python
AI_MODEL_CONFIGS = {
    'gpt': {
        'provider': 'openai',
        'model': 'gpt-4o',
        'api_key_env': 'OPENAI_API_KEY',
        'base_url': 'https://api.openai.com/v1'
    },
    'groq': {
        'provider': 'groq',
        'model': 'meta-llama/llama-4-maverick-17b-128e-instruct',
        'api_key_env': 'GROQ_API_KEY',
        'base_url': 'https://api.groq.com/openai/v1'
    },
    'gemini': {
        'provider': 'google',
        'model': 'gemini-2.0-flash-exp',
        'api_key_env': 'GEMINI_API_KEY'
    }
}
```

## 🚀 Usage

### Command Line Interface

#### Basic Usage
```bash
# Use default GPT provider
python cli.py task_001

# Specify AI provider
python cli.py task_001 --ai-provider groq
python cli.py task_001 --ai-provider gemini
python cli.py task_001 --ai-provider gpt

# Set confidence threshold
python cli.py task_001 --threshold 0.8

# Enable verbose output
python cli.py task_001 --verbose
```

#### Advanced Options
```bash
# Batch analysis with specific provider
python cli.py task_batch --ai-provider groq --threshold 0.75 --verbose

# Analysis with learning mode
python cli.py task_001 --learning-mode active --ai-provider gpt
```

### Programmatic Usage

#### Basic Analysis
```python
from hybrid_analyzer import HybridRootCauseAnalyzer
from models import TaskFailureInfo, StepInfo

# Initialize with specific AI provider
analyzer = HybridRootCauseAnalyzer(ai_provider='groq')

# Create task failure info
task_info = TaskFailureInfo(
    task_id="task_001",
    steps=[
        StepInfo(action="click", target="#submit-btn", result="failed"),
        StepInfo(action="type", target="#email", result="success")
    ],
    final_status="failed",
    error_messages=["Element not found: #submit-btn"]
)

# Run analysis
result = analyzer.analyze(task_info)
print(f"Root cause: {result.root_cause}")
print(f"Confidence: {result.confidence}")
print(f"Method: {result.analysis_method}")
```

#### Provider Comparison
```python
# Test all providers
providers = ['gpt', 'groq', 'gemini']
results = {}

for provider in providers:
    analyzer = HybridRootCauseAnalyzer(ai_provider=provider)
    result = analyzer.analyze(task_info)
    results[provider] = {
        'root_cause': result.root_cause,
        'confidence': result.confidence,
        'analysis_time': result.analysis_time_ms
    }

# Compare results
for provider, result in results.items():
    print(f"{provider}: {result['confidence']:.2f} confidence in {result['analysis_time']:.0f}ms")
```

## 🧪 Testing

### Test All Providers
```bash
python test_ai_providers.py
```

This will test all three AI providers and display:
- Configuration status
- API key validation
- Performance metrics
- Analysis results comparison

### Unit Tests
```bash
# Run deterministic analyzer tests
python -m pytest test_deterministic.py

# Run AI analyzer tests  
python -m pytest test_ai_analyzer.py

# Run integration tests
python -m pytest test_integration.py
```

## 📊 Performance Comparison

Based on our testing:

| Provider | Model | Avg Response Time | Reliability | Best Use Case |
|----------|-------|-------------------|-------------|---------------|
| **Groq** | meta-llama/llama-4-maverick-17b-128e-instruct | ~4.3s | ⭐⭐⭐⭐⭐ | Speed-critical applications |
| **GPT-4o** | gpt-4o | ~19.1s | ⭐⭐⭐⭐⭐ | High-quality analysis |
| **Gemini** | gemini-2.0-flash-exp | ~60s | ⭐⭐⭐⭐ | Complex reasoning tasks |

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Hybrid RCA System                      │
├─────────────────────────────────────────────────────────────┤
│  CLI Interface (cli.py)                                    │
├─────────────────────────────────────────────────────────────┤
│  Hybrid Analyzer (hybrid_analyzer.py)                     │
│  ├── Confidence-based routing                             │
│  ├── Multi-provider AI support                            │
│  └── Learning & adaptation                                │
├─────────────────────────────────────────────────────────────┤
│  Deterministic Analyzers           │  AI Analyzer          │
│  ├── Dropdown Analyzer             │  ├── GPT-4o          │
│  └── ArXiv Search Analyzer         │  ├── Groq Llama      │
│                                    │  └── Gemini          │
├─────────────────────────────────────────────────────────────┤
│  Learning System (learning_system.py)                     │
│  ├── Pattern recognition                                  │
│  ├── Rule enhancement                                     │
│  └── SQLite database                                      │
└─────────────────────────────────────────────────────────────┘
```

### Analysis Flow

1. **Input Processing**: Parse task failure information
2. **Deterministic Analysis**: Apply rule-based analyzers
3. **Confidence Evaluation**: Check if deterministic confidence meets threshold
4. **AI Analysis**: If needed, route to selected AI provider
5. **Result Synthesis**: Combine insights from multiple sources
6. **Learning Update**: Store results for future improvement

## 📋 Supported Failure Types

### Deterministic Detection
- **DOM Parsing Failures**: Element not found, invalid selectors
- **Interaction Failures**: Click failures, typing errors
- **Dynamic Content Issues**: Loading timeouts, async problems
- **Navigation Problems**: Page load failures, redirects
- **Form Submission Issues**: Validation errors, network problems

### AI-Enhanced Detection
- **Complex Context Analysis**: Multi-step failure analysis
- **Semantic Understanding**: Natural language error interpretation
- **Pattern Recognition**: Unusual failure combinations
- **Root Cause Inference**: Deep causal analysis

## 🔧 Configuration Options

### Confidence Thresholds
```python
class ConfidenceThreshold(Enum):
    LOW = 0.6       # Use AI if deterministic confidence below 60%
    MEDIUM = 0.75   # Use AI if deterministic confidence below 75% (default)
    HIGH = 0.9      # Use AI if deterministic confidence below 90%
```

### Learning Modes
```python
class LearningMode(Enum):
    PASSIVE = "passive"          # Only learn, don't update rules
    ACTIVE = "active"            # Learn and update rules (default)
    AGGRESSIVE = "aggressive"    # Proactively update based on patterns
```

### Provider Selection
- **Default**: GPT-4o (balanced quality/speed)
- **Speed**: Groq Llama (fastest response)
- **Quality**: GPT-4o (most accurate)
- **Experimental**: Gemini (latest features)

## 📝 API Reference

### HybridRootCauseAnalyzer

#### Constructor
```python
HybridRootCauseAnalyzer(
    confidence_threshold: float = 0.75,
    learning_mode: LearningMode = LearningMode.ACTIVE,
    ai_provider: str = None  # 'gpt', 'groq', 'gemini'
)
```

#### Methods
```python
analyze(task_info: TaskFailureInfo) -> AnalysisResult
get_learning_stats() -> Dict
update_confidence_threshold(threshold: float) -> None
```

### TaskFailureInfo
```python
@dataclass
class TaskFailureInfo:
    task_id: str
    steps: List[StepInfo]
    final_status: str
    error_messages: List[str] = field(default_factory=list)
    execution_time_ms: Optional[int] = None
    metadata: Dict = field(default_factory=dict)
```

### AnalysisResult
```python
@dataclass
class AnalysisResult:
    root_cause: str
    confidence: float
    analysis_method: str
    details: Dict
    learning_applied: bool
    analysis_time_ms: int
```

## 🔍 Troubleshooting

### Common Issues

#### API Key Problems
```bash
# Check if API keys are set
python -c "import os; print('OPENAI_API_KEY:', bool(os.getenv('OPENAI_API_KEY')))"
python -c "import os; print('GROQ_API_KEY:', bool(os.getenv('GROQ_API_KEY')))"
python -c "import os; print('GEMINI_API_KEY:', bool(os.getenv('GEMINI_API_KEY')))"
```

#### Provider Connection Issues
```bash
# Test specific provider
python test_ai_providers.py --provider groq
```

#### Database Issues
```bash
# Reset learning database
rm rca_hybrid/learning_database.sqlite
python cli.py --reset-learning
```

### Debug Mode
```bash
# Enable debug logging
export LOGGER_LEVEL=DEBUG
python cli.py task_001 --verbose
```

## 🎯 Performance Tuning

### Speed Optimization
- Use Groq provider for fastest analysis
- Set lower confidence threshold to use deterministic analysis more
- Reduce AI timeout settings in config.py

### Quality Optimization
- Use GPT-4o provider for highest quality
- Set higher confidence threshold to use AI analysis more
- Enable aggressive learning mode

### Cost Optimization
- Use deterministic analysis when possible
- Set appropriate confidence thresholds
- Monitor API usage in logs

## 🔄 Continuous Learning

The system automatically learns from each analysis:

1. **Pattern Storage**: Successful analyses are stored as learning cases
2. **Rule Enhancement**: Deterministic algorithms are improved based on AI insights
3. **Confidence Calibration**: Confidence scoring improves over time
4. **Provider Optimization**: System learns which provider works best for different scenarios

## 🤝 Contributing

### Development Setup
```bash
git clone <repository>
cd rca_hybrid
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
black rca_hybrid/
flake8 rca_hybrid/
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section above
2. Run the test suite to verify setup
3. Check logs in `hybrid_rca_analysis.log`
4. Create an issue with debug output

## 🎉 Quick Start Example

```bash
# 1. Set up environment
export OPENAI_API_KEY="your_key_here"
export GROQ_API_KEY="your_key_here"
export GEMINI_API_KEY="your_key_here"

# 2. Test the system
python test_ai_providers.py

# 3. Run analysis
python cli.py my_task_001 --ai-provider groq --verbose

# 4. Check results
cat hybrid_rca_analysis.log
```

## 🔮 Roadmap

- [ ] Additional AI providers (Claude, PaLM)
- [ ] Real-time streaming analysis
- [ ] Web dashboard interface
- [ ] Advanced pattern recognition
- [ ] Multi-language support
- [ ] Integration with monitoring systems