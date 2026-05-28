import time
import json
from pathlib import Path
from typing import Any, Dict, List
from pydantic import BaseModel
from ..base import BaseAgent
from ...schemas.agent_envelope import AgentResultEnvelope, AgentMetadata, AgentEscalation
from ...logging_config import get_logger
from ...llm.client import generate_structured_response

logger = get_logger(__name__)

class CompanyResearch(BaseModel):
    sentiment: str
    tech_stack: List[str]
    culture_signals: List[str]

class QuestionBankItem(BaseModel):
    question: str
    difficulty: str
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

    async def run(self, request_data: Dict[str, Any]) -> AgentResultEnvelope:
        start_time = time.time()
        company_name = request_data.get('company_name', 'Unknown Company')
        logger.info(f"InterviewPrepAgent starting for company: {company_name}")

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
            
            return AgentResultEnvelope(
                agent_id=self.agent_id,
                canonical_role=self.canonical_role,
                status="success",
                result=result.model_dump(),
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
