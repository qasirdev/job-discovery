# Learning: Step 1.2 - Docker Setup

## Learning Objectives
- Understand the concept of multi-stage Docker builds.
- Learn how to serve a static Next.js frontend and reverse-proxy a FastAPI backend using Nginx in a single container.
- Understand how `supervisord` manages multiple processes inside a single container for an MVP architecture.

## Technical Details
- **Multi-stage Docker Builds**: The `Dockerfile` uses multiple `FROM` instructions. The first stage (`frontend-builder`) compiles the Next.js React app into static files. The second stage (`runtime`) only copies those compiled files. This keeps the final image lightweight by excluding Node.js and all frontend build tools.
- **Nginx (`nginx.conf`)**: Nginx is configured to serve the static frontend files directly. For any request matching `/api/*`, it acts as a reverse proxy, forwarding the request to the internal FastAPI server running on `localhost:8000`.
- **Supervisor (`supervisord.conf`)**: Docker normally runs only one process (the `CMD`). Since we need Nginx, FastAPI, and Alembic migrations running, we use Supervisor as the primary process. Supervisor reads its config to start and monitor these three background tasks, ensuring the MVP runs entirely within one cohesive container.
