from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, timezone
from typing import Literal
from uuid import UUID

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Job(BaseModel):
    id: UUID = Field(examples=["123e4567-e89b-12d3-a456-426614174000"])
    title: str = Field(examples=["Senior Software Engineer"])
    company: str = Field(examples=["Tech Corp"])
    location: str = Field(examples=["London, UK (Hybrid)"])
    source: str = Field(examples=["linkedin"])
    url: str = Field(examples=["https://linkedin.com/jobs/view/123"])
    description: str = Field(examples=["We are looking for a Senior Software Engineer..."])
    salary_min: int | None = Field(default=None, examples=[80000])
    salary_max: int | None = Field(default=None, examples=[120000])
    currency: str = Field(default="GBP", examples=["GBP"])
    relevance_score: float | None = Field(default=None, examples=[85.5])
    embedding_status: Literal["pending", "processing", "ready"] = Field(default="pending", examples=["pending"])
    saved: bool = Field(default=False, examples=[False])
    scraped_at: datetime = Field(default_factory=utc_now, examples=["2026-05-24T18:00:00Z"])
    
    model_config = ConfigDict(from_attributes=True)

class ScrapeResult(BaseModel):
    source_id: str = Field(examples=["linkedin"])
    jobs_found: int = Field(examples=[150])
    jobs_saved: int = Field(examples=[25])
    errors: list[str] = Field(default=[], examples=[["Rate limit exceeded on page 3"]])
    duration_seconds: float = Field(examples=[45.2])
    
    model_config = ConfigDict(from_attributes=True)

class RankingResult(BaseModel):
    score: int = Field(examples=[85])
    is_relevant: bool = Field(examples=[True])
    reasoning: str = Field(examples=["Matches target role and location perfectly."])

class JobListResponse(BaseModel):
    total: int = Field(examples=[1000])
    page: int = Field(examples=[1])
    page_size: int = Field(examples=[20])
    has_next: bool = Field(examples=[True])
    next_cursor: str | None = Field(default=None, examples=["MjAyNi0wNS0yNFQxODowMDowMFp8MTIzZTQ1NjctZTg5Yi0xMmQzLWE0NTYtNDI2NjE0MTc0MDAw"])
    linkedin_count: int = Field(examples=[600])
    jobserve_count: int = Field(examples=[400])
    jobs: list[Job]
    
    model_config = ConfigDict(from_attributes=True)

class UserProfile(BaseModel):
    id: UUID = Field(examples=["00000000-0000-0000-0000-000000000000"])
    full_name: str = Field(examples=["Jane Doe"])
    email: str = Field(examples=["jane.doe@example.com"])
    target_role: str = Field(examples=["Senior Full Stack Engineer"])
    target_location: str = Field(examples=["Remote (UK)"])
    skills: list[str] = Field(examples=[["React", "TypeScript", "Python", "FastAPI"]])
    years_experience: int = Field(examples=[8])
    cv_filename: str | None = Field(default=None, examples=["jane_doe_cv_2026.pdf"])
    created_at: datetime = Field(default_factory=utc_now, examples=["2026-05-24T18:00:00Z"])
    updated_at: datetime = Field(default_factory=utc_now, examples=["2026-05-24T18:00:00Z"])
    
    model_config = ConfigDict(from_attributes=True)

class SavedJob(BaseModel):
    job_id: UUID = Field(examples=["123e4567-e89b-12d3-a456-426614174000"])
    user_id: UUID = Field(examples=["00000000-0000-0000-0000-000000000000"])
    saved_at: datetime = Field(default_factory=utc_now, examples=["2026-05-24T18:00:00Z"])
    
    model_config = ConfigDict(from_attributes=True)

class Application(BaseModel):
    id: UUID = Field(examples=["123e4567-e89b-12d3-a456-426614174001"])
    job_id: UUID = Field(examples=["123e4567-e89b-12d3-a456-426614174000"])
    user_id: UUID = Field(examples=["00000000-0000-0000-0000-000000000000"])
    status: Literal["draft", "applied", "awaiting_response", "interviewing", "offered", "rejected", "withdrawn"] = Field(examples=["applied"])
    notes: str | None = Field(default=None, examples=["Applied via company portal."])
    applied_at: datetime | None = Field(default=None, examples=["2026-05-24T18:00:00Z"])
    created_at: datetime = Field(default_factory=utc_now, examples=["2026-05-24T18:00:00Z"])
    updated_at: datetime = Field(default_factory=utc_now, examples=["2026-05-24T18:00:00Z"])
    
    model_config = ConfigDict(from_attributes=True)

class Recruiter(BaseModel):
    id: UUID = Field(examples=["123e4567-e89b-12d3-a456-426614174002"])
    name: str = Field(examples=["John Smith"])
    company: str = Field(examples=["Tech Recruits Ltd"])
    email: str | None = Field(default=None, examples=["john@techrecruits.com"])
    linkedin_url: str | None = Field(default=None, examples=["https://linkedin.com/in/johnsmith"])
    interaction_score: int = Field(default=0, examples=[4])
    notes: str | None = Field(default=None, examples=["Had a good chat about senior roles in Fintech."])
    created_at: datetime = Field(default_factory=utc_now, examples=["2026-05-24T18:00:00Z"])
    
    model_config = ConfigDict(from_attributes=True)

class RFC7807Error(BaseModel):
    type: str = Field(default="about:blank", examples=["about:blank"])
    title: str = Field(examples=["Not Found"])
    status: int = Field(examples=[404])
    detail: str = Field(examples=["The requested resource could not be found."])
