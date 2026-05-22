```
  @jobs-list/2026-python-ai-azure-roadmap-v2.md
go and create file according to @jobs-list/2026-learning-prompt-v3.md in folder learning-sprints for:

- **Wed 22 Apr** — PostgreSQL + Async SQLAlchemy: async engine, session factory, `Base` models, repository pattern, Alembic migrations. Wire the users API to a local PostgreSQL instance. Run `alembic revision --autogenerate` and `alembic upgrade head`.

```

# Sprint 1 · Day 3 · Wed 22 Apr 2026

**Topic:** PostgreSQL + Async SQLAlchemy — async engine, session factory, `DeclarativeBase` models with `AsyncAttrs` and `MappedAsDataclass`, repository pattern, Alembic migrations. Wire the `/users` CRUD API to a local PostgreSQL instance. Run `alembic revision --autogenerate` and `alembic upgrade head`.

**Day Type:** 🖥️ Backend
**Builds On:** `s1-d2-fastapi-production-setup-update2.md` — replaces the in-memory dict store with real PostgreSQL

---

## Step 1: Progressive Learning Steps & UK Job Market Relevance

### 🎯 Learning Objectives

This day covers the PostgreSQL and async database patterns that senior Python engineers are expected to know, specifically targeting:

1. **Async Engine and Session Factory**
   - `create_async_engine`, `async_sessionmaker`, `AsyncSession`
   - Why `asyncpg` is mandatory and `psycopg2` is not acceptable in a FastAPI app
   - `pool_pre_ping`, `pool_recycle`, `pool_size`, `max_overflow` — production pool configuration
   - Library: `sqlalchemy[asyncio]` 2.1.x + `asyncpg` 0.30.x

2. **SQLAlchemy 2.1 ORM Models**
   - `DeclarativeBase`, `Mapped[]`, `mapped_column`, nullable inference from type annotations
   - The 2026 combined base pattern: `AsyncAttrs + MappedAsDataclass + DeclarativeBase`
   - `MappedAsDataclass` — typed `__init__`, `__repr__`, `__eq__` from `Mapped[]` annotations
   - `AsyncAttrs` mixin — `awaitable_attrs` for controlled async relationship access
   - `WriteOnlyMapped` — prevents N+1 for unbounded collections at compile time

3. **Repository Pattern**
   - Encapsulate all DB queries in a dedicated class
   - PEP 695 `type UserId = int` domain aliases
   - Clean boundary between route logic and data access — the senior interview filter

4. **Alembic Migrations**
   - `alembic init`, async `env.py` with `run_sync` bridge, `NullPool`
   - `--autogenerate`, `upgrade head`, `downgrade -1`
   - Why all model modules must be imported before `Base.metadata` is read

5. **Testing with `aiosqlite`**
   - In-memory SQLite as async test driver — no real PostgreSQL required in CI
   - `dependency_overrides` for DB session
   - `conftest.py` structure, `asyncio_mode = "auto"`, coverage target 80%

### 📊 UK Job Market Relevance (£90k–£130k / £550–£750/day)

| Skill Area              | Market Frequency             | Interview Focus | Why It Matters                                                                                                |
| ----------------------- | ---------------------------- | --------------- | ------------------------------------------------------------------------------------------------------------- |
| **Async SQLAlchemy**    | ~70% of FastAPI roles        | Very High       | `asyncpg` vs `psycopg2` is a first-round filter; blocking DB calls in async routes are a known production bug |
| **`MappedAsDataclass`** | ~50% of senior roles         | High            | 2026 idiomatic ORM style — plain `DeclarativeBase` without it is considered legacy                            |
| **Repository pattern**  | ~65% of senior roles         | Very High       | Explicitly named in interviews; separates mid from senior-level candidates                                    |
| **Alembic**             | ~60% of backend roles        | Very High       | Interviewers expect walk-through: `--autogenerate`, `upgrade head`, `NullPool`, `run_sync`                    |
| **Connection pooling**  | ~45% of senior roles         | High            | `pool_pre_ping=True` absence in code review signals tutorial-level experience                                 |
| **Soft delete**         | ~50% of fintech/health roles | High            | Standard in regulated UK industries — hard delete is a red flag in domain design                              |
| **N+1 detection**       | ~55% of senior roles         | High            | `selectinload` vs `joinedload`, `echo=True` — expected at senior screen level                                 |

### ✅ Key Industry Patterns for 2026

- **`asyncpg` is mandatory** with async SQLAlchemy — `psycopg2` in an async app is a production performance bug and will be flagged in any serious code review
- **The 2026 ORM base is `AsyncAttrs + MappedAsDataclass + DeclarativeBase`** — MRO (Method Resolution Order) order is required; plain `DeclarativeBase` without `MappedAsDataclass` is considered legacy at senior level
- **Repository pattern** separates mid from senior — interviewers at scale-ups and enterprise ask for it by name and walk through your implementation
- **`pool_pre_ping=True` is expected** in production configuration — its absence signals copy-paste tutorial experience rather than production understanding
- **`uv`** is the 2026 default for Python tooling — all-in-one, Rust-based, replaces pyenv + poetry for new projects; `poetry` remains common in existing codebases
- **Python 3.14** is the current stable version — free-threaded builds (PEP 703) are available and evolving; multiprocessing remains relevant for CPU-bound work

### 💼 What UK Interviewers Will Ask

- "Why can't you use `psycopg2` with async FastAPI?" → sync driver blocks the event loop; `asyncpg` is required
- "What causes `MissingGreenlet` in SQLAlchemy async?" → lazy loading or sync DB call inside async context
- "Walk me through a database migration" → `alembic revision --autogenerate`, review the script, `upgrade head`
- "Why `NullPool` in Alembic?" → migration is a short-lived CLI op; default `QueuePool` causes `dispose()` to hang
- "What is the repository pattern and why use it?" → encapsulates DB queries, testable, reusable, clean boundary
- "How do you prevent N+1 in SQLAlchemy?" → `selectinload` for one-to-many, `joinedload` for many-to-one, `echo=True` to detect
- "What is your Python tooling setup?" → `uv` for new projects, `poetry` in existing codebases, both expected at senior level

---

## Step 2: Comprehensive Q&A and Code Artefacts

---

## 📦 Required Packages

First, set up your Python environment and add the Day 3 dependencies:

```bash
# --- Using uv (recommended) ---

# First-time project setup (if starting fresh)
uv python install 3.14
uv python pin 3.14
uv init fastapi-users-api
cd fastapi-users-api

# Add to existing Day 2 project
uv add "sqlalchemy[asyncio]>=2.1" asyncpg alembic
uv add --dev aiosqlite

# Run commands in the managed environment
uv run fastapi dev main.py          # development (hot reload)
uv run fastapi run main.py          # production
uv run alembic upgrade head
uv run pytest --cov=. --cov-fail-under=80
uv run ruff check .
uv run mypy .

# --- Using poetry (common in existing codebases) ---

# Add to existing Day 2 project
poetry add "sqlalchemy[asyncio]>=2.1" asyncpg alembic
poetry add --group dev aiosqlite

# Run commands
poetry run fastapi dev main.py
poetry run alembic upgrade head
poetry run pytest --cov=. --cov-fail-under=80
```

