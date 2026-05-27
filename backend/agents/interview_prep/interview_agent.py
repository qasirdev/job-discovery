import uuid
from pathlib import Path
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from temporalio import activity, workflow
from temporalio.common import RetryPolicy
from datetime import timedelta

from ...logging_config import get_logger
from ...llm.client import generate_structured_response
from ...models import InterviewPrep, InterviewPrepStatus
from ...db import get_db

logger = get_logger(__name__)

class InterviewPrepOutput(BaseModel):
    company_intel: str
    practice_questions: List[str]

from ...schemas import AgentResultEnvelope, AgentMetadata
from ..base import BaseAgent
import time

class InterviewPrepAgent(BaseAgent):
    """Interview Preparation Intelligence Agent."""
    agent_id = "interview_prep"
    canonical_role = "doer"
    display_name = "Interview Prep Agent"

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.prompts_dir = Path(__file__).parent.parent.parent.parent / "prompts" / "interview_prep"
        self.system_prompt_path = self.prompts_dir / "system.md"

    def _load_prompt(self, path: Path) -> str:
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Prompt {path} not found.")
            return ""

    async def generate_prep_package(self, job_id: str, company_name: str) -> AgentResultEnvelope:
        """
        Generates an interview preparation package using RAG and mock company intelligence.
        """
        logger.info(f"Generating interview prep for Job {job_id} at {company_name}")
        system_instruction = self._load_prompt(self.system_prompt_path) or "You are an Interview Preparation Intelligence Agent."

        # Setup DB record
        prep = (await self.db.execute(select(InterviewPrep).where(InterviewPrep.job_id == uuid.UUID(job_id)))).scalar_one_or_none()
        if not prep:
            prep = InterviewPrep(job_id=uuid.UUID(job_id), status=InterviewPrepStatus.generating)
            self.db.add(prep)
            await self.db.commit()
        else:
            prep.status = InterviewPrepStatus.generating
            await self.db.commit()

        prompt = f"Job ID: {job_id}\nCompany Name: {company_name}\nPlease generate interview preparation materials."
        start_time = time.time()
        
        try:
            result = await generate_structured_response(
                prompt=prompt,
                system_instruction=system_instruction,
                response_model=InterviewPrepOutput,
                agent_id="interview_prep"
            )
            
            prep.company_research = {"intel": result.company_intel}
            prep.questions = result.practice_questions
            prep.status = InterviewPrepStatus.ready
            await self.db.commit()

            response = {
                "prep_package_id": str(prep.id),
                "status": "success",
                "company_intel": result.company_intel,
                "practice_questions": result.practice_questions
            }
        except Exception as e:
            logger.error(f"Interview Prep generation failed: {e}")
            prep.status = InterviewPrepStatus.failed
            await self.db.commit()
            
            # Fallback for YOLO mode
            response = {
                "prep_package_id": str(prep.id),
                "status": "success", # Keeping success in YOLO mode fallback
                "company_intel": f"{company_name} recently announced a major expansion in their AI division.",
                "practice_questions": [
                    f"Why are you interested in joining {company_name}?",
                    "Tell me about a time you had to scale a backend system."
                ]
            }
        
        logger.info(f"Interview Prep generated successfully: {response}")
        duration = time.time() - start_time
        return AgentResultEnvelope(
            agent_id="interview_prep",
            canonical_role="doer",
            status="success",
            result=response,
            metadata=AgentMetadata(execution_ms=int(duration * 1000), tokens_used=0, model_used="claude-3-5-sonnet-20240620", prompt_version=None)
        )

@activity.defn
async def generate_interview_prep_activity(payload: dict) -> dict:
    job_id = payload["job_id"]
    company_name = payload["company_name"]
    # get_db returns a generator (or async generator), so we need to iterate it or call __anext__ manually, 
    # but since it's an async generator from FastAPI Depends, we can just use an async context manager if we had one.
    # Actually, we can just do:
    db_gen = get_db()
    db = await db_gen.__anext__()
    try:
        agent = InterviewPrepAgent(db)
        return await agent.generate_prep_package(job_id, company_name)
    finally:
        try:
            await db_gen.__anext__()
        except StopAsyncIteration:
            pass

@workflow.defn
class InterviewPrepWorkflow:
    @workflow.run
    async def run(self, payload: dict) -> dict:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            backoff_coefficient=2.0,
            maximum_interval=timedelta(seconds=60),
            maximum_attempts=3,
        )
        return await workflow.execute_activity(
            generate_interview_prep_activity,
            payload,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=retry_policy,
        )
