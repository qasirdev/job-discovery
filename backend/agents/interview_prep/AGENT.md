# Interview Preparation Agent — AGENT.md

## Role

**Canonical Role**: Doer, Learner, Presenter

The Interview Preparation Agent fetches live company intelligence and generates a comprehensive interview preparation pack — including company research, a question bank with difficulty ratings, and suggested answers. It acts as a **Learner** (gathering external research), a **Doer** (generating the prep materials), and an inline **Presenter** (formatting the final pack for the user).

Its research output (`CompanyResearch`) feeds downstream into the Application Assistant (Dedicated Presenter) via the Learner Feedback Protocol defined in `proposal-v4-structure.md`.

---

## Execution Model

The Interview Preparation Agent runs as a **Temporal activity** on the `interview-prep-tasks` queue, registered in `backend/agents/interview_prep/worker.py`.

### Temporal Queue Configuration
- **Task Queue**: `interview-prep-tasks`
- **Start-to-Close Timeout**: 180 seconds (web search + LLM synthesis is the longest agent operation)
- **Schedule-to-Start Timeout**: 15 seconds
- **Retry Policy**: max_attempts=2, initial_interval=5s, backoff_coefficient=2.0

### 504 Avoidance Strategy
The Orchestrator MUST invoke this agent **asynchronously via Temporal** and return a `202 Accepted` with a `workflow_id` for polling. Direct synchronous calls are prohibited. The 180-second timeout covers:
- Web search API call (~5-10s)
- RAG context retrieval (~2-4s)
- LLM synthesis of company research + question bank (~60-120s at Claude Opus 4)

### Feature Flag Gate
The endpoint `POST /api/v1/interview-prep/{job_id}` is gated by `FEATURE_INTERVIEW_PREP_AGENT=true` in `settings.py`. When false, returns HTTP 503 with a descriptive message (graceful degradation per JD-121).

---

## Learner Feedback Loop

Per `proposal-v4-structure.md`, this agent's research output feeds downstream agents:

| Produces | Consumed By | Storage | Access Pattern |
|---|---|---|---|
| `CompanyResearch` record | Application Assistant (Presenter) | PostgreSQL `company_research` table (keyed by `company_name_slug`) | `GET /api/v1/company-research?slug={slug}` or Orchestrator direct inject |
| Interview question bank | Q&A Agent (cross-reference) | PostgreSQL `interview_questions` table | Orchestrator routes questions to Q&A for follow-up answers |

**Feedback Protocol:**
1. Orchestrator invokes this agent **first** in any workflow requiring company intelligence
2. Agent returns `AgentResultEnvelope` with `result.company_research` and `result.question_bank`
3. Orchestrator injects `learner_context` into the Application Assistant's `<context>` prompt section
4. Application Assistant MUST NOT re-fetch company data — it uses the injected context

---

## Web Search Tool

The agent uses a mock web search tool (`_search_web_for_company`) in MVP 4. Production integration targets Serper or Tavily APIs:

```python
# Tool: web_search(query: str) -> str
# Returns: Recent news, engineering blog posts, Glassdoor sentiment signals
# Called with: f"site:glassdoor.com {company_name} culture review"
```

**SSRF allowlist** (`settings.ALLOWED_EXTERNAL_DOMAINS`): Must include `serper.dev`, `api.tavily.com`, `glassdoor.com` for production web search. No other domains permitted.

---

## Input Schema

```json
{
  "job_id": "uuid",
  "company_name": "string",
  "job_title": "string | null",
  "job_description": "string | null",
  "web_research": "string | null   // injected by agent internally after tool call"
}
```

---

## Output Schema

Returns a standard `AgentResultEnvelope` with:

```json
{
  "company_research": {
    "sentiment": "string — overall Glassdoor/public sentiment",
    "tech_stack": ["string"],
    "culture_signals": ["string — e.g. 'remote-first', 'fast-paced', 'strong mentorship'"]
  },
  "question_bank": [
    {
      "question": "string",
      "difficulty": "easy | medium | hard",
      "suggested_answer": "string"
    }
  ]
}
```

**Token Budget**: ~13,000 tokens total (input ~5,000 + output ~8,000) per `proposal-v4-structure.md` model matrix.

**Primary Model**: Claude Opus 4 | **Fallback**: GPT-5

---

## Escalation Policy

| Condition | Action |
|---|---|
| Web search API unavailable | Skip web research step; log warning; proceed with LLM knowledge only; note in `synthesize_warnings` |
| Company name not resolvable | Proceed with generic industry research; note gap |
| LLM synthesis failure | Return `AgentResultEnvelope(status="failure")` with `escalation.reason="tool_failure"`, target Orchestrator |
| Quality Critic rejection (after 2 cycles) | Escalate to DLQ with full revision history |

**Security Agent override**: Prompt injection in company name or job description → immediate block, no retry.

---

## Quality Gate

Output must pass Quality Critic review:
- **Factual accuracy**: Company tech stack must be consistent with publicly available data
- **Comprehensive coverage**: Minimum 5 interview questions with difficulty distribution (≥2 medium, ≥1 hard)
- **Question relevance**: Questions must reference the `job_description` if provided
- **max_revision_cycles**: 2

---

## ReAct Pattern Implementation

| Phase | Action |
|---|---|
| **Reason** | Parse job context; plan which tools to call (web search, RAG lookup) |
| **Act** | Execute web search; load CV embeddings from RAG if available |
| **Observe** | Validate company research coherence; check question bank coverage |
| **Answer** | Return structured `InterviewPrepOutput` as `AgentResultEnvelope.result` |

---

## References

- `proposal-v4-structure.md` → Learner Feedback Loops, Token Budget Enforcement, Model Selection Matrix
- `prompts/interview_prep/CONTRACT.md` — prompt version and eval set reference
- `evals/interview_prep/eval-set-v1.json` — eval coverage
- `backend/agents/interview_prep/worker.py` — Temporal worker registration
- `backend/agents/AGENT.md` — multi-agent rules and AgentResultEnvelope contract
- `docs/OBSERVABILITY.md` — retrieval precision monitoring (fed by this agent)
