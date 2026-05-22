```
<prompt>
@jobs-list/2026-python-ai-azure-roadmap-v3.md
go and create file according to @jobs-list/2026-learning-prompt-v5.md in folder learning-sprints for:
- **Fri 24 Apr** — JWT Authentication in FastAPI: OAuth2 password bearer, `pyjwt[crypto]` token issuance, hashed passwords with `pwdlib[argon2]` (Argon2 — OWASP recommended default, GPU-resistant), protected route dependencies, refresh token pattern, Redis token denylist for immediate revocation on logout or role change.

key structured example file which need to follow is [s1-d1-python-for-fastapi-engineers-update1.md]
</prompt>
```

# Sprint 2 · Day 1 · Fri 24 Apr 2026

**Topic:** JWT Authentication in FastAPI — OAuth2 password bearer flow, `pyjwt[crypto]` token issuance, hashed passwords with `pwdlib[argon2]` (Argon2 — OWASP recommended default, GPU-resistant), protected route dependencies, refresh token pattern, Redis token denylist for immediate revocation on logout or role change.

**Day Type:** 🖥️ Backend  
**Builds On:** `s1-d3-postgres-async-sqlalchemy.md` — adds a full auth layer on top of the existing async PostgreSQL users API

---

## Step 1: Progressive Learning Steps & UK Job Market Relevance

### 🎯 Learning Objectives

This day covers the JWT authentication patterns that senior Python engineers are expected to know, specifically targeting:

1. **OAuth2 Password Bearer Flow**
   - `fastapi.security.OAuth2PasswordBearer` declares a token URL and wires the bearer scheme into the OpenAPI spec automatically
   - At senior level you must explain the full OAuth2 grant flow, not just "we use JWT"
   - Library: built into FastAPI — no extra install

2. **Token Issuance with `pyjwt[crypto]`**
   - Sign JWTs with HS256 (symmetric, single-service) or RS256 (asymmetric, multi-service)
   - `pyjwt[crypto]` is the 2026 standard — `python-jose` is unmaintained since 2021 with open CVEs and must not appear in new code
   - Library: `pyjwt[crypto]` 2.9.x + `cryptography` 43.x

3. **Password Hashing with `pwdlib[argon2]`**
   - `PasswordHash.recommended()` selects Argon2 by default — memory-hard, GPU-resistant
   - Argon2 was the winner of the Password Hashing Competition (PHC) and is the OWASP recommended default for new systems in 2026
   - `passlib` is unmaintained: its `crypt` module dependency was removed in Python 3.13 (PEP 594) — never use it as the primary hasher on Python 3.13+/3.14
   - Library: `pwdlib[argon2]` latest stable

4. **Protected Route Dependencies with `Annotated`**
   - `get_current_user` declared via `Annotated[User, Depends(...)]` with a plain module-level assignment keeps route handlers clean, composable, and trivially overridable in tests
   - Use plain assignment `CurrentUser = Annotated[User, Depends(get_current_user)]` — NOT the PEP 695 `type` statement, which is for generic type aliases only
   - All dependency injection uses the 2026 idiomatic style

5. **Refresh Token Pattern with Token-Type Confusion Guard**
   - Access tokens are short-lived (15 min); refresh tokens are long-lived (7 days)
   - Verified by a separate `token_type` claim and rotated on each use
   - `jti` claim for production revocation; `SecretStr` on password schema fields to prevent accidental logging

6. **Redis Token Denylist for Immediate Revocation**
   - On logout, role change, or account deactivation: write the token's `jti` to Redis with TTL equal to remaining token lifetime
   - On each authenticated request: check the denylist before trusting the token
   - This is the mandatory production answer to "how do you revoke a JWT before expiry?"

### 📊 UK Job Market Relevance (£90k–£130k / £550–£750/day)

| Skill Area                           | Market Frequency          | Interview Focus | Why It Matters                                                             |
| ------------------------------------ | ------------------------- | --------------- | -------------------------------------------------------------------------- |
| **OAuth2 grant types**               | ~70% of senior roles      | Very High       | Password, code + PKCE, client credentials — architecture and system design |
| **JWT structure**                    | ~80% of backend roles     | Very High       | Header, payload, signature, Base64URL — technical deep-dive expected       |
| **HS256 vs RS256**                   | ~55% of senior roles      | High            | Shared secret vs asymmetric key pair — security / architecture             |
| **`pyjwt[crypto]` vs `python-jose`** | ~60% of code-review roles | High            | Library currency, open CVEs — dependency audit filter                      |
| **Refresh token rotation**           | ~50% of senior roles      | High            | `jti`, revocation, denylist — security best practices                      |
| **Redis token denylist**             | ~45% of senior roles      | High            | Immediate revocation — production security pattern                         |
| **DI for auth guards**               | ~75% of FastAPI roles     | Very High       | `Annotated` + `Depends`, composable chains — code review / API design      |
| **`pwdlib[argon2]`**                 | ~50% of roles             | High            | Argon2 over bcrypt — OWASP / memory-hardness                               |
| **Token confusion attack**           | ~40% of senior roles      | Medium          | `token_type` claim guard — senior security screen                          |
| **User enumeration**                 | ~60% of security roles    | High            | Constant-time comparison, uniform errors — OWASP / security audit          |

### ✅ Key Industry Patterns for 2026

- **`python-jose` is abandoned** — last release 2021, incompatible with Python 3.10+ stdlib changes; `pyjwt[crypto]` is the correct 2026 replacement
- **`passlib` is unmaintained** — its internal `crypt` module was removed in Python 3.13 (PEP 594); never use it as the primary hasher on Python 3.13+/3.14; use `pwdlib[argon2]` instead
- **`uv`** is the 2026 default for Python tooling — all-in-one, Rust-based; `poetry` remains common in existing codebases
- **Python 3.14** is the current stable version — always use `datetime.now(timezone.utc)`; `datetime.utcnow()` is deprecated since Python 3.12
- **Plain assignment for `Annotated` aliases** — `CurrentUser = Annotated[User, Depends(...)]` at module level; the PEP 695 `type` statement is for generics only
- **`frozenset` for role sets** in `require_role()` factories — immutable and hashable at definition time
- **`SecretStr`** from Pydantic prevents passwords from appearing in logs, repr, or `model_dump()` output

### 💼 What UK Interviewers Will Ask

- "Why can't you use `python-jose` in 2026?" → unmaintained, open CVEs, incompatible with `cryptography >= 42`; `pyjwt[crypto]` is the replacement
- "Why use Argon2 over bcrypt for new systems?" → memory-hard, GPU-resistant, PHC winner, OWASP recommended default
- "How do you revoke a JWT before it expires?" → Redis denylist keyed on `jti` with TTL equal to remaining lifetime
- "What is a token confusion attack?" → refresh token accepted by a protected route; `token_type` claim guard is the fix
- "How do you prevent user enumeration on a login endpoint?" → same 401 message for user-not-found and wrong-password; constant-time dummy hash
- "What HTTP status and header does a missing token require?" → `401` + `WWW-Authenticate: Bearer` per RFC 6750
- "How do you test a protected route without generating a real JWT?" → `app.dependency_overrides[get_current_user] = lambda: mock_user`

---

## Step 2: Comprehensive Q&A and Code Artefacts

---

## 📦 Required Packages

```bash
# --- Using uv (recommended) ---
uv python install 3.14
uv python pin 3.14
uv init auth-demo
cd auth-demo

uv add "pyjwt[crypto]>=2.9" "pwdlib[argon2]" redis
uv add --dev pytest-mock

# Run commands
uv run fastapi dev app/main.py        # development (hot reload)
uv run fastapi run app/main.py        # production
uv run pytest --cov=app --cov-report=term-missing --cov-fail-under=80
uv run ruff check app/
uv run mypy app/

# --- Using poetry (common in existing codebases) ---
poetry add "pyjwt[crypto]>=2.9" "pwdlib[argon2]" redis
poetry add --group dev pytest-mock
```

```toml
# pyproject.toml — full version pins (cumulative from Days 1–3)

[project]
name = "auth-demo"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = [
    "fastapi[standard]>=0.115",
    "pydantic>=2.11",
    "pydantic-settings>=2.7",
    "pyjwt[crypto]>=2.9",
    "pwdlib[argon2]",
    "redis>=5.0",
    "sqlalchemy[asyncio]>=2.1",
    "asyncpg>=0.30",
    "alembic>=1.14",
]

[dependency-groups]
dev = [
    "ruff>=1.0",
    "mypy>=1.18",
    "pytest>=8",
    "httpx>=0.28",
    "pytest-cov>=6",
    "pytest-asyncio>=0.24",
    "aiosqlite>=0.21",
    "pytest-mock>=3.14",
]

[tool.ruff]
line-length = 100
target-version = "py314"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.14"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --cov=app --cov-report=term-missing"
```