```toml
# pyproject.toml — full version pins including Day 2 carry-forwards

# --- uv / PEP 621 style (recommended for new projects) ---
[project]
name = "fastapi-users-api"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = [
    "fastapi[standard]>=0.115",
    "pydantic>=2.11",
    "pydantic-settings>=2.7",
    "PyJWT>=2.9",
    "cryptography>=43",
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
]

[tool.ruff]
line-length = 100
target-version = "py314"

[tool.ruff.lint]
<!-- select = ["E", "F", "I", "N", "W", "UP"] -->
select = [
    # Core rules
    "E", "W",     # pycodestyle (errors & warnings)
    "F",          # pyflakes (logic errors)
    "I",          # isort (import sorting)
    "N",          # pep8-naming (naming conventions)
    "UP",         # pyupgrade (modern syntax)

    # Popular & highly recommended
    "B",          # flake8-bugbear (common bugs & design issues)
    "C4",         # flake8-comprehensions (better comprehensions)
    "SIM",        # flake8-simplify (code simplification)
    "RUF",        # Ruff-specific rules (useful checks)
    "TID",        # flake8-tidy-imports (ban relative imports, etc.)
    "ARG",        # flake8-unused-arguments (unused function args)
    "PTH",        # flake8-use-pathlib (encourage pathlib over os.path)
    "PLC", "PLE", "PLW",  # Pylint (convention, error, warning)

    # Code quality & safety
    "S",          # flake8-bandit (security issues)
    "PERF",       # Perflint (performance anti-patterns)
    "DTZ",        # flake8-datetimez (timezone-aware datetime)
    "LOG",        # flake8-logging (logging best practices)
    "G",          # flake8-logging-format (logging format checks)

    # Maintainability
    "C90",        # mccabe (cyclomatic complexity)
    "PD",         # pandas-vet (pandas best practices)
    "PYI",        # flake8-pyi (type stub best practices)
    "RET",        # flake8-return (explicit return statements)
    "SLF",        # flake8-self (access to private members)
]

# Set maximum complexity threshold
[tool.ruff.lint.mccabe]
max-complexity = 10

[tool.mypy]
python_version = "3.14"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --cov=. --cov-report=term-missing"

# --- poetry style (legacy / existing codebases) ---
# [tool.poetry.dependencies]
# python = "^3.14"
# fastapi = {version = "^0.115", extras = ["standard"]}
# pydantic = "^2.11"
# pydantic-settings = "^2.7"
# PyJWT = "^2.9"
# cryptography = "^43"
# sqlalchemy = {version = "^2.1", extras = ["asyncio"]}
# asyncpg = "^0.30"
# alembic = "^1.14"
#
# [tool.poetry.group.dev.dependencies]
# ruff = "^1.0"
# mypy = "^1.18"
# pytest = "^8"
# httpx = "^0.28"
# pytest-cov = "^6"
# pytest-asyncio = "^0.24"
# aiosqlite = "^0.21"
```

| Package               | Version (stable May 2026) | Purpose                                                                     |
| --------------------- | ------------------------- | --------------------------------------------------------------------------- |
| `sqlalchemy[asyncio]` | 2.1.x                     | ORM + async support — 2.1 required for `WriteOnlyMapped` nullable inference |
| `asyncpg`             | 0.30.x                    | Native async PostgreSQL driver — mandatory with async SQLAlchemy            |
| `alembic`             | 1.14.x                    | Database migration tool                                                     |
| `aiosqlite`           | 0.21.x                    | In-memory async SQLite for tests — no real PostgreSQL required in CI        |
| `ruff`                | 1.x                       | Linter + formatter — Rust-based, replaces flake8/black/isort                |
| `mypy`                | 1.18+                     | Static type checker — `strict = true` is the 2026 senior standard           |

---

## 🖥️ Part 1: Async Engine, Sessions, and ORM Models

### Q&A Batch 1: Async Engine and Sessions

**Q1: What is the difference between a synchronous and asynchronous SQLAlchemy engine, and why does it matter in FastAPI?**
A: A synchronous engine blocks the OS thread while waiting for the database — in FastAPI's async event loop this blocks all other concurrent requests. `create_async_engine` issues database I/O via `asyncio`, keeping the event loop free. Using sync SQLAlchemy in `async def` routes is a production performance bug: under load a single slow query serialises every request.

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/mydb",
    echo=False,       # set True only in dev — logs every SQL statement
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,   # validates connections before use — free insurance
    pool_recycle=3600,    # recycles connections older than 1 hour
)
```

**Q2: What is `asyncpg` and why use it over `psycopg2` in an async FastAPI app?**
A: `psycopg2` is a synchronous C-extension driver — it blocks the thread on every query. `asyncpg` is a pure-Python driver built for `asyncio` from the ground up with no synchronous fallback. SQLAlchemy's async dialect (`postgresql+asyncpg://`) requires `asyncpg`. Using `psycopg2` with async SQLAlchemy causes `MissingGreenlet` errors at runtime — a well-known interview trap.

```python
# Using psycopg2 URL (sync driver)
engine = create_async_engine("postgresql://user:pass@localhost/db")
# CORRECT - Using asyncpg
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db"
)
# Miss that connection strings for async mode require the `+asyncpg` dialect
```

**Q3: What is `async_sessionmaker` and how does it differ from the older `sessionmaker`?**
A: `async_sessionmaker` (introduced SQLAlchemy 2.0) is the async-native factory for `AsyncSession` objects. The older `sessionmaker` creates synchronous `Session` objects. Using `async_sessionmaker` with `class_=AsyncSession` ensures every session operation is awaitable and correct in the async context.

```python
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # prevents MissingGreenlet after commit
)
```

**Q4: What does `expire_on_commit=False` do and what problem does it solve?**
A: After `session.commit()`, SQLAlchemy marks all loaded ORM attributes as expired — the next access triggers a database reload. In async sessions that reload raises `MissingGreenlet`. Setting `expire_on_commit=False` keeps in-memory values loaded post-commit. This is the correct behaviour for API responses that return the just-created object.

**Q5: How do you provide a database session to FastAPI route handlers safely?**
A: Use a `yield` dependency — the session is scoped to the request, committed on success, rolled back on exception, and always closed.

```python
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

**Q6: What is `pool_pre_ping=True` and when should you always set it?**
A: `pool_pre_ping` issues a lightweight `SELECT 1` before returning a pooled connection to the caller. If the connection is stale (database restarted, network dropped), the pool discards it and opens a fresh one. Always set it in production — without it, stale connections cause `OperationalError` on the first query after a database restart. Its absence in a code review signals tutorial-level experience.

**Q7: What is `pool_recycle` and why is it needed alongside `pool_pre_ping`?**
A: `pool_recycle=3600` closes and reopens connections held for longer than one hour. This prevents issues with PostgreSQL server-side connection timeouts (`idle_in_transaction_session_timeout`) that would otherwise silently invalidate long-lived pooled connections. `pool_pre_ping` catches stale connections on checkout; `pool_recycle` proactively prevents them from becoming stale.

**Q8: What is `pool_size` vs `max_overflow` — how do you choose the right values?**
A: `pool_size` is the number of persistent connections always kept open. `max_overflow` is the number of additional connections allowed during traffic spikes — closed when the burst ends. Rule of thumb: `pool_size` ≈ expected steady-state concurrent DB queries per server instance; `max_overflow` ≈ 2× `pool_size`. For a FastAPI app on a single VM, `pool_size=10, max_overflow=20` is a reasonable starting point.

**Q9: What is `MissingGreenlet` in SQLAlchemy async and what causes it?**
A: `MissingGreenlet` is raised when code attempts a synchronous database operation — such as lazy relationship loading or using `psycopg2` — inside an async context. Fixes: eager loading with `selectinload` or `joinedload`, `AsyncAttrs.awaitable_attrs` for deliberate async lazy access, or restructuring the query.

**Q10: How do you handle a unique constraint violation gracefully in a FastAPI route?**
A: Catch `IntegrityError` from SQLAlchemy and return `409 Conflict`. Never let database errors bubble up as `500 Internal Server Error` to API clients.

```python
from sqlalchemy.exc import IntegrityError

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(payload: UserCreate, repo: UserRepo):
    try:
        user = await repo.create(name=payload.name, email=payload.email, role=payload.role)
        return user
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email already registered")
```

**Q11: How do you define an ORM model in SQLAlchemy 2.0 / 2.1? What changed from v1?**
A: SQLAlchemy 2.0 introduced `DeclarativeBase` (replaces `declarative_base()`) and `Mapped[]` type annotations with `mapped_column` (replaces `Column(...)`). SQLAlchemy 2.1 refined nullable inference — `Mapped[str | None]` implies `nullable=True` without needing to set it explicitly.

```python
# SQLAlchemy 1.x — avoid in new projects
name = Column(String(100), nullable=False)

# SQLAlchemy 2.1 — use this
name: Mapped[str] = mapped_column(String(100))         # nullable=False inferred
email: Mapped[str | None] = mapped_column(String(255)) # nullable=True inferred
```

**Q12: What is `MappedAsDataclass` and what does it generate automatically?**
A: `MappedAsDataclass` applies Python's `@dataclass` transformation to an ORM model. It generates a typed `__init__`, `__repr__`, and `__eq__` from `Mapped[]` annotations — so you write `User(name="x", email="y@z.com")` rather than instantiating with keyword args that mypy cannot check. `init=False` excludes server-generated fields from the constructor.

```python
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, func
from datetime import datetime

class Base(MappedAsDataclass, DeclarativeBase):
    """Base class docstring."""
    pass

