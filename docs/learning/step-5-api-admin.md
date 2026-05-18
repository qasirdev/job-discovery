# Learning: Step 5.1 & 5.2 - Versioned APIs and Factor XII

## Learning Objectives
- Learn the concept of Cursor-Based Pagination vs Offset Pagination.
- Understand Twelve-Factor App principles specifically regarding Admin Processes.

## Technical Details
- **Cursor Pagination**: Unlike offset pagination (which skips rows and becomes extremely slow on large database tables), cursor-based pagination uses a pointer (the "cursor") to fetch the exact next batch of data. `routers/jobs.py` sets up the schema for this to ensure high performance in MVP 2.
- **Factor XII (Admin Processes)**: The Twelve-Factor methodology states that database migrations, console scripts, and one-off administrative tasks should run in an identical environment to the regular long-running processes (like the web server). By creating `backend/admin/seed_keywords.py`, we execute these tasks via `uv run` inside the exact same Docker container environment, guaranteeing consistency.
