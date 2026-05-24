import sys

with open("docs/tasks/todo.md", "a") as f:
    f.write("\n## Active Plan — MVP 2 Security & Orchestration (JD-E10) [YOLO Mode]\n- [ ] Step 1: Enhance `security_agent.py` and add OWASP middleware in `main.py` (JD-49).\n- [ ] Step 2: Implement Temporal workflow orchestrator in `orchestrator_agent.py` (JD-50).\n- [ ] Step 3: Implement Circuit Breakers per-agent (JD-51).\n- [ ] Step 4: Create Admin DLQ routes and frontend admin panel (JD-52).\n- [ ] Step 5: Update `docs/SECURITY.md`.\n")

with open("docs/tasks/lessons.md", "a") as f:
    f.write("\n| 2026-05-24 | Incomplete Security/Orchestrator layers | Initial MVP 1 scaffolding of security and orchestrator agents lacked Temporal workflow definition, OWASP middleware, and DLQ frontend integrations. | Always cross-reference Epic task constraints (e.g. Temporal, extra=\"forbid\") before marking MVP 2 agent tasks as done. |\n")
