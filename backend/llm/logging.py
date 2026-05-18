from ..logging_config import get_logger

logger = get_logger(__name__)

def log_llm_transaction(model: str, tokens_used: int, cost: float) -> None:
    """Log token usage and costs for Observability."""
    logger.info(
        "LLM Transaction",
        extra={
            "model": model,
            "tokens_used": tokens_used,
            "cost_usd": cost
        }
    )
