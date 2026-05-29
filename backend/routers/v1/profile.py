from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ...schemas import UserProfile, RFC7807Error
from ...logging_config import get_logger
from ...db import get_db
from ...models import UserProfile as DBUserProfile
from ...settings import get_settings

logger = get_logger(__name__)
router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get(
    "/export",
    summary="Export user data (GDPR Right to Data Portability)",
    description="Returns a full JSON archive of user profile, saved jobs, cover letters, and application history."
)
async def export_profile_data(db: AsyncSession = Depends(get_db)):
    user_id = get_settings().single_user_id
    
    # Fetch profile
    profile_query = select(DBUserProfile).where(DBUserProfile.id == user_id)
    profile_result = await db.execute(profile_query)
    profile = profile_result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    # We need to import the other models first
    from ...models import Application, CoverLetter, CV, SavedJob
    
    # Fetch applications
    app_query = select(Application).where(Application.user_id == user_id)
    app_result = await db.execute(app_query)
    applications = app_result.scalars().all()
    
    # Fetch cover letters
    cl_query = select(CoverLetter).where(CoverLetter.user_id == user_id)
    cl_result = await db.execute(cl_query)
    cover_letters = cl_result.scalars().all()
    
    # Fetch CVs
    cv_query = select(CV).where(CV.user_id == user_id)
    cv_result = await db.execute(cv_query)
    cvs = cv_result.scalars().all()
    
    # Fetch saved jobs (since it's single user, we just fetch all)
    sj_query = select(SavedJob)
    sj_result = await db.execute(sj_query)
    saved_jobs = sj_result.scalars().all()
    
    logger.info(f"GDPR Export requested for user_id={user_id}")
    
    return {
        "profile": UserProfile.model_validate(profile).model_dump() if profile else None,
        "applications": [{"id": str(a.id), "job_id": str(a.job_id), "status": a.status, "applied_at": a.applied_at.isoformat() if a.applied_at else None, "notes": a.notes} for a in applications],
        "cover_letters": [{"id": str(cl.id), "job_id": str(cl.job_id), "status": cl.status, "content": cl.content, "created_at": cl.created_at.isoformat()} for cl in cover_letters],
        "cvs": [{"id": str(cv.id), "filename": cv.filename, "created_at": cv.created_at.isoformat()} for cv in cvs],
        "saved_jobs": [{"job_id": str(sj.job_id), "saved_at": sj.saved_at.isoformat()} for sj in saved_jobs]
    }

@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user data (GDPR Right to Erasure)",
    description="Soft deletes the user profile and cascade deletes associated PII."
)
async def delete_profile(db: AsyncSession = Depends(get_db)):
    user_id = get_settings().single_user_id
    
    profile_query = select(DBUserProfile).where(DBUserProfile.id == user_id)
    profile_result = await db.execute(profile_query)
    profile = profile_result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    from ...models import Application, CoverLetter, CV, SavedJob
    
    # Soft delete / anonymize profile
    profile.full_name = "Anonymized User"
    profile.email = "anonymized@example.com"
    profile.target_role = "Anonymized"
    profile.target_location = "Anonymized"
    profile.skills = []
    profile.cv_filename = None
    
    # Delete related data
    await db.execute(Application.__table__.delete().where(Application.user_id == user_id))
    await db.execute(CoverLetter.__table__.delete().where(CoverLetter.user_id == user_id))
    await db.execute(CV.__table__.delete().where(CV.user_id == user_id))
    await db.execute(SavedJob.__table__.delete()) # Single user model
    
    await db.commit()
    logger.info(f"GDPR Erasure completed for user_id={user_id}")
    return

@router.get(
    "/",
    response_model=UserProfile,
    summary="Get user profile",
    description="Retrieve the current user's profile.",
    responses={
        404: {"model": RFC7807Error, "description": "Profile not found"}
    }
)
async def get_profile(db: AsyncSession = Depends(get_db)):
    """
    Get the current user's profile.
    """
    user_id = get_settings().single_user_id
    query = select(DBUserProfile).where(DBUserProfile.id == user_id)
    result = await db.execute(query)
    db_profile = result.scalar_one_or_none()
    
    if not db_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": status.HTTP_404_NOT_FOUND,
                "detail": "Profile not found"
            }
        )
    return UserProfile.model_validate(db_profile)

@router.post(
    "/",
    response_model=UserProfile,
    status_code=status.HTTP_201_CREATED,
    summary="Create user profile",
    description="Create a new profile for the current user.",
    responses={
        409: {"model": RFC7807Error, "description": "Profile already exists"},
        422: {"model": RFC7807Error, "description": "Validation Error"}
    }
)
async def create_profile(profile: UserProfile, db: AsyncSession = Depends(get_db)):
    """
    Create a new profile for the current user.
    """
    user_id = get_settings().single_user_id
    query = select(DBUserProfile).where(DBUserProfile.id == user_id)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "type": "about:blank",
                "title": "Conflict",
                "status": status.HTTP_409_CONFLICT,
                "detail": "Profile already exists"
            }
        )
    
    db_profile = DBUserProfile(
        id=user_id,
        full_name=profile.full_name,
        email=profile.email,
        target_role=profile.target_role,
        target_location=profile.target_location,
        skills=profile.skills,
        years_experience=profile.years_experience,
        cv_filename=profile.cv_filename
    )
    db.add(db_profile)
    await db.commit()
    await db.refresh(db_profile)
    return UserProfile.model_validate(db_profile)

@router.patch(
    "/",
    response_model=UserProfile,
    summary="Update user profile",
    description="Update the current user's profile partially.",
    responses={
        404: {"model": RFC7807Error, "description": "Profile not found"},
        422: {"model": RFC7807Error, "description": "Validation Error"}
    }
)
async def update_profile(profile_update: dict, db: AsyncSession = Depends(get_db)):
    """
    Update the current user's profile partially.
    """
    user_id = get_settings().single_user_id
    query = select(DBUserProfile).where(DBUserProfile.id == user_id)
    result = await db.execute(query)
    db_profile = result.scalar_one_or_none()
    
    if not db_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": status.HTTP_404_NOT_FOUND,
                "detail": "Profile not found"
            }
        )
    
    for k, v in profile_update.items():
        if hasattr(db_profile, k) and k not in ("id", "created_at"):
            setattr(db_profile, k, v)
            
    await db.commit()
    await db.refresh(db_profile)
    return UserProfile.model_validate(db_profile)
