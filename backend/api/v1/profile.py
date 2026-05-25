from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from pydantic import BaseModel
from ...schemas import UserProfile, RFC7807Error
from ...logging_config import get_logger
from ...db import get_db
from ...models import UserProfile as DBUserProfile

logger = get_logger(__name__)
router = APIRouter(prefix="/profile", tags=["Profile"])

from ...settings import get_settings

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
