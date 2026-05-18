from pydantic import BaseModel, Field
from datetime import datetime, timezone

def utc_now():
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
