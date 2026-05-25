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
        from ..models import SavedJob
        from ..settings import get_settings
        user_id = get_settings().single_user_id

        query = select(DBJob, SavedJob.job_id.is_not(None).label("is_saved"))\
            .outerjoin(SavedJob, and_(SavedJob.job_id == DBJob.id, SavedJob.user_id == user_id))

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
        rows = list(result.all())

        # Check for next page
        has_more = len(rows) > limit
        if has_more:
            rows_slice = rows[:limit]
            last_db_job, _ = rows_slice[-1]
            next_cursor = encode_cursor(last_db_job.scraped_at, str(last_db_job.id))
        else:
            rows_slice = rows
            next_cursor = None

        output_jobs = []
        for db_job, is_saved in rows_slice:
            job = Job.model_validate(db_job)
            job.saved = is_saved
            output_jobs.append(job)

        return output_jobs, next_cursor

    async def get_saved_jobs(self) -> list[Job]:
        """Fetch all saved jobs from Postgres."""
        from ..models import SavedJob
        from ..settings import get_settings
        user_id = get_settings().single_user_id

        query = select(DBJob).join(SavedJob, and_(SavedJob.job_id == DBJob.id, SavedJob.user_id == user_id)).order_by(SavedJob.saved_at.desc())
        result = await self.session.execute(query)
        db_jobs = list(result.scalars().all())
        
        output_jobs = []
        for db_job in db_jobs:
            job = Job.model_validate(db_job)
            job.saved = True
            output_jobs.append(job)
        return output_jobs

    async def set_job_saved(self, job_id: str, saved: bool) -> None:
        """Mark a job as saved or unsaved in Postgres."""
        from sqlalchemy import delete
        from sqlalchemy.dialects.postgresql import insert as pg_insert
        from ..models import SavedJob
        from ..settings import get_settings
        
        user_id = get_settings().single_user_id
        
        if saved:
            stmt = pg_insert(SavedJob).values(job_id=job_id, user_id=user_id)
            stmt = stmt.on_conflict_do_nothing(index_elements=["job_id", "user_id"])
            await self.session.execute(stmt)
        else:
            stmt = delete(SavedJob).where(and_(SavedJob.job_id == job_id, SavedJob.user_id == user_id))
            await self.session.execute(stmt)
        await self.session.flush()

    async def get_job_by_id(self, job_id: str) -> Job | None:
        """Fetch a single job by its ID from Postgres."""
        from ..models import SavedJob
        from ..settings import get_settings
        user_id = get_settings().single_user_id

        query = select(DBJob, SavedJob.job_id.is_not(None).label("is_saved"))\
            .outerjoin(SavedJob, and_(SavedJob.job_id == DBJob.id, SavedJob.user_id == user_id))\
            .where(DBJob.id == job_id)
            
        result = await self.session.execute(query)
        row = result.first()
        if row:
            db_job, is_saved = row
            job = Job.model_validate(db_job)
            job.saved = is_saved
            return job
        return None

def get_job_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> JobRepository:
    return JobRepository(db)

type JobRepo = Annotated[JobRepository, Depends(get_job_repo)]