class User(Base):
    """User class docstring."""
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), init=False)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    role: Mapped[str] = mapped_column(String(50), default="user")
```

**Q13: What is `AsyncAttrs` and what problem does it solve?**
A: `AsyncAttrs` is a SQLAlchemy mixin that adds `awaitable_attrs` to every ORM model instance. It solves `MissingGreenlet` — the error raised when code tries to access an unloaded relationship in an async context. Instead of always requiring eager loading, `AsyncAttrs` enables deliberate async lazy loading via `await obj.awaitable_attrs.relationship_name`.

```python
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase

# 2026 production base — MRO (Method Resolution Order) order is required
class Base(AsyncAttrs, MappedAsDataclass, DeclarativeBase):
    """
    AsyncAttrs:        awaitable_attrs for controlled async lazy access
    MappedAsDataclass: typed __init__, __repr__, __eq__
    DeclarativeBase:   ORM table registration
    MRO rule: AsyncAttrs and MappedAsDataclass must precede DeclarativeBase.
    """
    pass
```

**Q14: What is `WriteOnlyMapped` and when should you use it instead of `Mapped[list[...]]`?**
A: `WriteOnlyMapped[list[T]]` marks a collection as write-only — it cannot be loaded or iterated directly. Use it for any relationship where the child table could grow unbounded (audit logs, events, notifications). It prevents N+1 for those collections by making a full load a compile-time error rather than a runtime performance bug.

```python
from sqlalchemy.orm import WriteOnlyMapped, relationship

class User(Base):
    """User class docstring."""
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    role: Mapped[str] = mapped_column(String(50), default="user")
    audit_logs: WriteOnlyMapped[list["AuditLog"]] = relationship(
        back_populates="user", init=False
    )
```

**Q15: When should you use `AsyncAttrs.awaitable_attrs` vs `selectinload`?**
A: Use `selectinload` (eager loading) when you know at query time that the relationship will always be needed — two SQL queries total regardless of N. Use `awaitable_attrs` for conditional access where you only sometimes need the related data after the initial query. Never use `awaitable_attrs` in a loop — that is the N+1 problem in async form.

```python
# Eager loading — preferred for known access patterns
result = await session.execute(
    select(User).options(selectinload(User.posts)).where(User.id == user_id)
)
user = result.scalar_one_or_none()
posts = user.posts  # already loaded

# awaitable_attrs — for conditional access
user = await session.get(User, user_id)
if needs_posts:
    posts = await user.awaitable_attrs.posts  # async lazy load — safe
```

---

### 🎯 Working Code Artefact 1: Async Engine, Session Factory, and ORM Models

```python
"""
database.py and models/user.py — 2026 production async SQLAlchemy setup
Uses AsyncAttrs + MappedAsDataclass + DeclarativeBase combined base
"""

# --- database.py ---
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,   # logs SQL in dev; never True in production
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,    # validates connections before use — free insurance
    pool_recycle=3600,     # recycles connections older than 1 hour
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,    # ensures every session operation is awaitable and correct in the async context
    expire_on_commit=False,  # keeps attributes accessible after commit
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency — yields a scoped session, rolls back on error."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# --- models/user.py ---
from datetime import datetime
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    MappedAsDataclass,
    DeclarativeBase,
    Mapped,
    mapped_column,
    WriteOnlyMapped,
    relationship,
)


class Base(AsyncAttrs, MappedAsDataclass, DeclarativeBase):
    """
    2026 production base class.
    MRO: AsyncAttrs → MappedAsDataclass → DeclarativeBase (required order).
    AsyncAttrs:        awaitable_attrs for controlled async relationship access
    MappedAsDataclass: typed __init__, __repr__, __eq__ from Mapped[] annotations
    DeclarativeBase:   ORM table registration
    """
    pass


class User(Base):
    """User class docstring."""
    __tablename__ = "users"

    # init=False — DB generates these; excluded from __init__
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), init=False)
    is_active: Mapped[bool] = mapped_column(default=True, init=False)

    # Required constructor fields (no defaults)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    # Optional constructor field with default
    role: Mapped[str] = mapped_column(String(50), default="user")

    # WriteOnlyMapped — unbounded collection; must be queried explicitly
    audit_logs: WriteOnlyMapped[list["AuditLog"]] = relationship(
        back_populates="user", init=False
    )


class AuditLog(Base):
    """AuditLog class docstring."""
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(200))
    user: Mapped["User"] = relationship(back_populates="audit_logs", init=False)
```

### ✅ Key Concepts

- **Always use `asyncpg` + `create_async_engine`** — sync engines block the event loop and destroy throughput under concurrent load
- **`expire_on_commit=False` is not optional** — omitting it causes `MissingGreenlet` the first time you return a just-committed ORM object from a route
- **The 2026 base is `AsyncAttrs + MappedAsDataclass + DeclarativeBase`** — MRO order is required; `AsyncAttrs` and `MappedAsDataclass` must precede `DeclarativeBase`
- **`WriteOnlyMapped` prevents N+1 at compile time** for unbounded collections — `Mapped[list[T]]` allows accidental full loads; `WriteOnlyMapped[list[T]]` makes them a type error
- **`pool_pre_ping=True` is free insurance** — one `SELECT 1` per checkout eliminates a class of `OperationalError` failures after database restarts

### ⚠️ Common Pitfalls

- Using `psycopg2` (synchronous) as the driver — causes `MissingGreenlet` or silent thread blocking in `async def` routes
- Omitting `expire_on_commit=False` — the first attribute access on a returned ORM object after commit raises `MissingGreenlet`
- Forgetting `MRO` order on the combined base class — `class Base(DeclarativeBase, AsyncAttrs, MappedAsDataclass)` causes metaclass conflicts at import time
- Using `Mapped[list[T]]` for unbounded collections — accidental `user.audit_logs` access triggers a full table load; use `WriteOnlyMapped` instead
- Omitting `pool_pre_ping=True` — stale connections cause `OperationalError` on the first query after a database restart in production

---

## 🖥️ Part 2: Repository Pattern and Dependency Injection

### Q&A Batch 2: Repository Pattern

**Q16: What is the repository pattern and why is it preferred over querying directly in route handlers?**
A: The repository pattern encapsulates all database access for a domain entity behind a class interface. Route handlers call `user_repo.get_by_id(id)` rather than building SQLAlchemy queries inline. Benefits: testable (mock the repo, not the DB), reusable (same query across multiple routes), and maintainable (SQL changes in one place). Senior engineers are expected to name and apply this pattern — it is one of the first things senior interviewers probe.

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User

class UserRepository:
    """UserRepository class docstring."""
    def __init__(self, session: AsyncSession) -> None:
        """__init__ method docstring."""
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id, User.is_active == True)
        )
        return result.scalar_one_or_none()
```

**Q17: What are PEP 695 type aliases (`type UserId = int`) and why use them in repository signatures?**
A: PEP 695 (Python 3.12+) introduced the `type` statement as the language-native way to define type aliases. `type UserId = int` communicates domain intent — `get_by_id(user_id: UserId)` is more readable than `get_by_id(user_id: int)`. It is the single change point if `UserId` ever becomes a UUID. The `type` keyword is lazy-evaluated, requires no import, and is fully supported by mypy and pyright.

```python
# repositories/user.py — PEP 695 domain aliases
type UserId    = int    # single change point if `UserId` ever becomes a UUID
type UserEmail = str
type RoleName  = str

class UserRepository:
    """UserRepository class docstring."""
    async def get_by_id(self, user_id: UserId) -> User | None: ...
    async def get_by_email(self, email: UserEmail) -> User | None: ...
    async def get_all(self, role: RoleName | None = None) -> list[User]: ...
```

**Q18: How do you inject a repository as a FastAPI dependency using PEP 695 type aliases?**
A: Define a factory function and use PEP 695 `type` aliases to clean up route signatures. Routes import the alias and never write raw `Depends()` calls inline.

```python
# dependencies.py
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from repositories.user import UserRepository

def get_user_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    """get_user_repo function docstring."""
    return UserRepository(db)

type DBSession = Annotated[AsyncSession, Depends(get_db)]
type UserRepo  = Annotated[UserRepository, Depends(get_user_repo)]
```

```python
# Usage in router — clean, typed, no raw Depends calls
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, repo: UserRepo) -> User:
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

**Q19: What is `session.flush()` vs `session.commit()` and when do you use each?**
A: `flush()` writes pending changes to the database within the current transaction — data is visible to subsequent queries in the same session but not yet committed. `commit()` finalises the transaction and makes it visible to other sessions. Use `flush()` when you need the auto-generated `id` of a new row before committing a multi-step transaction.

**Q20: What is `session.refresh()` and when do you need to call it?**
A: `session.refresh(obj)` reloads all attributes of an ORM object from the database. Required after `flush()` to read server-generated values (`id`, `created_at`) back into the Python object. Without it, `user.id` is `None` because the value exists only in the DB, not yet reflected in memory.

```python
async def create(self, name: str, email: str, role: str = "user") -> User:
    user = User(name=name, email=email, role=role)
    self.session.add(user)
    await self.session.flush()       # writes to DB within current transaction
    await self.session.refresh(user) # loads server-generated id and created_at
    return user
