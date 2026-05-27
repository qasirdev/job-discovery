from pydantic import BaseModel, Field
from typing import Literal

class AgentMetadata(BaseModel):
    execution_ms: int = Field(description="Total execution time in milliseconds")
    tokens_used: int = Field(description="Total tokens consumed (mocked in MVP 1)")
    quality_score: float | None = Field(default=None, description="Quality/Confidence score (MVP 2)")
    model_used: str = Field(description="The model or engine used (e.g., 'playwright', 'gpt-4o')")
    prompt_version: str | None = Field(default=None, description="Version of the prompt template used")

class AgentEscalation(BaseModel):
    reason: str | None = Field(default=None)
    target_agent: str = Field(default="orchestrator")
    context: str | None = Field(default=None)

class AgentResultEnvelope(BaseModel):
    agent_id: str = Field(description="The ID of the agent that produced this result")
    canonical_role: Literal["doer", "planner", "tool_operator", "learner", "critic", "supervisor", "presenter"] = Field(description="The agent's canonical role")
    status: Literal["success", "failure", "needs_review"] = Field(description="Execution status")
    result: dict = Field(description="The actual payload data produced by the agent")
    metadata: AgentMetadata = Field(description="Execution telemetry")
    escalation: AgentEscalation | None = Field(default=None, description="Escalation payload if status is failure or needs_review")
