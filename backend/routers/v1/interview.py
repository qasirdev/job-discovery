from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..dependencies import require_rag_ready
from ...db import get_db
from ...models import Job
from ...settings import get_settings
import hashlib
from datetime import timedelta

router = APIRouter(prefix="/interview-prep", tags=["Interview Prep"])

@router.post("/{job_id}", dependencies=[Depends(require_rag_ready)])
async def generate_interview_prep(job_id: str, db: AsyncSession = Depends(get_db)):
    job = (await db.execute(select(Job).where(Job.id == job_id))).scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    from temporalio.client import Client
    settings = get_settings()
    client = await Client.connect(settings.temporal_server_url or "localhost:7233")
    workflow_id = f"interview_prep_{job_id}"
    
    payload = {
        "job_id": job_id,
        "company_name": job.company
    }
    
    # We don't await the result, we just trigger it and let it run
    try:
        await client.start_workflow(
            "InterviewPrepWorkflow",
            payload,
            id=workflow_id,
            task_queue="interview-tasks",
            execution_timeout=timedelta(minutes=10)
        )
    except Exception as e:
        logger = get_logger(__name__)
        logger.error(f"Failed to start interview prep workflow: {e}")
        # The frontend expects a JSON response indicating success or failure.
        # But if workflow is already running, Temporal throws an error.
        # We can ignore if it's already running.
        pass

    return {"status": "started", "job_id": job_id}

@router.get("/{job_id}", response_model=None)
async def get_interview_prep(job_id: str, db: AsyncSession = Depends(get_db)):
    from ...models import InterviewPrep
    import uuid
    prep = (await db.execute(select(InterviewPrep).where(InterviewPrep.job_id == uuid.UUID(job_id)))).scalar_one_or_none()
    if not prep:
        raise HTTPException(status_code=404, detail="Interview prep not found")
    
    return {
        "id": str(prep.id),
        "job_id": str(prep.job_id),
        "questions": prep.questions,
        "system_design_topics": prep.system_design_topics,
        "salary_benchmark": prep.salary_benchmark,
        "company_research": prep.company_research,
        "status": prep.status.value,
        "created_at": prep.created_at.isoformat()
    }
