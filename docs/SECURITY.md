# 🛡️ Security Architecture & Guardrails

This document describes the authentication, authorization, and sanitization guardrails protecting the Job Discovery Platform, in alignment with Twelve-Factor security principles.

---

## 🔐 1. Authentication & JWT Validation

The FastAPI gateway integrates standard JWT decoding middleware powered by **Supabase Auth**.

### Mechanics:
1. **Verification**: Token validation is handled on every request via the `get_current_user` dependency defined in [backend/auth.py](file:///Users/qasirmehmood/Projects/qasir-proflle-2026/job-discovery/backend/auth.py).
2. **Algorithm**: We strictly decode tokens using the `HS256` signature algorithm, verified against the private `SUPABASE_JWT_SECRET` environment variable.
3. **Audience Check**: Every token payload is checked for `"aud": "authenticated"` and standard expiration (`exp`) times.

### 🛡️ DIFA Local Development Fallback:
To ensure local developers do not need a live cloud secret configured during initial setup, the authorization engine falls back to a **trusted mock token bypass** if the secret is left as the placeholder `super-secret-key-change-me` or if the token is formatted as a mock string. This separates external platform dependencies and maintains perfect operational continuity.

---

## 🙅 2. Active Prompt Injection & Input Sanitization

To protect downstream RAG and semantic ranking processes from instructional hijackings, the **Security Agent** operates active defensive filtering:
- **XSS Stripping**: Input strings undergo HTML regex cleaning to completely strip executable script tags, iframe insertions, and active JavaScript events.
- **exploit Blockers**: Suspicious SQL query blocks and long encoded Base64 strings are aggressively intercepted and rejected before execution.
