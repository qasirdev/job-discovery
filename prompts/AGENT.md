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

| Agent | Source ID | Canonical Role | Reasoning Effort | Rationale |
|---|---|---|---|---|
| **LinkedIn Agent** | `linkedin` | Doer, Tool Operator | Low | DOM extraction and static keyword matching |
| **JobServe Agent** | `jobserve` | Doer, Tool Operator | Low | DOM extraction and static keyword matching |
| **Ranking Agent** | `ranking` | Doer | Medium | Cosine similarity + cross-encoder reranking |
| **RAG Agent** | `rag` | Tool Operator, Learner | High | CV alignment and personalised recommendations |
| **Cover Letter Agent** | `cover-letter` | Doer, Tool Operator | Medium | Playbook generation under static templates |
| **Q&A Agent** | `question-answer` | Doer, Tool Operator, Learner | High | RAG-powered contextual Q&A on job listings |
| **Security Agent** | `security` | Critic (Safety) | High | Adversarial payload and prompt injection defense |
| **Quality Critic Agent** | `quality-critic` | Critic (Quality) | Medium | Hallucination detection, factual consistency, schema conformance |
| **Orchestrator Agent** | `orchestrator` | Planner, Supervisor | X-High | Long-horizon Temporal workflow coordination + goal decomposition |
| **Interview Prep Agent** | `interview-prep` | Doer, Learner, Presenter | X-High | Company research + interview intelligence synthesis |

---

## 🔄 Prompt Versioning & Contracts

We use **Semantic Versioning** for prompts (e.g. `v1.0.0`). 

> [!CAUTION]
> **CRITICAL RULE FOR CREATING NEW AGENTS**: 
> If you create a new agent in the `prompts/` folder, it **MUST** automatically include ALL 6 of the following files, strictly following the XML schema. This is an architectural invariant. Do not just create `system.md` and skip the rest.

Every prompt subdirectory MUST contain exactly these 6 files:
1. `CONTRACT.md` — The strict schema-based SLA, containing:
   - Target model pin and version
   - Reasoning effort configuration
   - Maximum output tokens and expected token budget
   - Permitted tools
   - Eval set reference
2. `CHANGELOG.md` — Complete version log documenting updates.
3. `system.md` — The live system instruction file (using the `<role>`, `<context>`, `<instructions>`, `<constraints>`, `<output_format>`, `<example>` XML tags).
4. `skills.md` — Specialized domain capability rules using `<skills>` XML tags.
5. `tools.md` — Allowlisted tools and functions the agent may call using `<tools>` XML tags.
6. `guardrails.md` — Specific safety, error-recovery, and anti-injection instructions using `<guardrails>` XML tags.

---

## 📄 Reusable CONTRACT.md Template & Example

Every agent under `prompts/` MUST include a `CONTRACT.md` matching this template and set of fields exactly:

```markdown
# CONTRACT.md — [Agent Name]

## Target Model
[e.g. Claude 3.5 Sonnet / GPT-4o]

## Model Version Pinned
[e.g. openrouter/anthropic/claude-3-5-sonnet]

## Reasoning Effort
[low | medium | high | xhigh]

## Max Output Tokens
[e.g. 4096]

## Temperature
0.0  (Temperature=0 is mandatory for all structured outputs - no exceptions without documentation)

## Permitted Tools
- [Tool 1 Name]
- [Tool 2 Name]

## Expected Token Budget
~[Expected Tokens] tokens per invocation

## Eval Set Reference
evals/[Agent-folder]/eval-set-v1.json

## Backward Compatibility
v[X].x.x prompts are compatible with v[X].0.0 eval set.
Breaking changes increment the major version.

## Last Regression Run
[YYYY-MM-DD] — all evals passed
```
