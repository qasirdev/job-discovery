from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/company-research", tags=["Company Research"])

class CompanyResearchModel(BaseModel):
    id: str
    company_name_slug: str
    research_data: dict
    updated_at: datetime

# In-memory store for MVP
FAKE_COMPANY_RESEARCH = {
    "techcorp": CompanyResearchModel(
        id="c1",
        company_name_slug="techcorp",
        research_data={"funding": "Series A", "tech_stack": ["Python", "React"]},
        updated_at=datetime.utcnow()
    )
}

@router.get("")
async def get_company_research(company_slug: str):
    # Idempotent — if a fresh record already exists, returns 200 with the existing record.
    if company_slug in FAKE_COMPANY_RESEARCH:
        return {
            "status": "success",
            "company_slug": company_slug,
            "data": FAKE_COMPANY_RESEARCH[company_slug].dict()
        }
    
    # If it doesn't exist, in a real implementation this would trigger the research agent.
    # For now, return a placeholder or empty data.
    return {
        "status": "success",
        "company_slug": company_slug,
        "data": {}
    }
