# AGENT.md — Infrastructure & CI/CD

## Role
This directory governs all Cloud-Native Engineering, Infrastructure as Code (IaC), and Continuous Integration/Continuous Deployment (CI/CD) pipelines for the AI-Powered Job Discovery platform.

## Architecture

- **Primary Cloud**: Azure Container Apps (`terraform/azure/`)
- **Secondary/Fallback Cloud**: AWS ECS Fargate (`terraform/aws/`)
- **Container Strategy**: Single Docker container via Supervisor (MVP 1), migrating to distributed containers (MVP 3).
- **Deployment Manifests**: Helm charts (`helm/job-discovery/`) for potential Kubernetes transitions.

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
