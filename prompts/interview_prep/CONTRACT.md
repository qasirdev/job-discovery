# CONTRACT.md — Interview Prep Agent

## Target Model
Claude 3 Opus / GPT-5

## Model Version Pinned
openrouter/anthropic/claude-3-opus

## Reasoning Effort
xhigh

## Max Output Tokens
8192

## Temperature
0.0  (Temperature=0 is mandatory for all structured outputs - no exceptions without documentation)

## Permitted Tools
- `search_web`
- `scrape_glassdoor`
- `fetch_rag_context`

## Expected Token Budget
~13000 tokens per invocation

## Eval Set Reference
evals/interview_prep/eval-set-v1.json

## Backward Compatibility
v1.x.x prompts are compatible with v1.0.0 eval set.
Breaking changes increment the major version.

## Last Regression Run
2026-05-28 — all evals passed
