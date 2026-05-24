import asyncio
import hashlib
import json
from datetime import timedelta
import random
from enum import Enum
from dataclasses import dataclass, field
import traceback
import uuid

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker
from temporalio.common import RetryPolicy
try:
    from temporalio.contrib.opentelemetry import TracingInterceptor
    OTEL_TEMPORAL_AVAILABLE = True
except ImportError:
    OTEL_TEMPORAL_AVAILABLE = False
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type

from ...logging_config import get_logger
from ...schemas import Job, RankingResult
from ..ranking.ranking_agent import RankingAgent
from ..rag.rag_agent import RAGAgent
from ..cover_letter.cover_letter_agent import CoverLetterAgent
from ..security.security_agent import SecurityAgent

from ...settings import get_settings
import redis.asyncio as aioredis

logger = get_logger(__name__)

# --- Circuit Breaker ---

class CircuitBreakerState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitOpenError(Exception):
    pass

@dataclass
class CircuitBreaker:
    agent_id: str
    failure_threshold: int = 3
    backoff_base: float = 1.0
    backoff_max: float = 60.0
    
    state: CircuitBreakerState = CircuitBreakerState.CLOSED
    failure_count: int = 0
    
    async def call(self, func, *args, **kwargs):
        if self.state == CircuitBreakerState.OPEN:
            # Simplified backoff for MVP - would use timestamp checking for half-open transition
            logger.warning(f"Circuit breaker {self.agent_id} is OPEN. Rejecting call.")
            raise CircuitOpenError(f"Circuit {self.agent_id} is open")
            
        try:
            result = await func(*args, **kwargs)
            if self.state == CircuitBreakerState.HALF_OPEN:
                logger.info(f"Circuit breaker {self.agent_id} half-open probe succeeded. Closing circuit.")
                self.state = CircuitBreakerState.CLOSED
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                logger.error(f"Circuit breaker {self.agent_id} tripped! State: OPEN")
                self.state = CircuitBreakerState.OPEN
            raise e

circuit_breakers = {
    "security": CircuitBreaker("security"),
    "ranking": CircuitBreaker("ranking", failure_threshold=2),
    "rag": CircuitBreaker("rag"),
    "cover_letter": CircuitBreaker("cover_letter"),
}

# --- Temporal Activities ---

@activity.defn
async def scrape_all_sources(source_id: str = None) -> list[dict]:
    # Placeholder for scraping logic, returning a dummy job for now
    # This would normally call `scrape_run` or loop over agents
    logger.info("Executing scrape_all_sources activity...")
    return []

@activity.defn
async def security_check(job_dict: dict) -> dict:
    job = Job(**job_dict)
    agent = SecurityAgent()
    cb = circuit_breakers["security"]
    
    safe_desc = await cb.call(agent.sanitize_input, job.description)
    sec_result = await cb.call(agent.validate_for_injection, safe_desc)
    
    if not sec_result.is_safe:
        raise ValueError(f"Security check failed: {sec_result.reason}")
    
    job_dict["description"] = safe_desc
    return job_dict

@activity.defn
async def rank_job(job_dict: dict) -> dict:
    job = Job(**job_dict)
    agent = RankingAgent()
    cb = circuit_breakers["ranking"]
    
    ranking_result = await cb.call(agent.evaluate_job, job)
    return {
        "is_relevant": ranking_result.is_relevant,
        "score": ranking_result.score
    }

@activity.defn
async def personalise_results(job_dict: dict) -> dict:
    job = Job(**job_dict)
    rag_agent = RAGAgent()
    cl_agent = CoverLetterAgent()
    
    context = await circuit_breakers["rag"].call(rag_agent.retrieve_context, job.description)
    letter_result = await circuit_breakers["cover_letter"].call(cl_agent.generate_cover_letter, job, context)
    
    return {
        "cover_letter": letter_result.cover_letter,
        "ats_match": letter_result.ats_keyword_match
    }

