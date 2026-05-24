from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from pydantic import BaseModel
from ...schemas import UserProfile
from ...logging_config import get_logger
from ...db import get_db
from ...models import UserProfile as DBUserProfile

logger = get_logger(__name__)
router = APIRouter(prefix="/profile", tags=["Profile"])

SINGLE_USER_ID = "00000000-0000-0000-0000-000000000000"

@router.get("/", response_model=UserProfile)
async def get_profile(db: AsyncSession = Depends(get_db)):
    query = select(DBUserProfile).where(DBUserProfile.id == SINGLE_USER_ID)
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

@router.post("/", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
async def create_profile(profile: UserProfile, db: AsyncSession = Depends(get_db)):
    query = select(DBUserProfile).where(DBUserProfile.id == SINGLE_USER_ID)
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
        id=SINGLE_USER_ID,
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

@router.patch("/", response_model=UserProfile)
async def update_profile(profile_update: dict, db: AsyncSession = Depends(get_db)):
    query = select(DBUserProfile).where(DBUserProfile.id == SINGLE_USER_ID)
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
