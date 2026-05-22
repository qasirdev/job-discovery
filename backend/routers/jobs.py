from typing import List
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from ..models import Job
from ..logging_config import get_logger
from ..repositories.job import JobRepo

logger = get_logger(__name__)
router: APIRouter = APIRouter(prefix="/jobs", tags=["Jobs"])

class PaginatedJobsResponse(BaseModel):
    data: List[Job]
    next_cursor: str | None

@router.get("/", response_model=PaginatedJobsResponse)
async def list_jobs(
    repo: JobRepo,
    limit: int = Query(default=20, ge=1, le=100),
    cursor: str | None = Query(default=None),
    source: str | None = Query(default=None),
    keyword: str | None = Query(default=None),
):
    """
    List jobs with keyset pagination and filtering.
    Delegates completely to JobRepository.
    """
    output_jobs, next_cursor = await repo.get_paginated_jobs(
        limit=limit,
        cursor=cursor,
        source=source,
        keyword=keyword
    )
    return PaginatedJobsResponse(data=output_jobs, next_cursor=next_cursor)
