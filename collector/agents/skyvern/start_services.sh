#!/bin/bash
echo "Starting services initialization..."

# Source environment variables
if [ -f /app/.env ]; then
    source /app/.env
    echo "Sourced environment variables"
else
    echo "WARNING: .env file not found!"
fi

# Start LiteLLM proxy in background
litellm --config /app/litellm_custom_groq_config.yaml > /var/log/litellm.log 2>&1 & LITELLM_PID=$!
echo "LiteLLM starting with PID: $LITELLM_PID"

# Wait longer with status checks
for i in {1..10}; do
    sleep 3
    if ! ps -p $LITELLM_PID > /dev/null; then
        echo "ERROR: LiteLLM failed to start!"
        echo "----- LiteLLM Log -----"
        cat /var/log/litellm.log
        exit 1
    fi
    
    echo "Initializing... ($i/10)"
    if grep -q "LiteLLm: Proxy started" /var/log/litellm.log; then
        break
    fi
done

# Verify LiteLLM connection
echo "LiteLLM health check:"
curl -s http://localhost:4000/health
echo ""

# Additional debug for Groq connection
if curl -s http://localhost:4000/health | grep -q '"healthy_count":0'; then
    echo "ERROR: No healthy endpoints!"
    echo "----- Groq Connection Debug -----"
    echo "GROQ_API_KEY: ${GROQ_API_KEY:0:4}******"
    echo "Config file:"
    cat /app/litellm_custom_groq_config.yaml
    echo "----- LiteLLM Log Tail -----"
    tail -n 50 /var/log/litellm.log
    exit 1
fi

echo "Services started successfully!"

# Set environment variables for Skyvern
#export OPENAI_API_KEY=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
#export OPENAI_API_BASE=http://localhost:4000
#export OPENAI_MODEL=groq-llama

# Start main application
#./run.sh