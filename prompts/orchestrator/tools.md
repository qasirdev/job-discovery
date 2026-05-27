<tools>
  <tool>
    <name>start_workflow</name>
    <description>Initiates a new Temporal workflow execution.</description>
  </tool>
  <tool>
    <name>route_dlq</name>
    <description>Routes failed tasks to the Dead Letter Queue for manual review.</description>
  </tool>
</tools>

<tool_guardrails>
  - Workflows must only be started for validated inputs.
  - Only route to DLQ after exhausting configured retry policies.
</tool_guardrails>
