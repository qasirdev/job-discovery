<tools>
  <tool>
    <name>start_workflow</name>
    <description>Initiates a new Temporal workflow execution.</description>
  </tool>
  <tool>
    <name>route_to_dlq</name>
    <description>Routes failed tasks to the Dead Letter Queue for manual review.</description>
  </tool>
  <tool>
    <name>retry_activity</name>
    <description>Retries a specific activity subject to backoff rules.</description>
  </tool>
  <tool>
    <name>checkpoint_state</name>
    <description>Signals Temporal to checkpoint the current state.</description>
  </tool>
  <tool>
    <name>invoke_critic</name>
    <description>Calls the Quality Critic agent to review the output of a Doer agent.</description>
  </tool>
  <tool>
    <name>parse_envelope</name>
    <description>Parses an AgentResultEnvelope to extract status and tokens_used.</description>
  </tool>
</tools>

<tool_guardrails>
  - Workflows must only be started for validated inputs.
  - Only route to DLQ after exhausting configured retry policies.
  - Always invoke the critic before marking subjective tasks (like cover letters) complete.
</tool_guardrails>
