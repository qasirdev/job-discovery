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

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..dependencies import require_rag_ready

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
) -> QuestionAnswerResponse:
    """
    MVP 2 stub: Question Answer Agent is defined but not yet active.

    In MVP 2, this will:
    1. Validate job_id exists in the jobs table.
    2. Route the question through the RAG Agent to retrieve relevant context
       from CV, company metadata, and job_structured JSONB.
    3. Pass retrieved context to the Question Answer Agent for synthesis.
    4. Return the answer with source citations and confidence score.

    Reasoning effort: high (RAG-grounded retrieval and synthesis).
    """
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail={
            "type": "about:blank",
            "title": "Service Unavailable",
            "status": 503,
            "detail": (
                "Question Answer Agent is not yet active. "
                "This feature will be available in MVP 2."
            ),
        },
    )