| Package          | Version (stable May 2026) | Purpose                                                                |
| ---------------- | ------------------------- | ---------------------------------------------------------------------- |
| `pyjwt[crypto]`  | 2.9.x                     | JWT encode / decode — replaces unmaintained `python-jose`              |
| `cryptography`   | 43.x                      | RS256 key operations required by PyJWT (installed via `pyjwt[crypto]`) |
| `pwdlib[argon2]` | latest stable             | Argon2 password hashing — replaces unmaintained `passlib`              |
| `redis`          | 5.x                       | Token denylist for immediate JWT revocation                            |
| `pytest-mock`    | 3.14.x                    | `mocker` fixture for patching in fast tests                            |
| `ruff`           | 1.x                       | Linter + formatter — Rust-based, replaces flake8/black/isort           |
| `mypy`           | 1.18+                     | Static type checker — `strict = true` is the 2026 senior standard      |

> ⚠️ **`python-jose` is abandoned** — last release 2021, incompatible with Python 3.10+ stdlib changes. Never use it. Use `pyjwt[crypto]` instead. Import as `import jwt`.

> ⚠️ **`passlib` is unmaintained** — its `crypt` module dependency was removed in Python 3.13 (PEP 594). Never use `passlib` as the primary hasher on Python 3.13+/3.14. Use `pwdlib[argon2]` with `PasswordHash.recommended()` for all new hash write paths.

---

## 🖥️ Part 1: JWT Fundamentals

### Q&A Batch 1: JWT Fundamentals

**Q1: What are the three parts of a JWT and what does each contain?**  
A: A JWT (JSON Web Token) has three Base64URL-encoded sections separated by dots: the Header (algorithm name and token type), the Payload (claims — `sub`, `exp`, `iat`, `jti`, and custom fields), and the Signature (HMAC or RSA of `header.payload` using the signing key). The payload is readable by anyone — never store sensitive data in it. Only the signature proves authenticity.

```
eyJhbGciOiJIUzI1NiJ9          ← Header
.eyJzdWIiOiIxMjMiLCJleHAiOjE3...} ← Payload (readable — not encrypted)
.SflKxwRJSMeKKF2QT4fwpMeJf36POk   ← Signature (tamper-proof)
```

**Q2: What is the difference between HS256 and RS256?**  
A: `HS256` (HMAC SHA-256) uses a single shared secret — any service verifying tokens must also hold the secret. `RS256` uses an asymmetric key pair: the private key signs tokens (held only by the auth service); the public key verifies them (shared freely via a JWKS endpoint). Use `RS256` when tokens cross service boundaries. Use `HS256` only for single-service deployments or development.

**Q3: Why is `python-jose` no longer acceptable in 2026?**  
A: `python-jose` has had no meaningful maintenance since mid-2021, has open CVEs, and is incompatible with `cryptography >= 42`. `pyjwt[crypto]` is actively maintained, has a clean Pythonic API, passes all current security audits, and is the correct 2026 replacement. Mentioning `python-jose` in a code review signals stale dependency knowledge.

**Q4: What standard JWT claims should a production access token contain?**  
A: The minimum set of claims for a production-grade access token:

| Claim        | Name       | Value                                                         |
| ------------ | ---------- | ------------------------------------------------------------- |
| `sub`        | Subject    | User ID as a string — never email (emails change; IDs do not) |
| `exp`        | Expiration | Unix timestamp — typically 15 minutes from issue time         |
| `iat`        | Issued At  | Unix timestamp of creation                                    |
| `jti`        | JWT ID     | UUID per token — enables revocation via Redis denylist        |
| `token_type` | Custom     | `"access"` — prevents token confusion with refresh tokens     |

Avoid storing PII (name, email, role) in the payload — the payload is not encrypted and is readable by anyone who intercepts the token.

**Q5: Why should access tokens be short-lived (15 minutes)?**  
A: JWTs are stateless — once issued they cannot be revoked before expiry without maintaining a server-side denylist. A 15-minute window limits the exposure if a token is stolen. Refresh tokens extend session length without requiring long-lived access tokens — the separation of access and refresh lifetimes is the key design insight.

**Q6: What is the `jti` claim and why is it mandatory?**  
A: `jti` (JWT ID) is a unique identifier per token (typically UUID v4). It enables selective revocation: store the `jti` in Redis with a TTL matching the token's `exp`. On each request, check the `jti` against the Redis denylist and reject if present. Required for refresh token rotation, logout, and "sign out all devices" functionality. Without `jti`, you can only revoke all tokens by rotating the signing secret.

**Q7: What is a token confusion attack and how does the `token_type` claim prevent it?**  
A: A token confusion attack occurs when a refresh token is accepted by an endpoint that expects an access token. Both tokens are valid JWTs signed with the same key — without a type check, an attacker who obtains a refresh token can authenticate protected routes indefinitely. Including `token_type: "access"` in the access token payload and asserting it in `get_current_user` closes this vector.

**Q8: How does a Redis denylist work for immediate JWT revocation?**  
A: When a token is revoked (logout, role change, account deactivation), write its `jti` to Redis with `SETEX jti 1 remaining_ttl_in_seconds`. On each authenticated request, run `EXISTS denylist:{jti}` before trusting the token. If the key is present, reject with 401. The Redis key auto-expires when the token's natural lifetime ends, so no cleanup is needed.

**Q9: What is an algorithm confusion attack in JWT and how does `pyjwt` mitigate it?**  
A: An algorithm confusion attack exploits servers that accept any algorithm claimed in the token header. An attacker can modify an RS256 token to declare `alg: HS256` and re-sign it using the server's public key as the HMAC secret. `pyjwt` mitigates this by requiring `algorithms=["RS256"]` as an explicit allowlist in `jwt.decode()` — any token claiming a different algorithm is rejected regardless of the header value.

**Q10: What should the `sub` claim contain and what should it never be?**  
A: Per RFC 7519, `sub` is a locally or globally unique identifier for the token subject. Use the user's database ID as a string (`"123"` or a UUID string) — never the email address. Emails can change; IDs cannot.

**Q11: How does `OAuth2PasswordBearer` work in FastAPI?**  
A: `OAuth2PasswordBearer(tokenUrl="/auth/token")` declares an OAuth2 security scheme in the OpenAPI spec and extracts the bearer token from the `Authorization: Bearer <token>` request header. It raises `401` automatically if no token is present. It does NOT validate the token — that is the responsibility of the `get_current_user` dependency that consumes it.

**Q12: What does `OAuth2PasswordRequestForm` provide that a plain `BaseModel` does not?**  
A: `OAuth2PasswordRequestForm` parses `application/x-www-form-urlencoded` bodies (not JSON) with the OAuth2-standard fields: `username`, `password`, `scope`, `client_id`, `client_secret`. FastAPI renders a login form in Swagger UI automatically. Note: the field is `username` even if your system uses email — this is mandated by the OAuth2 spec.

**Q13: What HTTP status code is correct for an invalid or missing token and what header must accompany it?**  
A: `401 Unauthorized`. The `WWW-Authenticate: Bearer` response header is required by RFC 6750. Using `403 Forbidden` for a missing token is a common interview mistake — 403 means authenticated but not authorised.

**Q14: What is the OWASP Top 10 item most relevant to JWT authentication?**  
A: OWASP A07 — Identification and Authentication Failures. Covers: weak passwords, missing brute-force protection, improper session invalidation, weak or unenforced token algorithms, and storing JWTs in `localStorage` (vulnerable to XSS). Mitigations: Argon2 hashing, account lockout after N failed attempts, explicit algorithm allowlist in `jwt.decode()`, token revocation on password change via Redis denylist, `HttpOnly` cookies for refresh tokens.

**Q15: What is OWASP A02 (Cryptographic Failures) in the password storage context?**  
A: OWASP A02 covers weak or misapplied cryptography. Password-specific violations include: storing plain-text passwords, using MD5 or SHA-1/SHA-256 without salt (fast hashing — trivially brute-forced), using bcrypt with a work factor below 10, and exposing hashed passwords in API responses. `pwdlib[argon2]` with `PasswordHash.recommended()` satisfies all these requirements.

---

### 🎯 Working Code Artefact 1: JWT Utilities and Password Hashing

