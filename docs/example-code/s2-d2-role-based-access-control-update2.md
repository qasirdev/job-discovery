```
<prompt>
@jobs-list/2026-python-ai-azure-roadmap-v3.md
go and create file according to @jobs-list/2026-learning-prompt-v5.md in folder learning-sprints for:
- **Sat 25 Apr** — Role-Based Access Control: user roles model in PostgreSQL, permission guards as FastAPI dependencies, admin vs user vs service account separation. Mirror the RBAC patterns you used in your Azure Entra / Next.js work.

</prompt>
```

# Sprint 2 · Day 2 · Sat 25 Apr 2026

**Topic:** Role-Based Access Control: user roles model in PostgreSQL, permission guards as FastAPI dependencies, admin vs user vs service account separation. Mirror the RBAC patterns used in Azure Entra / Next.js work.

---

## Step 1: Progressive Learning Steps & UK Job Market Relevance

### 🖥️ Day Type: Backend

This is a pure backend day. All artefacts use FastAPI, PostgreSQL (async SQLAlchemy), and Pydantic v2. No frontend artefacts are produced.

---

### 🎯 Learning Objectives

This day builds a production-grade Role-Based Access Control (RBAC) system in FastAPI — the pattern that replaces Azure Entra External ID's app role assignments when you own the backend yourself.

1. **Roles Model in PostgreSQL**
   - `UserRole` enum column in the `users` table via SQLAlchemy `Enum` type
   - Role hierarchy: `admin` > `user` > `service_account`
   - Alembic migration to add the role column to an existing table
   - Optional: `roles` many-to-many join table for multi-role assignments

2. **Permission Guards as FastAPI Dependencies**
   - `Depends()` chain: `get_current_user` → `require_role(roles)` → protected route
   - `Annotated` type alias pattern for clean dependency declarations (`CurrentUser = Annotated[User, Depends(get_current_user)]`)
   - `HTTPException(403)` vs `HTTPException(401)` — when to use each
   - Returning `403 Forbidden` with RFC 7807 problem detail format

3. **Admin vs User vs Service Account Separation**
   - Route-level role enforcement: `@router.get("/admin/...", dependencies=[Depends(require_admin)])`
   - Service account pattern: API key header (`X-API-Key`) as a parallel auth path
   - Scope-based sub-permissions: `admin:read`, `admin:write`, `user:read` — mapping from Entra ID scope claims

4. **Bridging from Azure Entra / Next.js RBAC**
   - Azure Entra External ID uses `roles` claim in the JWT — FastAPI replicates this with DB-backed role lookup
   - `hasRole("Admin")` in Next.js middleware maps directly to `require_role(["admin"])` in FastAPI `Depends()`
   - Service account separation mirrors Entra ID Managed Identity vs user principal distinction

---

### 📊 UK Job Market Relevance (£90k–£130k / £550–£750/day)

| Skill Area                     | Market Frequency      | Interview Focus | Why It Matters                                                                      |
| ------------------------------ | --------------------- | --------------- | ----------------------------------------------------------------------------------- |
| **RBAC in FastAPI**            | ~70% of backend roles | Very High       | Almost every production API has roles; interviewers expect a working implementation |
| **FastAPI `Depends()` chains** | ~75% of FastAPI roles | High            | Core dependency injection pattern; tested in code reviews and system design         |
| **PostgreSQL role modelling**  | ~60% of senior roles  | High            | Schema design for access control is a senior filter question                        |
| **RFC 7807 error responses**   | ~45% of senior roles  | Medium          | Structured errors show production maturity                                          |
| **Service account auth**       | ~50% of roles         | Medium-High     | Service-to-service auth is expected in distributed systems                          |
| **Azure Entra RBAC mapping**   | ~35% of Azure roles   | High            | Direct transfer of your existing Entra / Next.js RBAC knowledge                     |

### ✅ Key Industry Patterns for 2026

- **RBAC via `Depends()` chains** is the FastAPI standard — not middleware, not decorators
- **`Enum` columns** in PostgreSQL with SQLAlchemy `Enum` type are the correct choice for a small, fixed role set
- **`Annotated` type aliases** (`CurrentUser = Annotated[User, Depends(get_current_user)]`) are the 2026 pattern — eliminates repeated `Depends()` declarations
- **Service accounts use API keys**, not JWTs, for machine-to-machine calls — separate auth path from user tokens
- **RFC 7807 problem details** (`application/problem+json`) are expected for `4xx`/`5xx` responses in enterprise APIs

### 💼 What UK Interviewers Will Ask

- "How would you implement RBAC in FastAPI?" → `Depends()` chains, role enum in DB, `require_role` dependency
- "What is the difference between authentication and authorisation?" → authn = who are you, authz = what can you do
- "How do you prevent privilege escalation?" → server-side role lookup per request, never trust client-supplied roles
- "How do you handle multi-role users?" → roles as a list/set on the user model or join table
- "When do you return 401 vs 403?" → 401 = not authenticated, 403 = authenticated but not authorised
- "How does your FastAPI RBAC compare to Azure Entra ID roles?" → Entra uses JWT `roles` claim, FastAPI uses DB lookup — both enforce at the dependency layer
- "How do you test protected routes?" → `dependency_overrides` to inject a mock user with a specific role

---

## Step 2: Comprehensive Q&A and Code Artefacts

---

## 📦 Required Packages

```bash
# --- Using uv (recommended) ---
uv python install 3.14
uv python pin 3.14

uv init fastapi-rbac
cd fastapi-rbac

# Core
uv add fastapi "uvicorn[standard]"
uv add pydantic pydantic-settings
uv add "sqlalchemy[asyncio]" asyncpg alembic
uv add "pyjwt[crypto]"
uv add "pwdlib[argon2]"
uv add redis structlog

# Dev
uv add --dev pytest pytest-asyncio httpx pytest-cov ruff mypy

# Run dev server
uv run fastapi dev app/main.py

# Run production server
uv run fastapi run app/main.py
```

```bash
# --- Using poetry (common in existing codebases) ---
poetry new fastapi-rbac
cd fastapi-rbac

poetry add fastapi "uvicorn[standard]"
poetry add pydantic pydantic-settings
poetry add sqlalchemy[asyncio] asyncpg alembic
poetry add "pyjwt[crypto]"
poetry add "pwdlib[argon2]"
poetry add redis structlog

poetry add --group dev pytest pytest-asyncio httpx pytest-cov ruff mypy
```

```toml
# pyproject.toml — 2026 version pins
[project]
name = "fastapi-rbac"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = [
    "fastapi>=0.115",
    "uvicorn[standard]>=0.32",
    "pydantic>=2.11",
    "pydantic-settings>=2.7",
    "sqlalchemy[asyncio]>=2.0",
    "asyncpg>=0.30",
    "alembic>=1.14",
    "pyjwt[crypto]>=2.9",
    "pwdlib[argon2]>=0.2",
    "redis>=5.0",
    "structlog>=24.4",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8",
    "pytest-asyncio>=0.24",
    "httpx>=0.28",
    "pytest-cov>=6",
    "ruff>=1.0",
    "mypy>=1.18",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"

[tool.mypy]
python_version = "3.14"
strict = true

[tool.ruff]
target-version = "py314"
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "SIM"]
```

---

## 🖥️ Artefact 1 — PostgreSQL Roles Model & Alembic Migration

### Project Layout

```
fastapi-rbac/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       ├── auth.py
│   │       └── users.py
│   └── core/
│       └── security.py
├── alembic/
│   ├── env.py
│   └── versions/
│       └── 001_add_role_column.py
├── tests/
│   ├── conftest.py
│   └── test_rbac.py
└── pyproject.toml
```

---

### `app/core/config.py`

```python
"""Application configuration using pydantic-settings."""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_rbac"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: SecretStr = SecretStr("change-me-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    api_key_header: str = "X-API-Key"


settings = Settings()
```

---

### `app/core/database.py`

```python
"""Async SQLAlchemy engine and session factory."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """Declarative base for all SQLAlchemy ORM models."""


engine = create_async_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=20,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session, ensuring it is closed on exit."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

---

### `app/models/user.py`

```python
"""SQLAlchemy ORM model for users, including the UserRole enum."""

