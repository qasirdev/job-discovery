from pydantic import BaseModel, Field
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime
from .db import Base

def utc_now():
    """Return the current UTC datetime."""
    return datetime.now(timezone.utc)

class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str | None = None
    description: str
    url: str
    source: str
    posted_at: datetime | None = None
    scraped_at: datetime = Field(default_factory=utc_now)

class ScrapeResult(BaseModel):
    source_id: str
    jobs_found: int
    jobs_saved: int
    errors: list[str] = []
    duration_seconds: float

class RankingResult(BaseModel):
    score: int
    is_relevant: bool
    reasoning: str

class DBJob(Base):
    """SQLAlchemy Model for the jobs table."""
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    company = Column(String, index=True, nullable=False)
    location = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    url = Column(String, nullable=False)
    source = Column(String, index=True, nullable=False)
    posted_at = Column(DateTime(timezone=True), nullable=True)
    scraped_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
