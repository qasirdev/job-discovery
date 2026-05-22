# Learning: Step 11 & 12 - Cloud Deploy & Advanced Prompts

## Learning Objectives
- Learn how to use Infrastructure-as-Code (IaC) via Terraform for predictable deployments.
- Understand how to structure Azure Resource Manager (ARM) deployments for containerized AI apps.

## Technical Details

### 1. Terraform State and Modularity
Our deployment infrastructure is located in `infrastructure/terraform/azure/`.
- `main.tf`: Contains the actual resource definitions (Resource Groups, Azure Container Apps, Cosmos DB / Postgres DB definitions).
- `variables.tf`: Parameterizes the deployment so that we can spin up `staging` and `production` environments securely using the exact same codebase, merely injecting different variables via GitHub Actions secrets.
- `outputs.tf`: Exports the generated endpoints (like the backend API URL) so the CI pipeline can pass them down to the Next.js frontend build step.

### 2. Multi-Environment Parity
By strictly enforcing Terraform deployments, we guarantee that our local `docker-compose` environment perfectly maps to the production Azure topology. There is zero drift.
