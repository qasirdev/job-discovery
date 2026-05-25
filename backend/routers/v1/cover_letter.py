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

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response
from pydantic import BaseModel

from ..dependencies import require_rag_ready

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
async def generate_cover_letter(job_id: str) -> CoverLetterResponse:
    """
    MVP 2 stub: Cover Letter Agent is defined but generation pipeline is not yet active.

    In MVP 2, this will:
    1. Validate job_id exists in the jobs table.
    2. Parse job description into job_structured via the Ranking Agent.
    3. Submit a Temporal workflow to the Cover Letter Agent.
    4. Return status="pending" immediately for the frontend to poll.

    ATS keyword match >= 60% is enforced by the Cover Letter Agent before delivery.
    """
    # MVP 2 stub — returns a pending cover letter object.
    # In MVP 2 this will trigger an async Temporal workflow.
    return CoverLetterResponse(
        id=str(uuid.uuid4()),
        job_id=job_id,
        user_id="00000000-0000-0000-0000-000000000000",
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
async def get_cover_letter(job_id: str) -> CoverLetterResponse:
    """
    MVP 2 stub: returns a simulated ready cover letter for the given job.

    In MVP 2, this will query the CoverLetter table by (job_id, user_id).
    Frontend polls this at 5-second intervals until status = "ready".
    """
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
) -> Response:
    """
    Export the cover letter for download.

    Behaviour:
    - 200: binary response with appropriate Content-Type and Content-Disposition headers.
    - 404: no CoverLetter row exists for this job_id.
    - 422: CoverLetter status is not "ready" — letter is not exportable.

    Frontend handling per proposal-v4.md:
    - On 422: show toast "Cover letter is no longer available. Please regenerate it."
              Do NOT offer a retry.
              Call queryClient.invalidateQueries(['cover-letter', job_id]).
    - On 500/network error: show toast "Download failed. Please try again."
                            Restore button to normal state (no spinner).
    """
    # MVP 2 stub — no CoverLetter records exist yet
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "type": "about:blank",
            "title": "Not Found",
            "status": 404,
            "detail": f"No cover letter found for job {job_id}.",
        },
    )
