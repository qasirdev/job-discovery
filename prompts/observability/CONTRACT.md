# CONTRACT.md — Observability Agent

## Target Model
Claude Sonnet 4

## Model Version Pinned
openrouter/anthropic/claude-3-5-sonnet

## Reasoning Effort
Medium

## Max Output Tokens
1000

## Temperature
0.0

## Permitted Tools
- `get_metrics`
- `raise_alert`

## Expected Token Budget
~4000 tokens per invocation (Input ~3000, Output ~1000)

## Eval Set Reference
evals/observability/eval-set-v1.json

## Backward Compatibility
v1.x.x prompts are compatible with v1.0.0 eval set.
Breaking changes increment the major version.

## Last Regression Run
Never
