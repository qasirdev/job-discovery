from typing import Dict, Type
from .base import BaseScrapeAgent
from ..logging_config import get_logger
from ..settings import get_settings

logger = get_logger(__name__)

_AGENTS: Dict[str, Type[BaseScrapeAgent]] = {}

def register(agent_class: Type[BaseScrapeAgent]) -> Type[BaseScrapeAgent]:
    """
    Decorator to register a scraper agent into the global registry.
    This prevents hardcoding agent instantiations in the orchestrator.
    """
    source_id = getattr(agent_class, "source_id", None)
    if not source_id:
        raise ValueError(f"Agent {agent_class.__name__} must define a 'source_id'")
        
    if source_id in _AGENTS:
        raise ValueError(f"Agent {source_id} is already registered.")
        
    _AGENTS[source_id] = agent_class
    logger.info(f"Registered agent: {source_id}")
    return agent_class

def get_all_agents() -> list[Type[BaseScrapeAgent]]:
    """Return all registered agents that are activated via feature flags."""
    settings = get_settings()
    active_agents = []
    for source_id, agent_class in _AGENTS.items():
        flag_name = f"feature_{source_id}_agent"
        if getattr(settings, flag_name, True):
            active_agents.append(agent_class)
    return active_agents

def get_agent(source_id: str) -> Type[BaseScrapeAgent] | None:
    """Return a registered agent by source ID if it is activated via feature flag."""
    settings = get_settings()
    flag_name = f"feature_{source_id}_agent"
    if not getattr(settings, flag_name, True):
        return None
    return _AGENTS.get(source_id)
