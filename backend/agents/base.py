from abc import ABC, abstractmethod
from ..schemas import AgentResultEnvelope
from ..logging_config import get_logger

# We use string annotation for JobRepository to avoid circular imports 
# or we can import it if it's safe. It should be safe here.
from ..repositories.job import JobRepository

logger = get_logger(__name__)

class BaseAgent(ABC):
    """
    Abstract Base Class for all non-scraper agents.
    Enforces a strict contract ensuring all agents return AgentResultEnvelope.
    """
    agent_id: str
    canonical_role: str
    display_name: str

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, 'agent_id'):
            raise TypeError(f"{cls.__name__} must define an 'agent_id' class attribute")
        if not cls.agent_id.islower() or ' ' in cls.agent_id:
            raise ValueError("agent_id must be lowercase and contain no spaces")
            
        if not hasattr(cls, 'canonical_role'):
            raise TypeError(f"{cls.__name__} must define a 'canonical_role' class attribute")
            
        if not hasattr(cls, 'display_name'):
            raise TypeError(f"{cls.__name__} must define a 'display_name' class attribute")

class BaseScrapeAgent(ABC):
    """
    Abstract Base Class for all scraper agents. 
    Enforces a strict contract ensuring all scrapers can be orchestrated identically.
    """
    source_id: str
    display_name: str

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, 'source_id'):
            raise TypeError(f"{cls.__name__} must define a 'source_id' class attribute")
        if not cls.source_id.islower() or ' ' in cls.source_id:
            raise ValueError("source_id must be lowercase and contain no spaces")
            
        if not hasattr(cls, 'display_name'):
            raise TypeError(f"{cls.__name__} must define a 'display_name' class attribute")

    @abstractmethod
    async def run(self, repo: JobRepository, max_jobs: int = 10) -> AgentResultEnvelope:
        """
        Executes the scraping process, normalizes the data into Job models,
        and returns a ScrapeResult summary.
        """
        pass