import enum
import uuid

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserRole(str, enum.Enum):
    """Enumeration of valid user roles.

    Roles are ordered from lowest to highest privilege:
    USER < ADMIN; SERVICE_ACCOUNT is a parallel auth path.
    """

    USER = "user"
    ADMIN = "admin"
    SERVICE_ACCOUNT = "service_account"


class User(Base):
    """ORM model representing a user record in the database."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="userrole"),
        default=UserRole.USER,
        nullable=False,
        index=True,
    )
    # SHA-256 hex digest of the raw API key — populated for SERVICE_ACCOUNT users only.
    # The raw key is issued once at account creation and never stored.
    api_key_hash: Mapped[str | None] = mapped_column(
        String(64), unique=True, nullable=True, index=True
    )

    def __repr__(self) -> str:
        """Return a developer-readable representation of the User instance."""
        return f"<User id={self.id} email={self.email} role={self.role}>"
```

---

### `app/schemas/user.py`

```python
"""Pydantic v2 request/response schemas for user operations."""

import uuid

from pydantic import BaseModel, EmailStr, field_validator

from app.models.user import UserRole


class UserCreate(BaseModel):
    """Schema for creating a new user account."""

    email: EmailStr
    password: str
    role: UserRole = UserRole.USER

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        """Validate that the password meets the minimum length requirement."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserRead(BaseModel):
    """Schema for reading a user record — never exposes hashed_password or api_key_hash."""

    id: uuid.UUID
    email: EmailStr
    is_active: bool
    role: UserRole

    model_config = {"from_attributes": True}


class UserRoleUpdate(BaseModel):
    """Schema for an admin updating a user's role."""

    role: UserRole


class TokenResponse(BaseModel):
    """Schema for the JWT token response returned on successful login."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for the decoded JWT token payload.

    jti (JWT ID) is a unique identifier per token required for denylist-based revocation.
    """

    sub: str  # user email
    role: UserRole
    jti: str  # unique token ID — uuid4 string, used as the Redis denylist key
```

---

### `app/core/security.py`

```python
"""JWT token creation, password hashing, and Redis token denylist utilities."""

import hashlib
import uuid
from datetime import UTC, datetime, timedelta

import jwt
import redis.asyncio as aioredis
from pwdlib import PasswordHash

from app.core.config import settings
from app.models.user import UserRole
from app.schemas.user import TokenPayload

# Argon2 via pwdlib — OWASP recommended default for new systems in 2026.
# GPU-resistant due to memory-hardness; replaces abandoned passlib/bcrypt.
password_hash = PasswordHash.recommended()

# Redis client — shared instance, connected lazily on first use.
_redis: aioredis.Redis | None = None


def get_redis() -> aioredis.Redis:
    """Return the shared Redis client, creating it on first call.

    Returns:
        An async Redis client connected to settings.redis_url.
    """
    global _redis
    if _redis is None:
        _redis = aioredis.from_url(settings.redis_url, decode_responses=True)
    return _redis


def hash_password(plain: str) -> str:
    """Return an Argon2 hash of the given plain-text password.

    Args:
        plain: The raw plain-text password string.

    Returns:
        Argon2 hash string safe for database storage.
    """
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Return True if the plain-text password matches the stored Argon2 hash.

    Args:
        plain: The raw plain-text password string.
        hashed: The stored Argon2 hash string.

    Returns:
        True if the password matches, False otherwise.
    """
    return password_hash.verify(plain, hashed)


def hash_api_key(raw_key: str) -> str:
    """Return a SHA-256 hex digest of the raw API key for safe database storage.

    The raw key is never stored — only this digest is persisted.

    Args:
        raw_key: The raw API key string issued to a service account.

    Returns:
        64-character lowercase hex string.
    """
    return hashlib.sha256(raw_key.encode()).hexdigest()


def create_access_token(payload: TokenPayload) -> str:
    """Create a signed JWT access token from the given payload.

    A unique jti (JWT ID) is embedded so the token can be individually
    revoked via the Redis denylist without rotating the signing secret.

    Args:
        payload: Token payload containing subject (email), role, and jti.

    Returns:
        Signed JWT string.
    """
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    claims: dict[str, object] = {
        "sub": payload.sub,
        "role": payload.role.value,
        "jti": payload.jti,
        "exp": expire,
    }
    return jwt.encode(
        claims,
        settings.secret_key.get_secret_value(),
        algorithm=settings.algorithm,
    )


def decode_access_token(token: str) -> TokenPayload:
    """Decode and validate a JWT access token.

    Args:
        token: The raw JWT string.

    Returns:
        Validated TokenPayload including jti for denylist checks.

    Raises:
        jwt.InvalidTokenError: If the token is invalid, expired, or malformed.
    """
    raw = jwt.decode(
        token,
        settings.secret_key.get_secret_value(),
        algorithms=[settings.algorithm],
    )
    return TokenPayload(sub=raw["sub"], role=UserRole(raw["role"]), jti=raw["jti"])


def make_token_payload(email: str, role: UserRole) -> TokenPayload:
    """Construct a TokenPayload with a freshly generated jti.

    Args:
        email: The authenticated user's email address (JWT subject).
        role: The user's current role from the database.

    Returns:
        TokenPayload ready for signing.
    """
    return TokenPayload(sub=email, role=role, jti=str(uuid.uuid4()))


async def revoke_token(jti: str) -> None:
    """Add a token's jti to the Redis denylist until the token's natural expiry.

    Call this on logout or when a user's role is changed mid-session.
    The TTL is set to access_token_expire_minutes so the key self-cleans.

    Args:
        jti: The unique JWT ID claim from the token being revoked.
    """
    redis = get_redis()
    ttl_seconds = settings.access_token_expire_minutes * 60
    await redis.setex(f"denylist:{jti}", ttl_seconds, "1")


async def is_token_revoked(jti: str) -> bool:
    """Return True if the token has been explicitly revoked via the denylist.

    Args:
        jti: The unique JWT ID claim to check.

    Returns:
        True if revoked, False if still valid.
    """
    redis = get_redis()
    return await redis.exists(f"denylist:{jti}") == 1
```

---

### `app/repositories/user.py`

```python
"""Database access layer for user records."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_api_key, hash_password
from app.models.user import User, UserRole
from app.schemas.user import UserCreate


class UserRepository:
    """Repository providing CRUD operations for the User model."""

    def __init__(self, db: AsyncSession) -> None:
        """Initialise the repository with an async database session."""
        self._db = db

    async def get_by_email(self, email: str) -> User | None:
        """Return the user with the given email, or None if not found."""
        result = await self._db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """Return the user with the given ID, or None if not found."""
        result = await self._db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_api_key_hash(self, raw_key: str) -> User | None:
        """Return the active service account whose stored key hash matches raw_key.

        The raw key is hashed on arrival and compared against the stored SHA-256
        digest — the raw key is never persisted or logged.

        Args:
            raw_key: The raw API key value from the X-API-Key header.

        Returns:
            The matching active User, or None if no match is found.
        """
        key_hash = hash_api_key(raw_key)
        result = await self._db.execute(
            select(User).where(
                User.api_key_hash == key_hash,
                User.role == UserRole.SERVICE_ACCOUNT,
                User.is_active.is_(True),
            )
        )
        return result.scalar_one_or_none()

    async def create(self, data: UserCreate) -> User:
        """Create and persist a new user record.

        Args:
            data: Validated UserCreate schema.

        Returns:
            The newly created User ORM instance.
        """
        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            role=data.role,
        )
        self._db.add(user)
        await self._db.flush()  # assigns id without committing
        await self._db.refresh(user)
        return user

    async def update_role(self, user: User, new_role: UserRole) -> User:
        """Update a user's role and persist the change.

        Args:
            user: The User ORM instance to update.
            new_role: The new role to assign.

        Returns:
            The updated User ORM instance.
        """
        user.role = new_role
        await self._db.flush()
        await self._db.refresh(user)
        return user