```

**Q21: What are `scalar_one_or_none()`, `scalar_one()`, and `scalars().all()`?**
A: Use `scalar_one_or_none()` for lookups by primary key or unique field — returns `None` if missing, raises if multiple. Use `scalar_one()` when you expect exactly one row. Use `scalars().all()` for list queries — returns an empty list if no rows.

**Q22: How do you soft-delete records rather than hard-deleting them?**
A: Add an `is_active: Mapped[bool]` column defaulting to `True`. Override the repository `delete` method to set `is_active = False`. Filter all list queries with `.where(User.is_active == True)`. Standard in UK regulated industries (fintech, healthcare, legal-tech) — hard delete is a red flag in domain design interviews.

```python
async def soft_delete(self, user: User) -> None:
    """Sets is_active=False — preserves audit history. Never hard-deletes."""
    user.is_active = False
    await self.session.flush()
```

**Q23: What is the N+1 query problem and how do you detect and fix it in SQLAlchemy?**
A: N+1 occurs when loading N parent objects triggers N additional queries for related data — 100 users then `user.posts` on each triggers 100 SELECTs. Fix with `selectinload` (two queries total) or `joinedload` (one JOIN). Detect with `echo=True` on the engine — count the SQL statements in log output.

```python
from sqlalchemy.orm import selectinload

# N+1 — 1 query for users + N for posts
users = (await session.execute(select(User))).scalars().all()
for u in users:
    _ = u.posts  # MissingGreenlet or N queries

# Fixed — 2 queries total
result = await session.execute(select(User).options(selectinload(User.posts)))
users = result.scalars().all()
```

**Q24: What is `selectinload` vs `joinedload` and when do you choose each?**
A: `selectinload` issues a second `SELECT ... WHERE id IN (...)` for related objects — preferred for one-to-many. `joinedload` adds a `JOIN` to the primary query — fewer round trips but can produce large result sets. Use `selectinload` for one-to-many (users → posts). Use `joinedload` for many-to-one (post → author).

**Q25: How do you prevent SQL injection in SQLAlchemy ORM queries?**
A: ORM queries via `select(User).where(User.email == email)` use bound parameters automatically. SQL injection is only possible via raw `text()` with f-strings. Never do `text(f"WHERE email = '{email}'")`.

```python
# SAFE — bound parameter
result = await session.execute(select(User).where(User.email == email))

# UNSAFE — SQL injection risk
result = await session.execute(text(f"SELECT * FROM users WHERE email = '{email}'"))

# SAFE raw query with binding
result = await session.execute(text("SELECT * FROM users WHERE email = :e"), {"e": email})
```

**Q26: How do you write a repository method that applies optional filters dynamically?**
A: Build the base statement, then conditionally add `.where()` clauses.

```python
async def get_all(self, skip: int = 0, limit: int = 20, role: str | None = None) -> list[User]:
    stmt = select(User).where(User.is_active == True).order_by(User.created_at.desc())
    if role is not None:
        stmt = stmt.where(User.role == role)
    result = await self.session.execute(stmt.offset(skip).limit(limit))
    return list(result.scalars().all())
```

**Q27: How do you run multiple database operations atomically?**
A: Keep all operations within one `get_db` request — the dependency commits at the end if no exception is raised. For complex multi-step operations, use multiple `flush()` calls to get generated IDs, but only one `commit()` at the end via the dependency.

**Q28: What is cursor-based pagination vs offset-based pagination?**
A: Offset pagination degrades at large offsets because the database must scan and discard rows. Cursor pagination uses a stable column value (`id`, `created_at`) as the cursor — `WHERE id > last_seen_id ORDER BY id LIMIT N`. This is O(log N) rather than O(N) and produces consistent results even when rows are inserted between pages.

```python
async def get_page(self, after_id: int = 0, limit: int = 20) -> list[User]:
    result = await self.session.execute(
        select(User)
        .where(User.id > after_id, User.is_active == True)
        .order_by(User.id.asc())
        .limit(limit)
    )
    return list(result.scalars().all())
```

**Q29: How does `MappedAsDataclass` interact with Pydantic response schemas?**
A: `MappedAsDataclass` models work exactly like standard ORM models for Pydantic serialisation. Your response schema still needs `model_config = ConfigDict(from_attributes=True)` to read ORM attributes. The `MappedAsDataclass` layer is purely a Python constructor convenience — it does not change how SQLAlchemy exposes attributes to Pydantic.

**Q30: What is the repository pattern's limitation and when do you reach for a service layer?**
A: The repository pattern handles single-entity DB access cleanly. When business logic spans multiple entities (create a user AND send a notification AND increment a counter atomically), a service layer is needed — it orchestrates multiple repositories within one transaction boundary and keeps route handlers free of business logic.

---

### 🎯 Working Code Artefact 2: Full Repository and Dependency Injection

```python
# repositories/user.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models.user import User

type UserId    = int
type UserEmail = str
type RoleName  = str


class UserRepository:
    """UserRepository class docstring."""
    def __init__(self, session: AsyncSession) -> None:
        """__init__ method docstring."""
        self.session = session

    async def get_by_id(self, user_id: UserId) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id, User.is_active == True)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: UserEmail) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        role: RoleName | None = None,
    ) -> list[User]:
        stmt = (
            select(User)
            .where(User.is_active == True)
            .order_by(User.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        if role is not None:
            stmt = stmt.where(User.role == role)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, name: str, email: UserEmail, role: RoleName = "user") -> User:
        user = User(name=name, email=email, role=role)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def update(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            if value is not None:
                setattr(user, key, value)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def soft_delete(self, user: User) -> None:
        user.is_active = False
        await self.session.flush()
```

```python
# dependencies.py
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from repositories.user import UserRepository


def get_user_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    """get_user_repo function docstring."""
    return UserRepository(db)


type DBSession = Annotated[AsyncSession, Depends(get_db)]
type UserRepo  = Annotated[UserRepository, Depends(get_user_repo)]
```

```python
# routers/users.py
from typing import Annotated
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from sqlalchemy.exc import IntegrityError

from schemas.user import UserCreate, UserUpdate, UserResponse
from dependencies import UserRepo

router = APIRouter(prefix="/users", tags=["users"])

type PageSkip  = Annotated[int, Query(ge=0)]
type PageLimit = Annotated[int, Query(ge=1, le=100)]


def _send_welcome_email(email: str) -> None:
    """_send_welcome_email function docstring."""
    print(f"[background] Sending welcome email to {email}")


@router.get("/", response_model=list[UserResponse])
async def list_users(
    repo: UserRepo,
    skip: PageSkip = 0,
    limit: PageLimit = 20,
    role: Annotated[str | None, Query()] = None,
) -> list:
    return await repo.get_all(skip=skip, limit=limit, role=role)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, repo: UserRepo):
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    payload: UserCreate,
    repo: UserRepo,
    background_tasks: BackgroundTasks,
):
    try:
        user = await repo.create(name=payload.name, email=payload.email, role=payload.role)
        background_tasks.add_task(_send_welcome_email, payload.email)
        return user
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Email already registered")


@router.patch("/{user_id}", response_model=UserResponse)
async def patch_user(user_id: int, payload: UserUpdate, repo: UserRepo):
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updates = payload.model_dump(exclude_unset=True)
    return await repo.update(user, **updates) # repo.update(user, name="John", email="john@example.com")


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, repo: UserRepo) -> None:
    user = await repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await repo.soft_delete(user)
