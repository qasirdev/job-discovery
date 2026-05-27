from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from uuid import UUID

router = APIRouter(prefix="/api/v1/interview-prep", tags=["Interview Prep"])

class InterviewPrepResponse(BaseModel):
    message: str

@router.post("/{job_id}", response_model=InterviewPrepResponse)
async def generate_interview_prep(job_id: UUID):
    """
    Generate interview prep materials for a specific job.
    Currently returns 503 Service Unavailable until the Interview Prep Agent is fully active in Post-MVP 3.
    """
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Interview Preparation Agent is not fully active yet."
    )
