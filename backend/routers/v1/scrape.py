from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from ...agents.registry import get_all_agents, get_agent
from ...schemas import ScrapeResult
from ...logging_config import get_logger
import asyncio
from ...repositories.job import JobRepository, get_job_repo

# Import specific agents to ensure decorators fire. 
# In a larger app, we'd use importlib to dynamically load the agents folder.
from ...agents.linkedin import linkedin_agent  # noqa: F401
from ...agents.jobserve import jobserve_agent  # noqa: F401

logger = get_logger(__name__)
router: APIRouter = APIRouter(prefix="/scrape", tags=["Scrape"])

class ScrapeRequest(BaseModel):
    source_id: str | None = None  # If None, run all registered scrapers
    max_jobs: int = 10



# MVP 1: In-process concurrency guard.
# MVP 2: Replace with Redis distributed lock `redis.lock("scrape:global")`
scrape_lock = asyncio.Lock()

@router.post("/", response_model=List[ScrapeResult])
async def trigger_scrape(req: ScrapeRequest, repo: JobRepository = Depends(get_job_repo)):
    """Trigger the scrape process for registered agents."""
    try:
        await asyncio.wait_for(scrape_lock.acquire(), timeout=5.0)
    except asyncio.TimeoutError:
        from fastapi import status
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Scrape already in progress"
        )
        
    try:
        results = []
        agents_to_run = []
        
        if req.source_id:
            agent_cls = get_agent(req.source_id)
            if not agent_cls:
                raise HTTPException(status_code=404, detail=f"Scraper '{req.source_id}' not found.")
            agents_to_run.append(agent_cls())
        else:
            agents_to_run = [cls() for cls in get_all_agents()]
            
        for agent in agents_to_run:
            try:
                logger.info(f"Triggering scrape for {agent.source_id}")
                envelope = await agent.run(repo=repo, max_jobs=req.max_jobs)
                
                # Map internal envelope back to public ScrapeResult for API consumers
                res_dict = envelope.result
                results.append(ScrapeResult(
                    source_id=envelope.agent_id,
                    jobs_found=res_dict.get("jobs_found", 0),
                    jobs_saved=res_dict.get("jobs_saved", 0),
                    errors=res_dict.get("errors", []),
                    duration_seconds=envelope.metadata.execution_ms / 1000.0
                ))
            except Exception as e:
                logger.error(f"Scraper {agent.source_id} failed: {e}", exc_info=True)
                results.append(ScrapeResult(
                    source_id=getattr(agent, "source_id", "unknown"),
                    jobs_found=0,
                    jobs_saved=0,
                    errors=[str(e)],
                    duration_seconds=0.0
                ))
                
        return results
    finally:
        scrape_lock.release()
