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
from ...models import Job, InterviewPrep, InterviewQuestion
from ...agents.question_answer.question_answer_agent import QAAgent

router = APIRouter(prefix="/question-answer", tags=["Question Answer"])

class QuestionAnswerRequest(BaseModel):
    question: str

class QuestionAnswerResponse(BaseModel):
    job_id: str
    question: str
    answer: str
    sources: list[str] = []
    confidence: float | None = None

@router.post(
    "/{job_id}",
    response_model=QuestionAnswerResponse,
    dependencies=[Depends(require_rag_ready)],
    summary="Answer specific questions about a job listing",
)
async def answer_question(
    job_id: str,
    body: QuestionAnswerRequest,
    db: AsyncSession = Depends(get_db)
) -> QuestionAnswerResponse:
    job_uuid = uuid.UUID(job_id)
    job = (await db.execute(select(Job).where(Job.id == job_uuid))).scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    context = job.job_structured if hasattr(job, "job_structured") and job.job_structured else "No extra context."
    if isinstance(context, dict):
        context = str(context)

    iqs = (await db.execute(select(InterviewQuestion).where(InterviewQuestion.job_id == job.id))).scalars().all()
    if iqs:
        questions_formatted = []
        for q in iqs:
            questions_formatted.append(f"Q: {q.question_text}\nDifficulty: {q.difficulty_rating}\nSuggested Answer: {q.suggested_answer or 'None'}")
        context += f"\n\nInterview Question Bank:\n" + "\n\n".join(questions_formatted)
    else:
        ip = (await db.execute(select(InterviewPrep).where(InterviewPrep.job_id == job.id))).scalar_one_or_none()
        if ip and ip.questions:
            context += f"\n\nInterview Question Bank:\n{ip.questions}"

    agent = QAAgent()
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
