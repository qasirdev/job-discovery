from typing import Any, Union
from .models import Job

EXCLUDED_KEYWORDS = ["senior", "staff", "principal", "manager", "lead", "director", "head", "vp"]
INCLUDED_KEYWORDS = ["software engineer", "full stack", "backend", "frontend", "react", "python", "developer"]

SENIORITY_KEYWORDS = ["senior", "lead", "principal", "architect", "staff"]
TECH_KEYWORDS = ["python", "fastapi", "next.js", "nextjs", "react", "typescript", "azure", "aws", "llm", "ai", "pgvector", "rag", "langchain", "developer", "engineer"]
CONTRACT_KEYWORDS = ["contract", "contractor", "freelance", "outside ir35", "outside-ir35", "day rate", "temporary"]

def is_relevant(job_title: str, job_description: str) -> bool:
    """
    MVP 1: Simple keyword filtering. 
    This will be upgraded to full AI relevance scoring via ranking_agent.py in MVP 2.
    """
    title_lower = job_title.lower()
    
    # Exclude seniority logic
    if any(kw in title_lower for kw in EXCLUDED_KEYWORDS):
        return False
        
    # Include core roles
    if any(kw in title_lower for kw in INCLUDED_KEYWORDS):
        return True
        
    return False

def filter_by_prompt_rules(job: Union[Job, Any]) -> bool:
    """
    Apply heuristic prompt-based pre-filtering according to filtering.md specs (JD-36).
    Returns True if the job satisfies the heuristics, False otherwise.
    """
    # Support both Pydantic model and raw dictionary
    if isinstance(job, dict):
        title = job.get("title", "")
        description = job.get("description", "")
    else:
        title = getattr(job, "title", "")
        description = getattr(job, "description", "")

    title_lower = title.lower()
    desc_lower = description.lower()

    # 1. Seniority Check: Filter out if it has junior/mid keywords and no senior keywords.
    is_junior = any(kw in title_lower or kw in desc_lower for kw in ["junior", "grad", "graduate", "trainee", "intern", "mid-level", "mid level", "associate"])
    is_senior = any(kw in title_lower or kw in desc_lower for kw in SENIORITY_KEYWORDS)
    if is_junior and not is_senior:
        return False
    if not is_senior and not any(kw in title_lower for kw in ["engineer", "developer", "architect"]):
        # Non-engineering roles or lower seniority without senior keywords
        return False

    # 2. Tech Stack Check: Must match our target tech keywords
    has_tech = any(kw in title_lower for kw in TECH_KEYWORDS) or any(kw in desc_lower for kw in TECH_KEYWORDS)
    if not has_tech:
        return False

    # 3. Contract Check: Filter out only if explicitly permanent-only with no contract mentions
    is_explicit_perm = any(kw in title_lower or kw in desc_lower for kw in ["permanent", "perm", "full-time", "full time"])
    has_contract_ref = any(kw in title_lower or kw in desc_lower for kw in CONTRACT_KEYWORDS)
    if is_explicit_perm and not has_contract_ref:
        return False

    return True
