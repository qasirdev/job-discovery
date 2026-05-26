import os
from pathlib import Path
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.common import RetryPolicy
from datetime import timedelta

from ...logging_config import get_logger
from ...llm.client import generate_structured_response
from ...db import get_db

logger = get_logger(__name__)

class ApplicationAssistantOutput(BaseModel):
    next_action: str
    recommended_email_draft: str
    status_update: str

class ApplicationAssistantAgent:
    """Autonomous Job Application Assistant Agent to manage application workflows."""

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.prompts_dir = Path(__file__).parent.parent.parent.parent / "prompts" / "application_assistant"
        self.system_prompt_path = self.prompts_dir / "system.md"

    def _load_prompt(self, path: Path) -> str:
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Prompt {path} not found.")
            return ""

    async def execute_react_loop(self, job_id: str, current_state: str, notes: str) -> Dict[str, Any]:
        """
        Executes a basic ReAct loop to determine the next best action.
        """
        logger.info(f"Running Application Assistant for Job {job_id}")
        system_instruction = self._load_prompt(self.system_prompt_path) or "You are an Autonomous Job Application Assistant Agent."

        prompt = f"Job ID: {job_id}\nApplication State: {current_state}\nNotes: {notes}"
        
        try:
            result = await generate_structured_response(
                prompt=prompt,
                system_instruction=system_instruction,
                response_model=ApplicationAssistantOutput
            )
            response = result.model_dump()
        except Exception as e:
            logger.error(f"Application Assistant failed: {e}")
            # Fallback for YOLO mode if LLM fails
            next_action = "Draft Follow-up Email"
            if current_state == "draft":
                next_action = "Submit Application"
            elif current_state == "applied":
                next_action = "Prepare for Initial Screen"

            response = {
                "next_action": next_action,
                "recommended_email_draft": "Hi hiring team,\n\nI recently applied and wanted to express my continued interest...",
                "status_update": "awaiting_response"
            }
        
        logger.info(f"Application Assistant completed: {response}")
        return response

@activity.defn
async def execute_assistant_activity(payload: dict) -> dict:
    job_id = payload["job_id"]
    current_state = payload["current_state"]
    notes = payload["notes"]
    
    db_gen = get_db()
    db = await db_gen.__anext__()
    try:
        agent = ApplicationAssistantAgent(db)
        return await agent.execute_react_loop(job_id, current_state, notes)
    finally:
        try:
            await db_gen.__anext__()
        except StopAsyncIteration:
            pass

@workflow.defn
class ApplicationAssistantWorkflow:
    @workflow.run
    async def run(self, payload: dict) -> dict:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            backoff_coefficient=2.0,
            maximum_interval=timedelta(seconds=60),
            maximum_attempts=3,
        )
        try:
            return await workflow.execute_activity(
                execute_assistant_activity,
                payload,
                start_to_close_timeout=timedelta(minutes=5),
                retry_policy=retry_policy,
            )
        except Exception as e:
            workflow.logger.error(f"Application Assistant workflow failed: {e}")
            from datetime import datetime
            from ..orchestrator.orchestrator_agent import route_to_dlq
            await workflow.execute_activity(
                route_to_dlq,
                {
                    "workflow_id": workflow.info().workflow_id, 
                    "error": str(e), 
                    "job_id": payload.get("job_id"),
                    "agent": "ApplicationAssistantWorkflow",
                    "created_at": datetime.utcnow().isoformat() + "Z",
                    "retry_count": 0
                },
                start_to_close_timeout=timedelta(seconds=10),
            )
            raise e
