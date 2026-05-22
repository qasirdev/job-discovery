# AI-Powered Job Discovery & Career Copilot

An autonomous, multi-agent AI system paired with a high-performance frontend dashboard, designed to discover, analyze, rank, and manage job opportunities based on a hyper-personalized professional profile.

## 🚀 Project Overview
This platform serves as an end-to-end career copilot. It autonomously scrapes job boards, scores opportunities using semantic RAG (Retrieval-Augmented Generation) against candidate profiles, provides interactive Q&A for specific roles, and dynamically generates tailored cover letters. Built with a focus on **scalability, security, and Twelve-Factor App principles**.

## 🛠 Tech Stack & Technologies (ATS Keywords)

### Frontend
- **Frameworks**: Next.js 16 (App Router, Static Export), React 19
- **Styling & UI**: Tailwind CSS v4, Responsive Design, Modern Flexbox Layouts
- **State & Data Fetching**: TanStack Query (React Query) with High-Performance Keyset (Cursor-based) Pagination

### Backend & AI
- **Language & Framework**: Python 3.14, FastAPI (Async), `uv` package manager
- **AI & LLMs**: Multi-Agent Architecture, RAG (Retrieval-Augmented Generation), Prompt Engineering, Strict XML Prompt Contracts
- **Web Scraping**: Playwright (Headless automated browser), BeautifulSoup, DOM Parsing, HTML traversal
- **Data Engineering**: Temporal (Distributed Workflow Orchestration)

### Database & Security
- **Database**: PostgreSQL (Supabase), `asyncpg` (Async Driver), `pgvector` (Vector Embeddings & Semantic Search)
- **Migrations**: Alembic
- **Caching**: Redis (`aioredis`)
- **Security**: Supabase Auth (JWT), Role-Based Access Control (RBAC), Row-Level Security (RLS), OWASP Hardening, Prompt Injection Defense

### Infrastructure & DevOps
- **Cloud & IaC**: Terraform, Azure Container Apps, AWS ECS Fargate
- **Containerization**: Docker, Docker Compose, Multi-stage builds, Nginx, Supervisord
- **CI/CD**: GitHub Actions (Linting, Eval Regression pipelines, Terraform plan/apply), Cosign (Docker Image Signing)
- **Observability**: OpenTelemetry, Prometheus, Loki, Grafana, Sentry, Microsoft Clarity

## 🧠 Multi-Agent Architecture
The system employs a decentralized swarm of AI agents, each strictly governed by local XML contracts and localized `AGENT.md` specifications:
1. **Scraping Agents** (LinkedIn, JobServe): Extracts job data using dynamic selectors and converts to structured schemas while navigating volatile session URLs.
2. **Ranking Agent**: Scores jobs against candidate CVs using cross-encoder confidence intervals and multi-dimensional criteria.
3. **RAG Agent**: Contextualizes job descriptions with candidate history using vector search (`pgvector`).
4. **Q&A Agent**: Provides grounded, hallucination-free answers about job postings.
5. **Cover Letter Agent**: Generates ATS-optimized cover letters tailored to the specific role and company culture.
6. **Orchestrator Agent**: Manages long-running workflows, retries, and dead-letter queues via Temporal.
7. **Observability Agent**: Monitors AI schema conformance, token budgets, and hallucination rates.
8. **Security Agent**: Sanitizes inputs and guards against prompt injections.

## ⚙️ Getting Started

### Option A: Native Development (Hot-Reload)
**1. Run the Backend (FastAPI)**
```bash
cd backend
uv sync
cd ..
uv run --project backend uvicorn backend.main:app --reload --port 8000
```
*API Docs available at: `http://localhost:8000/api/docs`*

**2. Run the Frontend (Next.js)**
```bash
cd frontend
npm install
npm run dev
```
*Dashboard accessible at: `http://localhost:3000`*

### Option B: Production Containerized Environment
The entire stack is orchestrated via Docker Compose for easy deployment.
```bash
docker compose up -d --build
```
*Unified application accessible at: `http://localhost`*

## 📜 Engineering Standards
This project strictly adheres to **Twelve-Factor App (2026)** principles and autonomous ReAct loop execution protocols.
- **Documentation Driven**: Every module and agent contains localized `AGENT.md` guidelines.
- **Reliability**: DIFA (Discover, Isolate, Fix, Assess) framework integration.
- **Performance**: High-performance keyset cursor pagination capable of scaling to millions of rows.
