import base64
import uuid
from datetime import datetime, timezone
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert
from typing import Annotated
from fastapi import Depends
from ..models import Job as DBJob
from ..schemas import Job
from ..db import get_db
from ..logging_config import get_logger

logger = get_logger(__name__)

def encode_cursor(scraped_at: datetime, job_id: str) -> str:
    """Encode scraped_at and job_id into a base64 opaque cursor."""
    raw_str = f"{scraped_at.isoformat()}|{job_id}"
    return base64.b64encode(raw_str.encode("utf-8")).decode("utf-8")

def decode_cursor(cursor_str: str) -> tuple[datetime, str] | None:
    """Decode a base64 cursor into scraped_at and job_id."""
    try:
        decoded_bytes = base64.b64decode(cursor_str.encode("utf-8"))
        decoded_str = decoded_bytes.decode("utf-8")
        iso_time, job_id = decoded_str.split("|", 1)
        return datetime.fromisoformat(iso_time), job_id
    except Exception:
        return None

class JobRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def upsert_jobs(self, jobs_to_process: list[dict], source_id: str) -> int:
        """Upsert jobs to Postgres."""
        jobs_saved = 0
        try:
            for job in jobs_to_process:
                job_id = uuid.uuid5(uuid.NAMESPACE_URL, job["url"])

                stmt = pg_insert(DBJob).values(
                    id=job_id,
                    title=job["title"],
                    company=job["company"],
                    location=job.get("location"),
                    description=job["description"],
                    url=job["url"],
                    source=source_id,
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
            logger.error(f"PostgreSQL database error during upsert ({e}).")
            raise
        return jobs_saved

    async def get_paginated_jobs(
        self, limit: int, cursor: str | None, source: str | None, keyword: str | None
    ) -> tuple[list[Job], str | None]:
        """Fetch paginated jobs from Postgres."""
        query = select(DBJob)

        # 1. Apply filters
        filters = []
        if source:
            filters.append(DBJob.source == source)
        if keyword:
            filters.append(
                or_(
                    DBJob.title.ilike(f"%{keyword}%"),
                    DBJob.description.ilike(f"%{keyword}%"),
                )
            )

        # 2. Keyset pagination filter using cursor
        if cursor:
            decoded = decode_cursor(cursor)
            if decoded:
                cursor_time, cursor_id = decoded
                filters.append(
                    or_(
                        DBJob.scraped_at < cursor_time,
                        and_(
                            DBJob.scraped_at == cursor_time,
                            DBJob.id < cursor_id,
                        ),
                    )
                )

        if filters:
            query = query.where(and_(*filters))

        query = query.order_by(DBJob.scraped_at.desc(), DBJob.id.desc())
        query = query.limit(limit + 1)

        result = await self.session.execute(query)
        db_jobs = list(result.scalars().all())

        # Check for next page
        has_more = len(db_jobs) > limit
        if has_more:
            jobs_slice = db_jobs[:limit]
            last_job = jobs_slice[-1]
            next_cursor = encode_cursor(last_job.scraped_at, str(last_job.id))
        else:
            jobs_slice = db_jobs
            next_cursor = None

        output_jobs = [
            Job.model_validate(job)
            for job in jobs_slice
        ]

        return output_jobs, next_cursor

    async def get_saved_jobs(self) -> list[Job]:
        """Fetch all saved jobs from Postgres."""
        query = select(DBJob).where(DBJob.saved).order_by(DBJob.scraped_at.desc())
        result = await self.session.execute(query)
        db_jobs = list(result.scalars().all())
        
        return [Job.model_validate(job) for job in db_jobs]

    async def set_job_saved(self, job_id: str, saved: bool) -> None:
        """Mark a job as saved or unsaved in Postgres."""
        from sqlalchemy import update
        stmt = update(DBJob).where(DBJob.id == job_id).values(saved=saved)
        await self.session.execute(stmt)
        await self.session.flush()

    async def get_job_by_id(self, job_id: str) -> Job | None:
        """Fetch a single job by its ID from Postgres."""
        query = select(DBJob).where(DBJob.id == job_id)
        result = await self.session.execute(query)
        db_job = result.scalar_one_or_none()
        if db_job:
            return Job.model_validate(db_job)
        return None

def get_job_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> JobRepository:
    return JobRepository(db)

type JobRepo = Annotated[JobRepository, Depends(get_job_repo)]
