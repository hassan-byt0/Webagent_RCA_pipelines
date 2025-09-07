#!/bin/bash
echo "Starting services initialization..."
# Start LiteLLM proxy in background
litellm --config /app/litellm_custom_groq_config.yaml > /var/log/litellm.log 2>&1 & LITELLM_PID=$!
sleep 5  # Wait for LiteLLM to start
echo "Waiting for LiteLLM to initialize..."
# Start Xvfb in background
#Xvfb :99 -screen 0 1024x768x24 -ac +extension GLX +render -noreset &
#sleep 2

# Verify LiteLLM is running
if ps -p $LITELLM_PID > /dev/null; then
    echo "LiteLLM proxy started successfully!"
    echo "LiteLLM health check:"
    curl -s http://localhost:4000/health
    echo ""
else
    echo "ERROR: LiteLLM failed to start! Check /var/log/litellm.log"
    echo "----- LiteLLM Log Tail -----"
    tail -n 20 /var/log/litellm.log
    echo "----------------------------"
    exit 1
fi

# Set environment variables for Skyvern
export OPENAI_API_KEY=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
export OPENAI_API_BASE=http://localhost:4000
export OPENAI_MODEL=groq-llama

# Start main application
#./run.sh