```python
# app/security.py
import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt  # pyjwt — not python-jose
from pwdlib import PasswordHash

from app.config import get_settings

settings = get_settings()

# PasswordHash.recommended() selects Argon2 by default.
# Argon2 is memory-hard and GPU-resistant — the OWASP recommended default for new systems.
password_hash = PasswordHash.recommended()

# Dummy hash for constant-time comparison when user does not exist.
# Prevents timing attacks that reveal which emails are registered.
_DUMMY_HASH = password_hash.hash("dummy-for-timing-safety")


def hash_password(plain: str) -> str:
    """Return an Argon2 hash of the plain-text password."""
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Return True if plain matches the stored Argon2 hash."""
    return password_hash.verify(plain, hashed)


def hash_api_key(raw_key: str) -> str:
    """Return a SHA-256 hex digest of the raw API key for safe storage.

    Store this digest in the database, never the raw key.
    On each request, hash the incoming key and compare against the stored digest.
    """
    return hashlib.sha256(raw_key.encode()).hexdigest()


def _create_token(data: dict[str, Any], expires_delta: timedelta) -> str:
    """Sign and return a JWT with standard claims."""
    payload = data.copy()
    now = datetime.now(timezone.utc)  # always timezone-aware — never use utcnow()
    payload["iat"] = now
    payload["exp"] = now + expires_delta
    payload["jti"] = str(uuid.uuid4())  # unique per token — required for denylist revocation
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def create_access_token(subject: str | int) -> str:
    """Return a signed access token for the given user ID."""
    return _create_token(
        {"sub": str(subject), "token_type": "access"},
        timedelta(minutes=settings.access_token_expire_minutes),
    )


def create_refresh_token(subject: str | int) -> str:
    """Return a signed refresh token for the given user ID."""
    return _create_token(
        {"sub": str(subject), "token_type": "refresh"},
        timedelta(days=settings.refresh_token_expire_days),
    )


def decode_token(token: str) -> dict[str, Any]:
    """Decode and verify a JWT signed with the application secret.

    Raises jwt.ExpiredSignatureError — token past its exp claim.
    Raises jwt.InvalidTokenError  — bad signature, malformed, or wrong algorithm.
    Never catch these silently — let the dependency layer convert to HTTPException(401).
    """
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],  # explicit allowlist — prevents algorithm confusion
    )


def authenticate_user(email: str, password: str):
    """Return the User on success, None on failure.

    Always calls verify_password even for unknown emails — constant-time defence
    against user enumeration via timing attacks.
    """
    from app.models import get_user_by_email
    user = get_user_by_email(email)
    if not user:
        verify_password(password, _DUMMY_HASH)  # constant-time — prevents timing attack
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
```

### ✅ Key Concepts

- **`pwdlib[argon2]` replaces `passlib` in 2026** — `passlib`'s `crypt` module dependency was removed in Python 3.13 (PEP 594); `PasswordHash.recommended()` selects Argon2 by default
- **`pyjwt[crypto]` replaces `python-jose`** — `python-jose` is unmaintained with open CVEs; import as `import jwt`
- **`jti` is mandatory in every token** — without it you cannot selectively revoke; you can only invalidate all tokens by rotating the signing secret
- **`algorithms=["HS256"]` must be a list** — prevents algorithm confusion attacks
- **`datetime.now(timezone.utc)` is mandatory** — `datetime.utcnow()` is deprecated in Python 3.12/3.14; naive datetimes in JWT `exp` claims cause subtle clock-comparison bugs
- **`hash_api_key()` for service account keys** — always store SHA-256 digests, never raw keys; look up by hash on each request

### ⚠️ Common Pitfalls

- Importing `from jose import jwt` — `python-jose` is unmaintained; use `import jwt` from `pyjwt[crypto]`
- Using `pwd_context = CryptContext(...)` from `passlib` — unmaintained on Python 3.13+; use `pwdlib`
- Calling `.decode("utf-8")` on `jwt.encode()` output — `pyjwt >= 2.0` returns `str`, not `bytes`
- Using `datetime.utcnow()` in token payloads — deprecated in Python 3.12, use `datetime.now(timezone.utc)`
- Omitting `jti` from tokens — makes Redis denylist revocation impossible
- Catching `jwt.InvalidTokenError` silently — hides forgery attempts

---

## 🖥️ Part 2: pwdlib, Argon2, and Security Utilities

### Q&A Batch 2: pwdlib, Argon2, and Security Utilities

**Q16: What is `pwdlib` and why replace `passlib` with it?**  
A: `pwdlib` is an actively maintained password hashing library designed as a `passlib` successor. `passlib` internally used the `crypt` module which was removed in Python 3.13 (PEP 594), making it incompatible with modern Python. `pwdlib` provides a clean, simple API with `PasswordHash.recommended()` selecting Argon2 by default. It is the 2026 production standard for Python 3.13+/3.14.

**Q17: What is the `pwdlib` API and how does it work?**  
A: `pwdlib` exposes a single `PasswordHash` class. `PasswordHash.recommended()` returns a pre-configured instance using Argon2. The instance provides `.hash()` and `.verify()` methods.

```python
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()  # Argon2 by default

hashed = password_hash.hash("plain_password")
is_valid = password_hash.verify("plain_password", hashed)  # True
is_invalid = password_hash.verify("wrong_password", hashed)  # False
```

**Q18: Why is Argon2 preferred over bcrypt for new systems in 2026?**  
A: Argon2 is memory-hard — it requires a configurable amount of RAM per hash attempt, making GPU and ASIC brute-force attacks significantly more expensive than bcrypt which relies on computational complexity alone. Argon2 was the winner of the Password Hashing Competition (PHC) and is the OWASP recommended default for new systems. bcrypt remains acceptable for legacy systems where migration cost is high but must not be chosen for new projects.

**Q19: How do you prevent a timing attack on the login endpoint when the user does not exist?**  
A: Always call `verify_password` even when the user is not found — pass a dummy hash so Argon2 runs regardless. Without the dummy call, the login endpoint returns faster for non-existent users — an attacker can enumerate valid emails by measuring response times.

```python
_DUMMY_HASH = password_hash.hash("dummy-for-timing-safety")

async def authenticate_user(email: str, password: str) -> User | None:
    user = await user_repo.get_by_email(email)
    if not user:
        verify_password(password, _DUMMY_HASH)  # constant-time — prevents timing attack
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
```

**Q20: How do you create an access token with `pyjwt`?**  
A: Build a payload dict with standard claims, always using `datetime.now(timezone.utc)` for timezone-aware timestamps, include a `jti` UUID, then encode with an explicit algorithm.

```python
from datetime import datetime, timedelta, timezone
from typing import Any
import uuid
import jwt

SECRET_KEY = "replace-with-env-var"
ALGORITHM = "HS256"

def create_access_token(subject: str | int) -> str:
    """Return a signed access token with jti for denylist revocation."""
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "token_type": "access",
        "iat": now,
        "exp": now + timedelta(minutes=15),
        "jti": str(uuid.uuid4()),  # unique per token — mandatory for revocation
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
```

**Q21: How do you decode and verify a JWT safely with `pyjwt`?**  
A: Always pass an explicit `algorithms` list — never a string. This prevents algorithm confusion attacks and is an intentional `pyjwt` API design choice.

```python
def decode_token(token: str) -> dict[str, Any]:
    """
    Raises jwt.ExpiredSignatureError — token past its exp claim.
    Raises jwt.InvalidTokenError — bad signature, malformed, wrong algorithm.
    Callers must catch these and raise HTTPException(401).
    """
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"],  # explicit allowlist — prevents algorithm confusion attacks
    )
```

**Q22: Why must `algorithms` in `jwt.decode()` always be a list and never a string?**  
A: Passing a list forces you to explicitly declare which algorithms you accept. This prevents algorithm confusion attacks — an attacker cannot switch the token header from `RS256` to `HS256` and re-sign with the public key because `HS256` is not in the allowlist. `pyjwt` raises `DecodeError` if a string is passed instead of a list — this is intentional to prevent the vulnerability.

**Q23: What is `datetime.now(timezone.utc)` and why must you use it instead of `datetime.utcnow()`?**  
A: `datetime.utcnow()` returns a naive datetime (no timezone info) and is deprecated since Python 3.12. `datetime.now(timezone.utc)` returns a timezone-aware datetime that pyjwt validates correctly. Naive datetimes in JWT `exp` claims cause subtle clock-comparison bugs in containerised environments where the system timezone differs from UTC.

**Q24: How do you use RS256 with `pyjwt` for a multi-service architecture?**  
A: The auth service holds the private key and signs tokens. All other services fetch the public key from a JWKS endpoint and verify tokens independently without network calls to the auth service on every request.

```python
from pathlib import Path
import jwt

private_key = Path("private.pem").read_bytes()  # held only by auth service
public_key  = Path("public.pem").read_bytes()   # distributed freely / JWKS endpoint

# Auth service — signs token
token = jwt.encode({"sub": "user-123", "jti": str(uuid.uuid4())}, private_key, algorithm="RS256")

# Resource service — verifies token using public key only
payload = jwt.decode(token, public_key, algorithms=["RS256"])
```

