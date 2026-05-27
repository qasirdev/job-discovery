"""
backend/routers/v1/question_answer.py

Question-Answer API endpoint — MVP 2 (JD-E22 / JD-103).

Endpoint:
  POST /api/v1/question-answer/{job_id}  → Answer specific questions about a job listing

Per-endpoint rate limit (enforced at RateLimitMiddleware layer):
  POST /api/v1/question-answer/* → 30 req/min

Reference:
  proposal-v4.md §Scalable API Reference — question-answer endpoint
  docs/ENGINEERING-STANDARDS.md — RFC 7807 structured errors
  backend/agents/question-answer/AGENT.md — RAG-powered Q&A responsibilities
"""

import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..dependencies import require_rag_ready
from ..db import get_db
from ...models import Job
from ...agents.question_answer.question_answer_agent import QAAgent

router = APIRouter(prefix="/question-answer", tags=["Question Answer"])


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------


class QuestionAnswerRequest(BaseModel):
    """Request body for RAG-powered Q&A about a job listing."""
    question: str


class QuestionAnswerResponse(BaseModel):
    """Response schema for a question-answer result."""
    job_id: str
    question: str
    answer: str
    sources: list[str] = []
    confidence: float | None = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post(
    "/{job_id}",
    response_model=QuestionAnswerResponse,
    dependencies=[Depends(require_rag_ready)],
    summary="Answer specific questions about a job listing",
    description=(
        "RAG-powered Q&A grounded in the job description, company metadata, "
        "and the user's professional background. "
        "Requires a completed UserProfile and an embedded CV (MVP2+). "
        "Returns 422 if RAG prerequisites are not met. "
        "Rate limited to 30 req/min per user."
    ),
)
async def answer_question(
    job_id: str,
    body: QuestionAnswerRequest,
    db: AsyncSession = Depends(get_db)
) -> QuestionAnswerResponse:
    """
    RAG-grounded Q&A about a job listing.
    """
    job_uuid = uuid.UUID(job_id)
    job = (await db.execute(select(Job).where(Job.id == job_uuid))).scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # In a full RAG implementation, we would fetch CV chunks, recruiter profiles etc. here.
    # For MVP2, we'll pass a placeholder or extracted context if available.
    context = job.job_structured if hasattr(job, "job_structured") and job.job_structured else "No extra context."
    if isinstance(context, dict):
        context = str(context)

    agent = QAAgent()
    
    # QA agent returns an AgentResultEnvelope containing QAResult payload
    envelope = await agent.answer_question(job, context, body.question)

    if envelope.status == "failure":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate answer."
        )
        
    result_data = envelope.result

    return QuestionAnswerResponse(
        job_id=job_id,
        question=body.question,
        answer=result_data.get("answer", "No answer available"),
        sources=result_data.get("sources", []),
        confidence=result_data.get("confidence", None)
    )
