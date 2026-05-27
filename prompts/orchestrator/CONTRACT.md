# CONTRACT.md — Orchestrator Agent

## Target Model
Claude Opus 4

## Model Version Pinned
claude-opus-4

## Reasoning Effort
X-High

## Max Output Tokens
4096

## Temperature
0.0

## Permitted Tools
- `start_workflow`
- `retry_activity`
- `route_to_dlq`
- `checkpoint_state`
- `invoke_critic`
- `parse_envelope`

## Expected Token Budget
~12000 tokens per orchestration run (warning: xhigh reasoning significantly increases cost — budget accordingly)

## Eval Set Reference
evals/orchestrator/eval-set-v1.json

## Backward Compatibility
v1.x.x prompts are compatible with v1.0.0 eval set.
Breaking changes increment the major version.

## Last Regression Run
2026-05-27 — all evals passed
