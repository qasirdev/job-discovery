# Learning Step: Prompt File Compliance

## Context
During the execution of Epic 12 (MVP 2 Prompts for AI Agents), a conflict arose between the `docs/proposal-v4-structure.md` and the root `AGENT.md` workflow rules.

## The Conflict
- `docs/proposal-v4-structure.md` explicitly listed custom directories for MVP 2 agents. For example, `ranking-agent/` only listed `CONTRACT.md`, `CHANGELOG.md`, `system.md`, `scoring.md`, `reranking.md`, and `filtering.md`.
- However, `AGENT.md` states: **"When creating a new agent in `prompts/`, you MUST create all 6 files (`CONTRACT.md`, `CHANGELOG.md`, `system.md`, `skills.md`, `tools.md`, `guardrails.md`) adhering to XML format. No exceptions."**

## The Mistake
In an attempt to follow the new structural proposal exactly, the existing `skills.md`, `tools.md`, and `guardrails.md` files were deleted for the MVP 2 agents. This violated the strict "No exceptions" rule in the root `AGENT.md`.

## The Resolution
The missing files were explicitly re-created and populated with their respective XML elements (`<skills>`, `<tools>`, `<guardrails>`) for all six MVP 2 agents (`ranking-agent`, `rag-agent`, `cover-letter-agent`, `question-answer-agent`, `security-agent`, `orchestrator`).

## The Rule
1. **Core Overrides Scaffold**: If a structural scaffold/proposal omits files that the root `AGENT.md` designates as mandatory ("No exceptions"), the `AGENT.md` rule takes precedence. You must create the mandatory files *in addition* to any custom files the proposal suggests (e.g., `scoring.md`).
2. **Never Delete Mandatory Files**: Do not blindly clean up files that belong to the core architecture pattern just because a specific diagram or proposal forgot to draw them.
