# CONTRACT.md — Orchestrator Agent

## Target Model
Claude 3.5 Sonnet / GPT-4o

## Model Version Pinned
openrouter/anthropic/claude-3-5-sonnet

## Reasoning Effort
xhigh

## Max Output Tokens
64000

## Temperature
0.0

## Permitted Tools
- `start_workflow`
- `retry_activity`
- `route_to_dlq`
- `checkpoint_state`

## Expected Token Budget
~12000 tokens per invocation

## Eval Set Reference
evals/orchestrator-agent/eval-set-v1.json

## Backward Compatibility
v1.x.x prompts are compatible with v1.0.0 eval set.
Breaking changes increment the major version.

## Last Regression Run
2026-05-25 — all evals passed
