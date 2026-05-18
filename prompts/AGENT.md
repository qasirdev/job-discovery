# Prompts Management & Engineering Standards Index

This directory contains the versioned system prompts, contract schemas, and changelogs for all agents in the AI-Powered Job Discovery monorepo.

---

## 🎨 AI Prompt Engineering Standards

All prompts comply with the following standards sourced from OpenAI Prompt Guidance (GPT-5.x) and Anthropic Claude Prompting Best Practices (Claude Opus 4.x / Sonnet 4.x).

### 1. Mandatory XML System Prompt Structure
Every system prompt must explicitly use the following tags to scope its concerns:

```xml
<role>
  Precise agent identity. No vague persona definitions or hand-wavy descriptions.
</role>
<context>
  All required background knowledge, including long documents or historical context, placed before the tasks.
</context>
<instructions>
  Ordered, numbered, imperative instructions defining exactly what the agent should execute.
</instructions>
<constraints>
  Hard prohibitions, guardrails, and adversarial injection defenses.
</constraints>
<output_format>
  The exact JSON schema or structure required for the response.
</output_format>
<example>
  A realistic representation of inputs and expected outputs matching the output_format exactly.
</example>
```

### 2. Reasoning Effort per Agent
We calibrate the reasoning tier of each model based on the complexity of its operational domain:

| Agent | Source ID | Reasoning Effort | Rationale |
|---|---|---|---|
| **LinkedIn Agent** | `linkedin` | Low | DOM extraction and static keyword matching |
| **JobServe Agent** | `jobserve` | Low | DOM extraction and static keyword matching |
| **Ranking Agent** | `ranking` | Medium | Cosine similarity + cross-encoder reranking |
| **RAG Agent** | `rag` | High | CV alignment and personalised recommendations |
| **Cover Letter Agent** | `cover-letter` | Medium | Playbook generation under static templates |
| **Security Agent** | `security` | High | Adversarial payload and prompt injection defense |
| **Orchestrator Agent** | `orchestrator` | X-High | Long-horizon Temporal workflow coordination |

---

## 🔄 Prompt Versioning & Contracts

We use **Semantic Versioning** for prompts (e.g. `v1.0.0`). Every prompt subdirectory must contain:
1. `CONTRACT.md` — The strict schema-based SLA, containing:
   - Target model pin and version
   - Reasoning effort configuration
   - Maximum output tokens and expected token budget
   - Permitted tools
   - Eval set reference
2. `CHANGELOG.md` — Complete version log documenting updates.
3. `system.md` — The live system instruction file.
4. `skills.md` — (Scraper-specific) Specialized domain capability rules.
5. `tools.md` — Allowlisted tools and functions the agent may call.
6. `guardrails.md` — Specific safety, error-recovery, and anti-injection instructions.