```

### ✅ Key Concepts

- **Repository pattern enforces a clean boundary** — route handlers describe _what_ to do; repositories describe _how_ to query
- **PEP 695 `type` aliases** — `type UserId = int` expresses domain intent and is the single change point if the type evolves
- **`flush()` then `refresh()`** — flush writes within the current transaction to get the DB-generated `id`; refresh reads it back into memory
- **Soft delete preserves audit history** — standard in regulated UK industries; hard delete is a red flag in domain design interviews
- **`scalar_one_or_none()`** is the correct method for primary key and unique field lookups

### ⚠️ Common Pitfalls

- Calling `session.commit()` inside the repository rather than letting the `get_db` dependency own the commit — breaks transaction atomicity for multi-step operations
- Forgetting `await session.flush()` before `await session.refresh(user)` — `refresh` reads from the DB; without `flush` the row does not yet exist
- Using `text(f"... {user_input}")` in any SQLAlchemy query — SQL injection vulnerability; always use bound parameters
- Not importing all model modules in `alembic/env.py` before reading `Base.metadata` — generates destructive `DROP TABLE` for unseen tables

---

## 🖥️ Part 3: Alembic Migrations

### Q&A Batch 3: Alembic

**Q31: What is Alembic and how does it relate to SQLAlchemy?**
A: Alembic is the official migration tool for SQLAlchemy. It tracks schema versions in an `alembic_version` table and provides `upgrade` / `downgrade` scripts. `--autogenerate` inspects the diff between `Base.metadata` and the live database to generate migration scripts automatically. It is to Python what Prisma Migrate is to Node.js / TypeScript.

**Q32: Walk through setting up Alembic from scratch in a FastAPI project.**
A: Initialise, patch `env.py` for async, generate, review, and apply.

```bash
# 1. Initialise (creates alembic/ directory and alembic.ini)
alembic init alembic

# 2. Edit alembic/env.py — point at async engine, import all models

# 3. Generate first migration from ORM models
alembic revision --autogenerate -m "create users table"

# 4. Review the generated file in alembic/versions/ — always before applying

# 5. Apply to database
alembic upgrade head

# 6. Roll back one step
alembic downgrade -1

# 7. Check current version
alembic current
```

**Q33: What changes are required in `alembic/env.py` for async SQLAlchemy?**
A: Use `run_async_migrations()` with `async_engine_from_config`, `connection.run_sync(do_run_migrations)` as the bridge, and `NullPool` to prevent hangs on `engine.dispose()`. Set `target_metadata = Base.metadata` so `--autogenerate` can compare ORM definitions to the live schema.

**Q34: Why is `connection.run_sync()` required in the async Alembic `env.py`?**
A: Alembic's migration context (`context.run_migrations()`) is synchronous — it was designed before `asyncio` was mainstream. `run_sync(do_run_migrations)` provides a synchronisation bridge: it executes a sync callable within an open async connection. Without it, calling the sync runner directly from an async function raises `RuntimeError`.

**Q35: Why must `NullPool` be used for the Alembic migration engine?**
A: Alembic migrations are a short-lived CLI operation, not a persistent server. Using the default `QueuePool` means SQLAlchemy holds open connections in the pool after migrations complete, causing `asyncio.run()` to block waiting for the pool to drain. `NullPool` creates connections on demand and closes them immediately.

**Q36: What happens if you forget to import a model in `alembic/env.py` before running `--autogenerate`?**
A: Alembic compares `Base.metadata` against the live database. If a model module is not imported, its table is absent from `metadata`. Alembic concludes that table should not exist and generates a `DROP TABLE` migration — destroying real data if applied.

```python
# ✅ Correct — import every model so Base.metadata is fully populated
from models.user import Base     # User and AuditLog both registered
target_metadata = Base.metadata

# ❌ Wrong — AuditLog module never imported
# result: alembic generates DROP TABLE audit_logs
```

**Q37: What is `alembic upgrade head` vs `alembic upgrade +1`?**
A: `upgrade head` applies all pending migrations in order — use in CI/CD startup scripts. `upgrade +1` applies exactly one step — use when testing individual scripts during development.

**Q38: What is `alembic stamp head` and when would you use it?**
A: `alembic stamp head` marks the database as being at the latest migration version without running any scripts. Use it when you have manually created the schema (e.g., via `Base.metadata.create_all()` in test setup) and want Alembic to start tracking from that point.

**Q39: How do you run Alembic migrations as part of application startup in production?**
A: In the `lifespan` function before `yield`, or as a dedicated init container in Kubernetes.

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    yield
```

**Q40: What alembic commands must you know for a UK senior backend interview?**

| Command                                    | Purpose                                                        |
| ------------------------------------------ | -------------------------------------------------------------- |
| `alembic init alembic`                     | Initialise migration directory                                 |
| `alembic revision --autogenerate -m "msg"` | Generate migration from ORM diff                               |
| `alembic upgrade head`                     | Apply all pending migrations                                   |
| `alembic upgrade +1`                       | Apply one migration step                                       |
| `alembic downgrade -1`                     | Roll back one step                                             |
| `alembic current`                          | Show current schema version                                    |
| `alembic history`                          | Show full migration history                                    |
| `alembic stamp head`                       | Mark DB at latest version without running scripts              |
| `alembic merge heads`                      | Merge branched migration histories from concurrent development |

**Q41: What is `alembic merge heads` and when do you need it?**
A: When two developers create migration files concurrently based on the same parent revision, Alembic detects multiple heads. `alembic merge heads` generates a new migration that merges the two branches back into a single linear history. Always run `alembic merge heads` before deploying if `alembic heads` shows more than one head.

**Q42: What is the `alembic.ini` setting you always override programmatically?**
A: `sqlalchemy.url` — always override it in `env.py` via `config.set_main_option("sqlalchemy.url", settings.database_url)`. This reads the URL from `pydantic-settings` at runtime rather than storing a real connection string in a committed file.

**Q43: How do you handle a long-running migration (backfilling a column with 10M rows) without locking the table?**
A: Use batched updates with `LIMIT` — process rows in chunks of 1,000–10,000 with a `WHERE backfilled = False` filter. Each chunk is a separate transaction, keeping lock duration minimal. Always test against a production-size data clone first.

**Q44: How would you design a zero-downtime migration strategy for a column rename?**
A: Three-step process: (1) add the new column, deploy code that writes to both old and new columns; (2) backfill the new column from the old; (3) deploy code that reads from the new column only, then remove the old column in a subsequent migration. Never rename in a single migration on a live system.

**Q45: What is the difference between optimistic and pessimistic locking in SQLAlchemy?**
A: Pessimistic locking uses `SELECT ... FOR UPDATE` to lock rows before reading. Optimistic locking adds a `version` column — before updating, check the version matches, raise a conflict error if not. Optimistic locking is preferred in high-read, low-conflict systems (most web APIs). Pessimistic locking is appropriate for financial transactions where conflicts are costly.

---

### 🎯 Working Code Artefact 3: Alembic env.py (Async, Fully Annotated)

```python
# alembic/env.py
import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool
from alembic import context

# Import ALL model modules before Base.metadata is referenced.
# Missing imports → --autogenerate generates DROP TABLE for unseen tables.
from models.user import Base  # registers User and AuditLog
from config import get_settings

settings = get_settings()
config = context.config

# Override sqlalchemy.url from pydantic-settings — never commit real URLs to alembic.ini
config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata  # what --autogenerate compares against


def do_run_migrations(connection) -> None:
    """
    Synchronous inner function — called via connection.run_sync().
    Alembic's context.run_migrations() is sync-only; this wrapper bridges
    the async connection to the sync migration runner.
    """
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    NullPool is mandatory — prevents connection reuse that would cause
    engine.dispose() to hang waiting for the pool to drain.
    """
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    """run_migrations_online function docstring."""
    asyncio.run(run_async_migrations())


run_migrations_online()
```

```bash
# Migration workflow

# 1. Start local PostgreSQL
docker compose up -d

# 2. Generate migration from ORM models — always review before applying
alembic revision --autogenerate -m "create users and audit_logs tables"

# 3. Open alembic/versions/<hash>_*.py
#    Verify op.create_table() calls match expected tables
#    Confirm downgrade() reverses every upgrade() change

# 4. Apply migration
alembic upgrade head

# 5. Verify
alembic current

# 6. Start the API
# Development (hot reload):
uv run fastapi dev main.py
# Production:
uv run fastapi run main.py
```

> **`fastapi dev` vs `fastapi run`:** Use `fastapi dev` during development for hot reload and debug tooling. Use `fastapi run` for production — it disables auto-reload and runs with production-appropriate defaults.

### ✅ Key Concepts

- **Always import all model modules in `alembic/env.py`** before reading `Base.metadata` — missing imports generate destructive `DROP TABLE` migrations
- **`NullPool` is mandatory** for the Alembic engine — `QueuePool` causes `engine.dispose()` to hang after migrations complete
- **`run_sync()` bridges async to sync** — Alembic's migration runner is synchronous; `run_sync` provides the correct context switch without blocking the event loop
- **Always review generated scripts** before applying — autogenerate misses default value changes, check constraints, custom types, and index renames
- **Override `sqlalchemy.url` programmatically** in `env.py` — never commit real database credentials to `alembic.ini`

