from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, Integer, Float, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid

# Assume db.py defines Base
from ..db import Base

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class Job(Base):
    """SQLAlchemy Model for the jobs table."""
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    company: Mapped[str] = mapped_column(String, index=True)
    location: Mapped[str | None] = mapped_column(String, default=None)
    source: Mapped[str] = mapped_column(String, index=True)
    url: Mapped[str] = mapped_column(String, unique=True, index=True)
    description: Mapped[str] = mapped_column(Text)
    salary_min: Mapped[int | None] = mapped_column(Integer, default=None)
    salary_max: Mapped[int | None] = mapped_column(Integer, default=None)
    currency: Mapped[str] = mapped_column(String, default="GBP")
    relevance_score: Mapped[float | None] = mapped_column(Float, default=None)
    embedding_status: Mapped[str] = mapped_column(String, default="pending")
    saved: Mapped[bool] = mapped_column(Boolean, default=False)
    scraped_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

class ScrapeResult(Base):
    """SQLAlchemy Model for the scrape_results table."""
    __tablename__ = "scrape_results"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    results: Mapped[dict] = mapped_column(JSON)
    total_inserted: Mapped[int] = mapped_column(Integer)
    duration_seconds: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
