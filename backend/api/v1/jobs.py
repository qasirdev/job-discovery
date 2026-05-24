from typing import List
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from ...schemas import Job
from ...logging_config import get_logger
from ...db import get_db
from ...repositories.job import JobRepo

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


from fastapi import HTTPException
from ...agents.orchestrator.orchestrator_agent import OrchestratorAgent

@router.post("/{job_id}/process")
async def process_job(job_id: str, repo: JobRepo):
    """
    Trigger the AI Orchestrator Pipeline for a specific job.
    Includes Security Validation, Ranking, RAG, and Cover Letter generation.
    """
    job = await repo.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    orchestrator = OrchestratorAgent()
    result = await orchestrator.process_job(job)
    return result

from ...agents.qa.qa_agent import QAAgent
from ...agents.rag.rag_agent import RAGAgent

class AskRequest(BaseModel):
    question: str

@router.post("/{job_id}/ask")
async def ask_question(job_id: str, request: AskRequest, repo: JobRepo):
    """
    Ask a question about a specific job. Uses RAG context and the QA Agent.
    """
    job = await repo.get_job_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    rag = RAGAgent()
    context = await rag.retrieve_context(job.description)

    qa = QAAgent()
    result = await qa.answer_question(job, context, request.question)
    
    return {"answer": result.answer}