### ⚠️ Common Pitfalls

- Running `alembic revision --autogenerate` without importing all model files in `env.py` — generates destructive `DROP TABLE` for every unseen table
- Using `QueuePool` instead of `NullPool` for the Alembic engine — causes the migration CLI process to hang indefinitely after completing
- Applying a migration script without reviewing it — autogenerate can produce unexpected `DROP TABLE` or `DROP COLUMN` statements
- Committing `alembic.ini` with a real `sqlalchemy.url` value — exposes database credentials in source control

---

## 🖥️ Part 4: Connection Pooling, Security, and Testing

### Q&A Batch 4: Connection Pooling, Security, and `aiosqlite` Testing

**Q46: What is a database connection pool and why is it critical in production?**
A: A connection pool is a set of pre-opened database connections reused across requests. Opening a TCP connection to PostgreSQL takes 20–100ms. Without pooling, each request bears that overhead. SQLAlchemy's async engine uses a pool by default (`pool_size=5`). In production, tune `pool_size` to expected concurrent queries and `max_overflow` for burst capacity.

```python
engine = create_async_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)
```

**Q47: What is OWASP A03 (Injection) in the context of SQLAlchemy?**
A: OWASP A03 covers attacks where untrusted input is executed as code. ORM queries via `select(User).where(User.email == email)` use bound parameters automatically. SQL injection is only possible via raw `text()` with f-strings. Use parameterised `text("... :param", {"param": value})` for any raw SQL.

**Q48: How do you manage `DATABASE_URL` across local dev, staging, and production environments?**
A: Read from environment variables via `pydantic-settings`. In local dev, load from `.env` (git-ignored). In staging and production, inject from Azure Key Vault, GitHub Actions secrets, or Kubernetes Secrets. Pass the same value to both `create_async_engine` and Alembic's `config.set_main_option`.

**Q49: How do you expose pool health metrics in a FastAPI monitoring endpoint?**
A: Access pool stats via `engine.pool` and return them from a non-schema endpoint.

```python
@app.get("/metrics/db", include_in_schema=False)
async def db_metrics():
    pool = engine.pool
    return {
        "pool_size": pool.size(),
        "checked_out": pool.checkedout(),
        "overflow": pool.overflow(),
        "invalid": pool.invalid(),
    }
```

**Q50: How does Python's free-threaded build (PEP 703) affect async SQLAlchemy workloads?**
A: Python 3.14 supports free-threaded builds (PEP 703) — the GIL can be disabled at runtime. For async SQLAlchemy I/O-bound workloads this makes no practical difference: the async event loop is single-threaded by design and the GIL was already released during I/O waits. Free-threaded builds provide benefit for CPU-bound Python code run across multiple threads. The ecosystem is still evolving — not all C extensions support no-GIL yet. Multiprocessing remains the robust approach for CPU-bound parallelism.

**Q51: How do you test async SQLAlchemy routes without a real PostgreSQL database?**
A: Use `aiosqlite` as the async test driver with an in-memory SQLite database. Create the schema with `Base.metadata.create_all`, override `get_db` via `app.dependency_overrides`, and run tests with `pytest-asyncio`.

**Q52: What is `asyncio_mode = "auto"` in `pyproject.toml` and why should you set it?**
A: `asyncio_mode = "auto"` removes the need to mark every async test with `@pytest.mark.asyncio`. All `async def` test functions are automatically run in an event loop. Recommended for FastAPI projects where most tests are async.

**Q53: Why does the test fixture drop and recreate the schema between tests?**
A: To guarantee test isolation — each test starts with a clean database with no data from previous tests. Without teardown, state leaks between tests cause non-deterministic failures.

**Q54: What is `app.dependency_overrides.clear()` and why must it be called in fixture teardown?**
A: `dependency_overrides.clear()` removes all test-injected dependency replacements. If not called in teardown, subsequent tests still use the test database session rather than the production dependency — causing false positives or cross-test contamination.

**Q55: What is the `ASGITransport` (Asynchronous Server Gateway Interface) pattern for `httpx.AsyncClient` and why is it preferred over `TestClient`?**
A: `ASGITransport(app=app)` routes requests directly to the FastAPI ASGI app without opening a network socket — faster, deterministic, and runnable without a running server. `TestClient` uses `requests` (synchronous) and does not support `async def` test functions naturally.

**Q56: How do you test a `409 Conflict` response for duplicate email?**
A: Create a user, then POST the same payload again and assert `status_code == 409`. The `IntegrityError` from the unique constraint should be caught in the route and returned as a 409.

**Q57: How do you test the soft-delete pattern — that a deleted user returns 404 on subsequent GET?**
A: Create, DELETE, then GET the same user ID and assert the GET returns 404. This confirms the soft delete was applied and the `get_by_id` repository method filters `is_active == True`.

**Q58: How do you load-test a FastAPI + async PostgreSQL stack to find the connection pool ceiling?**
A: Use `locust` or `k6` to ramp concurrent users. Monitor `pool.checkedout()` and `pool.overflow()` from the `/metrics/db` endpoint. When `checkedout + overflow >= pool_size + max_overflow`, new requests queue and response times spike. The pool ceiling is typically hit before CPU — tune `pool_size` first, then scale horizontally.

**Q59: What is the difference between `type UserId = int` (PEP 695) and `NewType("UserId", int)`?**
A: `type UserId = int` is a transparent alias — `int` and `UserId` are interchangeable at the type-checker level. `NewType("UserId", int)` creates a nominally distinct type — mypy rejects passing a plain `int` where `UserId` is expected. Use `NewType` when you want the type checker to enforce that user IDs and team IDs cannot be swapped. Use PEP 695 `type` aliases for readability and documentation.

**Q60: How do you structure the data layer in a large FastAPI application?**
A: Domain-driven structure — routes call services; services call repositories; repositories call the DB. No SQLAlchemy imports in route handlers.

```
app/
├── models/         # SQLAlchemy ORM models (MappedAsDataclass + AsyncAttrs)
├── repositories/   # Repository classes — all DB queries here
├── services/       # Business logic — calls repositories, no HTTP concerns
├── schemas/        # Pydantic request/response models
├── api/            # FastAPI routers — call services, handle HTTP
├── database.py     # engine + session factory
└── core/           # config, dependencies, security
```

---

### 🎯 Working Code Artefact 4: Testing with aiosqlite

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport #(Asynchronous Server Gateway Interface)
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from models.user import Base
from database import get_db
from main import app

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def db_session():
    """In-memory SQLite database — created fresh for each test function."""
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def client(db_session: AsyncSession):
    """AsyncClient with get_db overridden to use the test SQLite session."""
    async def override_get_db():
        yield db_session

    #(Asynchronous Server Gateway Interface)
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

```python
# tests/test_users.py
import pytest
from httpx import AsyncClient
from unittest.mock import patch


async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/v1/users/",
        json={"name": "Qasir", "email": "q@example.com", "role": "user"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "q@example.com"
    assert data["role"] == "user"
    assert "id" in data
    assert "password" not in data


async def test_get_user(client: AsyncClient):
    create = await client.post(
        "/v1/users/", json={"name": "Qasir", "email": "q@example.com", "role": "user"}
    )
    user_id = create.json()["id"]
    response = await client.get(f"/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id


async def test_get_user_not_found(client: AsyncClient):
    response = await client.get("/v1/users/99999")
    assert response.status_code == 404


async def test_list_users(client: AsyncClient):
    await client.post("/v1/users/", json={"name": "A", "email": "a@example.com", "role": "user"})
    await client.post("/v1/users/", json={"name": "B", "email": "b@example.com", "role": "admin"})
    response = await client.get("/v1/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_list_users_role_filter(client: AsyncClient):
    await client.post("/v1/users/", json={"name": "Admin", "email": "admin@example.com", "role": "admin"})
    await client.post("/v1/users/", json={"name": "User", "email": "user@example.com", "role": "user"})
    response = await client.get("/v1/users/?role=admin")
    assert response.status_code == 200
    assert all(u["role"] == "admin" for u in response.json())


async def test_patch_user_partial_update(client: AsyncClient):
    create = await client.post(
        "/v1/users/", json={"name": "Original", "email": "orig@example.com", "role": "user"}
    )
    user_id = create.json()["id"]
    response = await client.patch(f"/v1/users/{user_id}", json={"name": "Updated"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"
    assert response.json()["email"] == "orig@example.com"


async def test_soft_delete_returns_404_on_get(client: AsyncClient):
    create = await client.post(
        "/v1/users/", json={"name": "ToDelete", "email": "del@example.com", "role": "user"}
    )
    user_id = create.json()["id"]
    delete_response = await client.delete(f"/v1/users/{user_id}")
    assert delete_response.status_code == 204
    get_response = await client.get(f"/v1/users/{user_id}")
    assert get_response.status_code == 404


async def test_soft_delete_excluded_from_list(client: AsyncClient):
    create = await client.post(
        "/v1/users/", json={"name": "ToDelete", "email": "del2@example.com", "role": "user"}
    )
    user_id = create.json()["id"]
    await client.delete(f"/v1/users/{user_id}")
    response = await client.get("/v1/users/")
    assert all(u["id"] != user_id for u in response.json())


async def test_duplicate_email_returns_409(client: AsyncClient):
    payload = {"name": "Dup", "email": "dup@example.com", "role": "user"}
    await client.post("/v1/users/", json=payload)
    response = await client.post("/v1/users/", json=payload)
    assert response.status_code == 409
    assert "already registered" in response.json()["detail"]


async def test_create_user_triggers_background_email(client: AsyncClient):
    with patch("routers.users._send_welcome_email") as mock_email:
        response = await client.post(
            "/v1/users/", json={"name": "Qasir", "email": "bg@example.com", "role": "user"}
        )
    assert response.status_code == 201
    mock_email.assert_called_once_with("bg@example.com")


async def test_list_users_pagination(client: AsyncClient):
    for i in range(5):
        await client.post(
            "/v1/users/", json={"name": f"User{i}", "email": f"u{i}@example.com", "role": "user"}
        )
    response = await client.get("/v1/users/?skip=2&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2
```

