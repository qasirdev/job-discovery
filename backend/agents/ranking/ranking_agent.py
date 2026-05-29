from pathlib import Path
from jinja2 import Template
import time
import logging
from ...logging_config import get_logger
from ...schemas import Job, RankingResult, AgentResultEnvelope, AgentMetadata, AgentEscalation
from ...llm.client import generate_structured_response
from ..base import BaseAgent
from ..telemetry import trace_agent_run

logger = get_logger(__name__)

class RankingAgent(BaseAgent):
    """Evaluates and scores a job against a professional profile using an 8-step pipeline."""
    agent_id = "ranking"
    canonical_role = "doer"
    display_name = "AI Ranking Engine"

    def __init__(self) -> None:
        self.system_prompt_path = Path(__file__).parent.parent.parent.parent / "prompts" / "ranking" / "system.md"
        self.user_prompt_path = Path(__file__).parent.parent.parent.parent / "prompts" / "ranking" / "user.md"
        
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

    @trace_agent_run("ranking", "evaluate_job")
    async def evaluate_job(self, job: Job, candidate_profile: dict | None = None) -> AgentResultEnvelope:
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

        start_time = time.time()
        try:
            result = await generate_structured_response(
                prompt=prompt,
                system_instruction=system_instruction,
                response_model=RankingResult,
                agent_id="ranking"
            )
            duration = time.time() - start_time
            return AgentResultEnvelope(
                agent_id="ranking",
                canonical_role="doer",
                status="success",
                result=result.model_dump(),
                metadata=AgentMetadata(
                    execution_ms=int(duration * 1000),
                    tokens_used=0,
                    model_used="claude-3-5-sonnet-20240620",
                    prompt_version=None
                )
            )
        except Exception as e:
            logger.error(f"Ranking failed for job {job.id}: {e}")
            duration = time.time() - start_time
            return AgentResultEnvelope(
                agent_id="ranking",
                canonical_role="doer",
                status="failure",
                result=RankingResult(score=0, is_relevant=False, reasoning=str(e)).model_dump(),
                metadata=AgentMetadata(
                    execution_ms=int(duration * 1000),
                    tokens_used=0,
                    model_used="unknown",
                    prompt_version=None
                ),
                escalation=AgentEscalation(reason=str(e), target_agent="orchestrator", context=f"Job ID {job.id}")
            )
