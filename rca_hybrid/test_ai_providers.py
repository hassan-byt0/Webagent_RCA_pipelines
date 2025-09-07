#!/usr/bin/env python3
"""
Test script for all three AI model configurations
"""
import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rca_hybrid.hybrid_analyzer import HybridRootCauseAnalyzer
from rca_hybrid.models import HybridAnalysisRequest
from rca_hybrid.config import HybridAnalysisType, LearningMode, AI_MODEL_CONFIGS

async def test_ai_provider(provider_name: str):
    """Test a specific AI provider"""
    print(f"\n{'='*60}")
    print(f"TESTING {provider_name.upper()} PROVIDER")
    print(f"{'='*60}")
    
    # Check if API key is available
    config = AI_MODEL_CONFIGS[provider_name]
    api_key_env = config['api_key_env']
    api_key = os.getenv(api_key_env)
    
    if not api_key:
        print(f"❌ API key not found: {api_key_env}")
        print(f"Please set: export {api_key_env}='your-api-key'")
        return False
    
    print(f"✅ API key found: {api_key_env}")
    print(f"📋 Model: {config['model']}")
    print(f"🔗 Provider: {config['provider']}")
    
    try:
        # Initialize analyzer with specific provider
        analyzer = HybridRootCauseAnalyzer(
            confidence_threshold=0.75,
            learning_mode=LearningMode.ACTIVE,
            ai_provider=provider_name
        )
        
        # Create test task result
        class TestTaskResult:
            def __init__(self):
                self.reasoning_files = {
                    "agent_log.txt": "Failed to click dropdown option",
                    "selenium_log.txt": "ElementNotInteractableException: Element not clickable"
                }
                self.db_data = {
                    "actions": [
                        {"type": "click", "element": "#dropdown", "success": True},
                        {"type": "click", "element": "#option-1", "success": False}
                    ],
                    "errors": ["Element not found: #option-1"]
                }
        
        # Create test request
        request = HybridAnalysisRequest(
            task_id=f"test_{provider_name}_001",
            analysis_type=HybridAnalysisType.AUTO_DETECT,
            task_result=TestTaskResult(),
            failure_log=f"""
ERROR: Failed to select dropdown option (Test with {provider_name})
- Dropdown opened successfully  
- Target option #option-1 not found
- Operation timed out after 30 seconds
- Testing {provider_name.upper()} AI provider
""",
            dom_snapshot="""
<select id="dropdown">
    <option value="">Select option</option>
    <option value="1">Option 1</option>
</select>
""",
            action_sequence=[
                {"action": "click", "element": "#dropdown", "success": True},
                {"action": "click", "element": "#option-1", "success": False}
            ],
            framework="selenium"
        )
        
        print(f"🔄 Running analysis with {provider_name}...")
        result = await analyzer.analyze(request)
        
        print(f"✅ Analysis completed successfully!")
        print(f"📊 Results:")
        print(f"  - Root cause: {result.final_root_cause}")
        print(f"  - Method used: {result.primary_method}")
        print(f"  - Confidence: {result.final_confidence:.2f}")
        print(f"  - AI used: {result.ai_used}")
        print(f"  - Analysis time: {result.total_analysis_time_ms:.1f}ms")
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        return False

async def test_all_providers():
    """Test all AI providers"""
    print("🚀 HYBRID RCA AI PROVIDER TEST")
    print("Testing GPT-4o, Groq Llama, and Gemini providers")
    
    # Test each provider
    providers = ['gpt', 'groq', 'gemini']
    results = {}
    
    for provider in providers:
        try:
            success = await test_ai_provider(provider)
            results[provider] = success
        except Exception as e:
            print(f"❌ Provider {provider} failed: {e}")
            results[provider] = False
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    for provider, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        config = AI_MODEL_CONFIGS[provider]
        print(f"{provider.upper():<10} | {config['model']:<35} | {status}")
    
    # Overall result
    passed = sum(results.values())
    total = len(results)
    print(f"\n🎯 Overall: {passed}/{total} providers working")
    
    if passed == 0:
        print("\n⚠️  No AI providers are working. Please check your API keys:")
        for provider in providers:
            config = AI_MODEL_CONFIGS[provider]
            api_key_env = config['api_key_env']
            print(f"  export {api_key_env}='your-api-key'")
    elif passed < total:
        print(f"\n⚠️  Some providers failed. The system will use working providers as fallback.")
    else:
        print(f"\n🎉 All providers working! You can use any of: {', '.join(providers)}")

def show_provider_details():
    """Show details about each AI provider configuration"""
    print(f"\n{'='*60}")
    print("🔧 AI PROVIDER CONFIGURATIONS")
    print(f"{'='*60}")
    
    for provider_name, config in AI_MODEL_CONFIGS.items():
        print(f"\n{provider_name.upper()}:")
        print(f"  Provider: {config['provider']}")
        print(f"  Model: {config['model']}")
        print(f"  API Key Env: {config['api_key_env']}")
        print(f"  Base URL: {config.get('base_url', 'Default')}")
        print(f"  Temperature: {config['temperature']}")
        print(f"  Max Tokens: {config['max_tokens']}")
        
        # Check if API key is set
        api_key = os.getenv(config['api_key_env'])
        if api_key:
            print(f"  Status: ✅ API key found")
        else:
            print(f"  Status: ❌ API key missing")

async def main():
    """Main test function"""
    show_provider_details()
    await test_all_providers()
    
    print(f"\n{'='*60}")
    print("🔗 USAGE EXAMPLES")
    print(f"{'='*60}")
    
    print("\n# Programmatic usage:")
    print("analyzer = HybridRootCauseAnalyzer(ai_provider='gpt')")
    print("analyzer = HybridRootCauseAnalyzer(ai_provider='groq')")
    print("analyzer = HybridRootCauseAnalyzer(ai_provider='gemini')")
    
    print("\n# CLI usage:")
    print("python3 rca_hybrid/cli.py my_task --ai-provider gpt")
    print("python3 rca_hybrid/cli.py my_task --ai-provider groq")
    print("python3 rca_hybrid/cli.py my_task --ai-provider gemini")
    
    print("\n💡 Tip: The system will automatically fallback to other providers if one fails!")

if __name__ == "__main__":
    asyncio.run(main())
