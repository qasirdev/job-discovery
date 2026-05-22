import base64
import hashlib
from datetime import datetime, timezone
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert
from typing import Annotated
from fastapi import Depends
from ..models import DBJob, Job
from ..db import get_db, fake_db
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

    async def get_paginated_jobs(
        self, limit: int, cursor: str | None, source: str | None, keyword: str | None
    ) -> tuple[list[Job], str | None]:
        """Fetch paginated jobs with fallback to fake_db."""
        try:
            # Detect: Try querying the Supabase PostgreSQL database
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
                next_cursor = encode_cursor(last_job.scraped_at, last_job.id)
            else:
                jobs_slice = db_jobs
                next_cursor = None

            output_jobs = [
                Job(
                    id=job.id,
                    title=job.title,
                    company=job.company,
                    location=job.location,
                    description=job.description,
                    url=job.url,
                    source=job.source,
                    posted_at=job.posted_at,
                    scraped_at=job.scraped_at,
                )
                for job in jobs_slice
            ]

            return output_jobs, next_cursor

        except Exception as e:
            # Isolate & Alert: Log connection warning and fallback
            logger.warning(
                f"Supabase PostgreSQL database is unavailable ({e}). "
                "Gracefully falling back to in-memory store (DIFA-compliant)."
            )

            # Fallback: Query fake_db (in-memory mock store)
            jobs_pool = fake_db["jobs"]

            # Filter in-memory jobs
            filtered_jobs = jobs_pool
            if source:
                filtered_jobs = [j for j in filtered_jobs if j.source == source]
            if keyword:
                kw = keyword.lower()
                filtered_jobs = [
                    j for j in filtered_jobs
                    if kw in j.title.lower() or kw in j.description.lower()
                ]

            # In-memory cursor fallback
            start_idx = 0
            if cursor:
                try:
                    start_idx = int(cursor)
                except ValueError:
                    pass

            end_idx = start_idx + limit
            page_data = filtered_jobs[start_idx:end_idx]
            next_cursor = str(end_idx) if end_idx < len(filtered_jobs) else None

            return page_data, next_cursor

    async def get_job_by_id(self, job_id: str) -> Job | None:
        """Fetch a single job by its ID, falling back to fake_db."""
        try:
            # Query Postgres
            query = select(DBJob).where(DBJob.id == job_id)
            result = await self.session.execute(query)
            db_job = result.scalar_one_or_none()
            if db_job:
                return Job(
                    id=db_job.id,
                    title=db_job.title,
                    company=db_job.company,
                    location=db_job.location,
                    description=db_job.description,
                    url=db_job.url,
                    source=db_job.source,
                    posted_at=db_job.posted_at,
                    scraped_at=db_job.scraped_at,
                )
            return None
        except Exception as e:
            logger.warning(f"Database error fetching job {job_id} ({e}). Falling back to fake_db.")
            for j in fake_db["jobs"]:
                if j.id == job_id:
                    return j
            return None

def get_job_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> JobRepository:
    return JobRepository(db)

type JobRepo = Annotated[JobRepository, Depends(get_job_repo)]
