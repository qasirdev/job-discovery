from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/recruiters", tags=["Recruiters"])

class RecruiterModel(BaseModel):
    id: str
    name: str
    company: str
    email: Optional[str] = None
    quality_score: int = 0
    notes: Optional[str] = ""

class RecruiterUpdate(BaseModel):
    notes: Optional[str] = None

# In-memory store for MVP1
FAKE_RECRUITERS = {
    "r1": RecruiterModel(id="r1", name="Sarah Jenkins", company="TechTalent Partners", email="sarah.j@techtalent.com", quality_score=6, notes="Specialises in Python roles."),
    "r2": RecruiterModel(id="r2", name="Mark Roberts", company="Global Hire", email="mroberts@globalhire.net", quality_score=4, notes="Sent a few irrelevant roles recently.")
}

@router.get("/", response_model=List[RecruiterModel])
async def list_recruiters():
    return list(FAKE_RECRUITERS.values())

@router.post("/{id}/interaction")
async def log_interaction(id: str):
    if id not in FAKE_RECRUITERS:
        raise HTTPException(status_code=404, detail="Recruiter not found")
    
    recruiter = FAKE_RECRUITERS[id]
    recruiter.quality_score = min(10, recruiter.quality_score + 1)
    return recruiter

@router.patch("/{id}")
async def update_recruiter(id: str, update_data: RecruiterUpdate):
    if id not in FAKE_RECRUITERS:
        raise HTTPException(status_code=404, detail="Recruiter not found")
    
    recruiter = FAKE_RECRUITERS[id]
    if update_data.notes is not None:
        recruiter.notes = update_data.notes
    return recruiter