**Q25: What is `SecretStr` and why should password fields always use it?**  
A: `SecretStr` is a Pydantic type that stores the value securely and renders as `'**********'` in `repr()`, logs, and `model_dump()` output. The actual value is only accessible via `.get_secret_value()`. Without it, a password accidentally logged by a Pydantic `ValidationError` traceback leaks user credentials in plaintext.

```python
from pydantic import BaseModel, EmailStr, SecretStr

class UserCreate(BaseModel):
    """Input schema — password never leaks into logs or responses."""
    email: EmailStr
    password: SecretStr  # never appears in logs or model_dump()

# Usage in route
hashed = hash_password(payload.password.get_secret_value())
```

**Q26: How do you store service account API keys securely?**  
A: Store a SHA-256 hash of the API key in the database, not the raw key. On each request, hash the incoming key and compare against the stored hash. Never return the first active service account by role alone — this would give all service accounts the same key.

```python
import hashlib

def hash_api_key(raw_key: str) -> str:
    """Return a SHA-256 hex digest of the raw API key for safe storage."""
    return hashlib.sha256(raw_key.encode()).hexdigest()

# On each service account request:
incoming_hash = hash_api_key(raw_key_from_header)
service_account = await db.get_service_account_by_key_hash(incoming_hash)
# NOT: await db.get_first_service_account(role="service")  — wrong
```

**Q27: What is `jwt.InvalidTokenError` and when should you catch it separately from `jwt.ExpiredSignatureError`?**  
A: `jwt.ExpiredSignatureError` is a subclass of `jwt.InvalidTokenError` raised specifically when the `exp` claim is in the past. Catching it separately lets you return a distinct error detail — useful for clients that implement refresh-token flows and need to distinguish "expired" from "tampered".

```python
try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
except jwt.ExpiredSignatureError:
    raise HTTPException(401, detail="Token expired")
except jwt.InvalidTokenError:
    raise HTTPException(401, detail="Invalid token")
```

**Q28: Why should `jwt.InvalidTokenError` never be caught silently?**  
A: Silently swallowing token errors hides forgery attempts and makes debugging security incidents impossible. Always let them propagate to the dependency layer and convert to `HTTPException(401)`. Log the exception type (but not the raw token) for audit purposes.

**Q29: How do you implement Argon2 configuration tuning for production?**  
A: `PasswordHash.recommended()` applies sensible defaults. For environments with strict latency requirements, you can tune the Argon2 parameters via `pwdlib`'s configuration. In practice, start with `recommended()` and only tune after profiling shows a genuine latency issue on the login endpoint.

**Q30: What is the `aud` claim and when must it be validated?**  
A: `aud` (audience) identifies the intended recipient of the token. When an auth server issues tokens for multiple services, each service's token should have a distinct `aud` value. `pyjwt` validates `aud` when you pass `audience="my-api"` to `jwt.decode()` — preventing a token issued for the mobile app from being used against the admin API.

---

### 🎯 Working Code Artefact 2: Config, Schemas, and Models

```python
# app/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""
    secret_key: str = "dev-secret-key-replace-in-production-minimum-32-chars"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    debug: bool = False
    allowed_origins: list[str] = ["http://localhost:3000"]
    redis_url: str = "redis://localhost:6379"

    model_config = {"env_file": ".env"}


@lru_cache
def get_settings() -> Settings:
    """Return cached Settings instance — reads .env once per process."""
    return Settings()
```

```python
# app/schemas.py
from pydantic import BaseModel, EmailStr, SecretStr, ConfigDict


class UserCreate(BaseModel):
    """Input schema — password never appears in logs, repr, or model_dump()."""
    email: EmailStr
    password: SecretStr  # access via .get_secret_value() only at hash time


class UserOut(BaseModel):
    """Safe output schema — excludes all write-only fields."""
    id: int
    email: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Token pair returned on successful login or refresh."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Parsed claims from a decoded JWT."""
    sub: str | None = None
    token_type: str = "access"
    jti: str | None = None


class RefreshRequest(BaseModel):
    """Request body for the token refresh endpoint."""
    refresh_token: str
```

```python
# app/models.py — in-memory store (replaced by UserRepository in Sprint 2 Day 2)
from dataclasses import dataclass

type UserId    = int
type UserEmail = str


@dataclass
class User:
    """In-memory user record — wired to async SQLAlchemy on Sprint 2 Day 2."""
    id: UserId
    email: UserEmail
    hashed_password: str
    is_active: bool = True


_users: dict[UserId, User] = {}
_email_index: dict[UserEmail, UserId] = {}
_next_id: int = 1


def create_user(email: UserEmail, hashed_password: str) -> User:
    """Insert a new user into the in-memory store and return it."""
    global _next_id
    user = User(id=_next_id, email=email, hashed_password=hashed_password)
    _users[_next_id] = user
    _email_index[email] = _next_id
    _next_id += 1
    return user


def get_user_by_email(email: UserEmail) -> User | None:
    """Return the user with the given email, or None if not found."""
    uid = _email_index.get(email)
    return _users.get(uid) if uid else None


def get_user_by_id(uid: UserId) -> User | None:
    """Return the user with the given ID, or None if not found."""
    return _users.get(uid)
```

### ✅ Key Concepts

- **`SecretStr` on all password fields** — prevents passwords appearing in logs, `ValidationError` tracebacks, or `model_dump()` output
- **`lru_cache` on `get_settings()`** — `pydantic-settings` reads from env on each instantiation; `lru_cache` ensures a single Settings object across the process lifetime
- **`redis_url` in Settings** — required for the token denylist; read from env in production
- **`model_config = ConfigDict(from_attributes=True)` on `UserOut`** — required for Pydantic to read ORM model attributes when Day 2 wires to async SQLAlchemy

### ⚠️ Common Pitfalls

- Storing the raw `password` string in the User model — always hash immediately with `hash_password(payload.password.get_secret_value())` and discard the plaintext
- Hardcoding `SECRET_KEY` in source code — use `pydantic-settings` to read from env; rotate via Azure Key Vault or Kubernetes Secrets in production
- Hardcoding `redis_url` — always read from environment; the denylist is a production concern

---

## 🖥️ Part 3: Redis Token Denylist

### Q&A Batch 3: Redis Token Denylist

**Q31: Why is a Redis denylist necessary if JWTs are already short-lived?**  
A: A 15-minute access token window is too long in high-security contexts. If a user's role is changed, they are deactivated, or they log out, their existing access token remains valid for up to 15 minutes. The Redis denylist closes this window — the token is rejected immediately on the next request after revocation.

**Q32: What is the minimal Redis denylist pattern?**  
A: Store the token's `jti` in Redis with a TTL equal to the token's remaining lifetime. On each authenticated request, check the denylist before trusting the token. The key auto-expires when the token's natural lifetime ends.

```python
import redis.asyncio as aioredis

async def revoke_token(jti: str, expires_in_seconds: int, redis_client) -> None:
    """Add a token JTI to the Redis denylist until it expires."""
    await redis_client.setex(f"denylist:{jti}", expires_in_seconds, "1")

async def is_token_revoked(jti: str, redis_client) -> bool:
    """Return True if the token has been explicitly revoked."""
    return await redis_client.exists(f"denylist:{jti}") == 1
```

**Q33: How do you calculate the TTL for the Redis denylist entry?**  
A: Extract the `exp` claim from the decoded token, subtract the current time, and use the remaining seconds as the TTL. If `exp` is in the past, the TTL is 0 and Redis treats the key as already expired.

```python
from datetime import datetime, timezone

def get_remaining_seconds(exp: int) -> int:
    """Return seconds until the token expires, minimum 0."""
    now = int(datetime.now(timezone.utc).timestamp())
    return max(0, exp - now)
```

**Q34: How do you initialise a Redis client in FastAPI using lifespan?**  
A: Use the `lifespan` context manager to create the Redis client on startup and close it on shutdown. Attach it to `app.state` for access in dependencies.

```python
from contextlib import asynccontextmanager
import redis.asyncio as aioredis
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create Redis client on startup; close on shutdown."""
    app.state.redis = aioredis.from_url(settings.redis_url, decode_responses=True)
    yield
    await app.state.redis.aclose()
```

**Q35: How do you inject the Redis client into dependencies?**  
A: Create a `get_redis` dependency that reads from `app.state`.

```python
from fastapi import Request
import redis.asyncio as aioredis

async def get_redis(request: Request) -> aioredis.Redis:
    """Return the Redis client from app state."""
    return request.app.state.redis
```

**Q36: What happens to denylist entries when a token expires naturally?**  
A: Redis auto-expires the key when the TTL runs out — no cleanup job is needed. The denylist is self-maintaining as long as you set `SETEX` with the correct remaining TTL.

