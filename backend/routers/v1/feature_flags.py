from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ...settings import get_settings, AppSettings

router = APIRouter(prefix="/feature-flags", tags=["Feature Flags"])

class FeatureFlagsResponse(BaseModel):
    feature_interview_prep: bool
    feature_application_assistant: bool
    feature_admin_panel: bool
    feature_ranking_agent: bool
    feature_cover_letter_agent: bool
    feature_question_answer_agent: bool
    feature_scraper_reed: bool
    feature_serverless_ranking: bool

@router.get("/", response_model=FeatureFlagsResponse)
async def get_flags(settings: AppSettings = Depends(get_settings)):
    return FeatureFlagsResponse(
        feature_interview_prep=settings.feature_interview_prep_agent,
        feature_application_assistant=settings.feature_application_assistant_agent,
        # Default to false for UI features unless there's a setting for it
        feature_admin_panel=False,
        feature_ranking_agent=settings.feature_ranking_agent,
        feature_cover_letter_agent=settings.feature_cover_letter_agent,
        feature_question_answer_agent=settings.feature_question_answer_agent,
        feature_scraper_reed=False,
        feature_serverless_ranking=False
    )

