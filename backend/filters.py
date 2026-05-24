import os
import yaml
from typing import Any
from .schemas import Job, UserProfile
from .logging_config import get_logger

logger = get_logger(__name__)

DEFAULT_KEYWORDS: list[str] = [
    # Seniority
    "senior", "lead", "principal", "architect",
    # Stack
    "python", "fastapi", "next.js", "typescript", "azure", "aws", "llm", "ai",
    # Contract type
    "contract", "freelance", "outside ir35"
]

def load_relevance_profile() -> list[str]:
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "relevance_profile.yaml")
    if not os.path.exists(config_path):
        return DEFAULT_KEYWORDS
    try:
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
            if not data:
                return DEFAULT_KEYWORDS
            
            keywords = []
            for section in ["seniority_keywords", "stack_keywords", "contract_keywords"]:
                if section in data and data[section]:
                    keywords.extend(data[section])
            return keywords if keywords else DEFAULT_KEYWORDS
    except Exception as e:
        logger.warning("Failed to load relevance_profile.yaml, falling back to defaults", error=str(e))
        return DEFAULT_KEYWORDS

def merge_profile_keywords(profile: UserProfile | None) -> list[str]:
    """
    Returns base keywords merged with profile.skills and profile.target_role 
    tokens when profile is provided (MVP 1.1 hook).
    """
    base_keywords = load_relevance_profile()
    if profile is None:
        return base_keywords
        
    merged = set(base_keywords)
    if profile.skills:
        for skill in profile.skills:
            merged.add(skill.lower())
    if profile.target_role:
        for token in profile.target_role.split():
            merged.add(token.lower())
    return list(merged)

def filter_jobs(jobs: list[Job], keywords: list[str] | None = None) -> list[Job]:
    """
    Match case-insensitively against job.title + job.description.
    Returns jobs matching at least one keyword.
    """
    if not jobs:
        return []
        
    active_keywords = keywords if keywords is not None else DEFAULT_KEYWORDS
    active_keywords = [kw.lower() for kw in active_keywords]
    
    filtered_jobs = []
    for job in jobs:
        text_to_search = f"{job.title} {job.description}".lower()
        if any(kw in text_to_search for kw in active_keywords):
            filtered_jobs.append(job)
            
    filtered_count = len(jobs) - len(filtered_jobs)
    filter_rate = (filtered_count / len(jobs)) * 100
    
    logger.info("Jobs filtered", total_jobs=len(jobs), passed=len(filtered_jobs), filtered=filtered_count, filter_rate=f"{filter_rate:.1f}%")
    
    if filter_rate > 90.0:
        logger.warning("High filter rate detected", filter_rate=f"{filter_rate:.1f}%", keywords=active_keywords)
        
    return filtered_jobs
