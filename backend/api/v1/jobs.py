from typing import List
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from pydantic import BaseModel, Field
from ...schemas import Job, JobListResponse
from ...logging_config import get_logger
from ...db import get_db
from ...repositories.job import JobRepo
from ...fake_db import load_db, save_db, get_jobs, get_job

logger = get_logger(__name__)
router: APIRouter = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("/", response_model=JobListResponse)
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
    
    all_jobs = get_jobs()
    linkedin_count = sum(1 for j in all_jobs if j.source.lower() == 'linkedin')
    jobserve_count = sum(1 for j in all_jobs if j.source.lower() == 'jobserve')
    
    page = 1
    
    return JobListResponse(
        total=len(all_jobs),
        page=page,
        page_size=page_size,
        has_next=next_cursor is not None,
        next_cursor=next_cursor,
        linkedin_count=linkedin_count,
        jobserve_count=jobserve_count,
        jobs=output_jobs
    )

@router.get("/saved", response_model=List[Job])
async def list_saved_jobs(repo: JobRepo):
    """
    List all saved jobs.
    """
    logger.info("Listing saved jobs")
    all_jobs = get_jobs()
    return [j for j in all_jobs if getattr(j, 'saved', False)]

@router.get("/{id}", response_model=Job)
async def get_job_endpoint(id: str = Path(...), repo: JobRepo = Depends()):
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

@router.post("/{id}/save", response_model=SaveResponse)
async def save_job(id: str = Path(...), repo: JobRepo = Depends()):
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
        
    db = load_db()
    if id in db:
        db[id]['saved'] = True
        save_db(db)
        
    return SaveResponse(saved=True)

@router.delete("/{id}/save", response_model=SaveResponse)
async def unsave_job(id: str = Path(...), repo: JobRepo = Depends()):
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
        
    db = load_db()
    if id in db:
        db[id]['saved'] = False
        save_db(db)
        
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

from ...agents.qa.qa_agent import QAAgent
from ...agents.rag.rag_agent import RAGAgent

class AskRequest(BaseModel):
    question: str = Field(examples=["Is this role fully remote?"])

@router.post("/{job_id}/ask")
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

    rag = RAGAgent()
    context = await rag.retrieve_context(job.description)

    qa = QAAgent()
    result = await qa.answer_question(job, context, request.question)
    
    return {"answer": result.answer}
