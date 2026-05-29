import time
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from ..base import BaseAgent
from ..telemetry import trace_agent_run
from ...schemas.agent_envelope import AgentResultEnvelope, AgentMetadata, AgentEscalation
from ...logging_config import get_logger
from ...llm.client import generate_structured_response
from temporalio import workflow, activity
from datetime import timedelta

logger = get_logger(__name__)

class CompanyResearch(BaseModel):
    sentiment: str
    tech_stack: List[str]
    culture_signals: List[str]

class QuestionBankItem(BaseModel):
    question: str
    difficulty: str  # easy | medium | hard
    suggested_answer: str

class InterviewPrepOutput(BaseModel):
    company_research: CompanyResearch
    question_bank: List[QuestionBankItem]

class InterviewPrepAgent(BaseAgent):
    agent_id = "interview_prep"
    canonical_role = "learner"
    display_name = "Interview Preparation Agent"

    def __init__(self):
        self.system_prompt_path = Path(__file__).parent.parent.parent.parent / "prompts" / "interview_prep" / "system.md"

    def _load_prompt(self, path: Path) -> str:
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Prompt {path} not found.")
            return "You are the Interview Preparation Intelligence Agent."

    async def _search_web_for_company(self, company_name: str) -> str:
        # Mock web search tool for company research (JD-92)
        logger.info(f"Executing web search tool for company: {company_name}")
        # In a real scenario, this would call Serper/Tavily/etc.
        return f"Recent news for {company_name}: Strong quarterly earnings, focus on AI scaling, positive engineering culture."

    def _make_company_slug(self, company_name: str) -> str:
        """Generate a URL-safe slug from company name for DB keying."""
        return re.sub(r"[^a-z0-9]+", "-", company_name.lower()).strip("-")

    @trace_agent_run("interview_prep", "run")
    async def run(self, request_data: Dict[str, Any]) -> AgentResultEnvelope:
        start_time = time.time()
        company_name = request_data.get('company_name', 'Unknown Company')
        job_id = request_data.get('job_id', 'unknown')
        logger.info(f"InterviewPrepAgent starting for company: {company_name}, job_id: {job_id}")

        try:
            # 1. Execute Tool: Web Search
            web_research = await self._search_web_for_company(company_name)
            request_data['web_research'] = web_research

            # 2. Execute RAG-based answer generation (ReAct Answer Phase)
            system_instruction = self._load_prompt(self.system_prompt_path)
            prompt = f"Interview Request Context (including web research):\n{json.dumps(request_data, indent=2)}\n\nPlease research and generate the interview pack."
            
            result = await generate_structured_response(
                prompt=prompt,
                system_instruction=system_instruction,
                response_model=InterviewPrepOutput,
                agent_id=self.agent_id
            )

            execution_ms = int((time.time() - start_time) * 1000)
            
            # JD-119: Expose question bank for Orchestrator to route to Q&A agent.
            # The question_bank is stored in AgentResultEnvelope.result["question_bank"]
            # so the Orchestrator can inject it into the Q&A agent as cross-agent context.
            # In production this would also be persisted to the `interview_questions` table
            # (keyed by job_id + company_name_slug) for durable retrieval.
            company_slug = self._make_company_slug(company_name)
            logger.info(json.dumps({
                "event": "interview_questions_generated",
                "job_id": job_id,
                "company_name_slug": company_slug,
                "question_count": len(result.question_bank),
            }))
            
            return AgentResultEnvelope(
                agent_id=self.agent_id,
                canonical_role=self.canonical_role,
                status="success",
                result={
                    **result.model_dump(),
                    # Explicit top-level key so Orchestrator can extract without schema introspection
                    "question_bank_for_qa_agent": [q.model_dump() for q in result.question_bank],
                    "company_name_slug": company_slug,
                    "job_id": job_id,
                },
                metadata=AgentMetadata(
                    execution_ms=execution_ms,
                    tokens_used=1500, # Approx token usage
                    model_used="openrouter/anthropic/claude-3-opus",
                    prompt_version="v1.0.0",
                )
            )
        except Exception as e:
            logger.error(f"InterviewPrepAgent failed: {str(e)}")
            execution_ms = int((time.time() - start_time) * 1000)
            return AgentResultEnvelope(
                agent_id=self.agent_id,
                canonical_role=self.canonical_role,
                status="failure",
                result={},
                metadata=AgentMetadata(
                    execution_ms=execution_ms,
                    tokens_used=0,
                    model_used="openrouter/anthropic/claude-3-opus",
                    prompt_version="v1.0.0",
                ),
                escalation=AgentEscalation(
                    reason="Exception occurred during interview prep generation",
                    target_agent="orchestrator",
                    context=str(e)
                )
            )

@activity.defn
async def generate_interview_prep_activity(payload: dict) -> dict:
    agent = InterviewPrepAgent()
    envelope = await agent.run(payload)
    if envelope.status == "failure":
        raise Exception(f"Interview Prep failed: {envelope.escalation.context if envelope.escalation else 'unknown error'}")
        
    job_id_str = payload.get("job_id")
    if job_id_str:
        import uuid
        from sqlalchemy import select
        from sqlalchemy.ext.asyncio import AsyncSession
        from ...models import InterviewPrep, InterviewPrepStatus, InterviewQuestion
        from ...db import _get_engine
        
        job_id = uuid.UUID(job_id_str)
        session_maker = _get_engine()
        if session_maker:
            async with session_maker() as session:
                try:
                    result = await session.execute(select(InterviewPrep).where(InterviewPrep.job_id == job_id))
                    ip = result.scalar_one_or_none()
                    if not ip:
                        ip = InterviewPrep(job_id=job_id, status=InterviewPrepStatus.generating)
                        session.add(ip)
                        await session.flush()
                        
                    ip.status = InterviewPrepStatus.ready
                    ip.company_research = envelope.result.get("company_research")
                    
                    question_bank = envelope.result.get("question_bank_for_qa_agent", [])
                    ip.questions = [q["question"] for q in question_bank]
                    
                    iqs_to_delete = (await session.execute(select(InterviewQuestion).where(InterviewQuestion.interview_prep_id == ip.id))).scalars().all()
                    for existing_iq in iqs_to_delete:
                        await session.delete(existing_iq)
                        
                    for q_data in question_bank:
                        iq = InterviewQuestion(
                            job_id=job_id,
                            interview_prep_id=ip.id,
                            question_text=q_data["question"],
                            difficulty_rating=q_data["difficulty"],
                            suggested_answer=q_data.get("suggested_answer")
                        )
                        session.add(iq)
                        
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    logger.error(f"Failed to save interview prep: {e}")
                    raise

    return envelope.result

@workflow.defn
class InterviewPrepWorkflow:
    @workflow.run
    @trace_agent_run("interview_prep", "run")
    async def run(self, payload: dict) -> dict:
        result = await workflow.execute_activity(
            generate_interview_prep_activity,
            payload,
            start_to_close_timeout=timedelta(seconds=180),
            schedule_to_start_timeout=timedelta(seconds=15),
            retry_policy=workflow.RetryPolicy(maximum_attempts=2, initial_interval=timedelta(seconds=5), backoff_coefficient=2.0)
        )
        return result


