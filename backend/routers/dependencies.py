"""
backend/routers/dependencies.py

Reusable FastAPI dependencies — MVP 1.1+.

require_rag_ready: enforces at the API layer that the user has:
  1. A completed UserProfile
  2. An uploaded CV
  3. A CV with embedding_status = "ready"

Raises HTTP 422 for each unmet condition, per proposal-v4.md §Prerequisite Guard Middleware.

Reference: proposal-v4.md, infrastructure/AGENT.md.
"""

import jwt
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import get_db
from ..models import CV, UserProfile
from ..settings import get_settings


async def require_admin_claim(authorization: str = Header(None)) -> None:
    """Verify that the JWT contains an admin claim."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin claim required")
    token = authorization.split("Bearer ")[1]
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        if not decoded.get("admin", False):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin claim required")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin claim required")


async def require_rag_ready(db: AsyncSession = Depends(get_db)) -> None:
    """
    FastAPI dependency that enforces the RAG readiness prerequisite.

    Raises HTTP 422 (Unprocessable Entity) for each of three unmet conditions:
      1. UserProfile not found — user has not completed onboarding.
      2. CV not uploaded — no CV row exists for this user.
      3. CV embedding not ready — embedding_status is not "ready".

    Applied to:
      POST /api/v1/cover-letter/{job_id}
      POST /api/v1/interview-prep/{job_id}

    Reference: proposal-v4.md §Prerequisite Guard Middleware
    """
    user_id = get_settings().single_user_id

    # ── Guard 1: UserProfile must exist ──────────────────────────────────────
    profile_query = select(UserProfile).where(UserProfile.id == user_id)
    profile_result = await db.execute(profile_query)
    if not profile_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "type": "about:blank",
                "title": "Unprocessable Entity",
                "status": 422,
                "detail": "UserProfile not found. Complete onboarding before generating content.",
            },
        )

    # ── Guard 2: CV must exist ────────────────────────────────────────────────
    cv_query = select(CV).where(CV.user_id == user_id)
    cv_result = await db.execute(cv_query)
    cv = cv_result.scalar_one_or_none()

    if not cv:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "type": "about:blank",
                "title": "Unprocessable Entity",
                "status": 422,
                "detail": "CV not uploaded. Upload your CV before generating content.",
            },
        )

    # ── Guard 3: embedding_status must be "ready" ─────────────────────────────
    if cv.embedding_status != "ready":
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "type": "about:blank",
                "title": "Unprocessable Entity",
                "status": 422,
                "detail": (
                    f"CV embedding not ready (status: {cv.embedding_status}). "
                    "Wait for processing to complete."
                ),
            },
        )
