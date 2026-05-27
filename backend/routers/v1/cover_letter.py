"""
backend/routers/v1/cover_letter.py

Cover Letter API endpoints — MVP 2 (JD-E22 / JD-103).

Endpoints:
  POST   /api/v1/cover-letter/{job_id}          → Generate tailored cover letter
  GET    /api/v1/cover-letter/{job_id}           → Retrieve generated cover letter status/content
  GET    /api/v1/cover-letter/{job_id}/export    → Download cover letter as PDF or Markdown

Per-endpoint rate limit (enforced at RateLimitMiddleware layer):
  POST /api/v1/cover-letter/* → 20 req/min

Reference:
  proposal-v4.md §Scalable API Reference — cover letter endpoints
  proposal-v4.md — cover letter click stream
  docs/ENGINEERING-STANDARDS.md — RFC 7807 structured errors
"""

import uuid
from typing import Literal
import markdown
from weasyprint import HTML

from fastapi import APIRouter, Depends, HTTPException, Query, status, BackgroundTasks
from fastapi.responses import Response
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import require_rag_ready
from ..db import get_db
from ...models import CoverLetter, Job
from ...agents.cover_letter.cover_letter_agent import CoverLetterAgent
from ...settings import get_settings

router = APIRouter(prefix="/cover-letter", tags=["Cover Letter"])


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------


class CoverLetterRequest(BaseModel):
    """Request body for cover letter generation. Currently job_id is path param."""
    pass


class CoverLetterResponse(BaseModel):
    """Response schema for generated cover letter."""
    id: str
    job_id: str
    user_id: str
    status: Literal["pending", "generating", "ready", "failed"]
    content: str | None = None
    ats_score: float | None = None
    generated_at: str | None = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post(
    "/{job_id}",
    response_model=CoverLetterResponse,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(require_rag_ready)],
    summary="Generate tailored cover letter",
    description=(
        "Triggers cover letter generation for the given job. "
        "Requires a completed UserProfile and an embedded CV (MVP2+). "
        "Returns 422 if RAG prerequisites are not met. "
        "Rate limited to 20 req/min per user."
    ),
)
async def generate_cover_letter(job_id: str, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)) -> CoverLetterResponse:
    """
    Triggers cover letter generation asynchronously.
    Returns status="pending" immediately for the frontend to poll.
    """
    user_id = uuid.UUID(get_settings().single_user_id)
    job_uuid = uuid.UUID(job_id)

    # 1. Validate job_id exists
    job = (await db.execute(select(Job).where(Job.id == job_uuid))).scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # 2. Check if a CoverLetter already exists
    cl = (await db.execute(select(CoverLetter).where(CoverLetter.job_id == job_uuid))).scalar_one_or_none()
    
    if cl and cl.status == "generating":
        return CoverLetterResponse(
            id=str(cl.id),
            job_id=job_id,
            user_id=str(user_id),
            status=cl.status.value,
            content=cl.content,
            ats_score=cl.ats_score,
            generated_at=cl.created_at.isoformat() if cl.created_at else None,
        )

    # We will let the CoverLetterAgent handle the DB record creation/updating
    agent = CoverLetterAgent(db=db)
    
    # 3. Trigger async generation
    background_tasks.add_task(agent.generate, job_uuid, user_id)

    return CoverLetterResponse(
        id=str(cl.id) if cl else str(uuid.uuid4()),
        job_id=job_id,
        user_id=str(user_id),
        status="pending",
        content=None,
        ats_score=None,
        generated_at=None,
    )


@router.get(
    "/{job_id}",
    response_model=CoverLetterResponse,
    summary="Retrieve cover letter status and content",
    description=(
        "Poll this endpoint to check cover letter generation status. "
        "Returns content once status = 'ready'. "
        "Returns 404 if no cover letter exists for this job."
    ),
)
async def get_cover_letter(job_id: str, db: AsyncSession = Depends(get_db)) -> CoverLetterResponse:
    """
    Returns the current status of the cover letter.
    """
    job_uuid = uuid.UUID(job_id)
    cl = (await db.execute(select(CoverLetter).where(CoverLetter.job_id == job_uuid))).scalar_one_or_none()
    
    if not cl:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": 404,
                "detail": f"No cover letter found for job {job_id}. "
                          "Generate one first via POST /api/v1/cover-letter/{job_id}.",
            },
        )

    return CoverLetterResponse(
        id=str(cl.id),
        job_id=job_id,
        user_id=str(cl.user_id) if hasattr(cl, "user_id") else get_settings().single_user_id,
        status=cl.status.value if hasattr(cl.status, "value") else cl.status,
        content=cl.content,
        ats_score=cl.ats_score,
        generated_at=cl.created_at.isoformat() if cl.created_at else None,
    )


@router.get(
    "/{job_id}/export",
    summary="Export cover letter as PDF or Markdown",
    description=(
        "Download the generated cover letter. "
        "Query param: format=pdf | format=markdown. "
        "Returns binary PDF or plain Markdown. "
        "Returns 404 if no cover letter exists. "
        "Returns 422 if cover letter status is not 'ready'. "
        "On 422, frontend must NOT retry — invalidate the query cache and re-render."
    ),
)
async def export_cover_letter(
    job_id: str,
    format: Literal["pdf", "markdown"] = Query(
        default="pdf",
        description="Export format: 'pdf' returns application/pdf, 'markdown' returns text/markdown.",
    ),
    db: AsyncSession = Depends(get_db),
) -> Response:
    """
    Export the cover letter for download.
    """
    job_uuid = uuid.UUID(job_id)
    cl = (await db.execute(select(CoverLetter).where(CoverLetter.job_id == job_uuid))).scalar_one_or_none()
    
    if not cl:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": 404,
                "detail": f"No cover letter found for job {job_id}.",
            },
        )
        
    cl_status = cl.status.value if hasattr(cl.status, "value") else cl.status
    if cl_status != "ready" or not cl.content:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "type": "about:blank",
                "title": "Unprocessable Entity",
                "status": 422,
                "detail": "Cover letter is no longer available. Please regenerate it.",
            },
        )

    if format == "markdown":
        return Response(
            content=cl.content,
            media_type="text/markdown",
            headers={"Content-Disposition": f'attachment; filename="cover_letter_{job_id}.md"'}
        )
    else:
        # Generate PDF
        html_content = f"<html><body>{markdown.markdown(cl.content)}</body></html>"
        pdf_bytes = HTML(string=html_content).write_pdf()
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="cover_letter_{job_id}.pdf"'}
        )
