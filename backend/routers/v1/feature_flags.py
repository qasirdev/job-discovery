from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/feature-flags", tags=["Feature Flags"])

class FeatureFlagsResponse(BaseModel):
    feature_interview_prep: bool
    feature_admin_panel: bool

    feature_ranking_agent: bool
    feature_cover_letter_agent: bool
    feature_question_answer_agent: bool
    feature_scraper_reed: bool
    feature_serverless_ranking: bool

@router.get("/", response_model=FeatureFlagsResponse)
async def get_flags():
    return FeatureFlagsResponse(
        feature_interview_prep=False,
        feature_admin_panel=False,
        feature_ranking_agent=False,
        feature_cover_letter_agent=False,
        feature_question_answer_agent=False,
        feature_scraper_reed=False,
        feature_serverless_ranking=False
    )
