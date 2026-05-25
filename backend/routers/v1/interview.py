from fastapi import APIRouter, HTTPException, Depends
from ..dependencies import require_rag_ready

router = APIRouter(prefix="/interview-prep", tags=["Interview Prep"])

@router.post("/{job_id}", dependencies=[Depends(require_rag_ready)])
async def generate_interview_prep(job_id: str):
    raise HTTPException(status_code=503, detail="Interview Preparation Agent is not fully active yet")
