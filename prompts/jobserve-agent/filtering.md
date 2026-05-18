# Filtering Rules — JobServe Agent

This document defines the prompt-based pre-filtering heuristics applied to crawled jobs before deep ranking.

## Seniority Heuristics
- **seniority**: We target senior roles.
- **Allowed Seniority Keywords**:
  - `senior`
  - `lead`
  - `principal`
  - `architect`
- **Action**: Filter out junior, graduate, trainee, mid-level, or administrative positions.

## Tech Stack Heuristics
- **stack**: Role must involve the target technical stack or close equivalents.
- **Primary Tech Stack**:
  - Python (FastAPI, Flask, Django)
  - JavaScript / TypeScript (Next.js, React, Node.js)
  - Cloud / DevOps (Azure, AWS, Docker, Kubernetes)
  - AI / ML / LLMs (pgvector, RAG, OpenAI, Anthropic, LangChain, Temporal, LiteLLM)
- **Action**: Exclude roles completely unrelated to these engineering domains.

## Contract / Engagement Heuristics
- **contract**: Prioritize contract engagements, especially outside IR35.
- **Contract Type Keywords**:
  - `contract`
  - `contractor`
  - `freelance`
  - `outside ir35`
  - `day rate`
- **Action**: Filter out permanent-only roles if contract-only mode is active, or score them lower.
