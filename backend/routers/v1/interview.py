from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Any, Dict
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...settings import get_settings, AppSettings
from ...logging_config import get_logger
from ...agents.interview_prep.interview_agent import InterviewPrepAgent
from ...db import get_db
from ...models import InterviewPrep, InterviewQuestion, InterviewPrepStatus

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/interview-prep", tags=["Interview Prep"])

class InterviewPrepRequest(BaseModel):
    company_name: str | None = None
    job_title: str | None = None
    job_description: str | None = None

class InterviewPrepResponse(BaseModel):
    job_id: str
    status: str
    result: Dict[str, Any] | None = None
    message: str | None = None

@router.get("/{job_id}", response_model=InterviewPrepResponse)
async def get_interview_prep(
    job_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    ip = (await db.execute(select(InterviewPrep).where(InterviewPrep.job_id == job_id))).scalar_one_or_none()
    if not ip:
        raise HTTPException(status_code=404, detail="Interview preparation not found")
        
    result = {
        "company_research": ip.company_research,
        "questions": ip.questions,
        "system_design_topics": ip.system_design_topics,
        "salary_benchmark": ip.salary_benchmark
    }
    
    iqs = (await db.execute(select(InterviewQuestion).where(InterviewQuestion.interview_prep_id == ip.id))).scalars().all()
    if iqs:
        result["questions"] = [q.question_text for q in iqs]
        result["question_bank"] = [{"question": q.question_text, "difficulty": q.difficulty_rating, "suggested_answer": q.suggested_answer} for q in iqs]

    return InterviewPrepResponse(
        job_id=str(job_id),
        status=ip.status.value,
        result=result
    )

@router.post("/{job_id}", response_model=InterviewPrepResponse)
async def generate_interview_prep(
    job_id: UUID,
    body: InterviewPrepRequest = InterviewPrepRequest(),
    settings: AppSettings = Depends(get_settings),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate interview prep materials for a specific job.

    Gated by FEATURE_INTERVIEW_PREP_AGENT. Returns 503 when the flag is false
    (graceful degradation per JD-121). When active, delegates to InterviewPrepAgent
    and returns the structured interview pack.
    """
    if not settings.feature_interview_prep_agent:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Interview Preparation Agent is not currently enabled. "
                   "Set FEATURE_INTERVIEW_PREP_AGENT=true to activate.",
        )

    ip = (await db.execute(select(InterviewPrep).where(InterviewPrep.job_id == job_id))).scalar_one_or_none()
    if not ip:
        ip = InterviewPrep(job_id=job_id, status=InterviewPrepStatus.generating)
        db.add(ip)
        await db.commit()
        await db.refresh(ip)
    else:
        ip.status = InterviewPrepStatus.generating
        await db.commit()

    request_data: Dict[str, Any] = {
        "job_id": str(job_id),
        "company_name": body.company_name or "Unknown Company",
        "job_title": body.job_title or "",
        "job_description": body.job_description or "",
    }

    logger.info(f"interview_prep request for job_id={job_id}, company={request_data['company_name']}")

    from temporalio.client import Client
    from datetime import timedelta
    
    try:
        client = await Client.connect(settings.temporal_server_url or "localhost:7233")
        workflow_id = f"interview_prep_{job_id}"
        await client.start_workflow(
            "InterviewPrepWorkflow",
            request_data,
            id=workflow_id,
            task_queue="interview-tasks",
            execution_timeout=timedelta(minutes=10)
        )
    except Exception as e:
        logger.error(f"Failed to start Interview Prep workflow for job_id={job_id}: {e}")
        ip.status = InterviewPrepStatus.failed
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Interview preparation generation failed to start. Please try again.",
        )

    return InterviewPrepResponse(
        job_id=str(job_id),
        status=ip.status.value,
        result=None,
    )
