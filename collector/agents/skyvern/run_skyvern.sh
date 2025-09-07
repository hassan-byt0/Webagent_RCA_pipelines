#!/bin/bash

cd "$(dirname "$0")" || exit

pid=$(lsof -t -i :8000)
if [ -n "$pid" ]; then
  kill "$pid"
fi

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Please add your api keys to the .env file."
fi

# Add LiteLLM installation
#pip install litellm[proxy]

#cp collector/agents/skyvern/litellm_custom_groq_config.yaml ./litellm_custom_groq_config.yaml
#cp collector/agents/skyvern/start_services.sh ./start_services.sh
#chmod +x ./start_services.sh

# Start services and run Skyvern
#./start_services.sh 

#export OPENAI_API_KEY=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
#export OPENAI_API_BASE=http://localhost:4000
#export OPENAI_MODEL=groq-llama

python -m skyvern.forge
