<div align="center">
  <h1>🛡️ Enterprise Security & Compliance Architecture</h1>
  <p><strong>Zero-Trust Security, RBAC, and AI Prompt Injection Defense Mechanisms</strong></p>

  <!-- Badges -->
  <p>
    <img src="https://img.shields.io/badge/OWASP-Top_10-critical?style=for-the-badge&logo=owasp&logoColor=white" alt="OWASP Top 10" />
    <img src="https://img.shields.io/badge/Supabase-Auth-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white" alt="Supabase Auth" />
    <img src="https://img.shields.io/badge/GDPR-Compliant-blue?style=for-the-badge" alt="GDPR Compliant" />
    <img src="https://img.shields.io/badge/Zero--Trust-Architecture-black?style=for-the-badge" alt="Zero Trust Architecture" />
  </p>
</div>

## 🌟 Overview

This document serves as the definitive security architecture for the **Job Discovery** platform. Built upon **Zero-Trust principles** and **Twelve-Factor App methodology**, the system enforces rigorous security standards across all layers—from API gateway authentication to deep database-level isolation. It is engineered to meet and exceed 2026 enterprise compliance requirements, ensuring data integrity, robust threat mitigation, and fully observable audit trails.

---

## 🔐 1. Identity & Access Management (Supabase Auth & JWT)

Authentication is handled via Supabase Auth, strictly validating JWTs across all private FastAPI endpoints.

- **Cryptographic Validation**: JWTs are validated using `pyjwt[crypto]`, strictly avoiding deprecated libraries (e.g., `python-jose`) with active CVEs.
- **Mandatory Claims**: Tokens must possess valid `sub` (User UUID), `role` (user/admin/service), and `email` claims.
- **Clock Skew Tolerance**: A strict 30-second leeway is enforced on token expiration (`exp`).
- **Real-Time Revocation**: Revoked tokens (`jti` claim) are instantly added to a Redis-backed denylist with TTLs matching remaining validity, immediately neutralizing compromised sessions.
- **Service-to-Service Trust**: Internal workflows (e.g., Temporal orchestration calling FastAPI) are authenticated via service account JWTs signed by the `SUPABASE_SERVICE_ROLE_KEY`.
- **Identity-Centric Governance**: Employs cryptographic verification of all agents and immutable auditability for AI decision-making paths.

---

## 🛡️ 2. Role-Based Access Control (RBAC)

RBAC is strictly enforced via FastAPI dependency injection middleware, segregating endpoint access:

- `user`: Standard access to `/api/v1/*` routes, strictly scoped to the authenticated user's data context.
- `admin`: Elevated access to `/api/v1/admin/*` administrative routes.
- `service`: Specialized roles for automated agents (e.g., Scraper Agents) to perform system-level ingestion without user interaction.

*Forbidden Access*: Attempted privilege escalation automatically triggers a `403 Forbidden` response and logs a high-severity security event.

---

## 🗃️ 3. Row-Level Security (RLS) Data Isolation

Data multi-tenancy and isolation are enforced at the PostgreSQL database engine layer using Supabase RLS. 

| Table Domain | Read Access (`SELECT`) | Write Access (`INSERT/UPDATE/DELETE`) |
|--------------|------------------------|---------------------------------------|
| **`jobs`** | All authenticated users | Restricted to `service` role only |
| **User Data** (`applications`, `cv`, etc.) | Scoped: `auth.uid() = user_id` | Scoped: `auth.uid() = user_id` |
| **`audit_log`** | `service` role only (Immutable to users) | Authenticated & `service` roles |

---

## 📋 4. OWASP Top 10 Readiness

The platform is fortified against the OWASP Top 10 vulnerabilities with dedicated controls:

| Category | Enterprise Control Implemented |
|---|---|
| **A01 Broken Access Control** | RLS + RBAC middleware; strict JWT verification at the API gateway. |
| **A02 Cryptographic Failures** | TLS 1.2+ mandatory. Azure Key Vault integration for secrets via Terraform. |
| **A03 Injection** | Pydantic `extra="forbid"` on all JSON parsing; Active AI prompt injection defense. |
| **A04 Insecure Design** | Threat-modeled Temporal DLQ and Circuit Breaker patterns. |
| **A05 Security Misconfiguration** | Immutable infrastructure (Terraform); no `.env` files committed to version control. |
| **A06 Vulnerable Components** | `trivy-scan` executed in CI container builds; Dependabot automation enabled. |
| **A07 Auth Failures** | Supabase Managed Auth leveraging PKCE and Redis token denylists. |
| **A08 Software/Data Integrity** | CI-enforced Bandit static analysis; Docker image signing via Cosign. |
| **A09 Logging Failures** | Structured Loki audit logging and real-time Sentry error tracking. |
| **A10 SSRF** | Explicit `ALLOWED_EXTERNAL_DOMAINS` restriction for all outbound network requests. |

### LLM-Specific Defenses (OWASP for AI)
- **Hallucinated Planning**: Orchestrators mandate strict validation of execution plans against defined XML schemas before tool execution.
- **Unsafe Tool Use**: Principle of Least Privilege applied to all AI agent integrations and toolchains.

---

## 🤖 5. AI Agent Isolation & Prompt Injection Defense

To combat adversarial AI manipulation, user-generated content is sanitized by a dedicated **Security Agent** prior to orchestration.

- **Threat Taxonomy**: Actively scans for `ignore-previous-instructions`, goal-hijacking, and data exfiltration payloads.
- **Detection Pipeline**: Utilizes heuristics combined with lightweight, secondary LLM evaluation.
- **Automated Mitigation**: Detected threats route the payload to a Dead-Letter Queue (DLQ) and generate a `SecurityViolationError` in the `audit_log`.
- **Defense-in-Depth**: Employs instruction hierarchy enforcement, XML schema contracts, strict context isolation, HTML/Markdown sanitization, and whitelist-only tool access.

---

## 🇪🇺 6. GDPR Data Flow & Compliance Lifecycle

The platform is built to natively support European GDPR mandates regarding data retention, export, and right-to-be-forgotten requests.

| Data Type | Storage Engine | Retention Policy | Deletion Mechanism |
|---|---|---|---|
| **User Profiles & CVs** | PostgreSQL | Indefinite (until user deletion) | `DELETE /api/v1/user` (Hard delete) |
| **AI Embeddings (RAG)** | `pgvector` | Tied to user lifecycle | Cascading delete via Profile |
| **Session State** | Redis | 15 Minutes TTL | TTL Expiration / Logout Eviction |
| **Raw Scrape Data** | PostgreSQL | 90 Days Rolling | Temporal Cron (`0 2 * * *`) |
| **Security Audit Logs** | PostgreSQL | **Indefinite** | Exempted under legal compliance |

### Automated Privacy Rights
- **Right to Access (Portability)**: Users can export their entire dataset via `GET /api/v1/user/export?format=json`.
- **Right to Erasure (Deletion)**: Full data destruction via `DELETE /api/v1/user`, cascading across PostgreSQL, pgvector, and Redis caches.

---
<div align="center">
  <i>Secured and architected by Qasir Mehmood to ensure uncompromising data integrity and trust.</i>
</div>
