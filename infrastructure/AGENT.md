# AGENT.md — Infrastructure & CI/CD

## Role
This directory governs all Cloud-Native Engineering, Infrastructure as Code (IaC), and Continuous Integration/Continuous Deployment (CI/CD) pipelines for the AI-Powered Job Discovery platform.

## Architecture

- **Primary Cloud**: Azure Container Apps (`terraform/azure/`)
- **Secondary/Fallback Cloud**: AWS ECS Fargate (`terraform/aws/`)
- **Container Strategy**: Single Docker container via Supervisor (MVP 1), migrating to distributed containers (MVP 3).
- **Deployment Manifests**: Helm charts (`helm/job-discovery/`) for potential Kubernetes transitions.

## CI/CD Pipeline Steps

The GitHub Actions pipeline (`.github/workflows/ci.yml`) must include:
1. Linting & Type Checking
2. Testing (Unit & Integration)
3. Prompt Regression Tests (DeepEval) & Ragas retrieval eval
4. Docker Builds & Cosign Image Signing
5. Terraform Validate + Plan
6. Terraform Apply (with manual approval gate via `production` environment)

## Rules
- All infrastructure must be managed via Terraform. No manual clicking in cloud consoles.
- Secrets must NEVER be hardcoded. Use Azure Key Vault or AWS Secrets Manager and inject at runtime via secret references.
- Docker images must be cryptographically signed using Cosign.
