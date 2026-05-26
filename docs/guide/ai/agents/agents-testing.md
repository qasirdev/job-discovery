# AI Agents Testing Guide

This guide explains how we evaluate and verify the behavior of AI agents, particularly ensuring that they respect constraints defined in files like `guardrails.md`. Our system treats prompt instructions as code and uses a rigorous evaluation framework powered by `DeepEval` and `Ragas`.

## 1. How Testing Works During a PR Merge

When you open a Pull Request (PR) or push changes to the repository, the GitHub Actions CI pipeline (`.github/workflows/ci.yml`) automatically runs verification checks:

### Fast Schema Validation (Blocks PRs)
The `prompt-regression-fast` job runs on every PR. It verifies the structural integrity of all prompt files—including `guardrails.md`, `system.md`, and others—to ensure no XML tags are broken and the prompt contracts are valid. 
**If `guardrails.md` or any other prompt file is malformed, this job will fail and block the PR from being merged.**

### Full Behavioral Evaluation (Post-Merge / Main Branch)
Jobs like `prompt-regression-full` and `eval-regression-rag` run full LLM regression tests against agents. These jobs simulate queries using LLM APIs to ensure the agents still respect the constraints defined in `guardrails.md` (e.g., checking for hallucinations, testing tone, ensuring the agent doesn't overstep boundaries). If an agent starts violating the guardrails, metrics like `faithfulness` and `answer_relevancy` will drop below allowed thresholds.

## 2. How to Test Locally Before Merging

If you make changes to `guardrails.md` or any other prompt file, you should test your changes locally using the evaluation runner script before creating a PR.

### Validating Structure and Schema (Fast)
To quickly validate structure and schema without making costly LLM API calls:

```bash
PYTHONPATH=. uv run --project backend python -m backend.admin.run_evals --agent application_assistant --fast
```
*Tip: You can replace `application_assistant` with `all` to run schema validations for all agents.*

### Running a Full Behavioral Evaluation
To run a full behavioral evaluation (testing if the agent respects the new guardrails using actual LLM calls):

```bash
PYTHONPATH=. uv run --project backend python -m backend.admin.run_evals --agent application_assistant
```
*(Note: Full evaluation requires you to have your `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` exported in your terminal).*

## Summary

Our system treats prompt engineering as a rigorous software engineering discipline. The `run_evals.py` script acts as the "unit test" suite for our agents, and the GitHub CI pipeline strictly enforces these tests to ensure regressions and guardrail violations are caught early.
