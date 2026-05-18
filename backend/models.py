from pydantic import BaseModel, Field
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
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

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True, nullable=False)
    company: Mapped[str] = mapped_column(String, index=True, nullable=False)
    location: Mapped[str | None] = mapped_column(String, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str] = mapped_column(String, index=True, nullable=False)
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

