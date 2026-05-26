# CONTRACT.md — RAG Agent

## Target Model
Claude 3.5 Sonnet / GPT-4o

## Model Version Pinned
claude-3-5-sonnet-20240620 / gpt-4o-2024-05-13

## Reasoning Effort
high

## Max Output Tokens
2048

## Temperature
0.0

## Permitted Tools
- `query_vector_db`

## Expected Token Budget
~2000 tokens per invocation

## Eval Set Reference
evals/rag/eval-set-v1.json

## Backward Compatibility
v1.x.x prompts are compatible with v1.0.0 eval set.
Breaking changes increment the major version.
