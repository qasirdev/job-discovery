# Orchestrator Agent Contract

- **Model:** claude-sonnet-4-6
- **Reasoning Effort:** xhigh
- **Max Tokens:** 64000
- **Temperature:** 0
- **Permitted Tools:** `[start_workflow, retry_activity, route_to_dlq, checkpoint_state]`
- **Expected Token Budget:** ~12000 tokens per orchestration run
  - *Cost Note:* The xhigh reasoning effort significantly increases cost. Please budget accordingly and monitor token usage so the cost governance agent can alert if exceeded by > 20%.
- **Eval Set Reference:** `evals/orchestrator/eval-set-v1.json`
