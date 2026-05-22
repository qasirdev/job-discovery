import hashlib
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert
from typing import Annotated
from fastapi import Depends
from ..models import DBJob, Job
from ..db import get_db, fake_db
from ..logging_config import get_logger

logger = get_logger(__name__)

class JobRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def upsert_jobs(self, jobs_to_process: list[dict], source_id: str) -> int:
        """Upsert jobs to Postgres or fallback to fake_db on error."""
        jobs_saved = 0
        try:
            for job in jobs_to_process:
                job_id = hashlib.sha256(job["url"].encode("utf-8")).hexdigest()[:16]

                stmt = pg_insert(DBJob).values(
                    id=job_id,
                    title=job["title"],
                    company=job["company"],
                    location=job["location"],
                    description=job["description"],
                    url=job["url"],
                    source=source_id,
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

                await self.session.execute(stmt)
                jobs_saved += 1

            await self.session.flush()
            logger.info(f"Successfully upserted {jobs_saved} jobs from {source_id} to PostgreSQL.")
        except Exception as e:
            # Fallback DIFA implementation
            logger.warning(
                f"PostgreSQL database error ({e}). "
                f"Storing {len(jobs_to_process)} jobs inside in-memory fake_db instead (DIFA Fallback)."
            )
            for job in jobs_to_process:
                job_id = hashlib.sha256(job["url"].encode("utf-8")).hexdigest()[:16]
                job_model = Job(
                    id=job_id,
                    title=job["title"],
                    company=job["company"],
                    location=job["location"],
                    description=job["description"],
                    url=job["url"],
                    source=source_id,
                    posted_at=datetime.now(timezone.utc),
                    scraped_at=datetime.now(timezone.utc),
                )
                if not any(j.id == job_id for j in fake_db["jobs"]):
                    fake_db["jobs"].append(job_model)
                    jobs_saved += 1
        return jobs_saved

def get_job_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> JobRepository:
    return JobRepository(db)

type JobRepo = Annotated[JobRepository, Depends(get_job_repo)]
