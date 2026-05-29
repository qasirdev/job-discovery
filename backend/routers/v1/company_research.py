from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...db import get_db
from ...models import CompanyResearch

router = APIRouter(prefix="/api/v1/company-research", tags=["Company Research"])

class CompanyResearchResponse(BaseModel):
    id: UUID
    company_name_slug: str
    research_data: Dict[str, Any]
    sentiment_score: Optional[float] = None
    funding_stage: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    culture_signals: Optional[str] = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="forbid")

@router.get("", response_model=CompanyResearchResponse)
async def get_company_research(
    company_slug: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Fetches company research data by company_name_slug.
    Idempotent — if a fresh record already exists, returns 200 with the existing record.
    """
    stmt = select(CompanyResearch).where(CompanyResearch.company_name_slug == company_slug)
    result = await db.execute(stmt)
    research = result.scalar_one_or_none()
    
    if not research:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company research not found"
        )
        
    if not research.research_data:
        research.research_data = {}
        
    return CompanyResearchResponse.model_validate(research)