```

---

## 🖥️ Artefact 2 — RBAC FastAPI Dependencies (Permission Guards)

### `app/api/deps.py`

```python
"""FastAPI dependency functions for authentication and authorisation.

This module implements the RBAC guard chain:
    get_current_user → require_role([...]) → protected route

Mirrors the Azure Entra ID roles claim pattern:
    Entra JWT `roles` claim  →  DB-backed role lookup
    Next.js `hasRole("Admin")` →  `require_role([UserRole.ADMIN])`
"""

from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_access_token, is_token_revoked
from app.models.user import User, UserRole
from app.repositories.user import UserRepository

# Plain Annotated alias — the correct 2026 FastAPI pattern.
# Do NOT use the PEP 695 `type` statement here; that syntax is for generic
# type aliases (e.g. `type Vector[T] = list[T]`), not for Depends() shortcuts.
DbDep = Annotated[AsyncSession, Depends(get_db)]

_bearer = HTTPBearer(auto_error=False)
_api_key_header = APIKeyHeader(name=settings.api_key_header, auto_error=False)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    db: DbDep,
) -> User:
    """Extract and validate the JWT bearer token, returning the authenticated user.

    Also checks the Redis denylist — a revoked token (e.g. after logout or role
    change) is rejected even if its signature and expiry are still technically valid.

    Args:
        credentials: Bearer token extracted from the Authorization header.
        db: Injected async database session.

    Returns:
        The authenticated User ORM instance.

    Raises:
        HTTPException 401: If the token is missing, invalid, expired, or revoked.
        HTTPException 401: If the user no longer exists or is inactive.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "type": "https://example.com/errors/unauthorized",
            "title": "Unauthorised",
            "status": 401,
            "detail": "Could not validate credentials",
        },
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not credentials:
        raise credentials_exception

    try:
        payload = decode_access_token(credentials.credentials)
    except jwt.InvalidTokenError:
        raise credentials_exception

    # Denylist check — reject tokens explicitly revoked on logout or role change.
    if await is_token_revoked(payload.jti):
        raise credentials_exception

    repo = UserRepository(db)
    user = await repo.get_by_email(payload.sub)

    if user is None or not user.is_active:
        raise credentials_exception

    return user


# Reusable annotated type — eliminates repeated Depends() in route signatures
CurrentUser = Annotated[User, Depends(get_current_user)]


def require_role(*roles: UserRole):
    """Return a FastAPI dependency that enforces role membership.

    Usage:
        @router.get("/admin/stats", dependencies=[Depends(require_role(UserRole.ADMIN))])

        async def admin_stats(user: CurrentUser = Depends(require_role(UserRole.ADMIN))):
            ...

    Args:
        *roles: One or more UserRole values that are permitted to access the route.

    Returns:
        An async dependency function that returns the current user if authorised.

    Raises:
        HTTPException 403: If the current user's role is not in the permitted set.
    """
    permitted: frozenset[UserRole] = frozenset(roles)

    async def _guard(current_user: CurrentUser) -> User:
        """Verify the current user holds one of the permitted roles."""
        if current_user.role not in permitted:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "type": "https://example.com/errors/forbidden",
                    "title": "Forbidden",
                    "status": 403,
                    "detail": (
                        f"Role '{current_user.role.value}' is not permitted. "
                        f"Required: {[r.value for r in permitted]}"
                    ),
                },
            )
        return current_user

    return _guard


# Convenience aliases — mirrors Entra ID role names
require_admin = require_role(UserRole.ADMIN)
require_user_or_admin = require_role(UserRole.USER, UserRole.ADMIN)


async def get_service_account(
    api_key: Annotated[str | None, Security(_api_key_header)],
    db: DbDep,
) -> User:
    """Authenticate a service account by looking up the SHA-256 hash of the API key.

    The raw key value is hashed on arrival and compared against the `api_key_hash`
    column — the raw key is never stored or logged. Each service account has its own
    unique key, issued once at account creation and stored only as a digest.

    In production, the raw key is stored in Azure Key Vault via Managed Identity
    and injected into the calling service at deploy time.

    Args:
        api_key: Value of the X-API-Key header.
        db: Injected async database session.

    Returns:
        The service account User ORM instance.

    Raises:
        HTTPException 401: If the API key is missing, invalid, or has no matching account.
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "type": "https://example.com/errors/unauthorized",
                "title": "Unauthorised",
                "status": 401,
                "detail": "Missing API key",
            },
        )

    repo = UserRepository(db)
    service_user = await repo.get_by_api_key_hash(api_key)

    if not service_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "type": "https://example.com/errors/unauthorized",
                "title": "Unauthorised",
                "status": 401,
                "detail": "Invalid API key",
            },
        )
    return service_user


ServiceAccount = Annotated[User, Depends(get_service_account)]
```

---

## 🖥️ Artefact 3 — Protected Route Handlers

### `app/api/v1/users.py`

```python
"""User management routes with role-based access control.

Route protection summary:
    GET  /v1/users/me          → any authenticated user
    GET  /v1/users/            → admin only
    PATCH /v1/users/{id}/role  → admin only
    GET  /v1/users/service-data → service account only
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import (
    CurrentUser,
    ServiceAccount,
    require_admin,
    require_user_or_admin,
)
from app.core.database import get_db
from app.models.user import User, UserRole
from app.repositories.user import UserRepository
from app.schemas.user import UserRead, UserRoleUpdate

router = APIRouter(prefix="/users", tags=["users"])

DbDep = Annotated[AsyncSession, Depends(get_db)]


@router.get(
    "/me",
    response_model=UserRead,
    summary="Get current user profile",
)
async def get_my_profile(current_user: CurrentUser) -> UserRead:
    """Return the profile of the currently authenticated user.

    Accessible by: USER, ADMIN (any authenticated user).
    """
    return UserRead.model_validate(current_user)


@router.get(
    "/",
    response_model=list[UserRead],
    summary="List all users (admin only)",
    dependencies=[Depends(require_admin)],
)
async def list_users(
    current_user: CurrentUser,
    db: DbDep,
) -> list[UserRead]:
    """Return all user records.

    Accessible by: ADMIN only.
    Non-admin requests receive 403 Forbidden before this function executes.
    """
    from sqlalchemy import select

    result = await db.execute(select(User))
    users = result.scalars().all()
    return [UserRead.model_validate(u) for u in users]


@router.patch(
    "/{user_id}/role",
    response_model=UserRead,
    summary="Update a user's role (admin only)",
    dependencies=[Depends(require_admin)],
)
async def update_user_role(
    user_id: uuid.UUID,
    body: UserRoleUpdate,
    current_user: CurrentUser,
    db: DbDep,
) -> UserRead:
    """Change the role of a user identified by user_id.

    Accessible by: ADMIN only.

    Args:
        user_id: UUID of the target user.
        body: New role to assign.
        current_user: The authenticated admin performing the update.
        db: Injected async database session.

    Raises:
        HTTPException 404: If the target user does not exist.
        HTTPException 403: If the admin attempts to downgrade their own role.
    """
    repo = UserRepository(db)
    target = await repo.get_by_id(user_id)

    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "https://example.com/errors/not-found",
                "title": "Not Found",
                "status": 404,
                "detail": f"User {user_id} not found",
            },
        )

    # Prevent self-demotion — admin cannot remove their own admin role
    if target.id == current_user.id and body.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "type": "https://example.com/errors/forbidden",
                "title": "Forbidden",
                "status": 403,
                "detail": "Admins cannot demote themselves",
            },
        )

    updated = await repo.update_role(target, body.role)
    return UserRead.model_validate(updated)


@router.get(
    "/service-data",
    summary="Internal data endpoint (service account only)",
)
async def get_service_data(service_account: ServiceAccount) -> dict[str, str]:
    """Return internal data accessible only to service accounts.

    Accessible by: SERVICE_ACCOUNT (API key auth), not by user JWTs.
    Mirrors the Entra ID Managed Identity → service endpoint pattern.

    Args:
        service_account: The authenticated service account user.

    Returns:
        A dict confirming service account identity.
    """
    return {
        "status": "ok",
        "service_account_email": service_account.email,
        "message": "Internal service data — not accessible via user JWT",
    }
```

---

### `app/api/v1/auth.py`

```python
"""Authentication routes: login, registration, and logout."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    decode_access_token,
    make_token_payload,
    revoke_token,
    verify_password,
)
from app.repositories.user import UserRepository
from app.schemas.user import TokenResponse, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])

