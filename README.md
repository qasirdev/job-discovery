# AI-Powered Job Discovery Platform

An autonomous, AI-driven backend engine paired with a highly responsive frontend dashboard designed to discover, filter, and score job opportunities based on a hyper-personalized professional profile.

## Features

- **Extensible Scraper Registry**: Factory-pattern based architecture to easily integrate crawlers for LinkedIn, JobServe, and other platforms.
- **RAG-Powered AI Intelligence** *(MVP 2)*: Scores jobs based on professional identity, filtering out irrelevant listings with a highly deterministic framework.
- **Modern Tech Stack**:
  - **Frontend**: Next.js 16 (Static Export), React 19, Tailwind CSS v4.
  - **Backend**: Python 3.14, FastAPI, `uv` for dependency management.
  - **Infrastructure**: Multi-stage Dockerfile governed by Supervisor and Nginx.

## Getting Started

### Option A: Native Development (Hot-Reload)

**1. Run the Backend (FastAPI)**
```bash
cd backend
uv sync
cd ..
uv run --project backend uvicorn backend.main:app --reload --port 8000
```
The API docs will be accessible at: `http://localhost:8000/api/docs`

**2. Run the Frontend (Next.js)**
```bash
cd frontend
npm install
npm run dev
```
The frontend dashboard will be accessible at: `http://localhost:3000`

### Option B: Production-like Containerized Environment

The entire stack is orchestrated via Docker Compose.
```bash
docker compose up -d --build
```
Access the unified dashboard at: `http://localhost`

## Architecture & Engineering Standards

This project adheres strictly to **Twelve-Factor App (2026)** principles and autonomous ReAct loop execution protocols. Please review the following before contributing:
- `AGENT.md` (Root Index)
- `docs/ARCHITECTURE.md`
- `docs/ENGINEERING-STANDARDS.md`
- `docs/RELIABILITY.md` (DIFA Framework)
