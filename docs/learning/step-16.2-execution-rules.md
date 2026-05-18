# Learning: Step 16.2 - Execution Rules

## Learning Objectives
- Understand how to establish strict, unbreakable rules for a codebase.
- Learn why "ReAct" (Reasoning and Acting) loops are critical for autonomous AI agents.

## Technical Details
- **Execution Rules**: The `EXECUTION-RULES.md` file serves as the system's "constitution". By explicitly forbidding anti-patterns (e.g., pseudo-code, mock metrics) and mandating processes (e.g., verification gates), it ensures high quality across a sprawling project.
- **The ReAct Loop**: Autonomous agents often drift or hallucinate if left unchecked. The ReAct loop formalizes stopping points: the agent must *plan* (reason), *implement* (act), and *verify* (observe) before moving to the next step. This deterministic approach drastically reduces error rates.
