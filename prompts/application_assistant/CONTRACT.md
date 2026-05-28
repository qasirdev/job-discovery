# CONTRACT.md — Application Assistant Agent

## Target Model
Claude 3.5 Sonnet

## Model Version Pinned
openrouter/anthropic/claude-3-5-sonnet

## Reasoning Effort
high

## Max Output Tokens
8192

## Temperature
0.0  (Temperature=0 is mandatory for all structured outputs - no exceptions without documentation)

## Permitted Tools
- `fetch_job_details`
- `fetch_cover_letter`
- `fetch_interview_prep`
- `fetch_company_research`

## Expected Token Budget
~10000 tokens per invocation

## Eval Set Reference
evals/application_assistant/eval-set-v1.json

## Backward Compatibility
v1.x.x prompts are compatible with v1.0.0 eval set.
Breaking changes increment the major version.

## Last Regression Run
2026-05-28 — all evals passed
