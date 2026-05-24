# GUARDRAILS — Orchestrator Agent

This file describes operation safety boundaries for the Orchestrator Agent.

## 1. Safety Intercept
- Do not let a high-ranking job description bypass the security filter if it has been marked as malicious or unsafe.

## 2. Resource Boundaries
- Limit loop counts and execution retry steps to prevent circular calling dependencies between child agents.
