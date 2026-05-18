import os
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from ...logging_config import get_logger
from ...llm.client import generate_structured_response

logger = get_logger(__name__)


class RetrievedExperience(BaseModel):
    title: str
    relevance_explanation: str
    key_achievements: List[str]


class RAGResponse(BaseModel):
    retrieved_experiences: List[RetrievedExperience]


class RAGAgent:
    """Retrieves relevant profile context to augment LLM scoring using semantic search."""

    def __init__(self) -> None:
        self.system_prompt_path = os.path.join("prompts", "rag-agent", "system.md")
        self.context_window_budget = 8000  # tokens
        self.chunk_size = 512  # tokens
        self.chunk_overlap = 50  # tokens

    def _load_prompt(self) -> str:
        """Load the system instruction prompt from disk."""
        try:
            with open(self.system_prompt_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("RAG system prompt not found, using fallback.")
            return "You are a RAG agent. Extract relevant experiences from candidate profile."

    async def retrieve_context(self, job_description: str, candidate_profile: Dict[str, Any] | None = None) -> str:
        """
        Fetch profile details most relevant to the given job description.
        
        Args:
            job_description: The target job description
            candidate_profile: Optional candidate profile data (CV, applications, etc.)
        
        Returns:
            Formatted context string with retrieved experiences
        """
        logger.info("RAG Agent retrieving context...")
        
        if not candidate_profile:
            logger.warning("No candidate profile provided, returning empty context")
            return ""
        
        system_instruction = self._load_prompt()
        
        # Build prompt with job description and candidate profile
        profile_context = self._format_candidate_profile(candidate_profile)
        prompt = f"Target Job: {job_description}\n\nCandidate Profile:\n{profile_context}"
        
        try:
            # Generate structured response using LLM
            response = await generate_structured_response(
                prompt=prompt,
                system_instruction=system_instruction,
                response_model=RAGResponse
            )
            
            # Format retrieved experiences into context string
            context_parts = []
            for exp in response.retrieved_experiences:
                context_parts.append(f"Project/Role: {exp.title}")
                context_parts.append(f"Relevance: {exp.relevance_explanation}")
                context_parts.append(f"Achievements: {'; '.join(exp.key_achievements)}")
                context_parts.append("---")
            
            context = "\n".join(context_parts)
            
            # Check context window budget
            estimated_tokens = len(context.split()) * 1.3  # Rough estimate
            if estimated_tokens > self.context_window_budget:
                logger.warning(f"Context exceeds budget ({estimated_tokens} > {self.context_window_budget}), truncating")
                context = self._truncate_context(context, self.context_window_budget)
            
            logger.info(f"RAG retrieved {len(response.retrieved_experiences)} experiences")
            return context
            
        except Exception as e:
            logger.error(f"RAG retrieval failed: {e}")
            # Fallback: return basic profile info
            return self._format_candidate_profile(candidate_profile)

    def _format_candidate_profile(self, profile: Dict[str, Any]) -> str:
        """Format candidate profile into a structured string for LLM consumption."""
        parts = []
        
        if "skills" in profile:
            parts.append(f"Skills: {', '.join(profile['skills'])}")
        
        if "experience" in profile:
            parts.append("Experience:")
            for exp in profile["experience"]:
                parts.append(f"- {exp.get('title', 'Unknown')} at {exp.get('company', 'Unknown')}")
                if exp.get("description"):
                    parts.append(f"  {exp['description']}")
        
        if "projects" in profile:
            parts.append("Projects:")
            for proj in profile["projects"]:
                parts.append(f"- {proj.get('name', 'Unknown')}: {proj.get('description', 'No description')}")
        
        return "\n".join(parts)

    def _truncate_context(self, context: str, max_tokens: int) -> str:
        """Truncate context to fit within token budget, preserving priority order."""
        # Simple truncation by character count (rough approximation)
        max_chars = int(max_tokens * 4)  # ~4 chars per token
        if len(context) <= max_chars:
            return context
        return context[:max_chars] + "..."

    async def get_personalized_recommendations(self, job_description: str, candidate_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized job recommendations using retrieved context.
        
        Args:
            job_description: The target job description
            candidate_profile: Candidate profile data
        
        Returns:
            Dictionary with personalized insights and match score
        """
        logger.info("Generating personalized recommendations...")
        
        context = await self.retrieve_context(job_description, candidate_profile)
        
        if not context:
            return {
                "personalized": False,
                "reason": "No candidate profile available",
                "match_score": 0,
                "context": ""
            }
        
        # Calculate simple match score based on context length and content
        match_score = min(100, len(context.split()) // 10)
        
        return {
            "personalized": True,
            "match_score": match_score,
            "context": context,
            "reason": "Personalized based on candidate profile"
        }