### ✅ Key Concepts

- **`aiosqlite` in-memory** replaces PostgreSQL in tests — no Docker, no network, fast CI
- **`dependency_overrides`** injects the test session into every route cleanly — no monkey-patching the ORM
- **`asyncio_mode = "auto"`** removes `@pytest.mark.asyncio` from every test — set it once in `pyproject.toml`
- **`ASGITransport`** routes requests through the ASGI app directly — no network socket, deterministic, fast
- **`dependency_overrides.clear()`** in fixture teardown prevents test contamination across the suite

### ⚠️ Common Pitfalls

- Not calling `app.dependency_overrides.clear()` in fixture teardown — subsequent tests silently use the wrong session
- Forgetting `Base.metadata.drop_all` in fixture teardown — schema state leaks between test functions
- Using `TestClient` (synchronous) instead of `httpx.AsyncClient` + `ASGITransport` — breaks `async def` test functions
- Setting `asyncio_mode = "auto"` in the wrong section of `pyproject.toml` — must be under `[tool.pytest.ini_options]`

---

## 🖥️ Part 5: Junior → Senior Interview Tier

### Q&A Batch 5: Interview Tier — Junior to Senior

### Junior to Mid-Level (£50k–£70k)

**Q61: Explain the difference between a synchronous and asynchronous database driver in simple terms.**
A: A synchronous driver (like `psycopg2`) makes the server wait for each database response before doing anything else — like a waiter who stands at one table until the kitchen delivers. An async driver (like `asyncpg`) lets the server handle other requests while waiting — like a waiter who puts in one order and serves other tables while the kitchen works.

**Q62: What is an ORM and why use one instead of raw SQL?**
A: An ORM (Object Relational Mapper) maps Python classes to database tables. You write `User(name="x")` and Python generates the SQL. Benefits: type safety, composable queries, database-agnostic code, and automatic protection against SQL injection. Raw SQL is still appropriate for complex analytics queries where the ORM expression builder becomes unwieldy — SQLAlchemy supports both.

**Q63: What is a database migration and why do you need one?**
A: A migration is a versioned script that changes the database schema (adds a column, creates a table). Without migrations, schema changes must be applied manually to every environment — error-prone and unauditable. Migrations are committed to source control and applied in order, guaranteeing that dev, staging, and production all have the same schema.

**Q64: What is `nullable=False` and what happens if you try to insert a row without a required column?**
A: `nullable=False` means the column cannot contain `NULL`. Attempting an INSERT without providing a value raises `IntegrityError` (PostgreSQL error code `23502 — not null violation`). Pydantic validation should catch missing required fields before they reach the database.

**Q65: What is a connection pool in plain terms?**
A: A pre-warmed set of open database connections shared across all requests. Instead of opening a new TCP connection to PostgreSQL for every HTTP request (20–100ms), the app reuses existing ones from the pool, reducing latency and allowing more concurrent load.

### Mid to Senior Level (£70k–£90k)

**Q66: How do you handle database migrations in production with zero downtime?**
A: Three-step deploy for breaking changes: (1) add the new column and deploy code writing to both old and new; (2) backfill; (3) deploy code reading only from the new column, then drop the old column. Use an init container in Kubernetes to run `alembic upgrade head` before app pods start. Always commit migration files to source control.

**Q67: How do you write a repository method that applies optional filters dynamically?**
A: Build the base statement, then conditionally add `.where()` clauses based on which filters are provided — see `get_all()` in Working Code Artefact 2. This pattern composes cleanly and is fully type-safe with mypy.

**Q68: How do you run multiple database operations atomically?**
A: Keep all operations within one `get_db` request scope — the dependency commits at the end if no exception is raised. For complex multi-step operations, use multiple `flush()` calls to get generated IDs, but only one `commit()` via the dependency.

**Q69: What is an index in PostgreSQL and when should you add one in SQLAlchemy?**
A: An index speeds up `WHERE` clause lookups at the cost of additional storage and slower INSERTs. Add `index=True` on `mapped_column` for any column frequently used in `WHERE`, `JOIN`, or `ORDER BY` with high cardinality. The `email` column in a users table is a classic candidate — always queried in login flows, high cardinality, unique.

**Q70: How does Python's GIL affect async SQLAlchemy workloads?**
A: The GIL means only one thread executes Python bytecode at a time. For async SQLAlchemy this is irrelevant — the async event loop is single-threaded by design and the GIL is released during I/O waits. Python 3.14 supports free-threaded builds (PEP 703) where the GIL can be disabled, which benefits CPU-bound multi-threaded code. The free-threaded ecosystem is still evolving — not all C extensions support it yet. Multiprocessing remains the robust approach for CPU-bound parallelism.

### Senior Level (£90k–£130k)

**Q71: How would you design a zero-downtime migration strategy for a column rename?**
A: Three-step process: (1) add the new column, deploy code that writes to both; (2) backfill the new column from the old; (3) deploy code that reads from the new column only, then remove the old column in a subsequent migration. Never rename a column in a single migration in a live system — it breaks any running instance that still references the old name.

**Q72: Explain your approach to testing the repository layer in isolation.**
A: Use `aiosqlite` in-memory with `dependency_overrides` — no mocking of SQLAlchemy itself. Instantiate the repository directly with the test session and call its methods. Assert on the returned ORM objects rather than on SQL calls. This tests real query logic without network overhead.

**Q73: How do you detect slow queries in a FastAPI + async SQLAlchemy application in production?**
A: Use `echo=True` only in development. In production, configure the `pg_stat_statements` extension in PostgreSQL and query it for slow statements. Alternatively, use APM tools (Azure Monitor, Datadog) that instrument the SQLAlchemy connection pool via `event.listen`.

**Q74: How do you structure Alembic migrations in a multi-team monorepo?**
A: Each service owns a distinct table prefix or schema. Configure Alembic `version_table` to a service-specific name (e.g., `users_alembic_version`) so migration histories are independent. Apply migrations per service in CI. Alternatively, adopt a shared migration repository with explicit ownership conventions — though this introduces coordination overhead.

**Q75: What is the difference between `type UserId = int` and `NewType("UserId", int)` — which do you use and when?**
A: PEP 695 `type UserId = int` is transparent — `int` and `UserId` are interchangeable at the type-checker level; use for readability and documentation. `NewType("UserId", int)` creates a nominally distinct type — mypy enforces that user IDs and team IDs cannot be swapped; use when you want that enforcement. Both are fully supported by mypy 1.18+.

---

### 🎯 Working Code Artefact 5: Full Project Structure

