from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/feature-flags", tags=["Feature Flags"])

class FeatureFlagsResponse(BaseModel):
    feature_interview_prep: bool
    feature_admin_panel: bool

@router.get("/", response_model=FeatureFlagsResponse)
async def get_flags():
    return FeatureFlagsResponse(
        feature_interview_prep=False,
        feature_admin_panel=False
    )
