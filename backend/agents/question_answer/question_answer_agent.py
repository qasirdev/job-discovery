import os
from pydantic import BaseModel
from jinja2 import Template
from ...logging_config import get_logger
from ...llm.client import generate_structured_response
from ...schemas import Job

logger = get_logger(__name__)

class QAResult(BaseModel):
    answer: str

from pathlib import Path
import time
from ...schemas import AgentResultEnvelope, AgentMetadata, AgentEscalation
from ..base import BaseAgent

class QAAgent(BaseAgent):
    """Answers candidate questions strictly grounded in the RAG context."""

    def __init__(self) -> None:
        self.system_prompt_path = Path(__file__).parent.parent.parent.parent / "prompts" / "question_answer" / "system.md"
        self.user_prompt_path = Path(__file__).parent.parent.parent.parent / "prompts" / "question_answer" / "user.md"

    def _load_prompt(self, path: Path) -> str:
        """Load prompt from disk."""
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"QA prompt {path} not found.")
            return ""

    async def answer_question(self, job: Job, context: str, question: str) -> AgentResultEnvelope:
        """
        Answer a specific question about the job leveraging RAG context.
        
        Args:
            job: The job object
            context: RAG-retrieved context about the candidate
            question: The user's question
            
        Returns:
            QAResult containing the answer.
        """
        logger.info(f"Answering question for job: {job.id}")
        
        system_instruction = self._load_prompt(self.system_prompt_path) or "You are an expert technical recruiter and job discovery assistant. Answer questions."
        user_template_str = self._load_prompt(self.user_prompt_path)
        
        if user_template_str:
            try:
                template = Template(user_template_str)
                prompt = template.render(
                    job_title=job.title,
                    job_company=job.company,
                    job_description=job.description,
                    context=context or "No specific context available.",
                    question=question
                )
            except Exception as e:
                logger.error(f"Prompt rendering error: {e}")
                prompt = f"Job: {job.title}\nCompany: {job.company}\nDescription: {job.description}\n\nContext:\n{context}\n\nQuestion:\n{question}"
        else:
            prompt = f"Job: {job.title}\nCompany: {job.company}\nDescription: {job.description}\n\nContext:\n{context}\n\nQuestion:\n{question}"

        start_time = time.time()
        try:
            response = await generate_structured_response(
                prompt=prompt,
                system_instruction=system_instruction,
                response_model=QAResult
            )
            logger.info("Successfully generated QA response.")
            duration = time.time() - start_time
            return AgentResultEnvelope(
                agent_id="question_answer",
                canonical_role="doer",
                status="success",
                result=response.model_dump(),
                metadata=AgentMetadata(execution_ms=int(duration * 1000), tokens_used=0, model_used="claude-3-5-sonnet-20240620", prompt_version=None)
            )
        except Exception as e:
            logger.error(f"QA Agent failed to generate answer: {e}")
            duration = time.time() - start_time
            return AgentResultEnvelope(
                agent_id="question_answer",
                canonical_role="doer",
                status="failure",
                result=QAResult(answer="I'm sorry, I encountered an error while trying to answer your question. Please try again later.").model_dump(),
                metadata=AgentMetadata(execution_ms=int(duration * 1000), tokens_used=0, model_used="unknown", prompt_version=None),
                escalation=AgentEscalation(reason=str(e), target_agent="orchestrator")
            )
