# CONTRACT.md — RAG Agent

## Target Model
Claude 3 Haiku / GPT-4o-mini

## Model Version Pinned
openrouter/anthropic/claude-3-haiku

## Reasoning Effort
medium

## Max Output Tokens
4096

## Temperature
0.0

## Permitted Tools
- `retrieve_context`
- `query_embeddings`

## Expected Token Budget
~2000 tokens per invocation

## Eval Set Reference
evals/rag-agent/eval-set-v1.json

## Backward Compatibility
v1.x.x prompts are compatible with v1.0.0 eval set.
Breaking changes increment the major version.

## Last Regression Run
2026-05-18 — all evals passed
