# evals/ — Prompt Regression Evaluation Framework

**MVP:** 1.1  
**Tickets:** JD-E7 (Eval Framework), JD-37 (Runner), JD-38 (DeepEval + Ragas), JD-39 (CI step)

---

## Overview

This directory contains evaluation fixtures for all AI agents in the Job Discovery platform.  
The evaluation framework runs in two modes:

| Mode | When | What runs | LLM required |
|---|---|---|---|
| `--fast` | Every PR and push | Schema-only field-level checks | No |
| Full | Push to `main` only | DeepEval (AnswerRelevancy, Faithfulness) + Ragas (context_precision, context_recall) | Yes |

---

## Directory Structure

```
evals/
├── README.md                      # This file
├── eval_report.json               # Latest eval report (written by run_evals.py)
├── linkedin-agent/
│   └── eval-set-v1.json           # Ground-truth eval fixtures for the LinkedIn scraper
└── jobserve-agent/
    └── eval-set-v1.json           # Ground-truth eval fixtures for the JobServe scraper
```

Each new agent added to `prompts/` MUST have a corresponding `evals/{agent}/eval-set-v1.json`.  
The CONTRACT.md in each prompt folder references the eval set.

---

## Eval Fixture Format

Every `eval-set-v1.json` is a JSON array of test cases:

```json
[
  {
    "input": "<div><h1>Job Title</h1>...</div>",
    "expected_output": {
      "title": "Job Title",
      "company": "Company Name",
      "location": "Remote, UK",
      "description": "Full job description text.",
      "source": "linkedin"
    }
  }
]
```

### Required fields (all must be present and non-empty)

| Field | Type | Description |
|---|---|---|
| `title` | string | Extracted job title |
| `company` | string | Extracted company name |
| `location` | string | Extracted location |
| `description` | string | Full extracted job description |
| `source` | string | Must match agent name (e.g. `linkedin`, `jobserve`) |

---

## Thresholds

| Metric | Threshold | Notes |
|---|---|---|
| Schema pass rate | 100% | All required fields present and non-empty |
| Agent pass rate gate | ≥ 80% | Fraction of cases that pass all checks |
| DeepEval AnswerRelevancy | ≥ 0.70 | Full mode only |
| DeepEval Faithfulness | ≥ 0.70 | Full mode only |
| Ragas context_precision | ≥ 0.70 | Full mode only — blocks deployment if below |
| Ragas context_recall | ≥ 0.70 | Full mode only — blocks deployment if below |

---

## Running Evaluations Locally

```bash
# Fast mode (schema-only — no API keys needed)
PYTHONPATH=. uv run --project backend python -m backend.admin.run_evals --all --fast

# Specific agent, fast mode
PYTHONPATH=. uv run --project backend python -m backend.admin.run_evals --agent linkedin --fast

# Full mode (requires OPENAI_API_KEY or ANTHROPIC_API_KEY)
PYTHONPATH=. uv run --project backend python -m backend.admin.run_evals --all

# Full mode for one agent
PYTHONPATH=. uv run --project backend python -m backend.admin.run_evals --agent jobserve
```

Install eval dependencies first:

```bash
cd backend && uv sync --group evals
```

---

## CI Integration (JD-39)

The evaluation runner is integrated into GitHub Actions CI:

- **Every PR / push:** `prompt-regression-fast` job in `ci.yml` runs `--all --fast`. Blocks merge if schema compliance fails.
- **Push to `main` only:** `prompt-regression-full` job runs full DeepEval + Ragas. Blocks deployment if quality thresholds drop.

---

## Adding Evals for a New Agent

1. Create the directory: `evals/{agent-name}/`
2. Add `eval-set-v1.json` with ≥ 5 representative test cases
3. Update `prompts/{agent-name}/CONTRACT.md` → `Eval Set Reference` field
4. Verify locally: `python -m backend.admin.run_evals --agent {agent-name} --fast`

---

## eval_report.json Schema

```json
{
  "linkedin-agent": {
    "total": 5,
    "passed": 5,
    "pass_rate": 1.0,
    "agent_passed": true,
    "fast_mode": true,
    "evaluated_at": "2026-05-25T17:00:00+00:00",
    "cases": [
      {
        "case_number": 1,
        "passed": true,
        "errors": [],
        "deepeval_scores": {}
      }
    ]
  }
}
```
