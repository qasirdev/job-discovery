from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from ...db import get_db
from ...models import Recruiter, InteractionEvent

router = APIRouter(prefix="/api/v1/recruiters", tags=["Recruiters"])

class RecruiterBase(BaseModel):
    name: str
    company: str
    email: Optional[str] = None
    linkedin_url: Optional[str] = None
    interaction_score: int = 0
    notes: Optional[str] = None

class RecruiterResponse(RecruiterBase):
    id: UUID
    created_at: datetime

class RecruiterUpsert(BaseModel):
    name: str
    company: str
    email: Optional[str] = None
    linkedin_url: Optional[str] = None

class RecruiterPatch(BaseModel):
    notes: str

class InteractionEventCreate(BaseModel):
    event_type: str
    notes: Optional[str] = None

@router.get("", response_model=List[RecruiterResponse])
async def list_recruiters(db: AsyncSession = Depends(get_db)):
    """
    Fetch list of recruiters.
    """
    result = await db.execute(select(Recruiter).order_by(Recruiter.created_at.desc()))
    return result.scalars().all()

@router.post("", response_model=Optional[RecruiterResponse])
async def upsert_recruiter(recruiter: RecruiterUpsert, db: AsyncSession = Depends(get_db)):
    """
    Upsert endpoint with linkedin_url deduplication rules.
    Deduplication edge case: If linkedin_url is absent from the scraped data, 
    the recruiter record is skipped (not created with a null key).
    """
    if not recruiter.linkedin_url:
        return None
    
    stmt = insert(Recruiter).values(
        name=recruiter.name,
        company=recruiter.company,
        email=recruiter.email,
        linkedin_url=recruiter.linkedin_url
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=['linkedin_url'],
        set_=dict(
            name=stmt.excluded.name,
            company=stmt.excluded.company,
            email=stmt.excluded.email
        )
    ).returning(Recruiter)
    
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()

@router.patch("/{id}", response_model=RecruiterResponse)
async def update_recruiter_notes(id: UUID, update_data: RecruiterPatch, db: AsyncSession = Depends(get_db)):
    """
    Update notes for a specific recruiter.
    """
    stmt = update(Recruiter).where(Recruiter.id == id).values(notes=update_data.notes).returning(Recruiter)
    result = await db.execute(stmt)
    updated = result.scalar_one_or_none()
    if not updated:
        raise HTTPException(status_code=404, detail="Recruiter not found")
    await db.commit()
    return updated

@router.post("/{id}/interaction", status_code=status.HTTP_201_CREATED)
async def log_interaction(id: UUID, interaction: InteractionEventCreate, db: AsyncSession = Depends(get_db)):
    """
    Log interactions for a specific recruiter.
    """
    recruiter = (await db.execute(select(Recruiter).where(Recruiter.id == id))).scalar_one_or_none()
    if not recruiter:
        raise HTTPException(status_code=404, detail="Recruiter not found")
        
    event = InteractionEvent(
        recruiter_id=id,
        event_type=interaction.event_type,
        notes=interaction.notes
    )
    db.add(event)
    
    # Optional: Update interaction score logic
    recruiter.interaction_score += 1
    
    await db.commit()
    return {"status": "success", "event_id": event.id}
