from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from ..models import UserProfile, CV
from ..settings import get_settings

async def require_rag_ready(db: AsyncSession = Depends(get_db)) -> None:
    # 1. Check if UserProfile exists in PostgreSQL
    user_id = get_settings().single_user_id
    query = select(UserProfile).where(UserProfile.id == user_id)
    result = await db.execute(query)
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=503,
            detail={
                "code": "profile_not_ready",
                "message": "Please complete your profile before using this feature."
            }
        )
    
    # 2. Check CV embedding_status (must be ready)
    cv_query = select(CV).where(CV.user_id == user_id)
    cv_result = await db.execute(cv_query)
    cv = cv_result.scalar_one_or_none()
    
    # Order matters: we need to check if the CV exists, and if it's ready.
    if not cv:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "cv_not_ready",
                "message": "CV embedding is not yet available. Please upload your CV and wait for processing to complete."
            }
        )
