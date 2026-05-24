import os
from pydantic import BaseModel
from ...logging_config import get_logger
from ...llm.client import generate_structured_response
from ...schemas import Job

logger = get_logger(__name__)

class QAResult(BaseModel):
    answer: str

class QAAgent:
    """Answers user questions about a specific job based on the job description and candidate context."""

    def __init__(self) -> None:
        self.system_prompt_path = os.path.join("prompts", "qa-agent", "system.md")

    def _load_prompt(self) -> str:
        """Load the system instruction prompt from disk."""
        try:
            with open(self.system_prompt_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("QA system prompt not found, using fallback.")
            return "You are an expert technical recruiter and job discovery assistant. Answer questions based on the provided job description and candidate context."

    async def answer_question(self, job: Job, context: str, question: str) -> QAResult:
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
        
        system_instruction = self._load_prompt()
        
        prompt = f"""Job Title: {job.title}
Company: {job.company}
Job Description: {job.description}

Candidate Context:
{context if context else "No specific context available."}

User Question:
{question}
"""

        try:
            response = await generate_structured_response(
                prompt=prompt,
                system_instruction=system_instruction,
                response_model=QAResult
            )
            logger.info("Successfully generated QA response.")
            return response
        except Exception as e:
            logger.error(f"QA Agent failed to generate answer: {e}")
            return QAResult(answer="I'm sorry, I encountered an error while trying to answer your question. Please try again later.")
