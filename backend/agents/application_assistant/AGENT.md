# Application Assistant Agent

- **Canonical Role**: Doer, Presenter
- **Role**: Synthesises cover letter, interview prep, and company research into a compound application package with consistent formatting, tone, and cross-referencing.
- **Input**: `ApplicationData` (Contains `job_id`, `cover_letter_id`, `interview_prep_id`, `company_research`)
- **Output**: `AgentResultEnvelope` (Contains synthesized application documents)
- **Escalation Policy**: Escalates to Orchestrator on failure.
- **Quality Gate**: Output must pass Quality Critic review for schema conformance and factual consistency.
