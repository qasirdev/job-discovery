# Learning: Step 1.1 - Monorepo Initialization

## Learning Objectives
- Understand the foundational structure of a monorepo for a modern AI-powered full-stack application.
- Learn the purpose of environment templates (`.env.example`) and version control ignoring (`.gitignore`).
- Understand how a root `AGENT.md` acts as a central index for AI agents and developers to navigate project standards and workflow rules.

## Technical Details
- **`.env.example`**: Serves as a template for required environment variables. It ensures that any new developer or deployment environment knows exactly what secrets and configurations are needed without exposing actual sensitive data in version control.
- **`.gitignore`**: Prevents unnecessary files (like `node_modules/`, Python cache files, and local `.env` secrets) from being committed to the Git repository. This keeps the repository clean and secure.
- **Root `AGENT.md`**: In an AI-native project, documentation is structured to guide autonomous agents. The root `AGENT.md` doesn't contain all rules but acts as an index pointing to specific concern-based `.md` files (like `backend/AGENT.md` or `docs/ARCHITECTURE.md`). It establishes strict workflow rules (e.g., "Plan mode", "Done gate") that govern how changes are implemented.
