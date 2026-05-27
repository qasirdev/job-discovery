<guardrails>
  - Never skip defined sequence steps (e.g., scrape -> rank -> personalise -> notify)
  - Always honor downstream circuit breakers (immediately route to DLQ on OPEN)
  - Never exceed the 24-hour workflow execution timeout
  - Enforce the Critic Revision Protocol: strictly limit retries to max 2 when Doer agent outputs are flagged as needs_review
  - Enforce Learner Feedback Loops: never bypass injecting learner context if available
  - Context window discipline: strictly parse `AgentResultEnvelope` and budget appropriately
</guardrails>
