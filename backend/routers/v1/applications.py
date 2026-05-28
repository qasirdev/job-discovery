from typing import List, Literal
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from ...schemas import Application, ApplicationWithJob, RFC7807Error
from ...models import Application as DBApplication, ApplicationStatus
from ...db import get_db
from ...logging_config import get_logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ...settings import get_settings

logger = get_logger(__name__)
router: APIRouter = APIRouter(prefix="/applications", tags=["Applications"])

class CreateApplicationRequest(BaseModel):
    job_id: UUID
    notes: str | None = None

class UpdateApplicationRequest(BaseModel):
    status: Literal["draft", "applied", "awaiting_response", "interviewing", "offered", "rejected", "withdrawn"] | None = None
    notes: str | None = None

@router.post(
    "/",
    response_model=Application,
    status_code=status.HTTP_201_CREATED,
    summary="Log a new application",
    description="Logs a new job application and ties it to the given job_id.",
    responses={
        409: {"model": RFC7807Error, "description": "Application already exists"},
        422: {"model": RFC7807Error, "description": "Validation Error"}
    }
)
async def create_application(req: CreateApplicationRequest, db: AsyncSession = Depends(get_db)):
    """
    Log a new application for a job.
    """
    logger.info(f"Logging application for job {req.job_id}")
    
    user_id = get_settings().single_user_id
    
    query = select(DBApplication).where(DBApplication.job_id == req.job_id, DBApplication.user_id == user_id)
    result = await db.execute(query)
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "type": "about:blank",
                "title": "Conflict",
                "status": status.HTTP_409_CONFLICT,
                "detail": "Application already logged for this job.",
                "existing_id": str(existing.id)
            }
        )

    new_app = DBApplication(
        job_id=req.job_id,
        user_id=user_id,
        status=ApplicationStatus("applied"),
        notes=req.notes
    )
    
    db.add(new_app)
    await db.flush()
    await db.refresh(new_app)
    
    return Application.model_validate(new_app)

@router.get(
    "/",
    response_model=List[ApplicationWithJob],
    summary="List applications",
    description="Retrieve all applications for the current user.",
)
async def get_applications(db: AsyncSession = Depends(get_db)):
    """
    Get all applications for the current user.
    """
    user_id = get_settings().single_user_id
    
    query = (
        select(DBApplication)
        .where(DBApplication.user_id == user_id)
        .options(selectinload(DBApplication.job))
        .order_by(DBApplication.created_at.desc())
    )
    
    result = await db.execute(query)
    apps = result.scalars().all()
    
    return [ApplicationWithJob.model_validate(app) for app in apps]

@router.get(
    "/{id}",
    response_model=ApplicationWithJob,
    summary="Get application",
    description="Retrieve a single application by ID.",
    responses={
        404: {"model": RFC7807Error, "description": "Application not found"}
    }
)
async def get_application(id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Get a single application by ID for the current user.
    """
    user_id = get_settings().single_user_id
    
    query = (
        select(DBApplication)
        .where(DBApplication.id == id, DBApplication.user_id == user_id)
        .options(selectinload(DBApplication.job))
    )
    
    result = await db.execute(query)
    app = result.scalar_one_or_none()
    
    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": status.HTTP_404_NOT_FOUND,
                "detail": "Application not found."
            }
        )
        
    return ApplicationWithJob.model_validate(app)

@router.patch(
    "/{id}",
    response_model=Application,
    summary="Update application",
    description="Update the status or notes of an existing application.",
    responses={
        404: {"model": RFC7807Error, "description": "Application not found"}
    }
)
async def update_application(id: UUID, req: UpdateApplicationRequest, db: AsyncSession = Depends(get_db)):
    """
    Update an application status or notes.
    """
    user_id = get_settings().single_user_id
    
    query = select(DBApplication).where(DBApplication.id == id, DBApplication.user_id == user_id)
    result = await db.execute(query)
    app = result.scalar_one_or_none()
    
    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "about:blank",
                "title": "Not Found",
                "status": status.HTTP_404_NOT_FOUND,
                "detail": "Application not found."
            }
        )
        
    if req.status is not None:
        app.status = ApplicationStatus(req.status)
    if req.notes is not None:
        app.notes = req.notes
        
    await db.flush()
    await db.refresh(app)
    
    return Application.model_validate(app)


@router.post(
    "/{id}/assistant",
    summary="Trigger Application Assistant",
    description="Invokes the Application Assistant agent via Temporal to get the next best action and an email draft."
)
async def trigger_assistant(id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Trigger the Application Assistant for an existing application via Temporal workflow.
    """
    user_id = get_settings().single_user_id
    query = select(DBApplication).where(DBApplication.id == id, DBApplication.user_id == user_id)
    result = await db.execute(query)
    app = result.scalar_one_or_none()
    
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    from temporalio.client import Client
    settings = get_settings()
    client = await Client.connect(settings.temporal_server_url or "localhost:7233")
    workflow_id = f"app_assistant_{id}"
    
    from ...models import Job, CompanyResearch, CoverLetter, InterviewPrep
    job = (await db.execute(select(Job).where(Job.id == app.job_id))).scalar_one_or_none()
    
    company_research_data = None
    if job and job.company_slug:
        cr_query = select(CompanyResearch).where(CompanyResearch.company_name_slug == job.company_slug)
        cr = (await db.execute(cr_query)).scalar_one_or_none()
        if cr:
            company_research_data = cr.research_data

    # Fetch interview prep data (for the questions)
    ip_query = select(InterviewPrep).where(InterviewPrep.job_id == app.job_id)
    ip = (await db.execute(ip_query)).scalar_one_or_none()

    # Fetch cover letter data
    cl_query = select(CoverLetter).where(CoverLetter.job_id == app.job_id)
    cl = (await db.execute(cl_query)).scalar_one_or_none()

    payload = {
        "job_id": str(app.job_id), 
        "current_state": app.status.value if app.status else "draft", 
        "notes": app.notes or "",
        "company_research": company_research_data,
        "interview_prep": ip.questions if ip else None,
        "cover_letter": cl.content if cl else None,
    }
    
    from datetime import timedelta
    try:
        await client.start_workflow(
            "ApplicationAssistantWorkflow",
            payload,
            id=workflow_id,
            task_queue="application-tasks",
            execution_timeout=timedelta(minutes=10)
        )
    except Exception as e:
        logger.error(f"Failed to start Application Assistant workflow: {e}")
        pass
        
    return {"status": "started", "application_id": str(id)}