**Q37: Should the denylist check happen before or after signature verification?**  
A: After — signature verification is cheap and stateless; it should always run first to reject forged tokens without touching Redis. Only after a token passes signature and expiry checks should you hit the denylist.

**Q38: How do you handle Redis unavailability in the denylist check?**  
A: In high-security systems, fail closed — reject the request with 503 if Redis is unavailable. In lower-security systems, you may choose to fail open (log the error and allow the request). Document the decision clearly and default to fail-closed in production.

```python
async def is_token_revoked(jti: str, redis_client) -> bool:
    """Return True if revoked. On Redis error, fail closed for security."""
    try:
        return await redis_client.exists(f"denylist:{jti}") == 1
    except Exception:
        # Fail closed — log this; never silently allow unknown revocation state
        raise HTTPException(503, detail="Authentication service temporarily unavailable")
```

---

### 🎯 Working Code Artefact 3: Dependencies and Auth Router (with Redis Denylist)

```python
# app/dependencies.py
from datetime import datetime, timezone
from typing import Annotated

import jwt
import redis.asyncio as aioredis
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from app.models import User, get_user_by_id
from app.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Shared 401 exception — reused across all auth dependencies
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},  # required by RFC 6750
)


async def get_redis(request: Request) -> aioredis.Redis:
    """Return the Redis client from app state."""
    return request.app.state.redis


async def is_token_revoked(jti: str, redis_client: aioredis.Redis) -> bool:
    """Return True if the token JTI is on the Redis denylist."""
    try:
        return await redis_client.exists(f"denylist:{jti}") == 1
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Authentication service temporarily unavailable",
        )


async def revoke_token(jti: str, exp: int, redis_client: aioredis.Redis) -> None:
    """Add a token JTI to the Redis denylist with TTL equal to remaining lifetime."""
    now = int(datetime.now(timezone.utc).timestamp())
    remaining = max(0, exp - now)
    if remaining > 0:
        await redis_client.setex(f"denylist:{jti}", remaining, "1")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    redis_client: Annotated[aioredis.Redis, Depends(get_redis)],
) -> User:
    """Validate JWT, check denylist, and return the authenticated user."""
    try:
        payload = decode_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise CREDENTIALS_EXCEPTION

    # Token confusion guard — refresh tokens must not be accepted here
    if payload.get("token_type") != "access":
        raise CREDENTIALS_EXCEPTION

    raw_sub: str | None = payload.get("sub")
    jti: str | None = payload.get("jti")

    if raw_sub is None or jti is None:
        raise CREDENTIALS_EXCEPTION

    # Redis denylist check — immediate revocation on logout or role change
    if await is_token_revoked(jti, redis_client):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_id(int(raw_sub))
    if user is None or not user.is_active:
        raise CREDENTIALS_EXCEPTION

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Composable dependency — chains on get_current_user."""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Plain module-level Annotated aliases — NOT PEP 695 type statement
# PEP 695 `type X = ...` is for generic type aliases only (e.g. type Vector[T] = list[T])
# Annotated dependency shortcuts must use plain assignment at module level
CurrentUser = Annotated[User, Depends(get_current_user)]
ActiveUser  = Annotated[User, Depends(get_current_active_user)]
```

```python
# app/routers/auth.py
from datetime import datetime, timezone
from typing import Annotated

import jwt
import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import ActiveUser, get_redis, revoke_token
from app.models import User, create_user, get_user_by_email
from app.schemas import RefreshRequest, Token, UserCreate, UserOut
from app.security import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=201)
async def register(payload: UserCreate) -> User:
    """Register a new user. Returns 409 if email already exists."""
    if get_user_by_email(payload.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    return create_user(
        email=payload.email,
        hashed_password=hash_password(payload.password.get_secret_value()),
    )


@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """OAuth2 password grant — accepts application/x-www-form-urlencoded.

    Same error for user-not-found and wrong-password — prevents user enumeration.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(payload: RefreshRequest) -> Token:
    """Exchange a valid refresh token for a new access + refresh pair.

    Production extension: persist tokens in DB and rotate (invalidate old on use).
    """
    _refresh_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        data = decode_token(payload.refresh_token)
    except jwt.InvalidTokenError:
        raise _refresh_exc

    if data.get("token_type") != "refresh":
        raise _refresh_exc

    sub: str | None = data.get("sub")
    if not sub:
        raise _refresh_exc

    return Token(
        access_token=create_access_token(sub),
        refresh_token=create_refresh_token(sub),
    )


@router.post("/logout", status_code=204)
async def logout(
    current_user: ActiveUser,
    token: Annotated[str, Depends(lambda r: r.headers.get("authorization", "").removeprefix("Bearer "))],
    redis_client: Annotated[aioredis.Redis, Depends(get_redis)],
) -> None:
    """Revoke the current access token by adding its jti to the Redis denylist."""
    try:
        payload = decode_token(token)
        jti: str | None = payload.get("jti")
        exp: int | None = payload.get("exp")
        if jti and exp:
            await revoke_token(jti, exp, redis_client)
    except jwt.InvalidTokenError:
        pass  # token already invalid — logout is idempotent


@router.get("/me", response_model=UserOut)
async def read_me(current_user: ActiveUser) -> User:
    """Return the authenticated user's profile."""
    return current_user
```

### ✅ Key Concepts

- **`token_type` claim is the only guard against token confusion** — access and refresh tokens are cryptographically identical without it
- **Redis denylist check runs after signature verification** — stateless verification is cheap; Redis hit only on valid, unexpired tokens
- **`revoke_token` uses `SETEX` with remaining TTL** — Redis auto-expires the key when the token's natural lifetime ends; no cleanup job needed
- **Plain assignment for `CurrentUser` and `ActiveUser`** — `Annotated[User, Depends(...)]` at module level; never `type CurrentUser = ...` (that misuses PEP 695)
- **`frozenset` for role sets in `require_role()` factories** — add when wiring RBAC on Sprint 2 Day 2

### ⚠️ Common Pitfalls

- Using `type CurrentUser = Annotated[...]` — this misuses PEP 695 which is for generics only; use plain assignment
- Omitting the Redis denylist check — a logged-out user's token remains valid for up to 15 minutes without it
- Failing open on Redis errors — in high-security contexts, always fail closed (503) if the denylist is unavailable
- Omitting `WWW-Authenticate: Bearer` from 401 responses — RFC 6750 violation; breaks some OAuth2 clients

---

## 🖥️ Part 4: Refresh Tokens, Session Management, and Testing

### Q&A Batch 4: Refresh Tokens and Testing Auth Flows

**Q39: What is refresh token rotation and why is it a security requirement?**  
A: Token rotation issues a new refresh token on every use and immediately invalidates the old one. If a stolen refresh token is used by an attacker, the legitimate user's next use of their copy will be rejected — both the old and new tokens are invalidated (detected concurrent use). Without rotation, a stolen refresh token is valid for its full 7-day lifetime with no detection mechanism.

**Q40: Where should refresh tokens be stored on the client?**  
A: In an `HttpOnly`, `Secure`, `SameSite=Strict` cookie — not in `localStorage` or `sessionStorage`. `localStorage` is accessible to JavaScript and is vulnerable to XSS attacks. An `HttpOnly` cookie cannot be read by JavaScript. This is the OWASP-recommended pattern for web clients.

**Q41: Should refresh tokens be stored in the database?**  
A: In production, yes. Store the hashed refresh token alongside the user ID and expiry date. This enables: explicit logout (delete the row), session management (list and revoke active sessions), and rotation tracking (invalidate the old token on use). Purely stateless refresh tokens cannot be revoked before their expiry.

**Q42: How do you implement a "sign out from all devices" feature with JWT?**  
A: Maintain a `sessions` table — one row per active refresh token. On "sign out all", delete all rows for the user and add all active access token JTIs to the Redis denylist. Access tokens continue working until the denylist entry TTL expires (up to 15 minutes); refresh tokens are immediately invalidated.

**Q43: How do you test refresh token rotation?**  
A: Login to get a token pair, use the refresh token to get a new pair, assert the tokens differ, then assert the old refresh token is now rejected with `401`.

```python
async def test_refresh_token_rotation(client: AsyncClient):
    tokens = await register_and_login(client)
    new_tokens = (await client.post(
        "/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )).json()
    assert new_tokens["access_token"] != tokens["access_token"]
    assert new_tokens["refresh_token"] != tokens["refresh_token"]
```

**Q44: How do you test that a revoked token is rejected?**  
A: Call `/auth/logout` with the access token, then attempt to use the same token on a protected endpoint and assert `401`.

```python
async def test_revoked_token_rejected(client: AsyncClient, fake_redis):
    tokens = await register_and_login(client)
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    logout = await client.post("/auth/logout", headers=headers)
    assert logout.status_code == 204
    me = await client.get("/auth/me", headers=headers)
    assert me.status_code == 401
```

