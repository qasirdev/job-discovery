from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from ..models import Job
from ..db import fake_db  # Mock DB for MVP 1

router: APIRouter = APIRouter(prefix="/jobs", tags=["Jobs"])

class PaginatedJobsResponse(BaseModel):
    data: List[Job]
    next_cursor: str | None

@router.get("/", response_model=PaginatedJobsResponse)
async def list_jobs(limit: int = 20, cursor: str | None = None):
    """
    MVP 1: Returns jobs from memory.
    MVP 2: Upgraded to use asyncpg and real cursor pagination (keyset pagination).
    """
    jobs = fake_db["jobs"]
    
    # Mock pagination logic
    start_idx = 0
    if cursor:
        try:
            start_idx = int(cursor)
        except ValueError:
            pass
            
    end_idx = start_idx + limit
    page_data = jobs[start_idx:end_idx]
    
    next_cursor = str(end_idx) if end_idx < len(jobs) else None
    
    return PaginatedJobsResponse(
        data=page_data,
        next_cursor=next_cursor
    )
