# Observability Agent — AGENT.md

## Role

**Canonical Role**: Supervisor, Critic, Learner

The Observability Agent is responsible for continuous monitoring and health checking of the AI ecosystem. It acts as a **Learner** (ingesting telemetry and metrics), a **Critic** (evaluating schema conformance, hallucination rates, and precision against strict baselines), and a **Supervisor** (enforcing token budgets and routing critical alerts).

Its aggregated output feeds the Grafana Dashboard via Prometheus and Loki, providing a unified `AI Health Status` for operations.

---

## Execution Model

The Observability Agent runs as a **periodic background task** via Temporal or standard asyncio scheduling, registered in `backend/agents/observability/worker.py` (or as part of the app lifecycle).

### Execution Configuration
- **Task Scheduling**: Periodic background execution (e.g., every 60 seconds)
- **Start-to-Close Timeout**: 30 seconds
- **Retry Policy**: max_attempts=3, initial_interval=2s, backoff_coefficient=2.0

### 504 Avoidance Strategy
This agent executes asynchronously in the background. It exposes its status via `GET /api/v1/observability/status` directly reading from an in-memory cache or fast DB store, avoiding any LLM processing inline with HTTP requests.

---

## Telemetry & Learner Feedback Pipeline

Per `proposal-v4-structure.md` and `docs/OBSERVABILITY.md`, this agent consumes and produces the following:

| Produces | Consumed By | Storage | Access Pattern |
|---|---|---|---|
| `AI Health Status` | Grafana / Admin Panel (`ObservabilityPanel.tsx`) | Prometheus / Loki / In-Memory | `GET /api/v1/observability/status` |
| Alert Warnings | Orchestrator / Sentry | Structured JSON Logs | Pushed via log stream |

**Feedback Protocol:**
1. Agent pulls telemetry (faithfulness, retrieval_precision, schema_conformance_rate) from internal metric stores.
2. Agent evaluates data against predefined thresholds.
3. If threshold breached, agent generates alerts.
4. Agent returns an `AgentResultEnvelope` containing the summarized health status.

---

## Tool Use

The Observability Agent does not perform web searches. It relies on internal system querying:

```python
# Tool: query_metrics(metric_name: str) -> float
# Returns: The current aggregated value of a given metric
# Tool: get_recent_traces(agent_id: str) -> list
# Returns: Trace latency data for the last N minutes
```

---

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

---

## Output Schema

Returns a standard `AgentResultEnvelope` with:

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

**Token Budget**: ~2,000 tokens per evaluation cycle.
**Primary Model**: GPT-4o-mini | **Fallback**: Claude 3.5 Haiku

---

## Metric Thresholds & Quality Gate

Output must pass internal validation against these thresholds:
- **Schema conformance rate**: Must be `>= 99%`. Alert if `< 99%`.
- **Hallucination rate**: Must be `< 1%`. Alert if `> 1%`.
- **Retrieval precision (RAG)**: Must be `>= 0.80`. Alert if `< 0.80`.
- **Latency**: Agent execution latency p95 `< 8s`. Alert if `> 8s`.

---

## Escalation Policy

| Condition | Action |
|---|---|
| DeepEval Faithfulness < 0.85 | Escalate to Sentry as CRITICAL, log hallucination alert |
| Schema Conformance < 99% | Escalate to Sentry, trigger circuit breaker for offending agent |
| Token Budget Exceeded | Log warning, expose to Prometheus gauge, disable non-critical features if > 150% |
| Telemetry Datastore Offline | Continue running, return degraded status block, use cached thresholds |

---

## ReAct Pattern Implementation

| Phase | Action |
|---|---|
| **Reason** | Parse incoming batch of telemetry payloads; determine which thresholds apply |
| **Act** | Aggregate metrics, query datastore tools if historical context needed |
| **Observe** | Evaluate if metrics breach `docs/OBSERVABILITY.md` guidelines |
| **Answer** | Return structured AI Health Status report |

---

## References

- `docs/proposal-v4-structure.md` → Architecture & Observability agent matrix
- `docs/OBSERVABILITY.md` → Thresholds and routing definitions
- `prompts/observability/CONTRACT.md` — Prompt version and eval set reference
- `evals/observability/eval-set-v1.json` — DeepEval + Ragas test cases
