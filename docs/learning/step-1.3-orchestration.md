# Learning: Step 1.3 - Local Orchestration

## Learning Objectives
- Understand how Docker Compose simplifies running multi-container or complex single-container setups for local development.
- Learn about automated health checks in Docker setups.

## Technical Details
- **Docker Compose**: The `docker-compose.yml` allows developers to build and run the application with a single `docker-compose up` command, instead of remembering long `docker build` and `docker run` flags. It maps ports (`80:80`) and automatically loads variables from `.env`.
- **Health Checks**: The `healthcheck` block ensures the orchestration system knows if the application is actually ready to receive traffic. It uses `curl` to hit the FastAPI `/health` endpoint (proxied through Nginx). This is an industry-standard 2026 best practice for reliable deployments.
