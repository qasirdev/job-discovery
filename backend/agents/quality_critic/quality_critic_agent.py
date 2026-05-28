from pathlib import Path
import time
from pydantic import BaseModel, Field
from ...schemas import AgentResultEnvelope, AgentMetadata, AgentEscalation
from ...llm.client import generate_structured_response
from ...logging_config import get_logger
from ..base import BaseAgent
from ..observability.observability_agent import ObservabilityAgent

logger = get_logger(__name__)

class QualityCriticResult(BaseModel):
    is_passing: bool = Field(description="True if the output meets quality standards with no hallucinations")
    score: float = Field(description="Quality score from 0.0 to 1.0")
    feedback: list[str] = Field(description="List of specific feedback, errors, or hallucinations detected")

class QualityCriticAgent(BaseAgent):
    """Evaluates output from Doer agents for hallucinations and schema correctness."""
    agent_id = "quality_critic"
    canonical_role = "critic"
    display_name = "Quality Critic"

    def __init__(self) -> None:
        self.system_prompt_path = Path(__file__).parent.parent.parent.parent / "prompts" / "quality_critic" / "system.md"
        
    def _load_prompt(self, path: Path) -> str:
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Prompt {path} not found.")
            return "You are a Quality Critic agent. Verify the output is free of hallucinations."

    async def evaluate_output(self, context_data: str, agent_output: str, retrieval_precision: float | None = None) -> AgentResultEnvelope:
        logger.info("Quality Critic Agent evaluating output")
        
        if retrieval_precision is not None and retrieval_precision < 0.80:
            logger.warning(f"RAG Agent retrieval precision ({retrieval_precision}) is below 0.80. Alerting critic.")
            
            obs_agent = ObservabilityAgent()
            obs_agent.record_metric("quality_critic_rag_alert", 1, {"precision": retrieval_precision})
            
            context_data = f"[WARNING: Context retrieval precision was low: {retrieval_precision}. Please be extra vigilant about hallucinations and verify facts.]\n\n" + context_data

        system_instruction = self._load_prompt(self.system_prompt_path)
        prompt = f"Context Data:\n{context_data}\n\nAgent Output:\n{agent_output}"

        start_time = time.time()
        try:
            result = await generate_structured_response(
                prompt=prompt,
                system_instruction=system_instruction,
                response_model=QualityCriticResult,
                agent_id="quality_critic"
            )
            duration = time.time() - start_time
            
            # According to the protocol, if the critic fails the output, the status is "needs_review"
            status = "success" if result.is_passing else "needs_review"
            
            return AgentResultEnvelope(
                agent_id="quality_critic",
                canonical_role="critic",
                status=status,
                result=result.model_dump(),
                metadata=AgentMetadata(
                    execution_ms=int(duration * 1000),
                    tokens_used=0,
                    model_used="claude-3-5-sonnet-20240620",
                    quality_score=result.score
                ),
                escalation=AgentEscalation(reason="quality_below_threshold", target_agent="orchestrator", context=str(result.feedback)) if status == "needs_review" else None
            )
        except Exception as e:
            logger.error(f"Quality Critic failed: {e}")
            duration = time.time() - start_time
            return AgentResultEnvelope(
                agent_id="quality_critic",
                canonical_role="critic",
                status="failure",
                result=QualityCriticResult(is_passing=False, score=0.0, feedback=[str(e)]).model_dump(),
                metadata=AgentMetadata(
                    execution_ms=int(duration * 1000),
                    tokens_used=0,
                    model_used="unknown"
                ),
                escalation=AgentEscalation(reason=str(e), target_agent="orchestrator")
            )