```
fastapi-users-api/
├── alembic/
│   ├── env.py                     ← async-patched (NullPool + run_sync)
│   └── versions/
│       └── 0001_create_users_table.py
├── alembic.ini
├── models/
│   └── user.py                    ← 2026 ORM model (AsyncAttrs + MappedAsDataclass)
├── repositories/
│   └── user.py                    ← repository pattern with PEP 695 aliases
├── routers/
│   └── users.py                   ← routes using PEP 695 type aliases
├── schemas/
│   └── user.py                    ← Pydantic schemas (carry-forward from Day 2)
├── tests/
│   ├── conftest.py                ← aiosqlite fixtures + dependency_overrides
│   └── test_users.py              ← 11 test functions, all verbs covered
├── database.py                    ← engine + session factory
├── dependencies.py                ← PEP 695 type aliases for routes
├── config.py                      ← pydantic-settings (includes DATABASE_URL)
├── main.py                        ← app + lifespan
├── docker-compose.yml             ← local PostgreSQL
├── .env
└── pyproject.toml
```

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: password
      POSTGRES_DB: usersdb
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d usersdb"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  pgdata:
```

```bash
# .env
APP_NAME=Users API
APP_VERSION=1.0.0
DEBUG=true
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173"]
DATABASE_URL=postgresql+asyncpg://app:password@localhost/usersdb
```

```python
# config.py
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings class docstring."""
    app_name: str = "Users API"
    app_version: str = "1.0.0"
    debug: bool = False
    allowed_origins: list[str] = ["http://localhost:3000"]
    database_url: str  # required — no default; must be in .env or environment

    model_config = {"env_file": ".env"}


@lru_cache
def get_settings() -> Settings:
    """get_settings function docstring."""
    return Settings()
```

### ✅ Key Concepts

- **Domain-driven folder structure** — `models/`, `repositories/`, `services/`, `schemas/`, `api/` — no SQLAlchemy imports in route handlers
- **`fastapi dev` for development, `fastapi run` for production** — the two commands have different defaults; never use `fastapi dev` in production
- **`DATABASE_URL` never committed** — always read from environment or secrets manager via `pydantic-settings`
- **All migration files committed to source control** — they form the versioned schema history; deleting or modifying committed files breaks the version chain

### ⚠️ Common Pitfalls

- Using `fastapi dev` in a production deployment — it enables hot reload and debug mode, not appropriate for production
- Storing real `DATABASE_URL` in `alembic.ini` or `.env` files that are committed to source control — use secrets management
- Not committing `alembic/versions/` to source control — breaks the migration chain for other team members and CI

---

## 📊 Quick Reference — SQLAlchemy 2.1 Async Patterns

| Task                             | Pattern                                                                         |
| -------------------------------- | ------------------------------------------------------------------------------- |
| Create engine                    | `create_async_engine(url, pool_size=10, pool_pre_ping=True, pool_recycle=3600)` |
| Create session factory           | `async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)`       |
| Yield session in dependency      | `async with AsyncSessionLocal() as session: yield session`                      |
| Single row or None               | `result.scalar_one_or_none()`                                                   |
| All rows as list                 | `result.scalars().all()`                                                        |
| Write then read back id          | `session.add(obj)` → `await session.flush()` → `await session.refresh(obj)`     |
| Filtered query                   | `select(Model).where(Model.col == val).order_by(Model.col.desc()).limit(n)`     |
| Eager load one-to-many           | `.options(selectinload(Model.relationship))`                                    |
| Eager load many-to-one           | `.options(joinedload(Model.relationship))`                                      |
| Query WriteOnlyMapped collection | `select(Child).where(Child.parent_id == id).limit(n)`                           |
| Async lazy access                | `await obj.awaitable_attrs.relationship`                                        |
| PEP 695 domain alias             | `type UserId = int`                                                             |
| PEP 695 dependency alias         | `type UserRepo = Annotated[UserRepository, Depends(get_user_repo)]`             |

### Mental Model Mapping (TypeScript → Python / SQLAlchemy)

| TypeScript                   | Python / SQLAlchemy                     | Notes                 |
| ---------------------------- | --------------------------------------- | --------------------- |
| Prisma `model User`          | `class User(Base)` with `Mapped[]`      | ORM model definition  |
| Prisma Migrate               | Alembic `--autogenerate`                | Schema migration      |
| `userId: number`             | `type UserId = int` (PEP 695)           | Domain type alias     |
| `async function findById`    | `async def get_by_id` in repository     | Async data access     |
| `Promise<User \| null>`      | `User \| None`                          | Nullable async return |
| `new PrismaClient()`         | `create_async_engine(...)`              | DB connection         |
| `prisma.$transaction([...])` | `await session.flush()` + single commit | Atomic operations     |
| `@prisma/client`             | `sqlalchemy[asyncio]` + `asyncpg`       | ORM + driver packages |

---

## 📚 Additional Resources

| Resource                       | URL                                                                                             |
| ------------------------------ | ----------------------------------------------------------------------------------------------- |
| SQLAlchemy 2.0 async docs      | https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html                                   |
| SQLAlchemy `MappedAsDataclass` | https://docs.sqlalchemy.org/en/20/orm/dataclasses.html                                          |
| SQLAlchemy `WriteOnlyMapped`   | https://docs.sqlalchemy.org/en/20/orm/collections.html#write-only-relationships                 |
| SQLAlchemy `AsyncAttrs`        | https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#sqlalchemy.ext.asyncio.AsyncAttrs |
| Alembic documentation          | https://alembic.sqlalchemy.org/en/latest/                                                       |
| Alembic async env.py guide     | https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic               |
| asyncpg documentation          | https://magicstack.github.io/asyncpg/current/                                                   |
| aiosqlite documentation        | https://aiosqlite.omnilib.dev/en/stable/                                                        |
| uv documentation               | https://docs.astral.sh/uv/                                                                      |
| OWASP Top 10                   | https://owasp.org/www-project-top-ten/                                                          |
| PEP 695 — Type Aliases         | https://peps.python.org/pep-0695/                                                               |
| PEP 703 — Free-Threading       | https://peps.python.org/pep-0703/                                                               |

---

## ✅ Today's Deliverable Checklist

By the end of today, you should have:

- [ ] Installed Python 3.14 via `uv python install 3.14` and pinned with `uv python pin 3.14`
- [ ] `docker compose up -d` running a local PostgreSQL 16 instance
- [ ] `pyproject.toml` updated with `requires-python = ">=3.14"`, `ruff>=1.0`, `mypy>=1.18`, `target-version = "py314"`, `python_version = "3.14"`
- [ ] `database.py` with `create_async_engine`, `pool_pre_ping=True`, `pool_recycle=3600`, `async_sessionmaker`, `expire_on_commit=False`
- [ ] `models/user.py` using the 2026 combined base: `AsyncAttrs + MappedAsDataclass + DeclarativeBase` in correct MRO order
- [ ] `User` model with `WriteOnlyMapped[list["AuditLog"]]` and `AuditLog` model registered in `Base.metadata`
- [ ] `is_active: Mapped[bool]` soft-delete column on `User`
- [ ] `repositories/user.py` with PEP 695 `type UserId = int` aliases and all CRUD methods including `soft_delete`
- [ ] `dependencies.py` with `type DBSession` and `type UserRepo` PEP 695 aliases
- [ ] `routers/users.py` using `UserRepo` alias throughout — no raw `Depends()` calls in route signatures
- [ ] `alembic init alembic` run, `env.py` patched with `run_sync`, `NullPool`, and all model imports
- [ ] `alembic revision --autogenerate -m "create users and audit_logs tables"` generates correct DDL — reviewed before applying
- [ ] `alembic upgrade head` applied successfully — `alembic current` shows the new version
- [ ] `tests/conftest.py` with `db_session` and `client` fixtures using `aiosqlite` and `dependency_overrides`
- [ ] `tests/test_users.py` with 11 test functions covering: create, get, not-found, list, role filter, partial update, soft delete (404 + list exclusion), duplicate email 409, background task mock, pagination
- [ ] `uv run pytest --cov=. --cov-fail-under=80` passing
- [ ] `uv run ruff check .` and `uv run mypy .` passing with zero errors
- [ ] `uv run fastapi dev main.py` confirmed for development (hot reload + Swagger at `http://localhost:8000/docs`)
- [ ] `uv run fastapi run main.py` confirmed as the production start command
- [ ] Committed to GitHub as `fastapi-users-api` — Day 3 branch or commit

---

**Next Sprint Day:** Thu 23 Apr — Rest Day

**Following Sprint Day:** Fri 25 Apr (Sprint 2 Day 1) — Authentication with JWT: OAuth2 password flow, hashed passwords with `passlib[bcrypt]`, protected routes, refresh tokens.

---

_This learning material is part of the 2026 Python · Azure · AI Engineering Roadmap targeting UK senior roles (£90k–£130k / £550–£750/day)._