**Q45: How do you structure `conftest.py` for an auth test suite with Redis?**  
A: Provide `client`, `access_token`, and `auth_headers` fixtures, a `reset_store` autouse fixture that clears the in-memory store between tests, and a `fake_redis` fixture that overrides the Redis dependency.

```python
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from app.main import app
from app.security import create_access_token
from app.dependencies import get_redis
import app.models as _store


@pytest.fixture(autouse=True)
def reset_store():
    """Clear in-memory user store between tests."""
    _store._users.clear()
    _store._email_index.clear()
    _store._next_id = 1


@pytest.fixture
def fake_redis():
    """In-memory dict-backed mock Redis client for denylist testing."""
    store: dict[str, str] = {}
    mock = AsyncMock()

    async def setex(key, ttl, value):
        store[key] = value

    async def exists(key):
        return 1 if key in store else 0

    mock.setex.side_effect = setex
    mock.exists.side_effect = exists
    return mock, store


@pytest.fixture
async def client(fake_redis):
    mock_redis, _ = fake_redis
    app.dependency_overrides[get_redis] = lambda: mock_redis
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
def access_token() -> str:
    """Direct access token for tests that don't need a real login flow."""
    return create_access_token(subject=1)


@pytest.fixture
def auth_headers(access_token: str) -> dict[str, str]:
    """Authorization header dict for authenticated test requests."""
    return {"Authorization": f"Bearer {access_token}"}
```

**Q46: How do you test a protected route without generating a real JWT?**  
A: Override the dependency entirely — no JWT, no HTTP headers, no mocking of `pyjwt`.

```python
from app.main import app
from app.dependencies import get_current_user

fake_user = User(id=1, email="test@example.com", hashed_password="x", is_active=True)

@pytest.fixture(autouse=True)
def override_auth():
    """Override auth for all tests in this module."""
    app.dependency_overrides[get_current_user] = lambda: fake_user
    yield
    app.dependency_overrides.clear()
```

**Q47: How do you test that `401` is returned when no token is provided?**  
A: Do NOT use `dependency_overrides` for this test — you are testing that the unoverridden `OAuth2PasswordBearer` correctly rejects missing tokens.

```python
async def test_protected_route_requires_token(client: AsyncClient):
    response = await client.get("/auth/me")
    assert response.status_code == 401
    assert response.headers.get("WWW-Authenticate") == "Bearer"
```

**Q48: How do you assert that `hashed_password` never appears in any API response?**  
A: Check the raw response text for any Argon2 hash prefix, the `hashed_password` key, and the plaintext password.

```python
async def test_password_never_leaked(client: AsyncClient):
    await client.post("/auth/register",
        json={"email": "q@example.com", "password": "secret123"})
    tokens = (await client.post("/auth/token",
        data={"username": "q@example.com", "password": "secret123"})).json()
    me_response = await client.get(
        "/auth/me", headers={"Authorization": f"Bearer {tokens['access_token']}"}
    )
    response_text = me_response.text
    assert "hashed_password" not in response_text
    assert "secret123" not in response_text
    assert "$argon2" not in response_text  # Argon2 hash prefix must never appear in output
```

---

### 🎯 Working Code Artefact 4: Full Test Suite

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from app.main import app
from app.security import create_access_token, create_refresh_token
from app.dependencies import get_redis
import app.models as _store


@pytest.fixture(autouse=True)
def reset_store():
    """Clears in-memory user store between tests — prevents cross-test contamination."""
    _store._users.clear()
    _store._email_index.clear()
    _store._next_id = 1


@pytest.fixture
def fake_redis():
    """Dict-backed async mock for Redis denylist operations."""
    store: dict[str, str] = {}
    mock = AsyncMock()

    async def setex(key: str, ttl: int, value: str) -> None:
        store[key] = value

    async def exists(key: str) -> int:
        return 1 if key in store else 0

    mock.setex.side_effect = setex
    mock.exists.side_effect = exists
    return mock, store


@pytest.fixture
async def client(fake_redis):
    """AsyncClient with fake Redis injected."""
    mock_redis, _ = fake_redis
    app.dependency_overrides[get_redis] = lambda: mock_redis
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
def access_token() -> str:
    """Direct token for tests that bypass the login flow."""
    return create_access_token(subject=1)


@pytest.fixture
def refresh_token_str() -> str:
    """Direct refresh token for rotation tests."""
    return create_refresh_token(subject=1)


@pytest.fixture
def auth_headers(access_token: str) -> dict[str, str]:
    """Authorization header dict for authenticated requests."""
    return {"Authorization": f"Bearer {access_token}"}


async def register_and_login(client: AsyncClient) -> dict:
    """Helper — registers a test user and returns the token pair."""
    await client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "secret123"},
    )
    resp = await client.post(
        "/auth/token",
        data={"username": "test@example.com", "password": "secret123"},
    )
    return resp.json()
```

```python
# tests/test_auth.py
import pytest
from httpx import AsyncClient
from tests.conftest import register_and_login


async def test_register_success(client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={"email": "new@example.com", "password": "secure123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert "hashed_password" not in data
    assert "$argon2" not in response.text  # Argon2 prefix must never appear in output


async def test_duplicate_registration_returns_409(client: AsyncClient):
    payload = {"email": "dup@example.com", "password": "secure123"}
    await client.post("/auth/register", json=payload)
    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 409


async def test_login_returns_token_pair(client: AsyncClient):
    tokens = await register_and_login(client)
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["token_type"] == "bearer"


async def test_wrong_password_returns_401(client: AsyncClient):
    await client.post("/auth/register",
        json={"email": "t@e.com", "password": "correct"})
    response = await client.post("/auth/token",
        data={"username": "t@e.com", "password": "wrong"})
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


async def test_unknown_email_returns_same_401(client: AsyncClient):
    response = await client.post("/auth/token",
        data={"username": "nobody@example.com", "password": "anything"})
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


async def test_protected_route_requires_token(client: AsyncClient):
    response = await client.get("/auth/me")
    assert response.status_code == 401
    assert response.headers.get("WWW-Authenticate") == "Bearer"


async def test_protected_route_with_valid_token(client: AsyncClient):
    tokens = await register_and_login(client)
    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert "hashed_password" not in response.json()


async def test_refresh_token_returns_new_pair(client: AsyncClient):
    tokens = await register_and_login(client)
    response = await client.post(
        "/auth/refresh", json={"refresh_token": tokens["refresh_token"]}
    )
    assert response.status_code == 200
    new_tokens = response.json()
    assert new_tokens["access_token"] != tokens["access_token"]
    assert new_tokens["refresh_token"] != tokens["refresh_token"]


async def test_access_token_rejected_on_refresh_endpoint(client: AsyncClient):
    """Token confusion guard — access token must not be accepted by /refresh."""
    tokens = await register_and_login(client)
    response = await client.post(
        "/auth/refresh", json={"refresh_token": tokens["access_token"]}
    )
    assert response.status_code == 401


async def test_refresh_token_rejected_on_protected_route(client: AsyncClient):
    """Token confusion guard — refresh token must not be accepted by /me."""
    tokens = await register_and_login(client)
    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {tokens['refresh_token']}"},
    )
    assert response.status_code == 401


async def test_invalid_token_returns_401(client: AsyncClient):
    response = await client.get(
        "/auth/me",
        headers={"Authorization": "Bearer this.is.not.a.valid.jwt"},
    )
    assert response.status_code == 401


async def test_password_never_leaked_in_any_response(client: AsyncClient):
    tokens = await register_and_login(client)
    me = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert "hashed_password" not in me.text
    assert "secret123" not in me.text
    assert "$argon2" not in me.text  # Argon2 hash prefix must never appear


async def test_logout_revokes_token(client: AsyncClient, fake_redis):
    """After logout the access token must be on the denylist and rejected."""
    _, denylist_store = fake_redis
    tokens = await register_and_login(client)
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}

    logout = await client.post("/auth/logout", headers=headers)
    assert logout.status_code == 204

    # Verify the jti is now in the fake denylist store
    assert any("denylist:" in key for key in denylist_store)

    # The revoked token must now be rejected on protected routes
    me = await client.get("/auth/me", headers=headers)
    assert me.status_code == 401
