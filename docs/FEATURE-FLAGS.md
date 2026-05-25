# FEATURE-FLAGS.md

# Feature Flag Strategy

**MVP:** 2  
**Owner:** Platform Engineering  
**Governs:** `GET /api/v1/feature-flags`, FastAPI middleware, frontend conditional rendering

Feature flags are required for controlled rollout of AI agents, experimental workflows, and infrastructure migrations. Every new capability must be gated behind a flag before merging to main. Deployment is always decoupled from release.

---

## Governing Principles

- **No flag = no release.** Every new agent, route, or premium feature ships behind a flag.
- **Flags are not config.** A feature flag controls *availability*; environment variables control *behaviour*. Do not conflate them.
- **Server-side is authoritative.** Flags are evaluated in FastAPI middleware. The frontend receives a pre-evaluated JSON snapshot — it never evaluates flag logic itself.
- **Every flag has an owner and an expiry.** Permanent flags are banned. Each flag must have a cleanup ticket raised at the time of creation.

---

## Provider Architecture

### Recommended: OpenFeature-Compatible Provider

The platform uses an [OpenFeature](https://openfeature.dev)-compatible evaluation API to prevent vendor lock-in. The SDK interface is identical regardless of backend.

```python
# backend/services/feature_flags.py

from openfeature import api
from openfeature.provider.in_memory import InMemoryProvider

# Swap provider without changing any evaluation call sites
api.set_provider(InMemoryProvider(flags={}))

def is_enabled(flag_key: str, default: bool = False) -> bool:
    client = api.get_client()
    return client.get_boolean_value(flag_key, default)
```

### Self-Hosted Mode: Database-Backed Flag Table

For self-hosted deployments without external flag services, feature flags are stored in Supabase PostgreSQL:

```sql
-- migrations/versions/xxxx_create_feature_flags.sql
CREATE TABLE feature_flags (
    key             TEXT PRIMARY KEY,
    enabled         BOOLEAN NOT NULL DEFAULT FALSE,
    rollout_pct     SMALLINT NOT NULL DEFAULT 0 CHECK (rollout_pct BETWEEN 0 AND 100),
    allowed_users   UUID[] NOT NULL DEFAULT '{}',
    description     TEXT,
    owner           TEXT NOT NULL,
    expires_at      TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Automatically stamp updated_at on every mutation
CREATE OR REPLACE FUNCTION stamp_updated_at()
RETURNS TRIGGER LANGUAGE plpgsql AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$;

CREATE TRIGGER feature_flags_updated_at
BEFORE UPDATE ON feature_flags
FOR EACH ROW EXECUTE FUNCTION stamp_updated_at();
```

Row-Level Security is **not** applied to this table — it is admin-write, public-read within the service. Access is restricted to the service role key only.

### Optional: LaunchDarkly Integration

For teams requiring SaaS flag management with audit trails, LaunchDarkly is the recommended external provider:

```python
# backend/services/feature_flags.py (LaunchDarkly variant)

import ldclient
from ldclient.config import Config

ldclient.set_config(Config(settings.launchdarkly_sdk_key))
ld = ldclient.get()

def is_enabled(flag_key: str, user_key: str = "anonymous", default: bool = False) -> bool:
    return ld.variation(flag_key, {"key": user_key}, default)
```

Set `LAUNCHDARKLY_SDK_KEY` in `.env`. When absent, the platform falls back to the database-backed provider automatically.

---

## MVP 1 — Env-Var Static Flags

In MVP 1, the `GET /api/v1/feature-flags` endpoint returns a static JSON object driven by environment variables. No database or external SDK is required. Every flag defaults to `false` if the env var is absent or set to any value other than `"true"`.

```python
# backend/routers/v1/jobs.py (feature-flags route — MVP 1)

import os
from fastapi import APIRouter

router = APIRouter()

_FLAG_KEYS = [
    "feature_admin_panel",
    "feature_ranking_agent",
    "feature_cover_letter_agent",
    "feature_question_answer_agent",
    "feature_interview_prep",
    "feature_scraper_reed",
    "feature_serverless_ranking",
]

@router.get("/feature-flags")
async def get_feature_flags() -> dict[str, bool]:
    """Return all feature flags as a static JSON object driven by env vars."""
    return {key: os.getenv(key, "false").lower() == "true" for key in _FLAG_KEYS}
```

Frontend consumption pattern:

```typescript
// frontend/hooks/useFeatureFlags.ts
import { useQuery } from "@tanstack/react-query";

export function useFeatureFlags() {
  return useQuery({
    queryKey: ["feature-flags"],
    queryFn: () => fetch("/api/v1/feature-flags").then((r) => r.json()),
    staleTime: 60_000, // re-fetch every 60s — flags are not real-time
  });
}
```

---

## Registered Feature Flags

| Flag Key | Default | Controls | MVP |
|---|---|---|---|
| `feature_admin_panel` | `false` | Admin panel page — DLQ management and scrape schedule controls | MVP 2 |
| `feature_ranking_agent` | `false` | AI ranking pipeline — scored results visible on dashboard | MVP 2 |
| `feature_cover_letter_agent` | `false` | Cover letter generation button on job detail page | MVP 2 |
| `feature_question_answer_agent` | `false` | Q&A panel on job detail page | MVP 2 |
| `feature_interview_prep` | `false` | Interview preparation button on job detail page | MVP 2 (stub) / MVP 3 (active) |
| `feature_scraper_reed` | `false` | Reed.co.uk scraper agent | Future |
| `feature_serverless_ranking` | `false` | Azure Function / AWS Lambda ranking offload | MVP 2 |

---

## Rollout Strategies

### Internal-Only Rollout

Features are enabled exclusively for developer and admin accounts before any external exposure. Use `allowed_users` on the database-backed flag row:

```sql
UPDATE feature_flags
SET allowed_users = '{00000000-0000-0000-0000-000000000001}'
WHERE key = 'feature_ranking_agent';
```

FastAPI evaluation checks `SINGLE_USER_ID` against `allowed_users` before checking `rollout_pct`.

### Percentage Rollout

Incremental rollout to a percentage of the active user base. The rollout hash is deterministic per `(user_id, flag_key)` to ensure a user always gets the same result on each evaluation:

```python
import hashlib

def in_rollout(user_id: str, flag_key: str, pct: int) -> bool:
    """Stable deterministic rollout — same user always gets the same bucket."""
    digest = hashlib.sha256(f"{user_id}:{flag_key}".encode()).hexdigest()
    bucket = int(digest[:4], 16) % 100  # 0–99
    return bucket < pct
```

Rollout ladder: `5% → 25% → 50% → 100%`. Advance only after observability metrics confirm no regression (error rate, p95 latency, hallucination rate).

### Per-User Rollout

Enable a flag for specific UUIDs regardless of percentage bucket. Used for beta testers and power users. Evaluation order:

1. Check `allowed_users` — if `user_id` is in the list, return `true`.
2. Check `enabled` — if `false`, return `false`.
3. Evaluate `rollout_pct` deterministic hash.

### Canary Deployment Validation

Feature flags gate canary traffic independently of deployment canaries. Sequence:

1. Deploy new image to 10% of containers (infrastructure canary).
2. Enable flag for 5% of users (`rollout_pct = 5`).
3. Monitor Grafana dashboards — error rate, p95 latency, agent success rate.
4. If thresholds hold for 30 minutes, advance rollout.
5. If threshold breach detected, kill-switch the flag immediately (see below).

### Emergency Kill-Switch

Every flag supports immediate toggle-off without redeployment:

```sql
-- Kill-switch: disable a flag instantly for all users
UPDATE feature_flags SET enabled = FALSE WHERE key = 'feature_ranking_agent';
```

In MVP 1 (env-var mode), set the env var to `"false"` and redeploy (or restart the container). No application code changes required.

---

## Frontend Gating Pattern

The frontend must never hard-code a flag value. All conditional rendering reads from the `feature-flags` query:

```typescript
// frontend/app/jobs/[id]/page.tsx

const { data: flags } = useFeatureFlags();

<Button
  disabled={!flags?.feature_cover_letter_agent || isOnboardingIncomplete}
  onClick={generateCoverLetter}
>
  Generate Cover Letter
</Button>
```

The admin panel navigation link is hidden entirely when `feature_admin_panel` is `false`:

```typescript
// Only render admin link in developer mode
{flags?.feature_admin_panel && (
  <NavLink href="/admin">Admin</NavLink>
)}
```

---

## FastAPI Middleware Integration (MVP 2+)

In MVP 2, flags are evaluated in a shared FastAPI dependency, not in individual route handlers:

```python
# backend/routers/dependencies.py

from fastapi import Depends, HTTPException
from services.feature_flags import is_enabled

def require_flag(flag_key: str):
    async def _guard():
        if not is_enabled(flag_key):
            raise HTTPException(status_code=404, detail=f"Feature '{flag_key}' is not available.")
    return Depends(_guard)
```

Usage:

```python
@router.post(
    "/cover-letter/{job_id}",
    dependencies=[Depends(require_rag_ready), require_flag("feature_cover_letter_agent")],
)
async def generate_cover_letter(job_id: str): ...
```

---

## Flag Lifecycle

| Phase | Action |
|---|---|
| **Creation** | Add to `_FLAG_KEYS` list + database migration + `.env.example` entry |
| **Internal** | Enable for `SINGLE_USER_ID` only via `allowed_users` |
| **Canary** | Set `rollout_pct = 5`, monitor dashboards for 30 minutes |
| **Progressive** | Advance `5% → 25% → 50% → 100%` per milestone |
| **GA** | Set `enabled = TRUE`, `rollout_pct = 100` |
| **Cleanup** | Remove flag check from code, drop row from `feature_flags`, archive ticket |

> **Rule:** A flag that has been at `100%` for more than 30 days with no open cleanup ticket is a tech debt violation. The CI lint step will fail if flag keys in `_FLAG_KEYS` have no corresponding cleanup issue in the backlog.
