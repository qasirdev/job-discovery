from fastapi import APIRouter, HTTPException, status
from ...schemas import UserProfile
from ...logging_config import get_logger
from pydantic import BaseModel

logger = get_logger(__name__)
router = APIRouter(prefix="/profile", tags=["Profile"])

# Mock DB for profiles
profiles_db: dict[str, UserProfile] = {}
SINGLE_USER_ID = "00000000-0000-0000-0000-000000000000"

@router.get("/", response_model=UserProfile)
async def get_profile():
    if SINGLE_USER_ID not in profiles_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": status.HTTP_404_NOT_FOUND,
                "detail": "Profile not found"
            }
        )
    return profiles_db[SINGLE_USER_ID]

@router.post("/", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
async def create_profile(profile: UserProfile):
    if SINGLE_USER_ID in profiles_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "type": "about:blank",
                "title": "Conflict",
                "status": status.HTTP_409_CONFLICT,
                "detail": "Profile already exists"
            }
        )
    profile.id = SINGLE_USER_ID
    profiles_db[SINGLE_USER_ID] = profile
    return profile

@router.patch("/", response_model=UserProfile)
async def update_profile(profile_update: dict):
    if SINGLE_USER_ID not in profiles_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": status.HTTP_404_NOT_FOUND,
                "detail": "Profile not found"
            }
        )
    
    current = profiles_db[SINGLE_USER_ID]
    update_data = profile_update
    
    for k, v in update_data.items():
        if hasattr(current, k):
            setattr(current, k, v)
            
    return current
