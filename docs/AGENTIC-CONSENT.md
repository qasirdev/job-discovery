# Agentic Consent Model

This document outlines the Agentic Consent Model for the Job Discovery platform, ensuring that autonomous agent actions remain transparent, accountable, and explicitly authorized by the user.

## 1. Dynamic Living Contracts

Traditional static consent (e.g., ticking a box during onboarding) is insufficient for agentic workflows where LLMs make dynamic decisions on behalf of users. We implement **Living Contracts**:

- **Granular Approvals**: Users approve specific agent capabilities (e.g., "Submit Application on my behalf") rather than blanket platform access.
- **Transaction Boundaries**: Every high-stakes action initiated by an agent must be bounded by a specific transaction (e.g., applying to a single job vs. auto-applying to 10 jobs).

## 2. Policy-Driven Governance & Time Constraints

To prevent unbounded autonomy while balancing convenience, the platform uses policy-driven governance:

- **Time-Bound Consent**: Consent is granted for a specific window of time (e.g., "Allow autonomous applications for the next 4 hours").
- **Auto-Revocation**: Once the time constraint is met, the consent token expires natively in the backend without requiring further user action.
- **Revocability**: Users can immediately terminate any active Living Contract via the Consent Dashboard.

## 3. Mitigating Consent Fatigue

To avoid overwhelming users with repetitive Just-In-Time (JIT) prompts:

1. **Batching**: Non-critical decisions can be aggregated and approved in bulk.
2. **Contextual Defaults**: If a user approves a specific transaction pattern (e.g., "Scrape jobs matching 'Senior Frontend'"), subsequent identical background operations within the time limit do not trigger new JIT prompts.
3. **Escalation to JIT**: JIT prompts are strictly reserved for boundary-crossing actions, such as finalizing an application submission or spending API quota.

## 4. System RBAC vs. Agentic Consent

- **System RBAC (Role-Based Access Control)**: Defines what data a user is legally allowed to access within the platform.
- **Agentic Consent**: Defines what *actions* the AI agents are authorized to take using the user's data on their behalf.
  - *Example*: A user has RBAC access to their CV, but the Cover Letter Agent still requires Agentic Consent to use that CV to generate a cover letter and send it to an external API.

## 5. Evaluation Checklist for Agent Autonomy

Before deploying a new autonomous capability, the following checklist must be met:
- [ ] Does the agent action require external API communication? (If yes, requires Consent).
- [ ] Is the data being shared PII or sensitive career information? (If yes, requires Consent).
- [ ] Is the consent request scoped to a specific time window or transaction?
- [ ] Can the user revoke the consent at any time via the Consent Dashboard?
- [ ] Is the action properly logged in the `audit_log` with the consent token ID?
