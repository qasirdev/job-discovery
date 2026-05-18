# Learning: Step 2.4 - FastAPI Application

## Learning Objectives
- Understand how to structure the entry point of a FastAPI application.
- Learn the purpose of middleware for global request logging.

## Technical Details
- **FastAPI Initialization**: `main.py` creates the global `app` object. By passing `docs_url` and `openapi_url`, it automatically generates an interactive Swagger UI for the API.
- **Middleware**: The `@app.middleware("http")` decorator injects code before and after every single HTTP request. This is the 2026 standard for observability: instead of manually logging inside every endpoint, the middleware calculates the duration and logs the path, method, and status code universally.
- **In-Memory DB**: For MVP 1, a simple Python dictionary `fake_db` is used to simulate database state. This prevents being blocked on infrastructure (like PostgreSQL) while iterating rapidly on core application logic.
