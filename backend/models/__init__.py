from datetime import datetime, timezone
import uuid
import enum
from sqlalchemy import String, Text, DateTime, Integer, Float, Boolean, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector

from ..db import Base
from ..settings import get_settings

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Recruiter(Base):
    __tablename__ = "recruiters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String)
    company: Mapped[str] = mapped_column(String, index=True)
    linkedin_url: Mapped[str | None] = mapped_column(String, unique=True, default=None)
    email: Mapped[str | None] = mapped_column(String, default=None)
    interaction_score: Mapped[int] = mapped_column(Integer, default=0)
    notes: Mapped[str | None] = mapped_column(Text, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=utc_now)


class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid.uuid4, index=True)
    full_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    target_role: Mapped[str] = mapped_column(String)
    target_location: Mapped[str] = mapped_column(String)
    skills: Mapped[list[str]] = mapped_column(JSONB, default=list)
    years_experience: Mapped[int] = mapped_column(Integer)
    cv_filename: Mapped[str | None] = mapped_column(String, default=None)
    
    target_roles: Mapped[list[str]] = mapped_column(JSONB, default=list)
    preferred_stack: Mapped[list[str]] = mapped_column(JSONB, default=list)
    seniority_level: Mapped[str | None] = mapped_column(String, default=None)
    target_salary_min: Mapped[int | None] = mapped_column(Integer, default=None)
    target_salary_max: Mapped[int | None] = mapped_column(Integer, default=None)
    preferred_location: Mapped[str | None] = mapped_column(String, default=None)
    notice_period: Mapped[str | None] = mapped_column(String, default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=utc_now)

class CompanyResearch(Base):
    __tablename__ = "company_research"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid.uuid4, index=True)
    company_name_slug: Mapped[str] = mapped_column(String, unique=True, index=True)
    research_data: Mapped[dict | None] = mapped_column(JSONB, default=None)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=utc_now)

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid.uuid4, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    company: Mapped[str] = mapped_column(String, index=True)
    company_slug: Mapped[str | None] = mapped_column(String, default=None)
    location: Mapped[str | None] = mapped_column(String, default=None)
    source: Mapped[str] = mapped_column(String, index=True)
    url: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(Text)
    salary_min: Mapped[int | None] = mapped_column(Integer, default=None)
    salary_max: Mapped[int | None] = mapped_column(Integer, default=None)
    currency: Mapped[str] = mapped_column(String, default="GBP")
    relevance_score: Mapped[float | None] = mapped_column(Float, default=None)
    embedding_status: Mapped[str] = mapped_column(String, default="pending")
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=utc_now)

    # Added for JD-E8 (MVP 2)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536), default=None)
    recruiter_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("recruiters.id"), default=None)
    similarity_score: Mapped[float | None] = mapped_column(Float, default=None)
    job_structured: Mapped[dict | None] = mapped_column(JSONB, default=None)


class ApplicationStatus(str, enum.Enum):
    draft = "draft"
    applied = "applied"
    awaiting_response = "awaiting_response"
    interviewing = "interviewing"
    offered = "offered"
    rejected = "rejected"
    withdrawn = "withdrawn"


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid.uuid4, index=True)
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id"), index=True)
    job: Mapped["Job"] = relationship("Job", init=False)
    
    # We default user_id dynamically or use the settings singleton
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default_factory=lambda: get_settings().single_user_id)
    status: Mapped[ApplicationStatus] = mapped_column(Enum(ApplicationStatus, native_enum=False), default=ApplicationStatus.draft)
    applied_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    notes: Mapped[str | None] = mapped_column(Text, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=utc_now)


class CVEmbeddingStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    ready = "ready"
    failed = "failed"

class CV(Base):
    __tablename__ = "cvs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid.uuid4, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, default_factory=lambda: get_settings().single_user_id)
    filename: Mapped[str | None] = mapped_column(String, default=None)
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536), default=None)
    embedding_status: Mapped[CVEmbeddingStatus] = mapped_column(Enum(CVEmbeddingStatus, native_enum=False), default=CVEmbeddingStatus.pending)
    version: Mapped[int] = mapped_column(Integer, autoincrement=True, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=utc_now)


class CoverLetterStatus(str, enum.Enum):
    draft = "draft"
    final = "final"
    pending = "pending"
    generating = "generating"
    ready = "ready"
    failed = "failed"


class CoverLetter(Base):
    __tablename__ = "cover_letters"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid.uuid4, index=True)
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id"), index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), index=True, default_factory=lambda: get_settings().single_user_id)
    content: Mapped[str] = mapped_column(Text)
    ats_score: Mapped[int | None] = mapped_column(Integer, default=None)
    status: Mapped[CoverLetterStatus] = mapped_column(Enum(CoverLetterStatus, native_enum=False), default=CoverLetterStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=utc_now)


class ScrapeRun(Base):
    __tablename__ = "scrape_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid.uuid4, index=True)
    source_id: Mapped[str] = mapped_column(String)
    jobs_found: Mapped[int] = mapped_column(Integer, default=0)
    jobs_inserted: Mapped[int] = mapped_column(Integer, default=0)
    errors: Mapped[int] = mapped_column(Integer, default=0)
    duration_seconds: Mapped[float] = mapped_column(Float, default=0.0)
    ran_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=utc_now)


class InterviewPrepStatus(str, enum.Enum):
    pending = "pending"
    generating = "generating"
    ready = "ready"
    failed = "failed"


class InterviewPrep(Base):
    __tablename__ = "interview_preps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid.uuid4, index=True)
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id"), index=True)
    questions: Mapped[list[str] | None] = mapped_column(JSONB, default=None)
    system_design_topics: Mapped[list[str] | None] = mapped_column(JSONB, default=None)
    salary_benchmark: Mapped[str | None] = mapped_column(String, default=None)
    company_research: Mapped[dict | None] = mapped_column(JSONB, default=None)
    status: Mapped[InterviewPrepStatus] = mapped_column(Enum(InterviewPrepStatus, native_enum=False), default=InterviewPrepStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=utc_now)


class SavedJob(Base):
    __tablename__ = "saved_jobs"

    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("jobs.id"), primary_key=True, index=True)
    saved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=utc_now)

class EvalMetric(Base):
    __tablename__ = "eval_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default_factory=uuid.uuid4, index=True)
    agent_id: Mapped[str] = mapped_column(String, index=True)
    metric_name: Mapped[str] = mapped_column(String, index=True)
    metric_value: Mapped[float] = mapped_column(Float)
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=utc_now)
