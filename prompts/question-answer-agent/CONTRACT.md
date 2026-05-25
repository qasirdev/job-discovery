# CONTRACT.md — Question Answer Agent

## Target Model
Claude 3.5 Sonnet / GPT-4o

## Model Version Pinned
openrouter/anthropic/claude-3-5-sonnet

## Reasoning Effort
high

## Max Output Tokens
1024

## Temperature
0.0

## Permitted Tools
- None

## Expected Token Budget
~500 tokens per invocation

## Eval Set Reference
evals/question-answer-agent/eval-set-v1.json

## Backward Compatibility
v1.x.x prompts are compatible with v1.0.0 eval set.
Breaking changes increment the major version.

## Last Regression Run
2026-05-25 — all evals passed