DbDep = Annotated[AsyncSession, Depends(get_db)]

_bearer = HTTPBearer(auto_error=False)


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(body: UserCreate, db: DbDep) -> UserRead:
    """Register a new user account.

    Args:
        body: Validated UserCreate payload.
        db: Injected async database session.

    Raises:
        HTTPException 409: If the email is already registered.
    """
    repo = UserRepository(db)
    existing = await repo.get_by_email(body.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "type": "https://example.com/errors/conflict",
                "title": "Conflict",
                "status": 409,
                "detail": f"Email '{body.email}' is already registered",
            },
        )
    user = await repo.create(body)
    return UserRead.model_validate(user)


@router.post("/login", response_model=TokenResponse)
async def login(body: UserCreate, db: DbDep) -> TokenResponse:
    """Authenticate a user and issue a JWT access token.

    A unique jti claim is embedded in every token, enabling per-token
    revocation via the Redis denylist without rotating the signing secret.

    Args:
        body: Email and password credentials.
        db: Injected async database session.

    Returns:
        JWT access token with embedded role and jti claims.

    Raises:
        HTTPException 401: If the credentials are invalid or the user is inactive.
    """
    repo = UserRepository(db)
    user = await repo.get_by_email(body.email)

    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "type": "https://example.com/errors/unauthorized",
                "title": "Unauthorised",
                "status": 401,
                "detail": "Invalid email or password",
            },
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "type": "https://example.com/errors/unauthorized",
                "title": "Unauthorised",
                "status": 401,
                "detail": "Account is inactive",
            },
        )

    token = create_access_token(make_token_payload(user.email, user.role))
    return TokenResponse(access_token=token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> None:
    """Revoke the current JWT by adding its jti to the Redis denylist.

    The token remains cryptographically valid until its natural expiry, but
    the denylist check in get_current_user will reject it on every subsequent
    request. This achieves immediate revocation without rotating the signing secret.

    Args:
        credentials: Bearer token from the Authorization header.

    Raises:
        HTTPException 401: If no token is provided.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "type": "https://example.com/errors/unauthorized",
                "title": "Unauthorised",
                "status": 401,
                "detail": "No token provided",
            },
        )
    import jwt as _jwt

    try:
        payload = decode_access_token(credentials.credentials)
        await revoke_token(payload.jti)
    except _jwt.InvalidTokenError:
        # Token is already invalid — treat logout as a no-op.
        pass
```

---

### `app/api/v1/router.py`

```python
"""V1 API router — aggregates all v1 route modules."""

from fastapi import APIRouter

from app.api.v1 import auth, users

router = APIRouter(prefix="/v1")
router.include_router(auth.router)
router.include_router(users.router)
```

---

### `app/main.py`

```python
"""FastAPI application factory with lifespan management."""

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.database import Base, engine

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Create database tables on startup (development only).

    In production, use Alembic migrations instead of create_all.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("database_tables_created")
    yield
    await engine.dispose()
    logger.info("database_engine_disposed")


app = FastAPI(
    title="FastAPI RBAC",
    description="Role-Based Access Control demo — Sprint 2 Day 2",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)


@app.get("/health", tags=["ops"])
async def health() -> dict[str, str]:
    """Return application health status."""
    return {"status": "ok"}
```

---

## 🖥️ Artefact 4 — Alembic Migration: Add Role Column

```bash
# Initialise Alembic (first time only)
uv run alembic init alembic

# Generate migration from model change
uv run alembic revision --autogenerate -m "add_role_column_to_users"

# Apply migration
uv run alembic upgrade head

# Rollback one step (if needed)
uv run alembic downgrade -1
```

```python
# alembic/versions/001_add_role_column.py
# Generated by: alembic revision --autogenerate -m "add_role_column_to_users"
"""add_role_column_to_users

Revision ID: 001abc123def
Revises:
Create Date: 2026-04-25 09:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

revision = "001abc123def"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add the userrole enum, role column, and api_key_hash column to the users table."""
    op.execute("CREATE TYPE userrole AS ENUM ('user', 'admin', 'service_account')")
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.Enum("user", "admin", "service_account", name="userrole"),
            nullable=False,
            server_default="user",
        ),
    )
    op.create_index("ix_users_role", "users", ["role"])
    # api_key_hash: SHA-256 digest of the raw API key — populated for SERVICE_ACCOUNT users only.
    op.add_column(
        "users",
        sa.Column("api_key_hash", sa.String(64), nullable=True, unique=True),
    )
    op.create_index("ix_users_api_key_hash", "users", ["api_key_hash"])


def downgrade() -> None:
    """Remove the role column, userrole enum, and api_key_hash column."""
    op.drop_index("ix_users_api_key_hash", "users")
    op.drop_column("users", "api_key_hash")
    op.drop_index("ix_users_role", "users")
    op.drop_column("users", "role")
    op.execute("DROP TYPE userrole")
```

---

### Key Concepts

- **`server_default="user"`** ensures existing rows receive a valid role without a backfill query — zero-downtime migration pattern.
- **`op.execute("CREATE TYPE ...")`** is required for PostgreSQL native enums — Alembic's `autogenerate` handles this automatically, shown here for clarity.
- **`api_key_hash` is `nullable=True`** — it is only populated for `SERVICE_ACCOUNT` users. Regular users have `NULL` in this column. The `unique=True` constraint prevents key reuse across accounts.
- **Always review autogenerated migrations** before applying to staging or production — `autogenerate` can miss index changes or generate incorrect `server_default` values.

---

## 🖥️ Artefact 5 — Tests

### `tests/conftest.py`

```python
"""Pytest fixtures for RBAC integration tests."""

from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.database import Base, get_db
from app.core.security import hash_api_key, hash_password
from app.main import app
from app.models.user import User, UserRole

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_rbac_test"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

# Raw key used only in tests — never persisted, only its hash is stored.
TEST_SERVICE_API_KEY = "test-service-key-do-not-use-in-production"


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_tables() -> AsyncGenerator[None, None]:
    """Create all tables before the test session and drop them after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    """Yield a test database session with rollback-on-exit for test isolation."""
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Yield an AsyncClient with the test DB session injected via dependency_overrides."""

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        """Override get_db to use the test session."""
        yield db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def admin_user(db: AsyncSession) -> User:
    """Create and persist an admin user for use in tests."""
    user = User(
        email="admin@example.com",
        hashed_password=hash_password("adminpass"),
        role=UserRole.ADMIN,
        is_active=True,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


@pytest_asyncio.fixture
async def regular_user(db: AsyncSession) -> User:
    """Create and persist a regular user for use in tests."""
    user = User(
        email="user@example.com",
        hashed_password=hash_password("userpass"),
        role=UserRole.USER,
        is_active=True,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


@pytest_asyncio.fixture
async def service_account_user(db: AsyncSession) -> User:
    """Create and persist a service account user with a hashed API key.

    The raw key (TEST_SERVICE_API_KEY) is only available in the test scope.
    Only the SHA-256 digest is stored in the database — matching production behaviour.
    """
    user = User(
        email="service@example.com",
        hashed_password=hash_password("unused-service-password"),
        role=UserRole.SERVICE_ACCOUNT,
        is_active=True,
        api_key_hash=hash_api_key(TEST_SERVICE_API_KEY),
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user
```

---

### `tests/test_rbac.py`

```python
"""Integration tests for RBAC route protection."""

import pytest
from httpx import AsyncClient

from app.models.user import User
from tests.conftest import TEST_SERVICE_API_KEY


async def get_token(client: AsyncClient, email: str, password: str) -> str:
    """Helper: authenticate and return the JWT access token."""
    response = await client.post(
        "/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


class TestGetMyProfile:
    """Tests for GET /v1/users/me."""

    async def test_authenticated_user_can_read_own_profile(
        self,
        client: AsyncClient,
        regular_user: User,
    ) -> None:
        """A valid JWT should return the user's own profile."""
        token = await get_token(client, "user@example.com", "userpass")
        response = await client.get(
            "/v1/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["email"] == "user@example.com"
        assert response.json()["role"] == "user"

    async def test_unauthenticated_request_returns_401(self, client: AsyncClient) -> None:
        """A request without a token should return 401."""
        response = await client.get("/v1/users/me")
        assert response.status_code == 401


class TestAdminOnlyRoutes:
    """Tests for routes restricted to the admin role."""

    async def test_admin_can_list_users(
        self,
        client: AsyncClient,
        admin_user: User,
    ) -> None:
        """An admin JWT should return the full user list."""
        token = await get_token(client, "admin@example.com", "adminpass")
        response = await client.get(
            "/v1/users/",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200

    async def test_regular_user_cannot_list_users(
        self,
        client: AsyncClient,
        regular_user: User,
    ) -> None:
        """A non-admin JWT should receive 403 on admin-only routes."""
        token = await get_token(client, "user@example.com", "userpass")
        response = await client.get(
            "/v1/users/",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403
        assert response.json()["detail"]["status"] == 403

    async def test_admin_can_update_user_role(
        self,
        client: AsyncClient,
        admin_user: User,
        regular_user: User,
    ) -> None:
        """An admin should be able to promote a user to admin."""
        token = await get_token(client, "admin@example.com", "adminpass")
        response = await client.patch(
            f"/v1/users/{regular_user.id}/role",
            json={"role": "admin"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["role"] == "admin"

    async def test_admin_cannot_demote_self(
        self,
        client: AsyncClient,
        admin_user: User,
    ) -> None:
        """An admin should receive 403 when attempting to remove their own admin role."""
        token = await get_token(client, "admin@example.com", "adminpass")
        response = await client.patch(
            f"/v1/users/{admin_user.id}/role",
            json={"role": "user"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403


class TestExpiredToken:
    """Tests for JWT expiry and invalid token handling."""

    async def test_expired_token_returns_401(self, client: AsyncClient) -> None:
        """A clearly invalid/expired token should return 401, not 500."""
        response = await client.get(
            "/v1/users/me",
            headers={"Authorization": "Bearer not.a.real.token"},
        )
        assert response.status_code == 401


class TestServiceAccountAuth:
    """Tests for service account API key authentication."""

    async def test_valid_api_key_accesses_service_endpoint(
        self,
        client: AsyncClient,
        service_account_user: User,
    ) -> None:
        """A valid API key should return 200 on the service-only endpoint."""
        response = await client.get(
            "/v1/users/service-data",
            headers={"X-API-Key": TEST_SERVICE_API_KEY},
        )
        assert response.status_code == 200
        assert response.json()["service_account_email"] == "service@example.com"

    async def test_invalid_api_key_returns_401(self, client: AsyncClient) -> None:
        """An incorrect API key should return 401."""
        response = await client.get(
            "/v1/users/service-data",
            headers={"X-API-Key": "wrong-key"},
        )
        assert response.status_code == 401

    async def test_missing_api_key_returns_401(self, client: AsyncClient) -> None:
        """A request with no API key header should return 401."""
        response = await client.get("/v1/users/service-data")
        assert response.status_code == 401

    async def test_jwt_cannot_access_service_endpoint(
        self,
        client: AsyncClient,
        regular_user: User,
    ) -> None:
        """A regular JWT bearer token should not access the service-account-only endpoint."""
        token = await get_token(client, "user@example.com", "userpass")
        response = await client.get(
            "/v1/users/service-data",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 401


class TestLogoutAndDenylist:
    """Tests for token revocation via the Redis denylist."""

    async def test_logout_revokes_token(
        self,
        client: AsyncClient,
        regular_user: User,
    ) -> None:
        """A token used after logout should return 401 due to the denylist."""
        token = await get_token(client, "user@example.com", "userpass")

        # Confirm token is valid before logout.
        pre_logout = await client.get(
            "/v1/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert pre_logout.status_code == 200

        # Logout — adds jti to Redis denylist.
        logout_response = await client.post(
            "/v1/auth/logout",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert logout_response.status_code == 204

        # Same token is now rejected.
        post_logout = await client.get(
            "/v1/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert post_logout.status_code == 401

    async def test_logout_without_token_returns_401(self, client: AsyncClient) -> None:
        """Calling logout with no bearer token should return 401."""
        response = await client.post("/v1/auth/logout")
        assert response.status_code == 401
```

---

## 🗺️ Azure Entra / Next.js → FastAPI RBAC Mapping

| Azure Entra / Next.js Pattern                            | FastAPI Equivalent                                                | Notes                                                                        |
| -------------------------------------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| App role assignment in Entra ID portal                   | `UserRole` enum in PostgreSQL                                     | Source of truth shifts from Entra to your DB                                 |
| `roles` claim in JWT                                     | `role` field in JWT payload + DB lookup                           | Always verify role against DB — do not trust token alone                     |
| `hasRole("Admin")` in Next.js middleware                 | `Depends(require_admin)` on FastAPI route                         | Same semantics, different location                                           |
| `session.user.role` in Next.js server component          | `CurrentUser` annotated dependency                                | Injected by FastAPI's DI container                                           |
| Managed Identity → resource access                       | `SERVICE_ACCOUNT` role + per-account `api_key_hash`               | Each service account has its own key; hash stored, raw key never persisted   |
| MSAL `acquireTokenSilent`                                | `POST /v1/auth/login` → JWT                                       | For in-house auth without Entra; Entra remains preferred for enterprise      |
| Conditional Access — session revocation on policy change | Redis denylist on `POST /v1/auth/logout` + role-change revocation | `jti` claim enables per-token revocation without rotating the signing secret |

---

## ❓ Comprehensive Q&A

---

### 🔐 Authentication vs Authorisation

**Q1: What is the difference between authentication and authorisation?**
A: Authentication (authn) answers "who are you?" — validating identity via password, token, or certificate. Authorisation (authz) answers "what can you do?" — checking whether the authenticated identity has permission to perform the requested action. In FastAPI, `get_current_user` handles authn; `require_role()` handles authz.

**Q2: When should you return 401 vs 403?**
A: Return `401 Unauthorized` when the request lacks valid credentials — missing token, invalid token, or expired token. Return `403 Forbidden` when the identity is valid but lacks the required permission. Returning 403 for an unauthenticated request leaks information — always return 401 first.

**Q3: What is RFC 7807 and why does it matter in UK enterprise APIs?**
A: RFC 7807 (Problem Details for HTTP APIs) defines a standard `application/problem+json` error response format with fields: `type` (URI identifying the error), `title`, `status`, `detail`, and optionally `instance`. UK enterprise clients — especially in fintech and government — expect machine-readable structured errors. A single consistent error schema also simplifies frontend error handling and monitoring dashboards.

---

### 🎯 RBAC Design

**Q4: How do you implement RBAC in FastAPI?**
A: Store roles in PostgreSQL as an `Enum` column on the users table. Decode the JWT in a `get_current_user` dependency, look up the user in the DB (do not trust the token's role claim alone), then compose a `require_role()` dependency that raises `403` if the user's DB role is not in the permitted set. Inject via `Depends()` on the route or in the route's `dependencies=[]` list.

**Q5: Why should you look up the role from the database rather than trusting the JWT claim?**
A: A JWT is issued at login time and may be valid for 30 minutes. If an admin revokes a user's elevated role mid-session, the JWT still carries the old role claim. Always verify the current role from the DB on each request. Acceptable performance cost: a single indexed lookup on `users.id` is sub-millisecond with connection pooling.

**Q6: How would you model multi-role users (a user who is both admin and auditor)?**
A: Replace the single `role` Enum column with a many-to-many `user_roles` join table: `user_id` → `role_id`. `require_role()` then checks whether the user's role set intersects with the permitted set. Alternatively, use a `roles: list[UserRole]` column with PostgreSQL `ARRAY` type — simpler for small, fixed role sets.

**Q7: What is the difference between RBAC and Attribute-Based Access Control (ABAC)?**
A: RBAC grants permissions based on a user's role (admin, user, etc.) — coarse-grained and easy to manage. ABAC (Attribute-Based Access Control) grants permissions based on arbitrary attributes of the subject, resource, and environment (e.g., "user in department=finance AND resource.classification=internal AND time=business_hours"). ABAC is more expressive but significantly harder to reason about. Start with RBAC; layer ABAC only when role proliferation becomes a problem.

**Q8: How do you handle the case where an admin endpoint is accidentally left unprotected?**
A: Default-deny at the router level: create an `admin_router` with `dependencies=[Depends(require_admin)]` applied to the entire router, not per-route. Any new route added to `admin_router` is automatically protected. Per-route `dependencies=[]` is error-prone — a missed annotation is a privilege escalation vector.

---

### 🏗️ FastAPI Dependency Injection

**Q9: What is the `Annotated` pattern and why is it the 2026 standard for FastAPI dependencies?**
A: `Annotated[T, Depends(fn)]` co-locates the type and its dependency source in a single expression. Assigning it to a module-level name (`CurrentUser = Annotated[User, Depends(get_current_user)]`) eliminates repeated `Depends()` declarations across every route and makes the dependency graph explicit in the type annotation. Note: do NOT use the PEP 695 `type` statement for this — `type CurrentUser = Annotated[...]` is syntactically valid but misrepresents PEP 695's purpose, which is generic type aliases (`type Vector[T] = list[T]`). Use a plain assignment.

**Q10: How do you test routes that require authentication in FastAPI?**
A: Use `app.dependency_overrides[get_current_user] = lambda: mock_user` in the test fixture. This bypasses JWT validation entirely and injects a known User object directly. `httpx.AsyncClient` with `ASGITransport` provides a full ASGI integration test without a network socket. Never disable auth by monkeypatching `verify_password` — override the dependency at the FastAPI level.

**Q11: What is the difference between `dependencies=[]` on a route vs injecting a dependency as a function parameter?**
A: `dependencies=[Depends(fn)]` on the route runs the dependency for its side effects (authorisation, rate limiting, logging) without injecting the return value into the function body. Injecting as a parameter (`user: CurrentUser`) runs the same dependency and also provides the return value for use inside the handler. Use `dependencies=[]` for pure guards; use parameter injection when you need the resolved value.

---

### 🔑 Service Account Auth

**Q12: When would you use API key authentication instead of JWT for service-to-service calls?**
A: JWTs have expiry and require a token refresh flow — unsuitable for long-running background services. API keys are simpler for machine-to-machine: the calling service sends a static key in a custom header (`X-API-Key`), your API validates it against a hash stored in the database or Azure Key Vault. In production on Azure, prefer Managed Identity over API keys entirely — it eliminates key rotation overhead.

**Q13: How do you rotate API keys without downtime?**
A: Support two active keys simultaneously during the rotation window: `current_key` and `new_key`. The calling service starts sending the new key while the old key remains valid. After all services have switched, revoke the old key. In Azure Key Vault, use key versioning and Managed Identity to automate this without touching application config.

---

### 🛡️ Security

**Q14: What is privilege escalation and how do you prevent it in your RBAC implementation?**
A: Privilege escalation occurs when a user gains a higher role than they are entitled to — either by manipulating a request payload, exploiting a missing authorisation check, or self-assigning roles. Prevention: (1) server-side role lookup — never trust client-supplied role values; (2) block role self-assignment — only admins can change roles, and only for other users; (3) default-deny at the router level so new routes are protected unless explicitly relaxed.

**Q15: How do you handle OWASP Top 10 item A01 (Broken Access Control) in this RBAC system?**
A: A01 is the most common web vulnerability — insufficiently enforced access controls. Mitigations: enforce roles server-side on every request (not just on login), apply `require_admin` at router level not per-route, add integration tests that explicitly assert 403 for non-permitted roles, include access control checks in your CI pipeline, and audit role assignments in your logging pipeline.

**Q16: Why should you never store roles in the JWT and trust them without a DB lookup?**
A: The JWT is issued at authentication time and remains valid until expiry. If a role is revoked between issuance and expiry, the stale token still carries the elevated role claim. A DB lookup on each request ensures the current authoritative role is used. The performance cost is a single indexed primary-key lookup — negligible with connection pooling.

---

### 🧰 Tooling

**Q17: What is `uv` and why is it the 2026 recommended default for Python projects?**
A: `uv` is a Rust-based all-in-one Python package and project manager that replaces `pip`, `virtualenv`, and `pyenv` in a single tool. It resolves dependencies significantly faster than pip, manages Python versions via `uv python install`, and handles virtual environment creation automatically. It is the recommended default for new projects in 2026.

**Q18: When would you still use `poetry` over `uv`?**
A: `poetry` remains common in existing UK enterprise codebases that predate `uv` adoption. You will encounter it in interviews and legacy repositories. Senior engineers are expected to be familiar with both: `uv` for new projects, `poetry` for maintaining existing ones.

**Q19: What is `pandera` and when would you use it on a backend day like this?**
A: `pandera` is a schema validation library for DataFrames. It is not relevant to a pure RBAC backend day — no DataFrames are involved. It becomes relevant when the session involves data pipelines, ETL preprocessing, or ML feature engineering. Mentioning it in an RBAC interview context would be off-topic.

---

### 🔄 Architecture & System Design

**Q20: How would you scale this RBAC system for a multi-tenant SaaS application?**
A: Add a `tenant_id` foreign key to both `users` and a new `roles` table. Permission checks become: `user.role within tenant` rather than global role. Every query is scoped by `tenant_id` — enforce this at the repository layer, not the route layer, to prevent cross-tenant data leaks. Consider row-level security (RLS) in PostgreSQL as a defence-in-depth measure.

**Q21: How do you cache role lookups to reduce DB hits on high-traffic APIs?**
A: Use Redis with a short TTL (30–60 seconds) keyed on `user:{id}:role`. On each request, check the cache before the DB. On role update, invalidate the cache key immediately. Accept a brief inconsistency window equal to the TTL — appropriate for most role changes which are administrative and low-frequency. Do not cache for zero-TTL if your security requirements demand immediate revocation.

**Q22: How does your FastAPI RBAC implementation compare to Azure Entra ID's app roles?**
A: Entra ID stores role assignments in Azure AD and injects them as a `roles` claim in the OAuth2 JWT. Your FastAPI implementation replicates this pattern: roles stored in PostgreSQL, injected via the `get_current_user` dependency. The key difference is ownership — Entra delegates role management to Azure AD, your implementation manages it in-database. For enterprise deployments, Entra ID is preferred (centralised, auditable, integrated with Conditional Access). For products where you own the auth layer, the in-database pattern is appropriate.

---

### 🔑 Auth Libraries — 2026 Standards

**Q23: Why was `python-jose` replaced and what is the 2026 standard?**
A: `python-jose` has had no release since 2021. It is incompatible with Python 3.10+ because it references `collections.Mapping` which was removed from stdlib in 3.10. The 2026 standard is `pyjwt[crypto]` — actively maintained, used in the official FastAPI documentation, and supports RS256/ES256 via the `cryptography` extras package. Import as `import jwt`; exceptions are `jwt.InvalidTokenError` and its subclasses.

**Q24: Why was `passlib` replaced and what is the 2026 standard for password hashing?**
A: `passlib` internally used the `crypt` module which was deprecated in Python 3.12 and removed in Python 3.13 (PEP 594). The 2026 standard is `pwdlib[argon2]`. Use `PasswordHash.recommended()` which selects Argon2 by default. Argon2 is memory-hard — it is GPU and ASIC resistant in a way that bcrypt, which relies on computational complexity alone, is not. Argon2 was the winner of the Password Hashing Competition (PHC) and is the OWASP recommended default for new systems.

**Q25: What is the `jti` claim and why must every issued JWT include one?**
A: `jti` (JWT ID) is a unique identifier per token defined in RFC 7519. Without it, you cannot selectively revoke a single token — your only option is rotating the signing secret, which invalidates every token for every user simultaneously. Including a `uuid4` string as `jti` at issuance time allows you to target one specific token in the Redis denylist while all other tokens remain valid.

**Q26: How does the Redis token denylist achieve immediate revocation?**
A: On logout or role change, write the token's `jti` to Redis with a TTL equal to the token's remaining lifetime (`SETEX denylist:{jti} {ttl} 1`). On each authenticated request, before trusting the token, check `EXISTS denylist:{jti}`. If present, return 401. The Redis key self-deletes at TTL expiry, so the denylist never accumulates stale entries. Cost: one additional Redis round-trip per authenticated request — sub-millisecond with a local Redis instance and connection pooling.

**Q27: How do you store and validate service account API keys securely?**
A: Never store the raw key. At account creation, generate a cryptographically random key (e.g. `secrets.token_urlsafe(32)`), issue it once to the caller, and store only its SHA-256 digest in the database (`hashlib.sha256(raw.encode()).hexdigest()`). On each request, hash the incoming key and compare against the stored digest. This means a database breach does not expose the raw key — an attacker would need to brute-force a 256-bit preimage. Each service account has its own unique key, enforced by a `UNIQUE` constraint on the `api_key_hash` column.

---

### 🗄️ PostgreSQL & Schema Design

**Q28: Why use a PostgreSQL native `ENUM` type for roles rather than `VARCHAR` with a `CHECK` constraint?**
A: A native PostgreSQL `ENUM` (`CREATE TYPE userrole AS ENUM (...)`) is stored as a 4-byte integer internally, making index lookups and comparisons faster than `VARCHAR`. It also enforces valid values at the database engine level — a `CHECK` constraint enforces at write time but is invisible to the query planner. The tradeoff: adding a new role value requires `ALTER TYPE userrole ADD VALUE 'new_role'`, which is a DDL operation that cannot be rolled back in a transaction on older PostgreSQL versions (14+). For a small, stable role set, native `ENUM` is the correct choice. For a dynamic role set that changes frequently, a `roles` lookup table with a foreign key is more flexible.

**Q29: What is the zero-downtime Alembic migration pattern for adding a `NOT NULL` column with a default to an existing table?**
A: Never add a `NOT NULL` column without a `server_default` in a single migration on a live table — PostgreSQL locks the table to backfill every row. The zero-downtime pattern is two migrations: (1) add the column as `nullable=True` with `server_default="user"` — existing rows get the default without a table lock; (2) once all rows have a value, a second migration drops `nullable` and removes `server_default`. For the `role` column in this artefact, `server_default="user"` on the initial migration is safe for production with any table size.

**Q30: When would you choose UUID primary keys over integer IDs in a PostgreSQL users table?**
A: UUIDs (`uuid4`) are unpredictable — an attacker cannot enumerate users by incrementing `/users/1`, `/users/2`. They also simplify distributed inserts across shards or replicas with no coordination needed. The tradeoffs: UUID indexes are ~30% larger than integer indexes due to random ordering (use `gen_random_uuid()` or `uuid7` for sequential UUIDs in PostgreSQL 17+ to mitigate index fragmentation), and JOINs on UUID foreign keys are slightly slower. For user-facing resources in a security-sensitive context, the enumeration protection justifies the cost.

---

### ⚡ SQLAlchemy Async & FastAPI Internals

**Q31: Why does this implementation use `AsyncSession` rather than a synchronous SQLAlchemy session?**
A: FastAPI runs on an async event loop (via `uvicorn` and `asyncio`). A synchronous database call blocks the entire event loop thread — no other requests can be processed until the DB call returns. `AsyncSession` with `asyncpg` issues non-blocking database calls via the event loop, allowing other requests to be processed concurrently. The practical impact is significant under load: a synchronous DB call at 10ms blocks 100 other requests per second on a single worker; async releases that thread immediately.

**Q32: What is `FastAPI.lifespan` and why should you use it instead of `@app.on_event`?**
A: `@app.on_event("startup")` and `@app.on_event("shutdown")` are deprecated since FastAPI 0.93. The replacement is a `lifespan` async context manager passed to `FastAPI(lifespan=lifespan)`. It keeps startup and shutdown logic in a single function with a `yield` as the boundary, making resource lifecycle explicit and testable. It also composes cleanly with `asynccontextmanager` for the Redis connection and database engine teardown used in this RBAC artefact.

**Q33: What is the difference between `HTTPBearer` and `OAuth2PasswordBearer` in FastAPI, and which does this implementation use?**
A: `OAuth2PasswordBearer` is a specialisation of `HTTPBearer` that adds an OpenAPI `securitySchemes` entry pointing to a `tokenUrl` — this makes the "Authorise" button appear in the Swagger UI. `HTTPBearer` just extracts the token from the `Authorization: Bearer` header with no OpenAPI decoration. This implementation uses `HTTPBearer` with `auto_error=False` so that missing tokens return a clean `None` rather than a FastAPI-generated 403, giving full control over the error response format (RFC 7807). For the OpenAPI UI to show the Authorise button, swap to `OAuth2PasswordBearer(tokenUrl="/v1/auth/login")`.

---

### 🔷 Pydantic v2

**Q34: What does `model_config = {"from_attributes": True}` do and why is it required for ORM responses?**
A: By default, Pydantic v2 expects a plain dict as input to `model_validate()`. With `from_attributes = True`, it reads values from object attributes instead — necessary for SQLAlchemy ORM instances, which are Python objects, not dicts. Without it, `UserRead.model_validate(user_orm_instance)` raises a `ValidationError`. The equivalent in Pydantic v1 was `orm_mode = True` in the `Config` class — the rename to `from_attributes` is a v2 breaking change that commonly catches engineers migrating from older FastAPI tutorials.

**Q35: What is the difference between `@field_validator` and `@model_validator` in Pydantic v2?**
A: `@field_validator("field_name")` runs after the individual field is parsed — use it for single-field constraints like minimum length or format checks (`password_min_length` in this artefact). `@model_validator(mode="after")` runs after all fields are parsed and the model is fully constructed — use it for cross-field validation, such as asserting `password == confirm_password`. `mode="before"` on either validator runs on the raw input before any type coercion, useful for normalising input formats.

---

### 🛡️ OWASP Coverage

**Q36: How does this RBAC system address OWASP A02 (Cryptographic Failures)?**
A: A02 covers weak or absent cryptography protecting sensitive data. Mitigations in this implementation: (1) passwords hashed with Argon2 via `pwdlib` — memory-hard, not reversible; (2) JWT signed with HMAC-SHA256 (`HS256`) — tokens cannot be forged without the secret key; (3) API keys stored as SHA-256 digests — database breach does not expose raw keys; (4) `SecretStr` for `secret_key` in `pydantic-settings` — the raw value is never accidentally logged or serialised. For production, promote `HS256` to `RS256` with a private key in Azure Key Vault and a public key for verification, so the signing key is never in application memory.

**Q37: How does this RBAC system address OWASP A07 (Identification and Authentication Failures)?**
A: A07 covers broken authentication mechanisms. Mitigations: (1) Argon2 hashing with `PasswordHash.recommended()` — resistant to brute force; (2) short JWT expiry (30 minutes) limits the blast radius of a stolen token; (3) Redis denylist for immediate revocation on logout or role change — tokens cannot be reused after revocation; (4) `is_active` check on every request — deactivated accounts are denied even with a valid token; (5) no password in the JWT payload — credentials are never in the token. Remaining gap: no rate limiting on `POST /v1/auth/login` in this artefact — `slowapi` (Sprint 2, Day 3) closes that gap.

---

### 🔑 JWT Depth

**Q38: When should you use RS256 instead of HS256 for JWT signing?**
A: Use `HS256` (HMAC-SHA256) when a single service both issues and verifies tokens — one shared secret, simple to manage. Use `RS256` (RSA-SHA256) when multiple services need to verify tokens independently: the issuing service holds the private key; verifying services hold only the public key. In an Azure microservices architecture, storing the RS256 private key in Azure Key Vault via Managed Identity means no service ever has the signing key in memory or config. This is also the model Azure Entra ID uses — public JWKS endpoint, private key in Microsoft's HSM.

**Q39: What is the refresh token pattern and why does access/refresh token separation improve security?**
A: An access token is short-lived (5–30 minutes) and sent on every API request — a stolen access token has a limited blast radius. A refresh token is long-lived (days or weeks), stored server-side (Redis or DB) and sent only to a dedicated `POST /v1/auth/refresh` endpoint to obtain a new access token. This separates the high-frequency, high-exposure token (access) from the credential that grants new tokens (refresh). Revoking the refresh token immediately invalidates the user's ability to get new access tokens, without waiting for the access token to expire. This is the pattern used by Azure Entra ID and is expected knowledge at senior level.

**Q40: What are Argon2's `time_cost`, `memory_cost`, and `parallelism` parameters and how would you tune them?**
A: `time_cost` is the number of iterations (CPU cost). `memory_cost` is RAM in KiB (memory-hardness — the property that makes GPU attacks expensive). `parallelism` is the number of parallel threads. `pwdlib`'s `PasswordHash.recommended()` uses the Argon2id variant with RFC 9106's recommended defaults: `time_cost=3`, `memory_cost=65536` (64 MiB), `parallelism=4`. Tuning guidance: run a benchmark to find the highest `memory_cost` that keeps hash time under 100ms on your production hardware — higher memory cost is almost always more valuable than higher time cost for GPU resistance. Never reduce below 32 MiB.

---

### 🧪 Testing Depth

**Q41: What is `pytest-asyncio`'s `asyncio_mode = "auto"` and why is it the correct setting for a FastAPI test suite?**
A: By default, `pytest-asyncio` requires every async test function to be decorated with `@pytest.mark.asyncio`. With `asyncio_mode = "auto"` in `pyproject.toml` (`[tool.pytest.ini_options] asyncio_mode = "auto"`), all `async def` test functions are automatically treated as async tests. This removes boilerplate from every test function in a suite where every test is async (which is the case for a FastAPI + `AsyncSession` test suite). The setting also applies to async fixtures, removing the need for `@pytest_asyncio.fixture` — though keeping the explicit decorator is recommended for clarity in shared fixture modules.

**Q42: What is `factory-boy` and when would you use it over manually constructed fixture objects?**
A: `factory-boy` is a fixture generation library that generates ORM instances with realistic, randomised attribute values. Use it when: (1) tests need many different user variants (active, inactive, various roles) without a fixture per variant; (2) you want to express only the fields relevant to a test and rely on sensible defaults for the rest. Manual fixtures (as in this artefact's `conftest.py`) are clearer for a small number of well-named scenarios. `factory-boy` pays off when you have 10+ fixture variants or need fuzz-style coverage across field values.

---

### 🏗️ Architecture Depth

**Q43: What is the self-demotion guard pattern and why does it matter architecturally?**
A: The self-demotion guard prevents an admin from removing their own admin role via `PATCH /v1/users/{id}/role`. Without it, a single admin system is one erroneous API call away from having zero admins — a locked-out state with no recovery path except direct database access. The guard raises `422 Unprocessable Entity` if `current_user.id == target_user.id` and the new role is not `ADMIN`. Architecturally, this is an example of business rule enforcement at the service layer: it cannot be expressed as a database constraint and must be validated in code on every role update call.

**Q44: When would you use `FastAPI.BackgroundTasks` versus a task queue like Celery or ARQ for RBAC audit logging?**
A: `BackgroundTasks` runs the task in the same process after the response is sent — it has no retry logic, no durability, and no visibility. If the worker crashes mid-task, the audit log entry is lost. Use `BackgroundTasks` for non-critical fire-and-forget work (sending a welcome email, invalidating a cache key). For RBAC audit logs, which may be required for compliance (SOC 2, ISO 27001), use a durable task queue: ARQ (Redis-backed, async-native) for lightweight workloads, or Celery with a broker for high-volume enterprise deployments. Both persist the task to the broker before the response is sent, guaranteeing at-least-once execution.

**Q45: How does PostgreSQL row-level security (RLS) complement application-level RBAC?**
A: RLS enforces access control at the database engine level — even if application code has a bug that constructs an incorrect query, the database will not return rows the current user is not allowed to see. Application RBAC is fast and flexible; RLS is defence-in-depth. Typical implementation: a `current_setting('app.current_user_id')` session variable set via `SET LOCAL` on each connection, with a `CREATE POLICY` that filters `WHERE user_id = current_setting(...)::uuid`. The tradeoff: RLS adds query planning overhead and makes raw SQL queries in migrations harder to reason about. For multi-tenant SaaS where a cross-tenant data leak would be a critical incident, RLS is worth the complexity.

---

## 🧪 Practice Exercises

### Exercise 1: Scope-Based Sub-Permissions

Extend the `require_role()` dependency to support permission scopes, not just roles. Add a `permissions` `ARRAY(String)` column to the `users` table and create a `require_permission("users:write")` dependency. Protect `PATCH /v1/users/{id}/role` with `require_permission("users:write")` instead of `require_admin`. This mirrors OAuth2 scope-based authorisation used in Entra ID.

### Exercise 2: Role Audit Log

Add a `role_change_events` table with columns: `id`, `target_user_id`, `changed_by_user_id`, `old_role`, `new_role`, `changed_at`. In `update_user_role`, write a `role_change_events` record using an async background task (`BackgroundTasks`) so the audit write does not block the HTTP response. This is the pattern used in regulated UK industries (FSA/FCA compliance).

---

## ✅ Today's Deliverable Checklist

By the end of today, you should have:

- [ ] `UserRole` enum column added to the `users` table via Alembic migration
- [ ] `api_key_hash` column (`String(64)`, nullable, unique) added to the `users` table via Alembic migration
- [ ] `get_current_user` dependency that validates JWT, checks the Redis denylist, and looks up the user from the DB
- [ ] `require_role(*roles)` factory producing FastAPI guard dependencies with `frozenset` permitted set
- [ ] `CurrentUser` annotated type alias as a plain module-level assignment — NOT using PEP 695 `type` statement
- [ ] At minimum three protected routes: user-accessible, admin-only, service-account-only
- [ ] `POST /v1/auth/logout` that revokes the bearer token by writing its `jti` to the Redis denylist
- [ ] `SERVICE_ACCOUNT` auth path via `X-API-Key` header using per-account SHA-256 hash lookup
- [ ] RFC 7807 problem detail format on all `4xx` responses
- [ ] Self-demotion guard: admin cannot remove their own admin role
- [ ] `jti` claim present in every issued token; `make_token_payload` generates a fresh `uuid4` jti per login
- [ ] Integration tests using `dependency_overrides` and `ASGITransport` — not mocking `verify_password`
- [ ] Tests explicitly asserting 403 for non-permitted roles
- [ ] Test asserting token is rejected after logout (denylist check)
- [ ] Test asserting service account API key lookup uses hash comparison, not raw key or role fallback
- [ ] `ruff check .` and `ruff format .` with zero errors
- [ ] `mypy .` with `strict = true` and zero errors
- [ ] All classes, functions, and methods have docstrings with type-hinted parameters and return values

**Previous Sprint Day:** Fri 24 Apr — JWT Authentication: OAuth2 password bearer, token issuance, hashed passwords, refresh token pattern.

**Next Sprint Day:** Sun 26 Apr — API Design for Scale: URL versioning (`/v1/`), cursor-based pagination, RFC 7807 error responses, rate limiting with `slowapi` + Redis.

---

_This learning material is part of the 2026 Python · Azure · AI Engineering Roadmap (v3) targeting UK senior roles (£90k–£130k / £550–£750/day). Generated with 2026-learning-prompt-v5. Python 3.14 · uv · FastAPI · pyjwt[crypto] · pwdlib[argon2] · Pydantic v2 · SQLAlchemy async · Redis denylist · ruff · mypy._
