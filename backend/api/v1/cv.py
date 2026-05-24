from fastapi import APIRouter, HTTPException, UploadFile, File, status
from pydantic import BaseModel, Field
from ...logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/cv", tags=["CV"])

class CVStatus(BaseModel):
    embedding_status: str = Field(examples=["pending"])
    message: str = Field(examples=["CV received. Embedding available from MVP 2."])

@router.post("/")
async def upload_cv(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf') and not file.filename.endswith('.docx'):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "type": "about:blank",
                "title": "Unprocessable Entity",
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "detail": "Only PDF or DOCX allowed"
            }
        )
    
    return {"filename": file.filename, "status": "received"}

@router.get("/status", response_model=CVStatus)
async def get_cv_status():
    return CVStatus(
        embedding_status="pending",
        message="CV received. Embedding available from MVP 2."
    )
