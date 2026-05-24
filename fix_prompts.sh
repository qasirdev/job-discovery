#!/bin/bash

# Remove incorrect files
rm -f prompts/ranking-agent/{guardrails.md,skills.md,tools.md}
rm -f prompts/rag-agent/{guardrails.md,skills.md,tools.md}
rm -f prompts/cover-letter-agent/{guardrails.md,skills.md,tools.md}
rm -f prompts/question-answer-agent/{guardrails.md,skills.md}
rm -f prompts/security-agent/{guardrails.md,skills.md,tools.md}
rm -f prompts/orchestrator/{guardrails.md,skills.md,tools.md}

# Touch correct files to create them
touch prompts/ranking-agent/{scoring.md,reranking.md,filtering.md}
touch prompts/rag-agent/{retrieval.md,embeddings.md,personalization.md}
touch prompts/cover-letter-agent/{tone.md,generation.md,templates.md}

