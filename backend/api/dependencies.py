from fastapi import HTTPException
from .v1.profile import profiles_db, SINGLE_USER_ID

async def require_rag_ready() -> None:
    # 1. Check if UserProfile exists
    if SINGLE_USER_ID not in profiles_db:
        raise HTTPException(
            status_code=422,
            detail={
                "type": "profile_required",
                "title": "Profile not set up",
                "status": 422,
                "detail": "Complete your profile before using this feature"
            }
        )
    
    # 2. Check CV embedding_status
    # In MVP 1, CV embedding_status is hardcoded to 'pending' in get_cv_status
    # so we enforce it here as per JD-36b spec.
    embedding_status = 'pending' # Stub for MVP 1
    
    if embedding_status != 'ready':
        raise HTTPException(
            status_code=422,
            detail={
                "type": "cv_not_ready",
                "title": "CV not processed",
                "status": 422,
                "detail": "Upload and process your CV to enable this feature"
            }
        )
