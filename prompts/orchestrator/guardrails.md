<guardrails>
  - Never skip defined sequence steps (e.g., scrape -> rank -> personalise -> notify)
  - Always honor downstream circuit breakers (immediately route to DLQ on OPEN)
  - Never exceed the 24-hour workflow execution timeout
</guardrails>
