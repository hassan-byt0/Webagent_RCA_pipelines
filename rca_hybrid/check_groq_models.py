#!/usr/bin/env python3
"""
Check available Groq models
"""
import os
import sys
import requests
import json

def load_env_file(file_path):
    """Simple .env file parser"""
    env_vars = {}
    if not os.path.exists(file_path):
        return env_vars
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                # Remove quotes if present
                value = value.strip('"').strip("'")
                env_vars[key] = value
    return env_vars

def get_groq_models():
    """Get list of available Groq models"""
    
    # Load environment variables
    env_path = "/Users/hassanshaikh/Downloads/webagents/agent-collector/collector/.env"
    env_vars = load_env_file(env_path)
    api_key = env_vars.get('GROQ_API_KEY')
    
    if not api_key:
        print("❌ No GROQ_API_KEY found")
        return []
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        print("🔄 Fetching available Groq models...")
        response = requests.get(
            'https://api.groq.com/openai/v1/models',
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('data', [])
            print(f"✅ Found {len(models)} available models:")
            
            # Group by model family
            llama_models = []
            gemma_models = []
            other_models = []
            
            for model in models:
                model_id = model.get('id', '')
                print(f"   📋 {model_id}")
                
                if 'llama' in model_id.lower():
                    llama_models.append(model_id)
                elif 'gemma' in model_id.lower():
                    gemma_models.append(model_id)
                else:
                    other_models.append(model_id)
            
            print("\n🦙 Llama Models:")
            for model in llama_models:
                print(f"   - {model}")
            
            print("\n💎 Gemma Models:")
            for model in gemma_models:
                print(f"   - {model}")
                
            print("\n🔧 Other Models:")
            for model in other_models:
                print(f"   - {model}")
            
            return models
        else:
            print(f"❌ Failed to fetch models: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return []
            
    except Exception as e:
        print(f"💥 Error fetching models: {e}")
        return []

def test_model(model_id, api_key):
    """Test a specific model"""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'messages': [
            {
                'role': 'user',
                'content': 'Hello, respond with just "test successful"'
            }
        ],
        'model': model_id,
        'max_tokens': 10,
        'temperature': 0.1
    }
    
    try:
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return True, "✅ Working"
        else:
            return False, f"❌ Error {response.status_code}"
            
    except Exception as e:
        return False, f"💥 {str(e)[:50]}..."

def main():
    print("🔍 GROQ MODELS CHECKER")
    print("=" * 50)
    
    # Get available models
    models = get_groq_models()
    
    if not models:
        print("❌ No models found or API error")
        return False
    
    # Load API key for testing
    env_path = "/Users/hassanshaikh/Downloads/webagents/agent-collector/collector/.env"
    env_vars = load_env_file(env_path)
    api_key = env_vars.get('GROQ_API_KEY')
    
    # Test the most promising llama models
    test_models = [
        'llama-3.1-70b-versatile',
        'llama-3.1-8b-instant', 
        'llama3-70b-8192',
        'llama3-8b-8192'
    ]
    
    print("\n🧪 TESTING MODELS")
    print("=" * 50)
    
    working_models = []
    for model_id in test_models:
        if any(model.get('id') == model_id for model in models):
            print(f"🔄 Testing {model_id}...")
            success, result = test_model(model_id, api_key)
            print(f"   {result}")
            if success:
                working_models.append(model_id)
        else:
            print(f"⏭️  Skipping {model_id} (not available)")
    
    print("\n📋 RECOMMENDATIONS")
    print("=" * 50)
    
    if working_models:
        print("✅ Working models found:")
        for model in working_models:
            print(f"   - {model}")
        
        best_model = working_models[0]
        print(f"\n💡 Recommended model: {best_model}")
        print(f"📝 Update config.py with:")
        print(f"   'model': '{best_model}'")
    else:
        print("❌ No working models found")
        print("🔧 Try checking your API key or account access")
    
    return len(working_models) > 0

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
