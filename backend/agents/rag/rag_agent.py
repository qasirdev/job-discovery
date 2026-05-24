import os
from typing import List, Dict, Any
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ...logging_config import get_logger
from ...llm.client import generate_structured_response, generate_embedding
from ...models import CV, Job

logger = get_logger(__name__)


class RetrievedExperience(BaseModel):
    title: str
    relevance_explanation: str
    key_achievements: List[str]


class RAGResponse(BaseModel):
    retrieved_experiences: List[RetrievedExperience]


class RAGAgent:
    """Retrieves relevant profile context to augment LLM scoring using pgvector semantic search."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.system_prompt_path = os.path.join("prompts", "rag-agent", "system.md")
        self.context_window_budget = 8000  # tokens
        self.chunk_size = 512  # tokens
        self.chunk_overlap = 50  # tokens

    def _load_prompt(self) -> str:
        try:
            with open(self.system_prompt_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("RAG system prompt not found, using fallback.")
            return "You are a RAG agent. Extract relevant experiences from candidate profile."

    async def retrieve_context(self, job_description: str, candidate_profile: Dict[str, Any] | None = None) -> str:
        logger.info("RAG Agent retrieving context from PostgreSQL using pgvector...")
        
        # 1. Embed the job description
        job_embedding = await generate_embedding(job_description)

        # 2. Query Postgres for closest CV chunks / User profile info
        # Here we perform semantic search on the CV table
        query = select(CV).order_by(CV.embedding.cosine_distance(job_embedding)).limit(3)
        result = await self.db.execute(query)
        cv_matches = result.scalars().all()

        # 3. Query Saved Jobs for context
        saved_jobs_query = select(Job).where(Job.saved == True).order_by(Job.embedding.cosine_distance(job_embedding)).limit(3)
        saved_jobs_result = await self.db.execute(saved_jobs_query)
        saved_jobs_matches = saved_jobs_result.scalars().all()

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

        system_instruction = self._load_prompt()
        prompt = f"Target Job: {job_description}\n\nCandidate Profile Context:\n{raw_context}"
        
        try:
            response = await generate_structured_response(
                prompt=prompt,
                system_instruction=system_instruction,
                response_model=RAGResponse
            )
            
            structured_context = []
            for exp in response.retrieved_experiences:
                structured_context.append(f"Project/Role: {exp.title}")
                structured_context.append(f"Relevance: {exp.relevance_explanation}")
                structured_context.append(f"Achievements: {'; '.join(exp.key_achievements)}")
                structured_context.append("---")
            
            return "\n".join(structured_context)
            
        except Exception as e:
            logger.error(f"RAG retrieval failed: {e}")
            return raw_context

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
