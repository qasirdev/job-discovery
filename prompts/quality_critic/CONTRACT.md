# CONTRACT.md — Quality Critic Agent

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
- `flag_quality_issue`

## Expected Token Budget
~4000 tokens per invocation (Input ~3000, Output ~1000)

## Eval Set Reference
evals/quality_critic/eval-set-v1.json

## Backward Compatibility
v1.x.x prompts are compatible with v1.0.0 eval set.
Breaking changes increment the major version.

## Last Regression Run
2026-05-27 — all evals passed
