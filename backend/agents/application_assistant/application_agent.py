import time
import json
from pathlib import Path
from typing import Any, Dict
from pydantic import BaseModel
from ..base import BaseAgent
from ..telemetry import trace_agent_run
from ...schemas.agent_envelope import AgentResultEnvelope, AgentMetadata, AgentEscalation
from ...logging_config import get_logger
from ...llm.client import generate_structured_response
from temporalio import workflow, activity
from datetime import timedelta

logger = get_logger(__name__)

class CompoundPackage(BaseModel):
    summary: str
    cover_letter_ref: str
    interview_highlights: list[str]
    company_culture_notes: str

class ApplicationAssistantAgent(BaseAgent):
    agent_id = "application_assistant"
    canonical_role = "presenter"
    display_name = "Application Assistant Agent"

    def __init__(self):
        self.system_prompt_path = Path(__file__).parent.parent.parent.parent / "prompts" / "application_assistant" / "system.md"

    def _load_prompt(self, path: Path) -> str:
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Prompt {path} not found.")
            return "You are the Application Assistant Agent. Synthesise inputs into a compound application package."

    @trace_agent_run("application_assistant", "run")
    async def run(self, application_data: Dict[str, Any]) -> AgentResultEnvelope:
        start_time = time.time()
        job_id = application_data.get('job_id', 'unknown')
        logger.info(f"ApplicationAssistantAgent starting for job_id: {job_id}")

        try:
            # 1. Reason Phase: Validate required inputs before acting
            missing_fields = []
            if 'cover_letter' not in application_data:
                missing_fields.append('cover_letter')
            if 'interview_prep' not in application_data:
                missing_fields.append('interview_prep')
                
            if missing_fields:
                logger.warning(f"ApplicationAssistant missing required context: {missing_fields}")
                # We could escalate back to the orchestrator to gather missing data, 
                # but for MVP 4 we will proceed with what we have and let the LLM synthesize it.
                application_data['synthesize_warnings'] = f"Missing data: {', '.join(missing_fields)}"

            # 2. Act Phase: Synthesize package
            system_instruction = self._load_prompt(self.system_prompt_path)
            prompt = f"Application Context Data:\n{json.dumps(application_data, indent=2)}\n\nPlease synthesize this into the required compound package."
            
            result = await generate_structured_response(
                prompt=prompt,
                system_instruction=system_instruction,
                response_model=CompoundPackage,
                agent_id=self.agent_id
            )

            execution_ms = int((time.time() - start_time) * 1000)
            
            return AgentResultEnvelope(
                agent_id=self.agent_id,
                canonical_role=self.canonical_role,
                status="success",
                result={"compound_package": result.model_dump()},
                metadata=AgentMetadata(
                    execution_ms=execution_ms,
                    tokens_used=1000, # Approx token usage
                    model_used="openrouter/anthropic/claude-3-5-sonnet",
                    prompt_version="v1.0.0",
                )
            )
        except Exception as e:
            logger.error(f"ApplicationAssistantAgent failed: {str(e)}")
            execution_ms = int((time.time() - start_time) * 1000)
            return AgentResultEnvelope(
                agent_id=self.agent_id,
                canonical_role=self.canonical_role,
                status="failure",
                result={},
                metadata=AgentMetadata(
                    execution_ms=execution_ms,
                    tokens_used=0,
                    model_used="openrouter/anthropic/claude-3-5-sonnet",
                    prompt_version="v1.0.0",
                ),
                escalation=AgentEscalation(
                    reason="Exception occurred during package synthesis",
                    target_agent="orchestrator",
                    context=str(e)
                )
            )

@activity.defn
async def execute_assistant_activity(payload: dict) -> dict:
    agent = ApplicationAssistantAgent()
    envelope = await agent.run(payload)
    if envelope.status == "failure":
        raise Exception(f"Application Assistant failed: {envelope.escalation.context if envelope.escalation else 'unknown error'}")
    
    # Save results to DB
    app_id_str = payload.get("application_id")
    if app_id_str:
        import uuid
        from sqlalchemy import select
        from sqlalchemy.ext.asyncio import AsyncSession
        from ...models import Application
        from ...db import _get_engine
        
        app_id = uuid.UUID(app_id_str)
        session_maker = _get_engine()
        if session_maker:
            async with session_maker() as session:
                try:
                    result = await session.execute(select(Application).where(Application.id == app_id))
                    app = result.scalar_one_or_none()
                    if app:
                        # Workaround since models might not map JSON fields directly if they are frozen
                        # But Application model is standard SQLAlchemy mapping.
                        app.compound_package = envelope.result.get("compound_package")
                        await session.commit()
                except Exception as e:
                    await session.rollback()
                    logger.error(f"Failed to save application compound package: {e}")
                
    return envelope.result

@workflow.defn
class ApplicationAssistantWorkflow:
    @workflow.run
    @trace_agent_run("application_assistant", "run")
    async def run(self, payload: dict) -> dict:
        result = await workflow.execute_activity(
            execute_assistant_activity,
            payload,
            start_to_close_timeout=timedelta(seconds=120),
            schedule_to_start_timeout=timedelta(seconds=10),
            retry_policy=workflow.RetryPolicy(maximum_attempts=2)
        )
        return result

