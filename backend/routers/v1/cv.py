from fastapi import APIRouter, HTTPException, UploadFile, File, status, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ...logging_config import get_logger
from ...db import get_db
from ...models import UserProfile as DBUserProfile
from ...settings import get_settings
from ...schemas import RFC7807Error

logger = get_logger(__name__)
router = APIRouter(prefix="/cv", tags=["CV"])

class CVStatus(BaseModel):
    embedding_status: str = Field(examples=["pending"])
    message: str = Field(examples=["CV received. Embedding available from MVP 2."])

class CVUploadResponse(BaseModel):
    filename: str = Field(examples=["resume.pdf"])
    status: str = Field(examples=["received"])

@router.post(
    "/",
    response_model=CVUploadResponse,
    summary="Upload CV",
    description="Upload a CV document.",
    responses={
        422: {"model": RFC7807Error, "description": "Validation Error"}
    }
)
async def upload_cv(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    """
    Upload a CV document.
    """
    if not file.filename or (not file.filename.endswith('.pdf') and not file.filename.endswith('.docx')):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "type": "about:blank",
                "title": "Unprocessable Entity",
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "detail": "Only PDF or DOCX allowed"
            }
        )
    
    user_id = get_settings().single_user_id
    query = select(DBUserProfile).where(DBUserProfile.id == user_id)
    result = await db.execute(query)
    db_profile = result.scalar_one_or_none()
    
    if db_profile:
        db_profile.cv_filename = file.filename
        await db.commit()
    else:
        logger.warning("CV uploaded but no profile found to attach it to.")
        
    return CVUploadResponse(filename=file.filename, status="received")

@router.get(
    "/status",
    response_model=CVStatus,
    summary="Get CV status",
    description="Get the status of the CV embedding process."
)
async def get_cv_status():
    """
    Get the status of the CV embedding process.
    """
    return CVStatus(
        embedding_status="pending",
        message="CV received. Embedding available from MVP 2."
    )