```

### ✅ Key Concepts

- **`fake_redis` fixture** simulates the denylist without a real Redis server — `setex` and `exists` backed by a plain dict
- **`reset_store` autouse fixture** prevents cross-test contamination — clears in-memory state before each test
- **`asyncio_mode = "auto"`** removes `@pytest.mark.asyncio` from every test — set it once in `pyproject.toml`
- **`$argon2` prefix check** in test assertions — the Argon2 hash prefix must never appear in any API response body (replaces the old `$2b$` bcrypt check)
- **Logout test verifies denylist** — asserts both that the denylist store contains the jti key and that the revoked token is rejected on the next request

---

## 🖥️ Part 5: Junior → Senior Interview Tier

### Q&A Batch 5: Interview Tier — Junior to Senior

### Junior to Mid-Level (£50k–£70k)

**Q49: What is JWT in plain terms?**  
A: A JWT (JSON Web Token) is a self-contained, digitally signed token that proves identity. Instead of the server storing session data, it embeds the user's ID and an expiry timestamp into a string, signs it with a secret key, and sends it to the client. On each request, the client sends the token back; the server verifies the signature to confirm it has not been tampered with — no database lookup required for authentication.

**Q50: What is the difference between authentication and authorisation?**  
A: Authentication answers "who are you?" — verifying identity via a password or token. Authorisation answers "what are you allowed to do?" — checking permissions after identity is confirmed. In FastAPI, `get_current_user` handles authentication; `require_admin` (chained on top) handles authorisation. A common interview mistake is using `403 Forbidden` for unauthenticated requests (should be `401`).

**Q51: Why should passwords never be stored in plain text?**  
A: Plain-text storage means a database breach exposes every user's password immediately. Passwords must be hashed with a slow, memory-hard algorithm (Argon2, bcrypt) so brute-force attacks take years per hash. Argon2 embeds a random salt per hash — two users with the same password produce different hashes, defeating rainbow table attacks.

**Q52: What is a bearer token?**  
A: A bearer token is a credential that grants access to any request that "bears" (presents) it — no further proof of identity is required. The name comes from RFC 6750. The client includes it in the `Authorization: Bearer <token>` header. This is why HTTPS is mandatory — any intercepted bearer token gives the attacker full access until it expires or is revoked.

**Q53: What does `OAuth2PasswordBearer(tokenUrl="/auth/token")` do?**  
A: It creates a FastAPI security dependency that extracts the bearer token from the `Authorization` header and registers the `/auth/token` URL as the OAuth2 token endpoint in the OpenAPI spec. Swagger UI uses the `tokenUrl` to render the "Authorise" button and form. It does not validate the token — it only extracts it.

### Mid to Senior Level (£70k–£90k)

**Q54: How do you structure an auth service that scales to multiple FastAPI microservices?**  
A: Centralise token issuance in a dedicated auth service. Switch to RS256 — the auth service holds the private key; all other services fetch the public key from the JWKS endpoint and verify tokens locally. No inter-service call is needed per request. Each resource service runs its own `get_current_user` dependency that fetches and caches the JWKS on startup and verifies tokens independently. The Redis denylist must also be shared across services — use a shared Redis instance.

**Q55: How do you implement an account lockout after N failed login attempts?**  
A: Store a `failed_attempts` counter and `locked_until` timestamp per user in the database (or Redis for speed). On each failed login, increment the counter. If it exceeds N (e.g., 5), set `locked_until = now + 15 minutes`. On each login attempt, check `locked_until` first and return `429 Too Many Requests` if still locked. Reset `failed_attempts` to 0 on successful login.

**Q56: Walk through what happens end-to-end when a client makes an authenticated request.**  
A: The full chain from HTTP header to route handler response:

1. Client sends `GET /api/users/me` with `Authorization: Bearer <access_token>` header
2. `OAuth2PasswordBearer` extracts the token string
3. `get_current_user` calls `decode_token()` — `pyjwt` verifies the signature and `exp` claim
4. `get_current_user` checks `token_type == "access"` — prevents token confusion
5. `get_current_user` checks `jti` against the Redis denylist — rejects revoked tokens
6. `get_current_user` extracts `sub`, casts to `int`, calls `user_repo.get_by_id()`
7. The DB returns the user — `get_current_user` checks `is_active == True`
8. FastAPI injects the `User` object into the route handler
9. Route handler returns the user — `response_model=UserOut` filters out `hashed_password`

**Q57: Why use Argon2 over bcrypt for new systems in 2026?**  
A: Argon2 is memory-hard — it requires a configurable amount of RAM per hash attempt. This makes GPU attacks (which can run bcrypt at millions of attempts per second) far more expensive, since GPUs have limited memory bandwidth relative to compute. Argon2 won the Password Hashing Competition (PHC) and is the OWASP recommended default for new systems. bcrypt remains acceptable for legacy systems where migration cost is high.

**Q58: How do you handle a security incident where all user sessions must be invalidated immediately?**  
A: Rotate the JWT secret key immediately — all tokens signed with the old key become invalid. If using RS256, rotate the private key and immediately remove the old public key from the JWKS endpoint. For a softer approach, add a global `sessions_invalidated_at` timestamp in Redis and reject any token with `iat < sessions_invalidated_at`. Flush the entire denylist to avoid stale entries from the old key.

### Senior Level (£90k–£130k)

**Q59: How would you design a zero-downtime JWT secret key rotation strategy?**  
A: Implement key versioning with a `kid` (key ID) claim in the token header. Maintain a key registry with the current and N previous keys. On `jwt.decode()`, look up the `kid` from the token header and select the corresponding key. Tokens signed with old keys continue to work until they expire. New tokens are signed with the new key. No active sessions are invalidated during rotation.

**Q60: How would you architect auth for a system with both human users and machine-to-machine service accounts?**  
A: Human users: OAuth2 password grant → short-lived access tokens + refresh tokens. Service accounts: static API keys stored as SHA-256 hashes in the database, looked up by hash on each request. Both paths produce a user/principal object that flows into the same `Annotated` dependency chain. Guards that only allow human users assert `payload["token_type"] == "access"` — service accounts never produce JWTs.

**Q61: How would you migrate from bcrypt (passlib) to Argon2 (pwdlib) without forcing a password reset?**  
A: Add a `hash_scheme` column to the users table. On login, after successful bcrypt verification, re-hash the password with Argon2 and update the stored hash and scheme. New registrations use Argon2 immediately. After a migration period, users who have not logged in can be prompted to reset their password or remain on bcrypt until they do. This is a phased, transparent migration with no forced logouts.

---

### 🎯 Working Code Artefact 5: Full Application — main.py and Project Structure

```
auth_demo/
├── app/
│   ├── __init__.py
│   ├── main.py               ← FastAPI app with lifespan, CORS, Redis, timing middleware
│   ├── config.py             ← pydantic-settings with redis_url
│   ├── models.py             ← in-memory user store (replaced Sprint 2 Day 2)
│   ├── schemas.py            ← Pydantic schemas with SecretStr
│   ├── security.py           ← pyjwt + pwdlib[argon2] + hash_api_key utilities
│   ├── dependencies.py       ← Annotated aliases + Redis denylist + Depends chain
│   └── routers/
│       ├── __init__.py
│       └── auth.py           ← async route handlers including /logout
├── tests/
│   ├── conftest.py           ← AsyncClient fixtures + fake_redis + reset_store
│   └── test_auth.py          ← 13 async test functions including logout/denylist
├── pyproject.toml
└── .env
```

```
# .env
SECRET_KEY=dev-secret-key-replace-in-production-minimum-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
DEBUG=true
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173"]
REDIS_URL=redis://localhost:6379
```

```python
# app/main.py
import time
import uuid
from contextlib import asynccontextmanager

