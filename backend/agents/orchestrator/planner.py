import json
import time
from pydantic import BaseModel, Field
from ...llm.client import generate_structured_response, token_usage_ctx
from ...schemas import AgentResultEnvelope, AgentMetadata, AgentEscalation
from ...logging_config import get_logger

logger = get_logger(__name__)

class ExecutionStep(BaseModel):
    step_number: int = Field(description="Order of execution")
    agent_id: str = Field(description="The canonical ID of the agent to route to")
    action_description: str = Field(description="What this step will accomplish")
    required_inputs: list[str] = Field(description="List of inputs required from previous steps")

class ExecutionPlan(BaseModel):
    goal: str = Field(description="The primary objective")
    steps: list[ExecutionStep] = Field(description="Sequential execution plan")
    is_valid: bool = Field(description="True if the plan is logically sound and maps to registered agents")

class OrchestratorPlanner:
    """
    Implements the 'Reason' phase of the ReAct pattern for the Orchestrator.
    Decomposes goals into sequential multi-agent execution steps.
    """
    
    async def create_plan(self, goal: str, available_agents: list[str]) -> AgentResultEnvelope:
        logger.info(f"OrchestratorPlanner generating execution plan for goal: {goal}")
        
        system_instruction = (
            "You are the Orchestrator Planner. Decompose the user's goal into a sequential execution plan "
            "using only the tools/agents provided. Ensure that required inputs for later steps are generated "
            "by earlier steps."
        )
        
        prompt = (
            f"Goal: {goal}\n"
            f"Available Agents: {json.dumps(available_agents)}\n"
            "Create a valid execution plan."
        )
        
        start_time = time.time()
        try:
            result = await generate_structured_response(
                prompt=prompt,
                system_instruction=system_instruction,
                response_model=ExecutionPlan,
                agent_id="orchestrator"
            )
            duration = time.time() - start_time
            
            return AgentResultEnvelope(
                agent_id="orchestrator_planner",
                canonical_role="planner",
                status="success" if result.is_valid else "needs_review",
                result=result.model_dump(),
                metadata=AgentMetadata(
                    execution_ms=int(duration * 1000),
                    tokens_used=token_usage_ctx.get(),
                    model_used="claude-3-5-sonnet-20240620",
                    prompt_version=None
                ),
                escalation=AgentEscalation(
                    reason="invalid_plan_schema",
                    target_agent="orchestrator",
                    context="Planner generated an invalid step sequence"
                ) if not result.is_valid else None
            )
            
        except Exception as e:
            logger.error(f"Planner failed: {e}")
            duration = time.time() - start_time
            return AgentResultEnvelope(
                agent_id="orchestrator_planner",
                canonical_role="planner",
                status="failure",
                result=ExecutionPlan(goal=goal, steps=[], is_valid=False).model_dump(),
                metadata=AgentMetadata(
                    execution_ms=int(duration * 1000),
                    tokens_used=token_usage_ctx.get(),
                    model_used="unknown"
                ),
                escalation=AgentEscalation(reason=str(e), target_agent="orchestrator")
            )
