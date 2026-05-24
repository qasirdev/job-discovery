from ...schemas import Job, RankingResult
from ...llm.client import generate_structured_response
from ...logging_config import get_logger
import os

logger = get_logger(__name__)

class RankingAgent:
    """Evaluates and scores a job against a professional profile."""

    def __init__(self) -> None:
        self.system_prompt_path = os.path.join("prompts", "ranking-agent", "system.md")


    def _load_prompt(self) -> str:
        """Load the system instruction prompt from disk."""
        try:
            with open(self.system_prompt_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning("System prompt not found, using fallback.")
            return "You are a ranking agent. Score the job."

    async def evaluate_job(self, job: Job) -> RankingResult:
        """Score the job relevance."""
        logger.info(f"Ranking Agent evaluating job: {job.id}")
        
        system_instruction = self._load_prompt()
        prompt = f"Job Title: {job.title}\nCompany: {job.company}\nDescription: {job.description}"

        try:
            # Cast the return type to RankingResult
            _ = await generate_structured_response(
                prompt=prompt,
                system_instruction=system_instruction,
                response_model=RankingResult
            )
            
            # Since our LLM client is currently mocked/stubbed, we return a mock result
            # In production, we'd parse the 'response' object.
            return RankingResult(score=85, is_relevant=True, reasoning="Mock evaluation complete.")
            
        except Exception as e:
            logger.error(f"Ranking failed for job {job.id}: {e}")
            return RankingResult(score=0, is_relevant=False, reasoning=str(e))