import redis.asyncio as aioredis
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import auth

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: create Redis client. Shutdown: close it."""
    app.state.redis = aioredis.from_url(settings.redis_url, decode_responses=True)
    yield
    await app.state.redis.aclose()


app = FastAPI(
    title="JWT Auth Demo",
    version="1.0.0",
    description="Production-pattern JWT authentication with Redis denylist — Sprint 2 Day 1",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.middleware("http")
async def request_correlation(request: Request, call_next):
    """Adds X-Request-ID and X-Process-Time-Ms to every response."""
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-Ms"] = str(
        round((time.perf_counter() - start) * 1000, 2)
    )
    return response


app.include_router(auth.router)


@app.get("/health", include_in_schema=False)
async def health() -> dict[str, str]:
    """Health check endpoint — used by container orchestrators."""
    return {"status": "ok"}
```

```bash
# Run commands

# Development (hot reload + Swagger UI at /docs):
uv run fastapi dev app/main.py

# Production:
uv run fastapi run app/main.py

# Tests with coverage:
uv run pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=80

# Lint + type-check:
uv run ruff check app/
uv run mypy app/
```

---

## 📊 Quick Reference — Auth Patterns

| Pattern                     | Implementation                                                      |
| --------------------------- | ------------------------------------------------------------------- |
| Extract bearer token        | `Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="..."))]`     |
| Decode + verify JWT         | `jwt.decode(token, key, algorithms=["HS256"])`                      |
| Hash password (Argon2)      | `password_hash.hash(plain)` via `PasswordHash.recommended()`        |
| Verify password             | `password_hash.verify(plain, hashed)`                               |
| Prevent timing attack       | Always call `verify_password(plain, _DUMMY_HASH)` for unknown users |
| Token confusion guard       | `assert payload["token_type"] == "access"` in `get_current_user`    |
| Redis revocation            | `redis.setex(f"denylist:{jti}", remaining_ttl, "1")`                |
| Denylist check              | `await redis.exists(f"denylist:{jti}") == 1`                        |
| RFC 6750 compliant 401      | `HTTPException(401, headers={"WWW-Authenticate": "Bearer"})`        |
| Composable auth chain       | `ActiveUser = Annotated[User, Depends(get_current_active_user)]`    |
| Test auth override          | `app.dependency_overrides[get_current_user] = lambda: mock_user`    |
| Prevent password in logs    | `password: SecretStr` + `.get_secret_value()` only at hash time     |
| Service account key storage | `hashlib.sha256(raw_key.encode()).hexdigest()` — never raw key      |
| Role set in guards          | `frozenset({"admin", "superuser"})` — immutable at definition time  |

### Mental Model Mapping (TypeScript → Python / JWT Auth)

| TypeScript / Node.js              | Python / FastAPI                              | Notes                                              |
| --------------------------------- | --------------------------------------------- | -------------------------------------------------- |
| `jsonwebtoken` / `jose`           | `pyjwt[crypto]` (`import jwt`)                | JWT encode/decode — `python-jose` is abandoned     |
| `bcrypt` npm package              | `pwdlib[argon2]` `PasswordHash.recommended()` | Password hashing — Argon2 > bcrypt for new systems |
| `passport-jwt` strategy           | `get_current_user` `Depends` chain            | Bearer token extraction and validation             |
| Express middleware `authenticate` | `Annotated[User, Depends(get_current_user)]`  | Route-level auth guard                             |
| `req.user` in route handler       | `current_user: CurrentUser` in route handler  | Injected authenticated user                        |
| `process.env.JWT_SECRET`          | `pydantic-settings` `Settings.secret_key`     | Env var reading with type safety                   |
| Redis session store               | Redis denylist on `jti` with TTL              | Immediate JWT revocation                           |

---

## 🎯 Practice Exercises

**Exercise 1 — Add `token_expires_at` to the `/me` response**

Extend `UserOut` to a `UserWithExpiry` schema that includes `token_expires_at: datetime`. Modify `read_me` to accept `Annotated[str, Depends(oauth2_scheme)]` directly, decode the `exp` claim, and return it alongside the user fields. Write a test that asserts `token_expires_at` is a valid ISO datetime in the future.

**Exercise 2 — Introduce and fix the token confusion vulnerability empirically**

Remove the `token_type` check from `get_current_user`. Write a test that passes a refresh token to `GET /auth/me` and asserts `200`. Run it — it should pass (the vulnerability is present). Restore the `token_type` check and confirm the test now fails with `401`. This empirical cycle is the correct way to validate security guards.

**Exercise 3 — Add `require_role()` factory with `frozenset`**

Implement a `require_role(*roles: str)` dependency factory that:

- Takes permitted roles as arguments
- Stores them internally as `frozenset` — immutable and hashable at definition time
- Chains on `get_current_active_user`
- Returns `HTTPException(403)` if the user's role is not in the permitted set
- Write tests for admin-only and user-accessible routes

```python
# Scaffold — implement the body
def require_role(*roles: str):
    """Factory returning a FastAPI dependency that enforces role membership."""
    permitted: frozenset[str] = frozenset(roles)  # immutable at definition time
    async def _check_role(user: ActiveUser) -> User:
        ...
    return _check_role
```

---

## 📚 Additional Resources

| Resource                               | URL                                                                          |
| -------------------------------------- | ---------------------------------------------------------------------------- |
| pyjwt documentation                    | https://pyjwt.readthedocs.io/en/stable/                                      |
| pyjwt releases                         | https://github.com/jpadilla/pyjwt/releases                                   |
| pwdlib documentation                   | https://frankie567.github.io/pwdlib/                                         |
| pwdlib releases                        | https://github.com/frankie567/pwdlib/releases                                |
| FastAPI security docs                  | https://fastapi.tiangolo.com/tutorial/security/                              |
| uv documentation                       | https://docs.astral.sh/uv/                                                   |
| RFC 7519 — JWT specification           | https://www.rfc-editor.org/rfc/rfc7519                                       |
| RFC 6750 — Bearer Token Usage          | https://www.rfc-editor.org/rfc/rfc6750                                       |
| OWASP A07 — Auth Failures              | https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/ |
| OWASP A02 — Cryptographic Failures     | https://owasp.org/Top10/A02_2021-Cryptographic_Failures/                     |
| Password Hashing Competition           | https://www.password-hashing.net/                                            |
| PEP 695 — Type Aliases (generics only) | https://peps.python.org/pep-0695/                                            |
| PEP 703 — Free-Threading               | https://peps.python.org/pep-0703/                                            |
| Azure Entra External ID docs           | https://aka.ms/entra-external-id-docs                                        |

---

## ✅ Today's Deliverable Checklist

By the end of today, you should have:

- [ ] Installed Python 3.14 via `uv python install 3.14` and pinned with `uv python pin 3.14`
- [ ] `pyproject.toml` updated with `requires-python = ">=3.14"`, `ruff>=1.0`, `mypy>=1.18`, `target-version = "py314"`, `python_version = "3.14"`
- [ ] `pyjwt[crypto]>=2.9`, `pwdlib[argon2]`, and `redis>=5.0` in dependencies — no `python-jose` or `passlib` anywhere in `pyproject.toml`
- [ ] `app/config.py` with `pydantic-settings`, `lru_cache`, `redis_url`, and all auth settings read from `.env`
- [ ] `app/schemas.py` with `UserCreate` using `SecretStr` on `password` — never `str`
- [ ] `app/security.py` using `import jwt` (pyjwt), `from pwdlib import PasswordHash`, `PasswordHash.recommended()`, `datetime.now(timezone.utc)`, `uuid.uuid4()` in `jti`, explicit `algorithms=[settings.algorithm]` in `jwt.decode()`
- [ ] `hash_api_key()` function using `hashlib.sha256` for service account key storage
- [ ] `_DUMMY_HASH` constant and `authenticate_user` function with constant-time comparison for unknown emails
- [ ] `app/dependencies.py` with `get_redis`, `is_token_revoked`, `revoke_token`, and `get_current_user` using `Annotated[str, Depends(oauth2_scheme)]`
- [ ] `CurrentUser` and `ActiveUser` declared as **plain module-level assignments** — `CurrentUser = Annotated[User, Depends(get_current_user)]` — NOT using PEP 695 `type` statement
- [ ] Redis denylist check in `get_current_user` — after signature verification, before user DB lookup
- [ ] `token_type` guard in `get_current_user` — `payload.get("token_type") != "access"` raises 401
- [ ] `app/routers/auth.py` with five `async def` route handlers: `register`, `login`, `refresh_token`, `logout`, `read_me`
- [ ] `logout` endpoint calls `revoke_token` with the token's `jti` and `exp`
- [ ] `app/main.py` with `lifespan` creating and closing the Redis client, explicit CORS methods/headers, timing middleware, docs disabled in non-debug mode
- [ ] `uv run fastapi dev app/main.py` confirmed for development (Swagger UI at `http://localhost:8000/docs`)
- [ ] `uv run fastapi run app/main.py` confirmed as the production start command
- [ ] `tests/conftest.py` with `AsyncClient`, `fake_redis` fixture, `reset_store` autouse fixture, `auth_headers` fixture
- [ ] `tests/test_auth.py` with 13 async test functions covering all scenarios
- [ ] Both token confusion tests passing: refresh token rejected on `/me`, access token rejected on `/refresh`
- [ ] `test_logout_revokes_token` passing — token on denylist and rejected on next request
- [ ] `test_password_never_leaked_in_any_response` passing — `$argon2` prefix never in any response body
- [ ] `uv run pytest --cov=app --cov-fail-under=80` passing
- [ ] `uv run ruff check app/` and `uv run mypy app/` passing with zero errors
- [ ] Committed to GitHub — Sprint 2 Day 1 branch or commit

---

**Next Sprint Day:** Sprint 2 · Day 2 — Role-Based Access Control: user roles model in PostgreSQL, `require_role()` factory with `frozenset`, admin vs user vs service account separation. Wire the auth layer from today to the async PostgreSQL repository from Sprint 1 Day 3.

---

_This learning material is part of the 2026 Python · Azure · AI Engineering Roadmap targeting UK senior roles (£90k–£130k / £550–£750/day). Python 3.14 · uv · FastAPI · pyjwt[crypto] · pwdlib[argon2] · Redis denylist · Pydantic v2 · ruff · mypy._
