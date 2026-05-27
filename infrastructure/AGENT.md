# AGENT.md — Infrastructure & CI/CD

## Role
This directory governs all Cloud-Native Engineering, Infrastructure as Code (IaC), and Continuous Integration/Continuous Deployment (CI/CD) pipelines for the AI-Powered Job Discovery platform.

## Architecture

- **Primary Cloud**: Azure Container Apps (`terraform/azure/`)
- **Secondary/Fallback Cloud**: AWS ECS Fargate (`terraform/aws/`)
- **Container Strategy**: Single Docker container via Supervisor (MVP 1), migrating to distributed containers (MVP 3).
- **Deployment Manifests**: Helm charts (`helm/job-discovery/`) for potential Kubernetes transitions.

## Deployment Topology & Scaling (JD-107)

### Production Services
The platform is designed to decouple compute-intensive workloads from the API request path. The following services scale independently:

| Service | Responsibility | Scaling Strategy |
|---|---|---|
| **API Containers** | FastAPI uvicorn workers | Scales horizontally based on HTTP request volume. |
| **Temporal Workers** | Workflow orchestration | Scales independently based on active workflows. |
| **Scraper Workers** | Playwright agents | Scales independently based on scrape schedules/concurrency caps. |
| **Ranking Workers** | AI scoring pipeline | **Serverless/Burst Scaling** (see below). |
| **Observability Services** | Prometheus, Loki, Grafana | Dedicated instances/clusters. |

### Serverless AI Ranking Support (JD-105)
Ranking runs as a Temporal activity on dedicated worker(s) to isolate expensive AI workloads from the API request path.
- **Azure Container Apps**: Scale-to-zero supported (`min_replicas=0`, `max_replicas=10` on the `azurerm_container_app` resource). Scales based on Temporal task queue depth.
- **AWS Lambda Alternative**: Ranking activity can be packaged as a Lambda function with a 15-minute timeout for long-running scoring pipelines.
- **Benefits**: Burst scaling for batch ranking, reduced idle compute cost, complete isolation.

**Edge Cases & Constraints:**
- **Cold start latency**: Scale-from-zero incurs an expected cold start time of ~10-30s for container startup before ranking begins.
- **Lambda timeout**: The 15-minute AWS Lambda timeout may be exceeded during batch cross-encoder reranking. Fallback strategy: use chunked Temporal activities or AWS ECS Fargate (`desired_count` scaling) for unbounded execution time.

### Deployment Model: MVP 1 vs MVP 2

| Model | Setup | Scaling |
|---|---|---|
| **MVP 1 (Local Dev)** | Single container (Nginx + FastAPI + Next.js + Workers via Supervisor) | Monolithic scaling. |
| **MVP 2 (Production)** | Distributed containers (Azure Container Apps / AWS ECS) | Independent scaling per service type. |

## Release Tagging & Rollback Strategy (JD-106)

Every production deployment is tagged with its Git SHA: `image tag = {registry}/{image}:{git-sha}`.
After successful terraform apply, a Git tag `release/{git-sha-short}` is created by GitHub Actions.

### Rollback Strategy & Runbook
Rollback is achieved by re-deploying the previous known-good image by its SHA tag.
Maximum rollback window: 3 releases (beyond that requires full DR restore).

**Step-by-step Rollback:**
1. **Identify Previous Tag**: Find the previous successful `release/` tag in Git.
2. **Re-deploy**: Run `terraform apply` with the previous `image_tag` variable value.
3. **Verify**: Check the `/health` endpoint confirms rollback to the correct `APP_VERSION`.
4. **Database Rollback**: If a database migration accompanied the failed release, run `alembic downgrade -1`.
   *(Note: non-reversible/destructive migrations, such as dropping columns, altering enum types, or deleting tables, cannot be downgraded safely and require a full point-in-time restore.)*

## API Gateway Plugin Layer (MVP 2) — JD-103

The platform implements five gateway concerns via FastAPI/Starlette middleware. In MVP 2, these are enforced at the application middleware layer (`backend/middleware/`). In MVP 3+, they may be delegated to Kong or Azure API Management.

| Plugin Concern | Implementation | File |
|---|---|---|
| **rate-limiting** | Redis-backed sliding window per endpoint — 429 + Retry-After header | `backend/middleware/rate_limit.py` |
| **jwt** | JWT claim extraction and forwarding to `request.state.jwt_claims`; signature verification at route level via `verify_jwt()` | `backend/middleware/gateway.py` + `backend/middleware/auth.py` |
| **file-log** | Structured JSON audit log per request: method, path, status code, latency_ms, user_id (from JWT sub claim), X-Forwarded-For | `backend/middleware/gateway.py` |
| **cors** | CORSMiddleware in `main.py` (allowed origins: localhost:3000, 127.0.0.1:3000, localhost). Gateway-level CORS kept in sync. | `backend/main.py` |
| **request-transformer** | Strips sensitive headers (`x-internal-secret`, `proxy-authorization`, etc.); injects X-Request-ID (idempotent — preserves client value, generates UUID if absent) | `backend/middleware/gateway.py` |

### Middleware Execution Order

```
GatewayMiddleware        → JWT extraction, audit log, header transform
  RateLimitMiddleware    → per-endpoint sliding window rate limits
    OWASPMiddleware      → OWASP input validation
      correlation_id     → request correlation + duration logging
        Route handler
```

### Per-Endpoint Rate Limits

As specified in `proposal-v4-structure.md` Rate Limiting Strategy:

| Endpoint | Method | Limit |
|---|---|---|
| `/api/v1/jobs` | GET | 300 req/min |
| `/api/v1/cover-letter/*` | POST | 20 req/min |
| `/api/v1/question-answer/*` | POST | 30 req/min |
| `/api/v1/interview-prep/*` | POST | 10 req/min |
| `/api/v1/scrape` | POST | 1 concurrent globally (Redis distributed lock) |
| General API (`/api/*`) | ANY | 600 req/min |

**Bypass list** (never rate-limited): `/health`, `/api/docs`, `/api/openapi.json`, `/metrics`.

### X-Request-ID Behaviour

The gateway injects `X-Request-ID` on every request:
- If the client includes `X-Request-ID` in the request, that value is **preserved** (idempotent).
- If absent, the gateway generates a new `UUID4`.
- The same value is echoed back on the response `X-Request-ID` header.
- Downstream OpenTelemetry traces use this as the correlation ID.

### Rate Limit Response Headers

Every API response includes:
```
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 287
X-RateLimit-Window: 60
```

On 429:
```
Retry-After: 12
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 0
X-RateLimit-Reset: <epoch>
```

## CI/CD Pipeline Steps

The GitHub Actions pipeline (`.github/workflows/ci.yml`) must include:
1. Linting & Type Checking
2. Testing (Unit & Integration)
3. Prompt Regression Tests (DeepEval) & Ragas retrieval eval
4. Docker Builds & Cosign Image Signing
5. Terraform Validate + Plan
6. Terraform Apply (with manual approval gate via `production` environment)

## Rules
- All infrastructure must be managed via Terraform. No manual clicking in cloud consoles.
- Secrets must NEVER be hardcoded. Use Azure Key Vault or AWS Secrets Manager and inject at runtime via secret references.
- Docker images must be cryptographically signed using Cosign.
