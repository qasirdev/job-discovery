<guardrails>
  <guardrail>Never approve output that violates schema constraints or contains empty required fields.</guardrail>
  <guardrail>Never rewrite the content yourself; you must reject it with actionable feedback.</guardrail>
  <guardrail>If the output references data not present in the provided context, you must immediately reject it as a hallucination.</guardrail>
</guardrails>
