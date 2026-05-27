# CONTRACT.md — Question Answer Agent

## Target Model
Claude Sonnet 4

## Model Version Pinned
claude-sonnet-4

## Reasoning Effort
High

## Max Output Tokens
4096

## Temperature
0.0

## Permitted Tools
- None

## Expected Token Budget
~6000 tokens per invocation (Input ~4000, Output ~2000)

## Eval Set Reference
evals/question_answer/eval-set-v1.json

## Backward Compatibility
v1.x.x prompts are compatible with v1.0.0 eval set.
Breaking changes increment the major version.

## Last Regression Run
2026-05-27 — all evals passed
