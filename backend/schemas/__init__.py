from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Job(BaseModel):
    id: UUID
    title: str
    company: str
    location: str
    source: str
    url: str
    description: str
    salary_min: int | None = None
    salary_max: int | None = None
    currency: str = "GBP"
    relevance_score: float | None = None
    embedding_status: Literal["pending", "processing", "ready"] = "pending"
    saved: bool = False
    scraped_at: datetime = Field(default_factory=utc_now)
    
    model_config = ConfigDict(from_attributes=True)

class ScrapeResult(BaseModel):
    source_id: str
    jobs_found: int
    jobs_saved: int
    errors: list[str] = []
    duration_seconds: float
    
    model_config = ConfigDict(from_attributes=True)

class RankingResult(BaseModel):
    score: int
    is_relevant: bool
    reasoning: str

class JobListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    has_next: bool
    next_cursor: str | None = None
    linkedin_count: int
    jobserve_count: int
    jobs: list[Job]
    
    model_config = ConfigDict(from_attributes=True)

class UserProfile(BaseModel):
    id: UUID
    full_name: str
    email: str
    target_role: str
    target_location: str
    skills: list[str]
    years_experience: int
    cv_filename: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    
    model_config = ConfigDict(from_attributes=True)

class SavedJob(BaseModel):
    job_id: UUID
    user_id: UUID
    saved_at: datetime = Field(default_factory=utc_now)
    
    model_config = ConfigDict(from_attributes=True)

class Application(BaseModel):
    id: UUID
    job_id: UUID
    user_id: UUID
    status: Literal["draft", "applied", "awaiting_response", "interviewing", "offered", "rejected", "withdrawn"]
    notes: str | None = None
    applied_at: datetime | None = None
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
    
    model_config = ConfigDict(from_attributes=True)

class Recruiter(BaseModel):
    id: UUID
    name: str
    company: str
    email: str | None = None
    linkedin_url: str | None = None
    interaction_score: int = 0
    notes: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
    
    model_config = ConfigDict(from_attributes=True)
