import hashlib
import json
from datetime import timedelta
from enum import Enum
from dataclasses import dataclass

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.common import RetryPolicy
try:
    from temporalio.contrib.opentelemetry import TracingInterceptor
    OTEL_TEMPORAL_AVAILABLE = True
except ImportError:
    OTEL_TEMPORAL_AVAILABLE = False

from ...logging_config import get_logger
from ...schemas import Job
from ..ranking.ranking_agent import RankingAgent
from ..rag.rag_agent import RAGAgent
from ..cover_letter.cover_letter_agent import CoverLetterAgent
from ..security.security_agent import SecurityAgent

from ...settings import get_settings
import redis.asyncio as aioredis

logger = get_logger(__name__)

circuit_breaker_logger = get_logger("circuit_breaker")

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
    
    def _log_transition(self, from_state: CircuitBreakerState, to_state: CircuitBreakerState):
        from datetime import datetime
        circuit_breaker_logger.info(json.dumps({
            "agent_id": self.agent_id,
            "from_state": from_state.value,
            "to_state": to_state.value,
            "failure_count": self.failure_count,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }))

    async def call(self, func, *args, **kwargs):
        if self.state == CircuitBreakerState.OPEN:
            # Simplified backoff for MVP - would use timestamp checking for half-open transition
            logger.warning(f"Circuit breaker {self.agent_id} is OPEN. Rejecting call.")
            raise CircuitOpenError(f"Circuit {self.agent_id} is open")
            
        try:
            result = await func(*args, **kwargs)
            if self.state == CircuitBreakerState.HALF_OPEN:
                self._log_transition(self.state, CircuitBreakerState.CLOSED)
                self.state = CircuitBreakerState.CLOSED
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                if self.state != CircuitBreakerState.OPEN:
                    self._log_transition(self.state, CircuitBreakerState.OPEN)
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
    sec_result_env = await cb.call(agent.validate_for_injection, safe_desc)
    sec_result = sec_result_env.result
    
    if not sec_result.get("is_safe"):
        raise ValueError(f"Security check failed: {sec_result.get('reason')}")
    
    job_dict["description"] = safe_desc
    return job_dict

@activity.defn
async def security_check_output(output_dict: dict) -> dict:
    agent = SecurityAgent()
    cb = circuit_breakers["security"]
    
    sec_result_env = await cb.call(agent.validate_output, output_dict)
    sec_result = sec_result_env.result
    
    if not sec_result.get("is_safe"):
        raise ValueError(f"Security check on agent output failed: {sec_result.get('reason')}")
    
    return output_dict

@activity.defn
async def rank_job(job_dict: dict) -> dict:
    job = Job(**job_dict)
    agent = RankingAgent()
    cb = circuit_breakers["ranking"]
    
    ranking_result_env = await cb.call(agent.evaluate_job, job)
    ranking_result = ranking_result_env.result
    return {
        "is_relevant": ranking_result.get("is_relevant"),
        "score": ranking_result.get("score")
    }

@activity.defn
async def personalise_results(job_dict: dict) -> dict:
    job = Job(**job_dict)
    from ...settings import get_settings
    from ...db import get_db
    
    db_gen = get_db()
    db = await db_gen.__anext__()
    try:
        rag_agent = RAGAgent(db)
        cl_agent = CoverLetterAgent(db)
        user_id = get_settings().single_user_id
        
        context_env = await circuit_breakers["rag"].call(rag_agent.retrieve_context, job.description)
        context = context_env.result.get("context", "")
        
        # In a real workflow, context would be injected via DB or similar. CoverLetter agent fetches it.
        letter_result_env = await circuit_breakers["cover_letter"].call(cl_agent.generate, job.id, user_id)
        letter_result = letter_result_env.result
        
        return {
            "cover_letter": letter_result.get("content"),
            "ats_match": letter_result.get("ats_score")
        }
    finally:
        try:
            await db_gen.__anext__()
        except StopAsyncIteration:
            pass

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
                task_queue="ranking-tasks",
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
            
            # 3b. Security check output
            await workflow.execute_activity(
                security_check_output,
                personalisation,
                start_to_close_timeout=timedelta(seconds=10),
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
        
        await client.start_workflow(
            ScrapeAndRankWorkflow.run,
            job.model_dump(mode="json"),
            id=workflow_id,
            task_queue="job-discovery-tasks",
            execution_timeout=timedelta(hours=24),
        )
        logger.info(f"Started Temporal workflow {workflow_id} for job {job.id}")
        return workflow_id
