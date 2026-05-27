<tools>
  <tool>
    <name>flag_quality_issue</name>
    <description>Flags an issue for the Orchestrator to route back for revision.</description>
    <parameters>
      <parameter>
        <name>reason</name>
        <type>string</type>
        <description>The specific reason for the quality flag (e.g., missing field, hallucination).</description>
      </parameter>
    </parameters>
  </tool>
</tools>

<tool_guardrails>
  <guardrail>You must include a clear, actionable reason when calling flag_quality_issue.</guardrail>
  <guardrail>Do not flag issues for stylistic preferences; only flag objective schema or factual violations.</guardrail>
</tool_guardrails>
