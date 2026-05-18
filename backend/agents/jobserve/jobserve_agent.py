import time
from ...models import ScrapeResult
from ..base import BaseScrapeAgent
from ..registry import register
from ...logging_config import get_logger

logger = get_logger(__name__)

@register
class JobServeAgent(BaseScrapeAgent):
    source_id = "jobserve"
    display_name = "JobServe"

    async def run(self, max_jobs: int = 10) -> ScrapeResult:
        logger.info(f"Starting {self.source_id} scrape...")
        
        start_time = time.time()
        
        # Stub: Implement actual logic in MVP 2 or later.
        
        duration = time.time() - start_time
        
        return ScrapeResult(
            source_id=self.source_id,
            jobs_found=0,
            jobs_saved=0,
            errors=[],
            duration_seconds=duration
        )
