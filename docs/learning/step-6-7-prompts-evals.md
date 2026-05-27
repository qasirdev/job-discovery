# Learning: Prompt Engineering Infrastructure & Eval Framework

**Phase 2: MVP 1.1**
**Steps Covered**: 6.1 - 6.6, 7.1 - 7.3

## Learning Objectives
What a beginner developer should learn from the code and configuration introduced in these steps:
- **Prompt Organization**: How to treat prompts as code. Moving away from monolithic prompt strings buried inside backend functions to a dedicated, version-controlled `prompts/` directory.
- **Agent Roles**: Understanding the concept of "Reasoning Effort" (low, medium, high, xhigh) and how to pick the right LLM (e.g., GPT-4o-mini vs. Claude Opus 4) based on the task's cognitive load.
- **LLM Contracts**: Why every prompt needs a `CONTRACT.md` that strictly defines Token Budgets, temperature parameters, and permitted tools, acting as an SLA for the LLM.
- **Evaluation Frameworks**: The difference between a deterministic field-level check (schema validation) and heuristic LLM-based metrics (like DeepEval's AnswerRelevancy or Faithfulness).
- **CI/CD Integration**: How to use reusable GitHub Action workflows (`workflow_call`) to prevent deployment if an AI agent's performance drops below an acceptable quality threshold (Prompt Regression).

## Technical Details

### 1. The `prompts/` Directory Architecture
Instead of storing prompt text as variables in `linkedin_agent.py`, the project maintains a separation of concerns by keeping prompts in a root `prompts/` directory. 
Each agent has 6 strictly enforced files (e.g., `system.md`, `skills.md`, `tools.md`, `guardrails.md`, `CONTRACT.md`, and `CHANGELOG.md`). This allows prompt engineers to tune LLM behavior independently of backend API deployments. The agent code simply loads these files at runtime.

### 2. The `CONTRACT.md` SLA
The `CONTRACT.md` file guarantees predictable operational characteristics. For instance, the LinkedIn Agent's contract specifies `Temperature: 0.0` (because it outputs deterministic structured JSON data) and `Target Model: GPT-4o-mini` (because DOM extraction is a "Low" reasoning task). This contract also documents the `Expected Token Budget` (~2500 tokens), which acts as a circuit-breaker threshold in the backend to prevent runaway LLM costs.

### 3. Reusable CI/CD Workflows (`eval-regression.yml`)
To evaluate our prompts, we run `backend/admin/run_evals.py`. In our CI pipeline, we use GitHub Actions reusable workflows. By extracting the evaluation steps into `.github/workflows/eval-regression.yml`, our main `ci.yml` file becomes much cleaner. It uses the `uses: ./.github/workflows/eval-regression.yml` syntax. 

We utilize two modes:
- `--fast`: Runs on every PR. It does not call any external LLM APIs; it simply verifies that the test fixtures (the `expected_output` schemas) are structurally valid.
- `default (Full)`: Runs when code is pushed to `main`. It evaluates the actual output of the agent using DeepEval's Faithfulness and AnswerRelevancy metrics, ensuring that any prompt tweaks haven't degraded output quality below the 80% pass-rate gate.
