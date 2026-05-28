# Application Assistant Agent — AGENT.md

## Role

**Canonical Role**: Doer, Presenter

The Application Assistant Agent is the **Dedicated Presenter** introduced in Post-MVP 3. It synthesises the outputs of all upstream agents — Cover Letter, Interview Prep, and RAG company research — into a single, coherent **compound application package** with consistent formatting, tone, and cross-referencing. It is the final step in the multi-agent application workflow before delivery to the user.

This agent implements the **Presenter** role from the AI Agent Teams framework. It does NOT re-fetch data; all upstream context must be pre-assembled by the Orchestrator before invocation.

---

## Execution Model

The Application Assistant Agent runs as a **Temporal activity** on the `application-assistant-tasks` queue, registered in `backend/agents/application_assistant/worker.py`.

### Temporal Queue Configuration
- **Task Queue**: `application-assistant-tasks`
- **Start-to-Close Timeout**: 120 seconds (covers LLM synthesis latency)
- **Schedule-to-Start Timeout**: 10 seconds (alerts if no worker picks up within 10s)
- **Retry Policy**: max_attempts=2, no_wait_for_cancellation=True

### 504 Avoidance Strategy
The Orchestrator must invoke this agent **asynchronously via Temporal** and return a `202 Accepted` to the API layer with a `workflow_id` for polling. Direct synchronous HTTP calls to this agent are prohibited to prevent HTTP gateway 504 timeouts on the compound synthesis operation.

---

## Presenter Pattern (Post-MVP 3)

Per `proposal-v4-structure.md`, the Application Assistant is the **Dedicated Presenter** — the final MVP milestone implementation of the progressive Presenter pattern:

| MVP | Pattern | Implementation |
|---|---|---|
| MVP 1 | Inline Presenter | Each Doer formats its own output as a Pydantic model |
| MVP 2 | Orchestrator-as-Presenter | Orchestrator composes `AgentResultEnvelope.result` |
| **Post-MVP 3** | **Dedicated Presenter** | **This agent** — synthesises all agent outputs into a compound package |

---

## Input Schema

The Orchestrator MUST pre-assemble and inject the following context before invoking this agent:

```json
{
  "job_id": "uuid",
  "company_name": "string",
  "cover_letter": {
    "content": "string",
    "tone": "string",
    "word_count": "int"
  },
  "interview_prep": {
    "company_research": {
      "sentiment": "string",
      "tech_stack": ["string"],
      "culture_signals": ["string"]
    },
    "question_bank": [
      {
        "question": "string",
        "difficulty": "string",
        "suggested_answer": "string"
      }
    ]
  },
  "rag_context": {
    "cv_summary": "string",
    "skill_match_score": "float",
    "matched_skills": ["string"]
  },
  "synthesize_warnings": "string | null"
}
```

**Feedback Protocol (Learner → Presenter):**
1. Orchestrator invokes RAG and Interview Prep agents **first**
2. Learner results are passed as `rag_context` and `interview_prep` fields above
3. This agent MUST NOT re-fetch any data already provided — prevents redundant API calls

---

## Output Schema

Returns a standard `AgentResultEnvelope` with the following `result` payload:

```json
{
  "compound_package": {
    "summary": "string — executive summary of the application (2-3 sentences)",
    "cover_letter_ref": "string — reference ID or inline content",
    "interview_highlights": ["string — top 3-5 talking points"],
    "company_culture_notes": "string — culture alignment notes for the candidate"
  }
}
```

**Token Budget**: ~10,000 tokens total (input ~5,000 + output ~5,000) per `proposal-v4-structure.md` model matrix.

**Primary Model**: Claude Sonnet 4 | **Fallback**: GPT-4o

---

## Escalation Policy

| Condition | Action |
|---|---|
| Missing `cover_letter` field | Log warning, proceed with available data; note gap in `synthesize_warnings` |
| Missing `interview_prep` field | Log warning, proceed with available data |
| LLM synthesis failure | Return `AgentResultEnvelope(status="failure")` with `escalation.reason="tool_failure"`, target Orchestrator |
| Quality Critic rejection (after 2 revision cycles) | Escalate to DLQ with full revision history |

**Security Agent override**: Any prompt injection detected in compound package output → immediate block, no retry.

---

## Quality Gate

Output must pass Quality Critic review before delivery to the user:
- **Schema conformance**: All required fields present and correctly typed
- **Factual consistency**: Interview highlights must reference data from `rag_context` — no hallucinated skills
- **Tone consistency**: Cover letter tone must match throughout the compound package
- **max_revision_cycles**: 2 (as per Critic Revision Protocol in `proposal-v4-structure.md`)

---

## References

- `proposal-v4-structure.md` → Presenter Role, Learner Feedback Loops, Token Budget, Model Selection Matrix
- `prompts/application_assistant/CONTRACT.md` — prompt version and eval set reference
- `evals/application_assistant/eval-set-v1.json` — eval coverage
- `backend/agents/application_assistant/worker.py` — Temporal worker registration
- `backend/agents/AGENT.md` — multi-agent rules and AgentResultEnvelope contract
