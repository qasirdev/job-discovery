import time
from typing import List, Dict, Any, Optional
from pathlib import Path
from pydantic import BaseModel
from jinja2 import Template
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...logging_config import get_logger
from ...llm.client import generate_structured_response, generate_embedding
from ...models import CV, Job, SavedJob, EvalMetric
from ...schemas import AgentResultEnvelope, AgentMetadata, AgentEscalation
from ..observability.observability_agent import ObservabilityAgent

logger = get_logger(__name__)


class RetrievedExperience(BaseModel):
    title: str
    relevance_explanation: str
    key_achievements: List[str]


class RAGResponse(BaseModel):
    retrieved_experiences: List[RetrievedExperience]


from ..base import BaseAgent
from ..telemetry import trace_agent_run

class RAGAgent(BaseAgent):
    """Retrieves relevant profile context to augment LLM scoring using pgvector semantic search."""
    agent_id = "rag"
    canonical_role = "learner"
    display_name = "RAG Context Agent"

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.system_prompt_path = Path(__file__).parent.parent.parent.parent / "prompts" / "rag" / "system.md"
        self.user_prompt_path = Path(__file__).parent.parent.parent.parent / "prompts" / "rag" / "user.md"
        self.context_window_budget = 8000  # tokens
        self.chunk_size = 512  # tokens
        self.chunk_overlap = 50  # tokens

    def _load_prompt(self, path: Path) -> str:
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"RAG prompt {path} not found.")
            return ""

    @trace_agent_run("rag", "retrieve_context")
    async def retrieve_context(self, job_description: str, candidate_profile: Dict[str, Any] | None = None) -> AgentResultEnvelope:
        logger.info("RAG Agent retrieving context from PostgreSQL using pgvector...")
        
        # 1. Embed the job description
        job_embedding = await generate_embedding(job_description)

        # 2. Query Postgres for closest CV chunks / User profile info
        # Here we perform semantic search on the CV table
        query = select(CV, CV.embedding.cosine_distance(job_embedding).label('distance')).order_by('distance').limit(3)
        result = await self.db.execute(query)
        cv_matches_with_dist = result.all()
        cv_matches = [row.CV for row in cv_matches_with_dist]

        # 3. Query Saved Jobs for context
        saved_jobs_query = select(Job, Job.embedding.cosine_distance(job_embedding).label('distance')).join(SavedJob, Job.id == SavedJob.job_id).order_by('distance').limit(3)
        saved_jobs_result = await self.db.execute(saved_jobs_query)
        saved_jobs_matches_with_dist = saved_jobs_result.all()
        saved_jobs_matches = [row.Job for row in saved_jobs_matches_with_dist]
        
        # Calculate precision
        total_distance = sum([row.distance for row in cv_matches_with_dist if row.distance is not None]) + sum([row.distance for row in saved_jobs_matches_with_dist if row.distance is not None])
        count = len(cv_matches_with_dist) + len(saved_jobs_matches_with_dist)
        avg_distance = total_distance / count if count > 0 else 1.0
        retrieval_precision = max(0.0, 1.0 - avg_distance)
        
        # Store in eval_metrics table and as a Prometheus gauge
        metric = EvalMetric(
            agent_id="rag",
            metric_name="retrieval_precision",
            metric_value=retrieval_precision,
            metadata_json={"job_description_length": len(job_description)}
        )
        self.db.add(metric)
        
        obs_agent = ObservabilityAgent()
        obs_agent.record_metric("rag_retrieval_precision", retrieval_precision)

        # Build raw context string
        context_parts = []
        if cv_matches:
            context_parts.append("--- Relevant CV Snippets ---")
            for cv in cv_matches:
                context_parts.append(cv.content[:500] + "...")
        
        if saved_jobs_matches:
            context_parts.append("--- Similar Saved Jobs ---")
            for sj in saved_jobs_matches:
                context_parts.append(f"Title: {sj.title}, Company: {sj.company}")
                
        raw_context = "\n".join(context_parts)
        if not raw_context.strip():
            raw_context = self._format_candidate_profile(candidate_profile or {})

        system_instruction = self._load_prompt(self.system_prompt_path) or "You are a RAG agent. Extract relevant experiences."
        user_template_str = self._load_prompt(self.user_prompt_path)
        
        if user_template_str:
            try:
                template = Template(user_template_str)
                prompt = template.render(
                    retrieved_context=raw_context,
                    user_question=job_description
                )
            except Exception as e:
                logger.error(f"Prompt rendering error: {e}")
                prompt = f"Target Job: {job_description}\n\nCandidate Profile Context:\n{raw_context}"
        else:
            prompt = f"Target Job: {job_description}\n\nCandidate Profile Context:\n{raw_context}"
        
        start_time = time.time()
        try:
            response = await generate_structured_response(
                prompt=prompt,
                system_instruction=system_instruction,
                response_model=RAGResponse,
                agent_id="rag"
            )
            
            structured_context = []
            for exp in response.retrieved_experiences:
                structured_context.append(f"Project/Role: {exp.title}")
                structured_context.append(f"Relevance: {exp.relevance_explanation}")
                structured_context.append(f"Achievements: {'; '.join(exp.key_achievements)}")
                structured_context.append("---")
            
            duration = time.time() - start_time
            return AgentResultEnvelope(
                agent_id="rag",
                canonical_role="learner",
                status="success",
                result={"context": "\n".join(structured_context)},
                metadata=AgentMetadata(
                    execution_ms=int(duration * 1000),
                    tokens_used=0,
                    model_used="claude-3-5-sonnet-20240620",
                    prompt_version=None,
                    quality_score=retrieval_precision
                )
            )
            
        except Exception as e:
            logger.error(f"RAG retrieval failed: {e}")
            duration = time.time() - start_time
            return AgentResultEnvelope(
                agent_id="rag",
                canonical_role="learner",
                status="failure",
                result={"context": raw_context},
                metadata=AgentMetadata(
                    execution_ms=int(duration * 1000),
                    tokens_used=0,
                    model_used="unknown",
                    prompt_version=None
                ),
                escalation=AgentEscalation(reason=str(e), target_agent="orchestrator")
            )

    def _format_candidate_profile(self, profile: Dict[str, Any]) -> str:
        parts = []
        if "skills" in profile:
            parts.append(f"Skills: {', '.join(profile['skills'])}")
        if "experience" in profile:
            parts.append("Experience:")
            for exp in profile["experience"]:
                parts.append(f"- {exp.get('title', 'Unknown')} at {exp.get('company', 'Unknown')}")
                if exp.get("description"):
                    parts.append(f"  {exp['description']}")
        return "\n".join(parts)
