# Filtering Rules — LinkedIn Agent

This document defines the prompt-based pre-filtering heuristics applied to crawled jobs before deep ranking.

## Seniority Heuristics
- **seniority**: We target senior roles.
- **Allowed Seniority Keywords**:
  - `senior`
  - `lead`
  - `principal`
  - `architect`
- **Action**: Exclude roles that explicitly focus on junior, intern, entry, mid-level or general associate positions without these senior tags.

## Tech Stack Heuristics
- **stack**: Role must involve the target technical stack or close equivalents.
- **Primary Tech Stack**:
  - Python (FastAPI, Flask, Django)
  - JavaScript / TypeScript (Next.js, React, Node.js)
  - Cloud / DevOps (Azure, AWS, Docker, Kubernetes)
  - AI / ML / LLMs (pgvector, RAG, OpenAI, Anthropic, LangChain, Temporal, LiteLLM)
- **Action**: Exclude roles completely unrelated to these engineering domains (e.g. Java-only, C#/.NET-only, PHP, non-technical, or marketing roles).

## Contract / Engagement Heuristics
- **contract**: Role should prioritize contract/freelance engagements.
- **Contract Type Keywords**:
  - `contract`
  - `contractor`
  - `freelance`
  - `outside ir35`
  - `temporary`
- **Action**: Flag or prioritize outside IR35 or contract roles, while filtering out permanent-only requirements when contract-only constraints are enabled.
