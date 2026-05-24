from abc import ABC, abstractmethod
from ..schemas import ScrapeResult
from typing import Optional

# We use string annotation for JobRepository to avoid circular imports 
# or we can import it if it's safe. It should be safe here.
from ..repositories.job import JobRepository

class BaseScrapeAgent(ABC):
    """
    Abstract Base Class for all scraper agents. 
    Enforces a strict contract ensuring all scrapers can be orchestrated identically.
    """
    source_id: str
    display_name: str

    @abstractmethod
    async def run(self, repo: JobRepository, max_jobs: int = 10) -> ScrapeResult:
        """
        Executes the scraping process, normalizes the data into Job models,
        and returns a ScrapeResult summary.
        """
        pass
