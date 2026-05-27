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
    pass

class BaseScrapeAgent(ABC):
    """
    Abstract Base Class for all scraper agents. 
    Enforces a strict contract ensuring all scrapers can be orchestrated identically.
    """
    source_id: str
    display_name: str

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, 'source_id'):
            if not cls.source_id.islower() or ' ' in cls.source_id:
                raise AssertionError("source_id must be lowercase and contain no spaces")

    @abstractmethod
    async def run(self, repo: JobRepository, max_jobs: int = 10) -> AgentResultEnvelope:
        """
        Executes the scraping process, normalizes the data into Job models,
        and returns a ScrapeResult summary.
        """
        pass
