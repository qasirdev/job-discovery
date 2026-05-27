from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

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
async def list_recruiters():
    """
    Fetch list of recruiters.
    """
    # TODO: Implement DB fetch
    return []

@router.post("", response_model=Optional[RecruiterResponse])
async def upsert_recruiter(recruiter: RecruiterUpsert):
    """
    Upsert endpoint with linkedin_url deduplication rules.
    Deduplication edge case: If linkedin_url is absent from the scraped data, 
    the recruiter record is skipped (not created with a null key).
    """
    if not recruiter.linkedin_url:
        # Skip creation when linkedin_url is null
        return None
    
    # TODO: Implement DB upsert logic (insert or update on conflict by linkedin_url)
    pass

@router.patch("/{id}", response_model=RecruiterResponse)
async def update_recruiter_notes(id: UUID, update_data: RecruiterPatch):
    """
    Update notes for a specific recruiter.
    """
    # TODO: Implement DB update logic for notes
    pass

@router.post("/{id}/interaction", status_code=status.HTTP_201_CREATED)
async def log_interaction(id: UUID, interaction: InteractionEventCreate):
    """
    Log interactions for a specific recruiter.
    """
    # TODO: Implement DB insert into InteractionEvent table linking recruiter_id
    pass
