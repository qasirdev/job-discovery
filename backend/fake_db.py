import json
import os
import tempfile
from pathlib import Path
from typing import Any
from uuid import UUID
from .schemas import Job

# MVP 1 ONLY — replaced by Supabase asyncpg repository layer in MVP 2 (JD-E8)

DB_PATH = Path(__file__).parent / "fake_db.json"

def load_db() -> dict[str, dict[str, Any]]:
    if not DB_PATH.exists():
        return {}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_db(db: dict[str, dict[str, Any]]) -> None:
    fd, temp_path = tempfile.mkstemp(dir=DB_PATH.parent, text=True)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, default=str)
    os.replace(temp_path, DB_PATH)

def add_job(job: Job) -> bool:
    db = load_db()
    
    # deduplication logic: skip if job.url already exists
    for existing_job in db.values():
        if existing_job.get("url") == job.url:
            return False
            
    # job.id is UUID, convert to string for dict key
    job_id_str = str(job.id)
    db[job_id_str] = job.model_dump(mode="json")
    save_db(db)
    return True

def get_jobs() -> list[Job]:
    db = load_db()
    jobs = []
    for job_dict in db.values():
        jobs.append(Job.model_validate(job_dict))
    return jobs

def get_job(id: str) -> Job | None:
    db = load_db()
    job_dict = db.get(id)
    if job_dict:
        return Job.model_validate(job_dict)
    return None

def clear_jobs() -> None:
    save_db({})
