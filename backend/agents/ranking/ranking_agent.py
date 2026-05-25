import os
from pathlib import Path
from jinja2 import Template
from ...schemas import Job, RankingResult
from ...llm.client import generate_structured_response
from ...logging_config import get_logger

class RankingAgent:
    """Evaluates and scores a job against a professional profile using an 8-step pipeline."""

    def __init__(self) -> None:
        self.system_prompt_path = Path(__file__).parent.parent.parent.parent / "prompts" / "ranking-agent" / "system.md"
        self.user_prompt_path = Path(__file__).parent.parent.parent.parent / "prompts" / "ranking-agent" / "user.md"
        
    def _load_prompt(self, path: Path) -> str:
        """Load prompt from disk."""
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Prompt {path} not found.")
            return ""
        except FileNotFoundError:
            logger.warning("System prompt not found, using fallback.")
            return "You are a ranking agent. Score the job."

    async def evaluate_job(self, job: Job, candidate_profile: dict | None = None) -> RankingResult:
        """Score the job relevance."""
        logger.info(f"Ranking Agent evaluating job: {job.id}")
        
        system_instruction = self._load_prompt(self.system_prompt_path) or "You are a ranking agent. Score the job."
        user_template_str = self._load_prompt(self.user_prompt_path)
        
        if user_template_str:
            try:
                template = Template(user_template_str)
                prompt = template.render(
                    job_title=job.title,
                    job_company=job.company,
                    job_description=job.description,
                    candidate_profile=candidate_profile or "No profile provided"
                )
            except Exception as e:
                logger.error(f"Prompt rendering error: {e}")
                prompt = f"Job Title: {job.title}\nCompany: {job.company}\nDescription: {job.description}\n\nCandidate Profile:\n{candidate_profile}"
        else:
            prompt = f"Job Title: {job.title}\nCompany: {job.company}\nDescription: {job.description}\n\nCandidate Profile:\n{candidate_profile}"

        try:
            result = await generate_structured_response(
                prompt=prompt,
                system_instruction=system_instruction,
                response_model=RankingResult
            )
            return result
        except Exception as e:
            logger.error(f"Ranking failed for job {job.id}: {e}")
            return RankingResult(score=0, is_relevant=False, reasoning=str(e))
