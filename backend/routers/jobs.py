import base64
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from ..models import DBJob, Job

router: APIRouter = APIRouter(prefix="/jobs", tags=["Jobs"])


class PaginatedJobsResponse(BaseModel):
    data: List[Job]
    next_cursor: str | None


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


@router.get("/", response_model=PaginatedJobsResponse)
async def list_jobs(
    limit: int = Query(default=20, ge=1, le=100),
    cursor: str | None = Query(default=None),
    source: str | None = Query(default=None),
    keyword: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    """
    List jobs with keyset pagination and filtering.
    """
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
            # Filter condition for Keyset Pagination (scraped_at DESC, id DESC)
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

    # 3. Explicit ordering (scraped_at DESC, id DESC)
    query = query.order_by(DBJob.scraped_at.desc(), DBJob.id.desc())

    # Limit to fetch limit + 1 records to check if there is a next page
    query = query.limit(limit + 1)

    result = await db.execute(query)
    db_jobs = list(result.scalars().all())

    # 4. Check for next page
    has_more = len(db_jobs) > limit
    if has_more:
        jobs_slice = db_jobs[:limit]
        last_job = jobs_slice[-1]
        next_cursor = encode_cursor(last_job.scraped_at, last_job.id)
    else:
        jobs_slice = db_jobs
        next_cursor = None

    # Map SQLAlchemy objects to Pydantic Job models
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

    return PaginatedJobsResponse(data=output_jobs, next_cursor=next_cursor)
