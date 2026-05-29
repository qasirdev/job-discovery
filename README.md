<div align="center">
  <h1>🚀 AI-Powered Job Discovery & Career Copilot</h1>
  <p><strong>An Enterprise-Grade, Multi-Agent AI Platform for Autonomous Career Management</strong></p>

  <!-- Badges -->
  <p>
    <img src="https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.14" />
    <img src="https://img.shields.io/badge/Next.js-16-black?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js 16" />
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/Temporal-Black?style=for-the-badge&logo=temporal&logoColor=white" alt="Temporal" />
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
    <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
    <img src="https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white" alt="Terraform" />
  </p>
</div>

## 🌟 Overview

This platform is a state-of-the-art **AI Career Copilot** designed to demonstrate advanced software engineering, distributed systems, and AI agent orchestration. It autonomously discovers, scores, and manages job opportunities using a hyper-personalized professional profile. 

Built with an uncompromising focus on **scalability, security, and Twelve-Factor App principles**, this project reflects senior-level engineering practices ready for production environments.

## 🎯 Key Capabilities & Business Value

- 🧠 **Autonomous Multi-Agent Swarm**: A decentralized architecture of 8 specialized AI agents (Scraping, Ranking, RAG, Q&A, Cover Letter, Orchestrator, Observability, and Security) working in tandem via Temporal workflows.
- 🎯 **Semantic Matching (RAG)**: Uses `pgvector` and deep semantic search to rank job descriptions against candidate CVs with high precision, removing the noise of traditional keyword matching.
- 🛡️ **Enterprise Security**: Built-in OWASP hardening, Supabase JWT authentication, Role-Based Access Control (RBAC), Row-Level Security (RLS), and active prompt injection defenses.
- 📊 **Deep Observability**: Comprehensive telemetry with OpenTelemetry, Prometheus, Loki, Grafana, and Sentry for real-time monitoring of AI hallucinations, token budgets, and system latency.
- ☁️ **Cloud-Native Infrastructure**: Infrastructure as Code (IaC) via Terraform, supporting multi-cloud deployments to Azure Container Apps and AWS ECS Fargate, fully containerized with Docker.

## 🛠️ Technology Stack (2026 Modern Standard)

### Frontend (User Experience)
- **Framework:** Next.js 16 (App Router, Static Export), React 19
- **Styling:** Tailwind CSS v4, Modern Flexbox & Grid, Responsive Design
- **State Management:** TanStack Query (React Query) featuring high-performance Keyset (Cursor-based) Pagination capable of scaling to millions of rows.

### Backend & AI (Core Logic)
- **Language & Framework:** Python 3.14, FastAPI (Async), `uv` package manager
- **AI Engine:** Multi-Agent Architecture, RAG, Prompt Engineering, Strict XML Prompt Contracts
- **Web Scraping:** Playwright (Headless browser automation), BeautifulSoup
- **Orchestration:** Temporal for distributed, fault-tolerant workflow management and dead-letter queues.

### Database, Caching & Data Engineering
- **Primary Database:** PostgreSQL (Supabase) with `asyncpg`
- **Vector Search:** `pgvector` for localized AI embeddings
- **Caching & Rate Limiting:** Redis (`aioredis`) with sliding window algorithms
- **Schema Migrations:** Alembic

### DevOps & Infrastructure
- **CI/CD:** GitHub Actions (Linting, Ragas/DeepEval Regression testing, Terraform pipelines)
- **Containerization:** Docker multi-stage builds, Nginx reverse proxy, Supervisord
- **Security:** Cosign (Docker Image Signing), Bandit, Trivy

---

## 🧠 The AI Agent Swarm

The system is powered by a decentralized swarm of AI agents, each governed by strict XML contracts and isolated responsibilities:

| Agent | Responsibility |
|-------|----------------|
| **Scraping Agents** | Navigates volatile session URLs on LinkedIn/JobServe to extract and standardize data. |
| **Ranking Agent** | Scores jobs against candidate CVs using cross-encoder confidence intervals. |
| **RAG Agent** | Contextualizes job descriptions with candidate history via vector search. |
| **Q&A Agent** | Provides grounded, hallucination-free interactive answers about job postings. |
| **Cover Letter Agent** | Dynamically generates ATS-optimized, personalized cover letters. |
| **Orchestrator Agent** | Manages long-running workflows, circuit breakers, and retries via Temporal. |
| **Observability Agent** | Monitors AI schema conformance, tracks token budgets, and alerts on anomalies. |
| **Security Agent** | Sanitizes user inputs and actively guards against prompt injections. |

---

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 22+
- Python 3.14+ and `uv` package manager

### Option A: Production Containerized Environment (Recommended)

The entire stack is orchestrated via Docker Compose for a seamless setup.

> **Note**: An `.env` file must exist in the root directory before running Docker. Copy `.env.example` to `.env` and fill in your API keys and configuration.

```bash
cp .env.example .env
# Edit .env with your credentials
docker compose up -d --build
```
*The unified application is now accessible at: `http://localhost`*

### Option B: Native Development (Hot-Reload)

**1. Start the Backend (FastAPI)**
```bash
cd backend
uv sync
uv run --project backend uvicorn backend.main:app --reload --port 8000
```
*API Docs: `http://localhost:8000/api/docs`*

**2. Start the Frontend (Next.js)**
```bash
cd frontend
npm install
npm run dev
```
*Dashboard: `http://localhost:3000`*

---

## 📜 Engineering Standards & Culture

This project strictly adheres to **Twelve-Factor App (2026)** principles, demonstrating a mature engineering mindset:
- **Documentation Driven:** Every module and agent contains localized `AGENT.md` guidelines outlining input/output contracts.
- **Reliability First:** Integrated DIFA (Discover, Isolate, Fix, Assess) framework and ReAct loop execution protocols.
- **Test-Driven AI:** Prompt regression testing integrated directly into the CI pipeline using DeepEval and Ragas.
- **Zero Magic:** Explicit over implicit. No "pseudo-code" allowed in production—every feature is fully implemented and tested.

---
<div align="center">
  <i>Designed and developed by Qasir Mehmood to push the boundaries of AI-driven applications.</i>
</div>
