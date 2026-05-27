
# Security Standards

This document is the single source of truth for all security standards in the Job Discovery platform, covering Auth, RBAC, RLS, OWASP compliance, prompt injection defence, and GDPR data flows.

---

## 🔐 1. Supabase Auth & JWT

We use Supabase Auth to issue JWTs. All FastApi endpoints (except public routes) validate the JWT.

- **JWT Validation**: Uses `pyjwt[crypto]` (not `python-jose` due to active CVEs).
- **Claims**: Requires `sub` (User UUID), `role` (user/admin/service), and `email`.
- **Clock Skew**: 30 seconds leeway allowed on token expiry (`exp`).
- **Token Revocation (Denylist)**: Revoked tokens (`jti` claim) are stored in Redis with a TTL matching their remaining validity to block logged-out sessions immediately.
- **Service-to-Service Calls**: Internal agents (e.g., Temporal activities calling FastAPI) must use a service account JWT signed with `SUPABASE_SERVICE_ROLE_KEY`.
- **SINGLE_USER_ID Strategy**: A temporary single-user bridge strategy using `SINGLE_USER_ID` is employed until full multi-tenant onboarding is active.
- **Identity-Centric Governance**: Enforces strong identity verification (IDPs), cryptographic verification of agents and their actions, and full auditability of agent decision-making pathways.

---

## 🛡️ 2. RBAC (Role-Based Access Control)

Roles dictate endpoint accessibility via FastAPI dependency injection:
- `user`: Can access standard `/api/v1/*` routes (scoped to their own data).
- `admin`: Can access `/api/v1/admin/*` routes.
- `service`: Can bypass certain restrictions for automated system tasks (e.g. Scraper Agents writing jobs).

*Forbidden combos*: A `user` role attempting to access an `admin` route returns `403 Forbidden`.

---

## 🗃️ 3. RLS (Row-Level Security)

All user-scoped PostgreSQL tables enforce Supabase RLS. RLS policies guarantee data isolation at the database engine level.

**Policy Templates:**
- **Jobs Table (`jobs`)**: 
  - `SELECT`: `USING (true)` (All authenticated users can read)
  - `INSERT/UPDATE/DELETE`: Restricted to `service` role only.
- **User Data (`applications`, `cv`, `cover_letter`, `interview_prep`)**:
  - `SELECT/INSERT/UPDATE/DELETE`: `USING (auth.uid() = user_id)` (Strictly scoped)
- **Audit Log (`audit_log`)**:
  - `INSERT`: Authenticated & Service roles.
  - `SELECT/UPDATE/DELETE`: Service role only (immutable from user perspective).

---

## 📋 4. OWASP Top 10 Checklist

| Category | Implemented Control in this Platform |
|---|---|
| **A01 Broken Access Control** | RLS + RBAC middleware; JWT verification strictly enforced. |
| **A02 Cryptographic Failures** | TLS 1.2+ mandatory. Key Vault for secret management. *(Note: If password hashing is ever added, use `pwdlib[argon2]` for GPU-resistance).* |
| **A03 Injection** | Prompt injection defence + Pydantic `extra="forbid"` on all JSON parsing. |
| **A04 Insecure Design** | Threat modeling resulted in the DLQ & Circuit Breaker patterns. Security Agent reviews all agent outputs before storage. |
| **A05 Security Misconfiguration** | Azure Key Vault references used in Terraform; no `.env` checked into git. |
| **A06 Vulnerable Components** | `trivy-scan` in CI container builds; dependabot enabled. |
| **A07 Auth Failures** | Supabase managed Auth with PKCE and Redis token denylist. |
| **A08 Software/Data Integrity** | Bandit static analysis in CI (`uv run bandit -r backend/`) + Docker image signing in CI via GitHub Actions. |
| **A09 Logging Failures** | Structured audit logging (Loki) & Sentry error tracking. |
| **A10 SSRF** | Explicit `ALLOWED_EXTERNAL_DOMAINS` list in `settings.py` for all outbound requests. |
| **LLM: Hallucinated Planning** | Orchestrator MUST validate execution plans against available tool schemas before sub-agents can trigger tools. |
| **LLM: Unsafe Tool Use** | Enforce Least Privilege on all agent tooling and integrations. |

---

## 🤖 5. Agent Isolation & Prompt Injection Defense

All LLM inputs from user-generated content must pass through `security_agent.py` before hitting primary orchestrators.
- **Taxonomy**: Scans for ignore-previous-instructions, goal-hijacking, and exfiltration attempts.
- **Detection Method**: Heuristic and lightweight LLM secondary evaluation.
- **Escalation Path**: If injection is detected, route payload to DLQ and write to `audit_log` with `SecurityViolationError`.
- **Exact Mitigation Techniques**: Instruction hierarchy enforcement, schema validation, context isolation, allowlisted tools only, HTML and markdown sanitisation, output validation before storage.

---

## 🇪🇺 6. GDPR Data Flow & Compliance

Data must be managed according to the following retention and deletion standards.

| Data Type | Storage Location | Retention Period | Deletion Method |
|---|---|---|---|
| User Profile & CVs | PostgreSQL | Until user deletion | `DELETE /api/v1/user` hard delete |
| Embeddings (RAG) | pgvector (`cv_chunks`) | Until user deletion | Cascading delete with Profile |
| Applications & Preps| PostgreSQL | Until user deletion | `DELETE /api/v1/user` hard delete |
| Session Caches | Redis | 15 mins (TTL) | Expire TTL / Eviction on logout |
| Raw Scrape Runs | PostgreSQL | 90 Days | Temporal Cron job (`0 2 * * *`) |
| Audit Logs | PostgreSQL (`audit_log`)| **Indefinite** | Exempted under compliance obligation |

**GDPR Rights Supported:**
- Right to Access (Export): `GET /api/v1/user/export?format=json` (Streaming output)
- Right to Erasure (Deletion): `DELETE /api/v1/user` (Cascades to pgvector & Redis)
