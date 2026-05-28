import litellm
from pydantic import BaseModel
from .config import llm_settings
from ..logging_config import get_logger
from typing import Any, Type
from ..services.toon_parser import generate_toon_instruction, parse_toon_response

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
    fallbacks = []

    # Model Selection Matrix (JD-129)
    AGENT_MODEL_MAP = {
        "linkedin": {"primary": "gpt-4o-mini", "fallback": "local/gpt-oss-120b"},
        "jobserve": {"primary": "gpt-4o-mini", "fallback": "local/gpt-oss-120b"},
        "ranking": {"primary": "openrouter/anthropic/claude-3.5-sonnet", "fallback": "gpt-4o"},
        "rag": {"primary": "openrouter/anthropic/claude-3.5-sonnet", "fallback": "gpt-4o"},
        "cover_letter": {"primary": "openrouter/anthropic/claude-3.5-sonnet", "fallback": "gpt-4o"},
        "question_answer": {"primary": "openrouter/anthropic/claude-3.5-sonnet", "fallback": "gpt-4o"},
        "security": {"primary": "openrouter/anthropic/claude-3.5-sonnet", "fallback": "gpt-4o"},
        "quality_critic": {"primary": "openrouter/anthropic/claude-3.5-sonnet", "fallback": "gpt-4o-mini"},
        "orchestrator": {"primary": "openrouter/anthropic/claude-3-opus", "fallback": "gpt-5"},
        "interview_prep": {"primary": "openrouter/anthropic/claude-3-opus", "fallback": "gpt-5"},
        "application_assistant": {"primary": "openrouter/anthropic/claude-3.5-sonnet", "fallback": "gpt-4o"},
    }

    if agent_id and agent_id in AGENT_MODEL_MAP:
        target_model = AGENT_MODEL_MAP[agent_id]["primary"]
        fallbacks = [AGENT_MODEL_MAP[agent_id]["fallback"]]

    if agent_id:
        override = getattr(settings, f"model_override_{agent_id}", None)
        if override:
            target_model = override
            fallbacks = []

    logger.info(f"Generating LLM response using model {target_model} with fallbacks {fallbacks}")
    
    if response_model:
        system_instruction = f"{system_instruction}\n\n{generate_toon_instruction(response_model)}"
    
    try:
        # Mock integration for now. 
        # In a real environment, acompletion returns an object with choices.
        response = await litellm.acompletion(
            model=target_model,
            fallbacks=fallbacks,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            api_key=llm_settings.OPENROUTER_API_KEY,
            temperature=llm_settings.TEMPERATURE,
            max_tokens=llm_settings.MAX_TOKENS,
        )
        
        content = response.choices[0].message.content.strip()
        
        try:
            parsed_result = parse_toon_response(content, response_model)
            logger.info("Successfully generated and parsed LLM response using TOON parser.")
            return parsed_result
        except Exception as e:
            logger.error(f"Failed to parse LLM response: {content}")
            raise e
            
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