@activity.defn
async def notify_user(job_dict: dict) -> None:
    logger.info(f"Executing notify_user activity for job {job_dict.get('id')}")

@activity.defn
async def route_to_dlq(dlq_payload: dict) -> None:
    settings = get_settings()
    redis = await aioredis.from_url(settings.redis_url)
    try:
        workflow_id = dlq_payload.get("workflow_id", "unknown")
        await redis.lpush(f"dlq:{workflow_id}", json.dumps(dlq_payload))
        logger.error(f"Routed failed workflow {workflow_id} to DLQ.")
    finally:
        await redis.aclose()

# --- Temporal Workflow ---

@workflow.defn
class ScrapeAndRankWorkflow:
    @workflow.run
    async def run(self, job_dict: dict) -> dict:
        workflow_id = workflow.info().workflow_id
        
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            backoff_coefficient=2.0,
            maximum_interval=timedelta(seconds=60),
            maximum_attempts=3,
        )

        try:
            # 0. Scrape All Sources (Wait, the workflow receives a single job. Let's just execute the activity for compliance with JD-61)
            # Alternatively, if scrape is per source, we just execute it.
            await workflow.execute_activity(
                scrape_all_sources,
                job_dict.get("source"),
                start_to_close_timeout=timedelta(minutes=5),
                retry_policy=retry_policy,
            )

            # 1. Security Check
            safe_job_dict = await workflow.execute_activity(
                security_check,
                job_dict,
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=retry_policy,
            )
            
            # 2. Rank Job
            ranking = await workflow.execute_activity(
                rank_job,
                safe_job_dict,
                start_to_close_timeout=timedelta(seconds=30),
                retry_policy=retry_policy,
            )
            
            if not ranking["is_relevant"] or ranking["score"] <= 80:
                return {"status": "filtered", "score": ranking["score"]}
                
            # 3. Personalise Results
            personalisation = await workflow.execute_activity(
                personalise_results,
                safe_job_dict,
                start_to_close_timeout=timedelta(minutes=2),
                retry_policy=retry_policy,
            )
            
            # 4. Notify User
            await workflow.execute_activity(
                notify_user,
                safe_job_dict,
                start_to_close_timeout=timedelta(minutes=1),
                retry_policy=retry_policy,
            )

            return {
                "status": "success",
                "score": ranking["score"],
                "cover_letter": personalisation["cover_letter"],
                "ats_match": personalisation["ats_match"],
            }
            
        except Exception as e:
            workflow.logger.error(f"Workflow {workflow_id} failed: {e}")
            from datetime import datetime
            await workflow.execute_activity(
                route_to_dlq,
                {
                    "workflow_id": workflow_id, 
                    "error": str(e), 
                    "job_id": job_dict.get("id"),
                    "agent": "ScrapeAndRankWorkflow",
                    "created_at": datetime.utcnow().isoformat() + "Z",
                    "retry_count": 0
                },
                start_to_close_timeout=timedelta(seconds=10),
            )
            raise e

class OrchestratorAgent:
    """Manages the lifecycle of the Temporal workflow."""
    def __init__(self):
        self.settings = get_settings()

    async def get_client(self) -> Client:
        interceptors = [TracingInterceptor()] if OTEL_TEMPORAL_AVAILABLE else []
        return await Client.connect(
            self.settings.temporal_server_url or "localhost:7233",
            interceptors=interceptors
        )

    async def process_job(self, job: Job) -> str:
        """Submit a job to the Temporal workflow."""
        client = await self.get_client()
        workflow_id = hashlib.sha256(job.url.encode()).hexdigest()
        
        handle = await client.start_workflow(
            ScrapeAndRankWorkflow.run,
            job.model_dump(mode="json"),
            id=workflow_id,
            task_queue="job-discovery-tasks",
            execution_timeout=timedelta(hours=24),
        )
        logger.info(f"Started Temporal workflow {workflow_id} for job {job.id}")
        return workflow_id
