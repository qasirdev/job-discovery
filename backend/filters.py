def is_relevant(job_title: str, job_description: str) -> bool:
    """
    MVP 1: Simple keyword filtering. 
    This will be upgraded to full AI relevance scoring via ranking_agent.py in MVP 2.
    """
    title_lower = job_title.lower()
    
    # Exclude seniority logic
    excluded_keywords = ["senior", "staff", "principal", "manager", "lead", "director", "head", "vp"]
    if any(kw in title_lower for kw in excluded_keywords):
        return False
        
    # Include core roles
    included_keywords = ["software engineer", "full stack", "backend", "frontend", "react", "python", "developer"]
    if any(kw in title_lower for kw in included_keywords):
        return True
        
    return False
