#!/usr/bin/env python3
"""
Test script to verify Groq API key validity
"""
import os
import sys
import requests

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

def test_groq_api_key():
    """Test if the Groq API key from .env is valid"""
    
    # Load environment variables from the collector/.env file
    env_path = "/Users/hassanshaikh/Downloads/webagents/agent-collector/collector/.env"
    print(f"📁 Loading environment from: {env_path}")
    
    if not os.path.exists(env_path):
        print(f"❌ Environment file not found: {env_path}")
        return False
    
    env_vars = load_env_file(env_path)
    api_key = env_vars.get('GROQ_API_KEY')
    
    if not api_key:
        print("❌ No GROQ_API_KEY found in environment")
        print("🔍 Found environment variables:")
        for key in env_vars:
            if 'GROQ' in key.upper():
                print(f"   {key}: {env_vars[key][:20]}...")
        return False
    
    print(f"🔑 Testing API Key: {api_key[:20]}...")
    
    # Test the API key with a simple request
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Simple test payload
    payload = {
        'messages': [
            {
                'role': 'user',
                'content': 'Hello, respond with just "test successful"'
            }
        ],
        'model': 'meta-llama/llama-3.1-70b-versatile',
        'max_tokens': 10,
        'temperature': 0.1
    }
    
    try:
        print("🔄 Making test request to Groq API...")
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API key is valid!")
            data = response.json()
            content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"📝 Response: {content}")
            return True
        elif response.status_code == 401:
            print("❌ API key is invalid or expired")
            print(f"📄 Error details: {response.text}")
            return False
        else:
            print(f"⚠️  Unexpected response: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out")
        return False
    except requests.exceptions.RequestException as e:
        print(f"🚨 Request error: {e}")
        return False
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return False

def main():
    print("🧪 GROQ API KEY VALIDATION TEST")
    print("=" * 50)
    
    success = test_groq_api_key()
    
    print("=" * 50)
    if success:
        print("🎉 Groq API key is working correctly!")
        print("💡 The issue might be in the RCA system configuration.")
    else:
        print("🔧 Groq API key needs to be updated.")
        print("📋 Steps to fix:")
        print("   1. Get a new API key from https://console.groq.com/")
        print("   2. Update GROQ_API_KEY in collector/.env")
        print("   3. Re-run the test")
    
    return success

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
