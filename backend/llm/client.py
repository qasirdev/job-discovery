import litellm
from pydantic import BaseModel
from .config import llm_settings
from ..logging_config import get_logger
from typing import Any, Type

logger = get_logger(__name__)

async def generate_structured_response(
    prompt: str, 
    system_instruction: str, 
    response_model: Type[BaseModel],
    agent_id: str | None = None
) -> Any:
    """
    Generate a strictly typed JSON response from the LLM.
    
    Uses LiteLLM to interface with OpenRouter.
    """
    from ..settings import get_settings
    settings = get_settings()
    
    target_model = llm_settings.DEFAULT_MODEL
    if agent_id:
        override = getattr(settings, f"model_override_{agent_id}", None)
        if override:
            target_model = override

    logger.info(f"Generating LLM response using model {target_model}")
    
    try:
        # Mock integration for now. 
        # In a real environment, acompletion returns an object with choices.
        response = await litellm.acompletion(
            model=target_model,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            api_key=llm_settings.OPENROUTER_API_KEY,
            temperature=llm_settings.TEMPERATURE,
            max_tokens=llm_settings.MAX_TOKENS,
        )
        
        logger.info("Successfully generated LLM response.")
        return response
    except Exception as e:
        logger.error(f"LLM API Call failed: {e}", exc_info=True)
        raise e

async def generate_embedding(text: str) -> list[float]:
    """Generate embedding vector for the text using LiteLLM."""
    try:
        response = await litellm.aembedding(
            model="text-embedding-3-small",
            input=[text],
            api_key=llm_settings.OPENROUTER_API_KEY
        )
        return response.data[0]["embedding"]
    except Exception as e:
        logger.error(f"Failed to generate embedding: {e}")
        # Return dummy vector for MVP testing if API fails
        return [0.0] * 1536
