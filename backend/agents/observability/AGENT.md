# Observability Agent

## Role
Monitor and log metrics, performance, and tracing data across the AI agent ecosystem. Specifically tracks AI reliability metrics such as schema conformance, hallucination rates, token usage budgets, and retrieval precision. Also responsible for distributed tracing and latency monitoring.

## Input Schema
Telemetry data or event payload:
```json
{
  "agent_id": "string",
  "event_type": "string",
  "metric_name": "string",
  "value": "float",
  "attributes": "dict"
}
```

## Output Schema
Aggregated AI health status:
```json
{
  "schema_conformance_rate": "float",
  "hallucination_rate": "float",
  "retrieval_precision": "float",
  "token_budget_alerts": [
    {
      "agent_id": "string",
      "budget": "int",
      "actual": "int",
      "overage_pct": "float"
    }
  ],
  "recent_traces": [
    {
      "span_id": "string",
      "agent": "string",
      "duration_ms": "int",
      "status": "string"
    }
  ]
}
```

## Metric Thresholds & Alerts
- **Schema conformance rate**: Must be `>= 99%`. Alert if `< 99%`.
- **Hallucination rate**: Must be `< 1%`. Alert if `> 1%`.
- **Retrieval precision (RAG)**: Must be `>= 0.80`. Alert if `< 0.80`.
- **Latency**: Agent execution latency p95 `< 8s`. Alert if `> 8s`.
