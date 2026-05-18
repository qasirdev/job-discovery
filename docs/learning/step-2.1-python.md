# Learning: Step 2.1 - Python Environment Setup

## Learning Objectives
- Learn modern Python dependency management using `pyproject.toml`.
- Understand the role of `AGENT.md` at the sub-system level.

## Technical Details
- **`pyproject.toml` and `uv`**: The `pyproject.toml` file is the modern standard for defining Python package metadata and dependencies. We use `uv` as the package manager because it is built in Rust, resolving dependencies incredibly fast compared to older tools.
- **Sub-system Standards (`backend/AGENT.md`)**: While the root `AGENT.md` holds global workflow rules, the `backend/AGENT.md` holds technical standards specific to the FastAPI backend (e.g., cursor-based pagination, Pydantic typing, schema-first design). This modular documentation ensures AI agents contextually load only the standards relevant to the code they are modifying.
