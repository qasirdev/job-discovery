from typing import List
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from pydantic import BaseModel, Field
from ...schemas import Job, JobListResponse, RFC7807Error
from ...logging_config import get_logger
from ...db import get_db
from ...repositories.job import JobRepo
from ..dependencies import require_rag_ready

logger = get_logger(__name__)
router: APIRouter = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get(
    "/",
    response_model=JobListResponse,
    summary="List jobs",
    description="List jobs with keyset pagination and filtering."
)
async def list_jobs(
    repo: JobRepo,
    page_size: int = Query(default=20, ge=1, le=100),
    cursor: str | None = Query(default=None),
    keyword: str | None = Query(default=None),
):
    """
    List jobs with keyset pagination and filtering.
    """
    logger.info(f"Listing jobs with page_size={page_size}, cursor={cursor}, keyword={keyword}")
    output_jobs, next_cursor = await repo.get_paginated_jobs(
        limit=page_size,
        cursor=cursor,
        source=None,
        keyword=keyword
    )
    
    # We will need the counts from db, but for MVP 2 we could return dummy or count queries
    # For now, just returning empty stats as it's not the main focus and fake_db is removed
    linkedin_count = 0
    jobserve_count = 0
    
    page = 1
    
    return JobListResponse(
        total=len(output_jobs),
        page=page,
        page_size=page_size,
        has_next=next_cursor is not None,
        next_cursor=next_cursor,
        linkedin_count=linkedin_count,
        jobserve_count=jobserve_count,
        jobs=output_jobs
    )

@router.get(
    "/saved",
    response_model=List[Job],
    summary="List saved jobs",
    description="List all saved jobs for the current user."
)
async def list_saved_jobs(repo: JobRepo):
    """
    List all saved jobs.
    """
    logger.info("Listing saved jobs")
    return await repo.get_saved_jobs()

@router.get(
    "/{id}",
    response_model=Job,
    summary="Get job",
    description="Get a single job by ID.",
    responses={
        404: {"model": RFC7807Error, "description": "Job not found"}
    }
)
async def get_job_endpoint(repo: JobRepo, id: str = Path(...)):
    """
    Get a single job by ID.
    """
    logger.info(f"Fetching job {id}")
    job = await repo.get_job_by_id(id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": status.HTTP_404_NOT_FOUND,
                "detail": "Job not found"
            }
        )
    return job

class SaveResponse(BaseModel):
    saved: bool = Field(examples=[True])

@router.post(
    "/{id}/save",
    response_model=SaveResponse,
    summary="Save job",
    description="Mark a job as saved.",
    responses={
        404: {"model": RFC7807Error, "description": "Job not found"}
    }
)
async def save_job(repo: JobRepo, id: str = Path(...)):
    """
    Mark a job as saved.
    """
    logger.info(f"Saving job {id}")
    job = await repo.get_job_by_id(id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": status.HTTP_404_NOT_FOUND,
                "detail": "Job not found"
            }
        )
        
    await repo.set_job_saved(id, True)
        
    return SaveResponse(saved=True)

@router.delete(
    "/{id}/save",
    response_model=SaveResponse,
    summary="Unsave job",
    description="Mark a job as unsaved.",
    responses={
        404: {"model": RFC7807Error, "description": "Job not found"}
    }
)
async def unsave_job(repo: JobRepo, id: str = Path(...)):
    """
    Mark a job as unsaved.
    """
    logger.info(f"Unsaving job {id}")
    job = await repo.get_job_by_id(id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": status.HTTP_404_NOT_FOUND,
                "detail": "Job not found"
            }
        )
        
    await repo.set_job_saved(id, False)
        
    return SaveResponse(saved=False)

from ...agents.orchestrator.orchestrator_agent import OrchestratorAgent

@router.post("/{job_id}/process")
async def process_job(job_id: str, repo: JobRepo):
    """
    Trigger the AI Orchestrator Pipeline for a specific job.
    """
    job = await repo.get_job_by_id(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": status.HTTP_404_NOT_FOUND,
                "detail": "Job not found"
            }
        )
        
    orchestrator = OrchestratorAgent()
    result = await orchestrator.process_job(job)
    return result

from ...agents.question_answer.question_answer_agent import QAAgent
from ...agents.rag.rag_agent import RAGAgent

class AskRequest(BaseModel):
    question: str = Field(examples=["Is this role fully remote?"])

@router.post("/{job_id}/ask", dependencies=[Depends(require_rag_ready)])
async def ask_question(job_id: str, request: AskRequest, repo: JobRepo):
    """
    Ask a question about a specific job. Uses RAG context and the QA Agent.
    """
    job = await repo.get_job_by_id(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": status.HTTP_404_NOT_FOUND,
                "detail": "Job not found"
            }
        )

    rag = RAGAgent(db=repo.session)
    context = await rag.retrieve_context(job.description)

    qa = QAAgent()
    result = await qa.answer_question(job, context, request.question)
    
    return {"answer": result.answer}
