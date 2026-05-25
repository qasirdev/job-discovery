from fastapi import APIRouter
from typing import Dict, Any
from ...agents.observability.observability_agent import ObservabilityAgent

router = APIRouter(prefix="/observability", tags=["observability"])

# We can initialize a global ObservabilityAgent instance or get it via dependency injection.
obs_agent = ObservabilityAgent()

@router.get("/status", response_model=Dict[str, Any])
async def get_observability_status():
    """
    Returns all current metric values as JSON for internal monitoring use.
    Includes schema conformance rate, hallucination rate, retrieval precision,
    and token budget alerts. No authentication required.
    """
    return await obs_agent.get_status()
