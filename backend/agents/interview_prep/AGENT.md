# Interview Preparation Agent

- **Canonical Role**: Doer, Learner, Presenter
- **Role**: Fetches company research (Glassdoor sentiment, funding, tech stack, culture signals) and generates comprehensive interview prep materials and a question bank.
- **Input**: `InterviewRequest` (Contains `job_id`, `company_name`)
- **Output**: `AgentResultEnvelope` (Contains `CompanyResearch` and `InterviewPack`)
- **Escalation Policy**: Escalates to Orchestrator on failure.
- **Quality Gate**: Output must pass Quality Critic review for factual accuracy and comprehensive coverage.
