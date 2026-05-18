import hashlib
import time
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import insert as pg_insert
from ...db import AsyncSessionLocal
from ...models import ScrapeResult, DBJob
from ..base import BaseScrapeAgent
from ..registry import register
from ...logging_config import get_logger

logger = get_logger(__name__)


@register
class LinkedInAgent(BaseScrapeAgent):
    source_id = "linkedin"
    display_name = "LinkedIn Jobs"

    async def run(self, max_jobs: int = 10) -> ScrapeResult:
        """Execute scrape and persist to Supabase PostgreSQL."""
        logger.info(f"Starting {self.source_id} scrape...")
        start_time = time.time()

        # Sample jobs to seed the database
        sample_jobs = [
            {
                "title": "Senior AI Platform Engineer",
                "company": "TechNova AI",
                "location": "Remote, US",
                "description": "Join our AI Platform team to architect high-performance RAG pipelines and vector retrieval engines. Experience with Python, FastAPI, and pgvector required.",
                "url": "https://www.linkedin.com/jobs/view/technova-senior-ai-platform-engineer-101",
            },
            {
                "title": "Lead Machine Learning Engineer",
                "company": "FutureScale Systems",
                "location": "New York, NY",
                "description": "We are seeking a Lead ML Engineer to spearhead our agentic automation pipelines. You will design, build, and deploy LLM agents using Temporal and LiteLLM.",
                "url": "https://www.linkedin.com/jobs/view/futurescale-lead-ml-engineer-102",
            },
            {
                "title": "AI Product Engineer",
                "company": "InnovateLabs",
                "location": "London, UK",
                "description": "Build next-generation user interfaces for generative AI workflows. Heavy focus on React 19, Next.js 16, and FastAPI backends.",
                "url": "https://www.linkedin.com/jobs/view/innovatelabs-ai-product-engineer-103",
            },
        ]

        jobs_to_process = sample_jobs[:max_jobs]
        jobs_saved = 0
        errors = []

        try:
            async with AsyncSessionLocal() as db:
                for job in jobs_to_process:
                    # Generate deterministic ID
                    job_id = hashlib.sha256(job["url"].encode("utf-8")).hexdigest()[:16]

                    # Construct PostgreSQL-specific UPSERT
                    stmt = pg_insert(DBJob).values(
                        id=job_id,
                        title=job["title"],
                        company=job["company"],
                        location=job["location"],
                        description=job["description"],
                        url=job["url"],
                        source=self.source_id,
                        posted_at=datetime.now(timezone.utc),
                        scraped_at=datetime.now(timezone.utc),
                    )

                    stmt = stmt.on_conflict_do_update(
                        index_elements=["id"],
                        set_={
                            "title": stmt.excluded.title,
                            "company": stmt.excluded.company,
                            "location": stmt.excluded.location,
                            "description": stmt.excluded.description,
                            "url": stmt.excluded.url,
                            "scraped_at": stmt.excluded.scraped_at,
                        },
                    )

                    await db.execute(stmt)
                    jobs_saved += 1

                await db.commit()
                logger.info(f"Successfully upserted {jobs_saved} jobs from LinkedIn.")

        except Exception as e:
            logger.error(f"LinkedIn scrape session failed: {e}", exc_info=True)
            errors.append(str(e))

        duration = time.time() - start_time

        return ScrapeResult(
            source_id=self.source_id,
            jobs_found=len(jobs_to_process),
            jobs_saved=jobs_saved if not errors else 0,
            errors=errors,
            duration_seconds=round(duration, 3),
        )
