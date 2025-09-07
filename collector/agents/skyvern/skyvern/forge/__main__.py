import structlog
import uvicorn
from dotenv import load_dotenv
#from litellm import register_model
from skyvern import analytics
from skyvern.config import settings

LOG = structlog.stdlib.get_logger()


if __name__ == "__main__":
    
    port = settings.PORT
    LOG.info("Agent server starting.", host="0.0.0.0", port=port)
    load_dotenv()
    #register_model({
    # key is the exact model identifier + provider you’re using
    #"deepseek/deepseek-chat-v3-0324:free": {
    #    # maximum context length for this model
    #    "max_tokens": 8192,  
        # per‐token costs (fill in with the real OpenRouter pricing)
    #    "input_cost_per_token": 0.0,
    #    "output_cost_per_token": 0.0,
    #    # tell Litellm this is an OpenRouter-hosted chat model
    #    "litellm_provider": "openrouter",
    #    "mode": "chat"
    #}
#}#)

    reload = settings.ENV == "local"
    uvicorn.run(
        "skyvern.forge.api_app:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=reload,
    )
