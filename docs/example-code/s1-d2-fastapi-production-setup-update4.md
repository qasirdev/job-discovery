```
<prompt>
  @jobs-list/2026-python-ai-azure-roadmap-v2.md
go and create file according to @jobs-list/2026-learning-prompt-v3.md in folder learning-sprints for:
- **Tue 21 Apr** — FastAPI Production Setup: `APIRouter`, dependency injection, Pydantic request/response schemas, automatic OpenAPI docs, middleware, CORS, background tasks. Build a `/users` CRUD API with full validation and OpenAPI spec.
</prompt>
```

# Sprint 1 · Day 2 · Tue 21 Apr 2026

**Topic:** FastAPI Production Setup — `APIRouter`, dependency injection, Pydantic request/response schemas, automatic OpenAPI docs, middleware, CORS, background tasks. Build a `/users` CRUD API with full validation and OpenAPI spec.

**Day Type:** 🖥️ Backend

---

## 🎯 Step 1 — Topic Overview, Learning Steps & UK Interview Relevance

### Learning Steps

1. **`APIRouter` and Application Structure** — How to split a FastAPI app into domain-scoped modules. Maps directly to NestJS module organisation. Library: `fastapi` 0.120.x+.

2. **Dependency Injection with `Depends()` and `Annotated`** — The 2026 idiomatic pattern for shared logic (auth, DB sessions, pagination). PEP 593 `Annotated` + PEP 695 `type` aliases are the current standard. Library: `fastapi` 0.95+.

3. **Pydantic v2 Request/Response Schemas** — Separate input and output models, `field_validator`, `model_validator`, `ConfigDict`. Library: `pydantic` 2.11.x+.

4. **`pydantic-settings` Configuration Management** — Env-var config with `.env` file, `lru_cache` for single parse per process. Library: `pydantic-settings` 2.7.x+.

5. **Middleware and CORS** — Cross-cutting request hooks (timing, correlation IDs), CORS policy for Next.js frontend clients, OWASP A05 security implications.

6. **OpenAPI Documentation** — Auto-generated from type annotations, `generate_unique_id_function` for SDK-friendly operation IDs, disabling docs in production.

7. **Background Tasks** — Fire-and-forget post-response jobs, comparison with task queues.

8. **JWT Authentication with `PyJWT`** — Signed token creation and verification, HS256 vs RS256, `PyJWT` as the 2026 replacement for the unmaintained `python-jose`.

9. **Testing with `pytest-asyncio` and `httpx`** — Async test client, `conftest.py`, `dependency_overrides`, `asyncio_mode = "auto"` configuration.

### 📊 UK Interview Relevance (£90k–£130k / £550–£750/day)

| Area                      | Concept                                            | Interview Type                                            | Frequency |
| ------------------------- | -------------------------------------------------- | --------------------------------------------------------- | --------- |
| `APIRouter`               | Modular route organisation                         | Architecture: "How do you structure a large FastAPI app?" | Very High |
| `Depends()` + `Annotated` | Dependency injection, testability                  | Code review: "How would you refactor this?"               | Very High |
| Pydantic v2               | `field_validator`, `model_validator`, `ConfigDict` | Debugging: "Why is this validation failing?"              | Very High |
| Middleware                | Request lifecycle, correlation IDs                 | System design: "How do you implement observability?"      | High      |
| CORS                      | Allow-list policy, OWASP A05                       | Security: "How do you secure this API?"                   | High      |
| OpenAPI                   | Docs discipline, operation IDs, SDK generation     | Architecture: "How do you document your APIs?"            | High      |
| Background Tasks          | Fire-and-forget vs task queues                     | Design: "How do you handle async side-effects?"           | Medium    |
| JWT / `PyJWT`             | HS256 vs RS256, token lifecycle                    | Security: "Walk me through your auth implementation"      | High      |
| `pytest-asyncio`          | Async test patterns, `dependency_overrides`        | Code review: "How do you test this route?"                | High      |

### ✅ Key 2026 Industry Patterns

- **FastAPI** appears in 24.2% of UK Python job listings — interviewers expect hands-on fluency, not just awareness
- **Pydantic v2** (Rust-compiled core) is 5–50× faster than v1; understanding `model_validator`, discriminated unions, and `ConfigDict` separates mid from senior
- **`Annotated[..., Depends()]`** with PEP 695 `type` aliases is the 2026 idiomatic style — the older `= Depends(fn)` default-value pattern is legacy
- **`python-jose`** is unmaintained (no releases since 2023, open CVEs) — `PyJWT` is the correct 2026 replacement
- **`fastapi[standard]`** bundles `uvicorn[standard]`, `fastapi-cli`, `httpx`, and `email-validator` in one install — the recommended approach from FastAPI 0.111+; `fastapi dev` for development (hot reload), `fastapi run` for production

---

## 📦 Packages

```bash
# --- Using uv (recommended) ---
# Core runtime
uv add "fastapi[standard]" pydantic pydantic-settings PyJWT cryptography

# Dev / test
uv add --dev ruff mypy pytest httpx pytest-cov pytest-asyncio

# --- Using poetry (existing codebases) ---
# poetry add "fastapi[standard]" pydantic pydantic-settings PyJWT cryptography
# poetry add --group dev ruff mypy pytest httpx pytest-cov pytest-asyncio
```

```toml
# pyproject.toml — version pins (May 2026)

# --- uv-managed project (recommended) ---
[project]
requires-python = ">=3.14"
dependencies = [
    "fastapi[standard]>=0.120",
    "pydantic>=2.11",
    "pydantic-settings>=2.7",
    "PyJWT>=2.9",
    "cryptography>=43",
]

[tool.uv]
dev-dependencies = [
    "ruff>=1.0",
    "mypy>=1.18",
    "pytest>=8",
    "httpx>=0.28",
    "pytest-cov>=6",
    "pytest-asyncio>=0.24",
]

# --- poetry equivalent (existing codebases) ---
# [tool.poetry.dependencies]
# python = "^3.14"
# fastapi = {version = "^0.120", extras = ["standard"]}
# pydantic = "^2.11"
# pydantic-settings = "^2.7"
# PyJWT = "^2.9"
# cryptography = "^43"
#
# [tool.poetry.group.dev.dependencies]
# ruff = "^1.0"
# mypy = "^1.18"
# pytest = "^8"
# httpx = "^0.28"
# pytest-cov = "^6"
# pytest-asyncio = "^0.24"

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

| Package             | Version (stable May 2026) | Purpose                                                 |
| ------------------- | ------------------------- | ------------------------------------------------------- |
| `fastapi[standard]` | 0.120.x+                  | Framework + uvicorn + fastapi-cli + httpx               |
| `pydantic`          | 2.11.x                    | Validation and serialisation                            |
| `pydantic-settings` | 2.7.x                     | Env-var config management                               |
| `PyJWT`             | 2.9.x                     | JWT encode/decode — replaces unmaintained `python-jose` |
| `cryptography`      | 43.x                      | RS256 key operations (required by PyJWT)                |
| `ruff`              | 1.x                       | Linter + formatter                                      |
| `mypy`              | 1.18.x                    | Static type checker                                     |
| `pytest-asyncio`    | 0.24.x                    | Async test runner                                       |
| `httpx`             | 0.28.x                    | Async test client for FastAPI                           |
| `pytest-cov`        | 6.x                       | Coverage reporting                                      |

---

## 🖥️ Q&A Batch 1 of 6 — `APIRouter` and Application Structure

**Q1: What is `APIRouter` and why should you use it instead of putting all routes on `app`?**

`APIRouter` lets you split routes into separate modules (e.g., `routers/users.py`, `routers/items.py`) and register them on the main `app` with a prefix and tags. This mirrors NestJS module organisation — each router owns its domain. Changes to users routes never touch the items file.

```python
# routers/users.py
from fastapi import APIRouter
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
async def list_users(): ...

# main.py
from routers import users
app.include_router(users.router, prefix="/v1")
```

---

**Q2: How do you apply a common dependency (e.g., auth check) to every route in an `APIRouter`?**

Pass `dependencies=[Depends(verify_token)]` to `APIRouter(...)`. Every route in that router inherits it without repeating the decorator.

```python
router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_api_key)],  # applied to ALL routes in this router
)
```

---

**Q3: What is `tags` in `APIRouter` and why does it matter?**

`tags` groups routes under a named section in the auto-generated OpenAPI/Swagger UI. Without tags, all routes appear in a flat unlabelled list. For teams and API consumers, clear tagging is standard production practice and makes the OpenAPI spec navigable.

---

**Q4: How do you add a version prefix (`/v1`) to all routes without changing each router?**

Pass `prefix="/v1"` when calling `app.include_router(...)`. The router itself does not need to know its version — separation of concerns.

```python
app.include_router(users_router, prefix="/v1")   # GET /v1/users
app.include_router(items_router, prefix="/v1")   # GET /v1/items
```

---

**Q5: How do you expose a health check endpoint that is excluded from the OpenAPI schema?**

Set `include_in_schema=False` on the route decorator. Useful for internal probes that should not appear in the public API surface.

```python
@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok"}
```

---

**Q6: How do you add multiple routers to an app and give each a different prefix and tag?**

Call `include_router` once per router. Each router carries its own prefix and tags — the app just registers them.

```python
app.include_router(users.router, prefix="/v1")
app.include_router(items.router, prefix="/v1")
app.include_router(admin.router, prefix="/v1/admin", tags=["admin"])
```

---

**Q7: What is the `lifespan` context manager and why does it replace `@app.on_event("startup")`?**

`@app.on_event` is deprecated since FastAPI 0.95. The `lifespan` async context manager handles startup and shutdown in a single function using `yield`. Code before `yield` runs on startup; code after runs on shutdown. It integrates cleanly with `asynccontextmanager`.

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient()  # startup
    yield
    await app.state.http_client.aclose()          # shutdown

app = FastAPI(lifespan=lifespan)
```

---

**Q8: What HTTP status codes should a REST CRUD API return for each operation?**

| Operation              | Success Code     | Common Error Codes         |
| ---------------------- | ---------------- | -------------------------- |
| `GET` single           | `200 OK`         | `404 Not Found`            |
| `GET` list             | `200 OK`         | —                          |
| `POST` create          | `201 Created`    | `422 Unprocessable Entity` |
| `PUT` replace          | `200 OK`         | `404`, `422`               |
| `PATCH` partial update | `200 OK`         | `404`, `422`               |
| `DELETE`               | `204 No Content` | `404`                      |

---

**Q9: What is the difference between `response_model` and the `-> ReturnType` annotation?**

`response_model=UserResponse` tells FastAPI to serialise the return value through that Pydantic model and include it in the OpenAPI schema. The Python `-> ReturnType` annotation is for mypy only — FastAPI ignores it for serialisation. Always set `response_model` explicitly on routes that return DB objects to prevent leaking extra fields.

---

**Q10: What is `response_model_exclude_unset=True` and when is it useful?**

It excludes fields that were not explicitly set (still at their default value). Use it on `PATCH` responses to avoid serialising `null` for every optional field not included in the partial update.

```python
@router.patch("/{user_id}", response_model=UserResponse)
async def patch_user(user_id: int, payload: UserUpdate) -> dict:
    updates = payload.model_dump(exclude_unset=True)  # only fields explicitly sent
    _db[user_id].update(updates)
    return _db[user_id]
```

---

**Q11: How do you version a FastAPI API and what are the trade-offs between URL versioning and header versioning?**

URL versioning (`/v1/users`, `/v2/users`) is explicit, cacheable, and trivial to route in API gateways. Header versioning (`Accept: application/vnd.api+v2+json`) is cleaner conceptually but harder to test in browsers and poorly supported in most gateways. UK enterprise APIs almost universally use URL versioning.

---

**Q12: How do you mark a route as deprecated in the OpenAPI spec without removing it?**

Set `deprecated=True` on the route decorator. The Swagger UI renders it with a strikethrough and a deprecation badge.

```python
@router.get("/old-endpoint", deprecated=True)
async def old_endpoint(): ...
```

---

**Q13: What is the difference between `app.include_router()` and mounting a sub-application with `app.mount()`?**

`include_router` merges routes into the same OpenAPI spec and middleware stack. `mount` attaches a completely separate ASGI (Asynchronous Server Gateway Interface) application — it has its own middleware, error handlers, and is excluded from the parent's OpenAPI docs. Use `mount` for static files or entirely separate services; use `include_router` for everything within the same API domain.

---

**Q14: How do you apply a response header to every route in a router without repeating code?**

Use middleware on the main app or a custom `APIRoute` class. For a simpler case, set headers in a shared dependency that all routes in the router include.

---

**Q15: What is `generate_unique_id_function` and why does it matter for SDK generation?**

FastAPI's default operation IDs look like `list_users_v1_users_get` — when you generate a TypeScript or Python SDK from the spec, these become method names. `generate_unique_id_function` lets you produce clean IDs like `users:list-users`. Interviewers at API-platform companies recognise this as a production concern.

```python
from fastapi.routing import APIRoute

def custom_operation_id(route: APIRoute) -> str:
    """custom_operation_id function docstring."""
    tag = route.tags[0].lower().replace(" ", "_") if route.tags else "api"
    name = route.name.replace("_", "-")
    return f"{tag}:{name}"

app = FastAPI(generate_unique_id_function=custom_operation_id)
```

| Route                   | Default operationId                | Custom operationId  |
| ----------------------- | ---------------------------------- | ------------------- |
| `GET /v1/users`         | `list_users_v1_users_get`          | `users:list-users`  |
| `POST /v1/users`        | `create_user_v1_users_post`        | `users:create-user` |
| `DELETE /v1/users/{id}` | `delete_user_v1_users__id__delete` | `users:delete-user` |

---

## 🖥️ Q&A Batch 2 of 6 — Dependency Injection and `Annotated` Patterns

**Q16: Explain FastAPI's `Depends()` — how does it differ from manual imports?**

`Depends()` tells FastAPI to resolve a callable before executing the route. It supports async, request-scoped caching, and clean override in tests. Manual imports create tight coupling; `Depends()` allows injecting a mock in tests via `app.dependency_overrides`.

```python
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

@router.get("/{user_id}")
async def get_user(user_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    ...
```

---

**Q17: What is `Annotated` and why did FastAPI adopt it as the preferred dependency style?**

`Annotated[Type, metadata]` is a standard Python construct (PEP 593, Python 3.9+) that attaches metadata to a type hint without changing the type itself. FastAPI reads `Depends()`, `Query()`, `Path()`, `Body()`, and `Header()` from the metadata slot. It is preferred over `= Depends(fn)` because it works better with mypy, IDEs, and OpenAPI generation — the type and the DI declaration stay together.

---

**Q18: What is the PEP 695 `type` keyword and how does it apply to FastAPI dependency aliases?**

PEP 695 (Python 3.12, standard in 3.14) introduced the `type` statement as the language-native way to declare type aliases — replacing bare assignment (`X = Annotated[...]`) and the deprecated `typing.TypeAlias`. The `type` keyword evaluates lazily (safe for forward references), requires no import, and is fully supported by mypy, pyright, and ruff.

```python
# dependencies.py — PEP 695 throughout (Python 3.14)
from typing import Annotated
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

type DBSession   = Annotated[AsyncSession, Depends(get_db)]
type CurrentUser = Annotated[str, Depends(get_current_user_id)]
type PageSkip    = Annotated[int, Query(ge=0, description="Items to skip")]
type PageLimit   = Annotated[int, Query(ge=1, le=100, description="Items per page")]

# ❌ Pre-3.12 styles — legacy, avoid in new code
# DBSession = Annotated[AsyncSession, Depends(get_db)]          # bare assignment
# DBSession: TypeAlias = Annotated[AsyncSession, Depends(get_db)] # typing.TypeAlias
```

---

**Q19: What is the difference between `HS256` and `RS256` styles in DI-resolved JWTs, and when do you use each?**

This is covered in detail in the JWT batch — see Q46.

---

**Q20: What is `dependency_overrides` and when would you use it in tests?**

`app.dependency_overrides[get_db] = get_test_db` replaces a dependency for the duration of a test. This lets you swap a real database session for an in-memory one without touching production code.

```python
# conftest.py
def override_get_db():
    """override_get_db function docstring."""
    yield fake_session

app.dependency_overrides[get_db] = override_get_db
```

---

**Q21: Can `Depends()` be used for more than auth? Give two production examples.**

Yes. Beyond auth:

1. **Database session injection** — every route gets a scoped session, closed after the response
2. **Pagination parameters** — a shared `PaginationParams` dependency avoids repeating `skip: int, limit: int` on every list endpoint

```python
class PaginationParams:
    """PaginationParams class docstring."""
    def __init__(self, skip: int = 0, limit: int = Query(20, le=100)):
        """__init__ method docstring."""
        self.skip = skip
        self.limit = limit

@router.get("/")
async def list_users(pagination: Annotated[PaginationParams, Depends()]) -> list[dict]:
    return list(_db.values())[pagination.skip : pagination.skip + pagination.limit]
```

---

**Q22: What is request-scoped vs application-scoped objects in FastAPI?**

Application-scoped objects (HTTP client, connection pool, ML model) are created once at startup via `lifespan` and shared across all requests. Request-scoped objects (DB session, current user) are created per-request via `Depends()` and cleaned up after the response. Sharing a request-scoped object at app level is a common source of data corruption bugs.

---

**Q23: What happens if you use `Annotated` with both a `Depends` and a default value?**

The default value goes on the parameter, not inside `Annotated`. The `Annotated` slot holds FastAPI metadata; the `= default` on the parameter is the fallback if the query parameter is absent.

```python
# ✅ Correct — default on the parameter
async def endpoint(limit: Annotated[int, Query(ge=1)] = 20): ...

# ❌ Wrong — default inside Annotated is ignored by FastAPI
async def endpoint(limit: Annotated[int, Query(ge=1, default=20)]): ...
```

---

**Q24: How do you chain dependencies — for example, `require_admin` that depends on `get_current_user`?**

Return a value from the inner dependency and accept it as a parameter in the outer one. FastAPI resolves the chain automatically, caching each dependency once per request.

```python
async def get_current_user(user_id: CurrentUser) -> dict:
    return _db.get(user_id) or raise_401()

async def require_admin(user: Annotated[dict, Depends(get_current_user)]) -> dict:
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user
```

---

**Q25: What is `Annotated` vs `Optional` for nullable query parameters?**

Use `Annotated[str | None, Query()] = None` for an optional query parameter. The `Optional[str]` alias (`Union[str, None]`) is equivalent but `str | None` is the modern 3.10+ syntax.

```python
@router.get("/")
async def list_users(role: Annotated[str | None, Query()] = None) -> list[dict]:
    if role:
        return [u for u in _db.values() if u["role"] == role]
    return list(_db.values())
```

---

**Q26: How do you inject settings into a route using `Depends` instead of a global import?**

Wrap `get_settings` in `Depends()`. This makes settings mockable in tests and avoids module-level global state.

```python
type AppSettings = Annotated[Settings, Depends(get_settings)]

@app.get("/health")
async def health(settings: AppSettings) -> dict:
    return {"app": settings.app_name, "version": settings.app_version}
```

---

**Q27: Can a class be used as a FastAPI dependency? What pattern does this enable?**

Yes — FastAPI calls the class's `__init__` as the dependency function. This enables parameterised dependencies that behave like factories.

```python
class RoleChecker:
    """RoleChecker class docstring."""
    def __init__(self, allowed_roles: list[str]):
        """__init__ method docstring."""
        self.allowed_roles = allowed_roles

    def __call__(self, user: CurrentUser) -> None:
        """__call__ method docstring."""
        if user["role"] not in self.allowed_roles:
            raise HTTPException(status_code=403)

require_admin = Depends(RoleChecker(["admin"]))
require_editor = Depends(RoleChecker(["admin", "editor"]))
```

---

**Q28: What is the difference between `yield` and `return` in a dependency?**

A `yield` dependency runs code before the route (setup) and after the response (teardown). A `return` dependency only runs setup. Use `yield` for resource management — database sessions, file handles, locks.

```python
async def get_db():
    async with SessionLocal() as session:
        yield session   # session available to route
        # session closed here after response
```

---

**Q29: How do you apply a dependency to every route in the app, not just one router?**

Pass `dependencies=[Depends(fn)]` to `FastAPI(...)` directly.

```python
app = FastAPI(dependencies=[Depends(verify_rate_limit)])
```

---

**Q30: What is the `use_cache` parameter on `Depends()` and when would you set it to `False`?**

By default, FastAPI resolves each dependency once per request and caches the result. Set `use_cache=False` if you need a fresh instance per injection point — for example, two separate DB sessions within one request.

```python
async def get_db_fresh() -> AsyncSession:
    ...

@router.get("/")
async def endpoint(
    db1: Annotated[AsyncSession, Depends(get_db_fresh, use_cache=False)],
    db2: Annotated[AsyncSession, Depends(get_db_fresh, use_cache=False)],
): ...
```

---

## 🖥️ Q&A Batch 3 of 6 — Pydantic v2 Schemas

**Q31: What changed between Pydantic v1 and v2 that matters in interviews?**

v2 is a Rust-compiled rewrite — roughly 5–50× faster validation. Key API changes:

| v1 (legacy)       | v2 (current)                                      |
| ----------------- | ------------------------------------------------- |
| `@validator`      | `@field_validator`                                |
| `orm_mode = True` | `model_config = ConfigDict(from_attributes=True)` |
| `.dict()`         | `.model_dump()`                                   |
| `.json()`         | `.model_dump_json()`                              |
| `__fields__`      | `model_fields`                                    |

Interviewers at Python-heavy shops will test which version you have used. Saying `.dict()` in 2026 is a red flag.

---

**Q32: What is the difference between a request schema and a response schema, and why should they be separate?**

Request schemas validate incoming data — they are strict, never include `id` or `created_at`, and may include write-only fields like `password`. Response schemas control outbound serialisation — they exclude passwords, include computed fields. Mixing them forces awkward `Optional` hacks and risks leaking internal data.

```python
class UserCreate(BaseModel):       # request — no id, no created_at
    """UserCreate class docstring."""
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):     # response — no password
    """UserResponse class docstring."""
    id: int
    name: str
    email: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
```

---

**Q33: How do you validate a single field with a custom rule in Pydantic v2?**

Use `@field_validator`. Return the value if valid, raise `ValueError` if not. The validator runs after type coercion, so `v` is already the correct Python type.

```python
from pydantic import field_validator

class UserCreate(BaseModel):
    """UserCreate class docstring."""
    name: str
    email: EmailStr

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        """name_not_empty method docstring."""
        v = v.strip()
        if not v:
            raise ValueError("Name must not be blank")
        return v
```

---

**Q34: What is `model_validator` and when do you use it over `field_validator`?**

`field_validator` validates one field in isolation. `model_validator(mode="after")` runs after all fields are validated and receives the fully constructed model — use it when validation spans multiple fields (e.g., end date must be after start date).

```python
from pydantic import model_validator

class DateRange(BaseModel):
    """DateRange class docstring."""
    start: date
    end: date

    @model_validator(mode="after")
    def end_after_start(self) -> "DateRange":
        """end_after_start method docstring."""
        if self.end <= self.start:
            raise ValueError("end must be after start")
        return self
```

---

**Q35: What is `model_config = ConfigDict(from_attributes=True)` and when is it required?**

It tells Pydantic to read attributes from ORM objects (e.g., SQLAlchemy models) rather than requiring a plain dict. Without it, passing a SQLAlchemy row to a Pydantic model raises a validation error. Required on every response schema that maps from a DB model.

---

**Q36: What is `model_dump(exclude_unset=True)` and when do you use it?**

It returns only the fields that were explicitly provided in the request — fields at their default values are omitted. Critical in `PATCH` handlers to avoid overwriting existing data with `None`.

```python
@router.patch("/{user_id}", response_model=UserResponse)
async def patch_user(user_id: int, payload: UserUpdate) -> dict:
    updates = payload.model_dump(exclude_unset=True)  # only what the client sent
    _db[user_id].update(updates)
    return _db[user_id]
```

---

**Q37: How do you define a partial update schema (for `PATCH`) in Pydantic v2?**

Make all fields `Optional` with a default of `None`. Combine with `exclude_unset=True` when dumping to apply only the provided fields.

```python
class UserUpdate(BaseModel):
    """UserUpdate class docstring."""
    name: str | None = None
    email: EmailStr | None = None
    role: str | None = None
```

---

**Q38: What is `EmailStr` and what package provides it?**

`EmailStr` is a Pydantic string type that validates email format using the `email-validator` library. Pydantic raises a `ValidationError` if the value is not a valid email address. It is included when you install `fastapi[standard]`.

---

**Q39: How do you add a field alias in Pydantic v2 — e.g., to accept `user_id` from JSON but store it as `id`?**

Use `Field(alias="user_id")` and set `populate_by_name=True` in `ConfigDict` if you also want the Python attribute name to work.

```python
from pydantic import Field, ConfigDict

class UserResponse(BaseModel):
    """UserResponse class docstring."""
    id: int = Field(alias="user_id")
    model_config = ConfigDict(populate_by_name=True)
```

---

**Q40: What is `422 Unprocessable Entity` and when does FastAPI return it automatically?**

FastAPI returns `422` when a request fails Pydantic validation — wrong type, missing required field, or a custom validator raises `ValueError`. The response body includes a structured `detail` array with field path and message for every error. This is a free feature — no manual validation code required.

---

**Q41: How do you create a discriminated union in Pydantic v2?**

Use a `Literal` type field as the discriminator. Pydantic uses it to select the correct model during validation — essential for polymorphic payloads (e.g., different notification types).

```python
from typing import Literal
from pydantic import BaseModel

class EmailNotification(BaseModel):
    """EmailNotification class docstring."""
    type: Literal["email"]
    address: str

class SMSNotification(BaseModel):
    """SMSNotification class docstring."""
    type: Literal["sms"]
    phone: str

Notification = EmailNotification | SMSNotification

class Event(BaseModel):
    """Event class docstring."""
    notification: Notification
```

---

**Q42: What is the difference between `HTTPException` and a custom exception handler?**

`HTTPException` is the quick idiomatic path for error responses. For complex applications, define custom exception classes and register `@app.exception_handler(MyError)` handlers — this enables RFC 7807 structured error bodies and centralises error formatting.

```python
class UserNotFoundError(Exception):
    """UserNotFoundError class docstring."""
    def __init__(self, user_id: int):
        """__init__ method docstring."""
        self.user_id = user_id

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"type": "user_not_found", "user_id": exc.user_id},
    )
```

---

**Q43: What is OWASP A03 (Injection) and how does Pydantic help prevent it?**

OWASP A03 covers SQL injection, command injection, and similar attacks where untrusted input is executed as code. Pydantic validates and coerces all incoming data before it reaches business logic — a field typed as `int` will never pass a SQL injection string through. Combine with parameterised SQLAlchemy queries for full protection.

---

**Q44: How do you serialise a Pydantic model to JSON with custom field exclusions?**

Use `model_dump(exclude={"password", "internal_token"})` before passing to a response, or configure `response_model_exclude` on the route.

```python
@router.get("/{user_id}", response_model=UserResponse, response_model_exclude={"role"})
async def get_user(user_id: int) -> dict: ...
```

---

**Q45: What is `pydantic-settings` and how do you use it for multi-environment config?**

`pydantic-settings` provides `BaseSettings` — a Pydantic model that reads its field values from environment variables and `.env` files. Wrap the factory in `lru_cache` so the file is read once per process.

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Settings class docstring."""
    app_name: str = "Users API"
    app_version: str = "1.0.0"
    debug: bool = False
    allowed_origins: list[str] = ["http://localhost:3000"]
    model_config = {"env_file": ".env"}

@lru_cache
def get_settings() -> Settings:
    """get_settings function docstring."""
    return Settings()
```

---

## 🖥️ Q&A Batch 4 of 6 — Middleware, CORS, OpenAPI, Background Tasks

**Q46: What is middleware in FastAPI and how does it differ from a dependency?**

Middleware wraps every request/response passing through the app — it runs before routing. A dependency is route-scoped and resolved after routing. Use middleware for cross-cutting concerns (request timing, correlation IDs, security headers); use dependencies for per-route logic (auth, DB session).

```python
@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["X-Process-Time-Ms"] = str(round((time.perf_counter() - start) * 1000, 2))
    return response
```

---

**Q47: How do you add a request correlation ID to every log entry in FastAPI?**

Generate a UUID in middleware, store it in a `contextvars.ContextVar`, and read it in your structlog logger. This is a standard production observability pattern.

```python
import uuid, contextvars

request_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar("request_id")

@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    rid = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request_id_ctx.set(rid)
    response = await call_next(request)
    response.headers["X-Request-ID"] = rid
    return response
```

---

**Q48: What is CORS (Cross-Origin Resource Sharing) and why does a FastAPI backend need to configure it?**

CORS is a browser security mechanism that blocks JavaScript on `domain-a.com` from calling APIs on `domain-b.com` unless the server explicitly permits it via `Access-Control-Allow-Origin` headers. Without CORS middleware, Next.js frontend requests will be blocked in production.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,  # never use ["*"] in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key"],
)
```

⚠️ `allow_origins=["*"]` with `allow_credentials=True` is rejected by browsers and is an OWASP A05 Security Misconfiguration.

---

**Q49: What is a CORS preflight request and when does the browser send one?**

Before a non-simple request (e.g., `PUT` with a custom `Authorization` header), the browser sends an `OPTIONS` request to check permissions. The server must respond with the correct `Access-Control-Allow-*` headers. FastAPI's `CORSMiddleware` handles this automatically.

---

**Q50: Why should OpenAPI docs be disabled in production, and how do you do that in FastAPI?**

Docs expose your full API surface — endpoint paths, parameter names, authentication schemes. An attacker can use this to map attack vectors. Disable with `docs_url=None, redoc_url=None, openapi_url=None`. Note: hiding the UI but leaving `openapi_url` enabled still exposes the full schema to anyone who knows the URL.

```python
app = FastAPI(
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
)
```

---

**Q51: What are FastAPI `BackgroundTasks` and when should you use them vs a task queue like Celery or ARQ?**

`BackgroundTasks` run after the HTTP response is sent — ideal for lightweight fire-and-forget work (welcome email, audit log entry). Use Celery or ARQ for heavy, retryable, scheduled, or distributed work. `BackgroundTasks` share the same process and have no retry mechanism, timeout, or failure handling.

```python
from fastapi import BackgroundTasks

def send_welcome_email(email: str) -> None:
    """send_welcome_email function docstring."""
    print(f"[background] Sending welcome email to {email}")

@router.post("/", status_code=201)
async def create_user(payload: UserCreate, background_tasks: BackgroundTasks) -> dict:
    user = _create(payload)
    background_tasks.add_task(send_welcome_email, payload.email)
    return user
```

---

**Q52: What is the difference between `async def` and `def` route handlers in FastAPI?**

`async def` routes run on the main async event loop — never block with `time.sleep()` or sync I/O here. `def` routes run in a thread pool executor (FastAPI handles this automatically), making them safe for synchronous libraries. Use `async def` for async database calls, `httpx.AsyncClient`, and anything `await`-able.

---

**Q53: What is `lru_cache` and why is it used with `get_settings()`?**

`lru_cache` (Least Recently Used cache) memoises a function's return value. For settings, it means the `.env` file is parsed exactly once per process, not on every request. Without it, every dependency invocation re-reads the environment.

---

**Q54: How do you add security headers (e.g., `X-Content-Type-Options`) to every response?**

Use middleware to set the headers on the response object before returning it.

```python
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

---

**Q55: What is `fastapi-cli` and why is `fastapi dev main.py` preferred over `uvicorn main:app --reload`?**

`fastapi-cli` is bundled with `fastapi[standard]` since FastAPI 0.111. `fastapi dev main.py` wraps `uvicorn` with sensible development defaults (auto-reload via `watchfiles`, structured output) and is the officially recommended dev runner. `fastapi run main.py` is the production equivalent — no hot reload, optimal worker configuration.

```bash
fastapi dev main.py    # development — auto-reload, Swagger UI at /docs
fastapi run main.py    # production — no reload, optimised for throughput
```

> Do not use `fastapi dev` in production environments. The hot-reload watcher adds overhead and the development defaults are not tuned for production throughput.

---

**Q56: How does FastAPI generate OpenAPI docs automatically?**

FastAPI inspects route function signatures, type annotations, and Pydantic models at startup to build a JSON schema at `/openapi.json`. Swagger UI (`/docs`) and ReDoc (`/redoc`) read that schema. Customise at the `FastAPI()` constructor level with `title`, `description`, `version`, and per-route with `summary`, `description`, `response_description`.

---

**Q57: What is `lru_cache` vs `functools.cache` — which should you use in 2026?**

`functools.cache` (Python 3.9+) is an unbounded shorthand for `lru_cache(maxsize=None)`. For settings factories that are called once, either works. Use `lru_cache` when you want a bounded cache size; use `cache` for unlimited memoisation of pure functions.

---

**Q58: What is OWASP A05 (Security Misconfiguration) in the context of CORS?**

OWASP A05 covers misconfigured permissions and policies. Setting `allow_origins=["*"]` with `allow_credentials=True` is a textbook A05 misconfiguration — browsers reject it, and it signals that any origin can send credentialed requests. Always read allowed origins from environment config, never hardcode them.

---

**Q59: How do you handle async vs sync background tasks correctly in FastAPI?**

`BackgroundTasks.add_task()` accepts both sync and async functions. FastAPI runs sync tasks in a thread pool executor automatically. Prefer `async def` for I/O-bound background work to avoid blocking the executor pool.

---

**Q60: What is `contextvars.ContextVar` and why is it safe for async code?**

`ContextVar` stores values that are local to the current async task — unlike a global variable, each concurrent coroutine gets its own isolated copy. This makes it safe for storing per-request data (correlation IDs, user context) in async FastAPI middleware without risk of cross-request contamination.

---

## 🖥️ Q&A Batch 5 of 6 — JWT Authentication with `PyJWT`

**Q61: Why is `python-jose` no longer recommended in 2026?**

`python-jose` has had no meaningful maintenance since mid-2023, has open CVEs, and is incompatible with `cryptography >= 42`. `PyJWT` is actively maintained, has a clean Pythonic API, and is the correct 2026 replacement. Using `python-jose` in a code review or interview signals stale dependency knowledge.

---

**Q62: What is the difference between `HS256` and `RS256` in JWTs, and which should you use?**

`HS256` (HMAC SHA-256) uses a single shared secret — simple but requires every service that verifies tokens to know the secret. `RS256` uses an asymmetric key pair — the private key signs, the public key verifies. Use `RS256` in production microservice architectures where multiple services verify tokens without access to the signing key. Use `HS256` only for single-service or development setups.

```python
# RS256 with PyJWT — production pattern
import jwt
from pathlib import Path

private_key = Path("private.pem").read_bytes()
public_key  = Path("public.pem").read_bytes()

token = jwt.encode({"sub": "user-123"}, private_key, algorithm="RS256")
decoded = jwt.decode(token, public_key, algorithms=["RS256"])
```

---

**Q63: How do you create and verify a JWT using `PyJWT`?**

```python
from datetime import datetime, timedelta, timezone
from typing import Any
import jwt

SECRET_KEY = "replace-with-env-var"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(subject: str | int, extra: dict[str, Any] | None = None) -> str:
    """create_access_token function docstring."""
    payload: dict[str, Any] = {
        "sub": str(subject),
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """Raises jwt.ExpiredSignatureError or jwt.InvalidTokenError on failure."""
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

---

**Q64: What is `jwt.ExpiredSignatureError` and how should it be handled?**

It is raised by `PyJWT` when the `exp` claim is in the past. Always catch it separately from `jwt.InvalidTokenError` and return a distinct `401` response — this allows the client to distinguish between an expired token (trigger a refresh flow) and a completely invalid one (force re-login).

---

**Q65: How do you extract a JWT from an `Authorization: Bearer <token>` header in FastAPI?**

```python
from typing import Annotated
import jwt
from fastapi import Header, HTTPException, status

async def get_current_user_id(authorization: Annotated[str, Header()] = "") -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Missing or malformed Authorization header")
    token = authorization.removeprefix("Bearer ")
    try:
        payload = decode_access_token(token)
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
```

---

**Q66: What JWT claims are considered standard and what do they mean?**

| Claim | Name       | Meaning                                         |
| ----- | ---------- | ----------------------------------------------- |
| `sub` | Subject    | The user or entity the token represents         |
| `iat` | Issued At  | Unix timestamp when the token was created       |
| `exp` | Expiration | Unix timestamp after which the token is invalid |
| `iss` | Issuer     | The authority that created the token            |
| `aud` | Audience   | The intended recipient service                  |
| `jti` | JWT ID     | Unique token identifier, used for revocation    |

---

**Q67: What is `PyJWT` vs `authlib` — when would you choose each?**

| Library   | Use When                                                                                             |
| --------- | ---------------------------------------------------------------------------------------------------- |
| `PyJWT`   | You need straightforward JWT encode/decode with RS256 or HS256                                       |
| `authlib` | You need full OAuth2 / OpenID Connect flows (PKCE, token introspection, dynamic client registration) |

For a FastAPI CRUD API, `PyJWT` is sufficient. `authlib` becomes relevant in Sprint 2 when implementing a full OAuth2 password or PKCE flow.

---

**Q68: What is the Global Interpreter Lock (GIL) and does it affect FastAPI performance?**

The Global Interpreter Lock (GIL) is a mutex in CPython that allows only one thread to execute Python bytecode at a time. For FastAPI this matters less than it might seem — FastAPI runs on an async event loop (`asyncio`) which is single-threaded by design; coroutines yield at `await` points rather than relying on threads. CPU-bound work (ML inference, image processing) does block the GIL and should be offloaded to a `ProcessPoolExecutor` or a dedicated worker service. Python 3.14 supports free-threaded builds (PEP 703), removing the GIL for CPU-bound parallel workloads. Free-threaded mode is still maturing across the ecosystem; multiprocessing remains the safe default for CPU-bound work until library support is universal.

---

**Q69: How do you store secrets (JWT secret key, DB password) securely in a FastAPI project?**

Never hardcode secrets in source code. Read them from environment variables via `pydantic-settings`. In production, inject them from Azure Key Vault, AWS Secrets Manager, or Kubernetes Secrets mounted as environment variables. The `.env` file is for local development only and must be in `.gitignore`.

---

**Q70: What is token revocation and how do you implement it with JWTs?**

JWTs are stateless — once issued, they are valid until expiry. Revocation requires maintaining a server-side blocklist of revoked `jti` claims in Redis or a DB. On every request, check the token's `jti` against the blocklist before accepting it. Alternatively, use short expiry times (15 minutes) combined with refresh tokens.

---

**Q71: How do you rotate JWT signing keys without logging out all users?**

Use key versioning — embed a `kid` (key ID) claim in the token header. Maintain a JWKS (JSON Web Key Set) endpoint with all current and recently retired public keys. Verifiers look up the correct key by `kid`. This is the pattern used by all major identity providers.

---

**Q72: What is OWASP A02 (Cryptographic Failures) in the context of JWT?**

OWASP A02 covers weak or misapplied cryptography. JWT-specific failures include: using `algorithm="none"` (no signature), accepting multiple algorithms without an explicit allowlist, using short or low-entropy secrets for `HS256`, storing raw JWTs in `localStorage` instead of `HttpOnly` cookies.

---

**Q73: What is `algorithm=["HS256"]` (a list) vs `algorithm="HS256"` (a string) in `jwt.decode()`?**

`jwt.decode()` requires `algorithms` (plural) as a list — this is a security measure. Passing a list forces you to explicitly allowlist accepted algorithms. If you pass a string, `PyJWT` raises a `DecodeError`. This prevents algorithm confusion attacks (e.g., an attacker switching a token from `RS256` to `HS256` to forge signatures using the public key as the HMAC secret).

---

**Q74: What is an algorithm confusion attack in JWT and how does `PyJWT` mitigate it?**

An algorithm confusion attack occurs when an RS256 token is modified to declare `alg: HS256` and re-signed using the server's public key as the HMAC secret (which is public knowledge). By requiring an explicit `algorithms=["RS256"]` allowlist in `jwt.decode()`, `PyJWT` rejects any token claiming a different algorithm — the public key cannot be used as an HMAC secret.

---

**Q75: How do you write a pytest fixture that provides a valid JWT for authenticated route tests?**

```python
# conftest.py
import pytest
from auth.jwt import create_access_token

@pytest.fixture
def auth_token() -> str:
    """auth_token function docstring."""
    return create_access_token(subject="test-user-1")

@pytest.fixture
def auth_headers(auth_token: str) -> dict[str, str]:
    """auth_headers function docstring."""
    return {"Authorization": f"Bearer {auth_token}"}
```

---

## 🖥️ Q&A Batch 6 of 6 — Testing, Junior → Senior Interview Tier

### Junior to Mid-Level (£50k–£70k)

**Q76: What is `pytest-asyncio` and why is it needed for testing FastAPI routes?**

`pytest-asyncio` is a pytest plugin that allows test functions to be declared `async def` and runs them on an event loop. Without it, pytest cannot `await` async test helpers or `AsyncClient` calls. Configure `asyncio_mode = "auto"` in `pyproject.toml` to avoid decorating every async test individually.

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
```

---

**Q77: How do you write a basic integration test for a FastAPI `POST` endpoint?**

```python
# tests/test_users.py
import pytest
from httpx import AsyncClient, ASGITransport #(Asynchronous Server Gateway Interface)
from main import app

@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

async def test_create_user(async_client: AsyncClient):
    response = await async_client.post(
        "/v1/users",
        json={"name": "Qasir", "email": "q@example.com", "role": "user"},
        headers={"X-API-Key": "dev-key-replace-in-sprint-2"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "q@example.com"
    assert "id" in data
    assert "password" not in data  # response schema must not leak write-only fields
```

---

**Q78: What is `dependency_overrides` and how do you use it to mock auth in tests?**

```python
from main import app
from dependencies import get_current_user_id

def mock_user() -> str:
    """mock_user function docstring."""
    return "test-user-1"

app.dependency_overrides[get_current_user_id] = mock_user
```

---

**Q79: How do you test that a `422` validation error is returned for invalid input?**

```python
async def test_create_user_invalid_email(async_client: AsyncClient):
    response = await async_client.post(
        "/v1/users",
        json={"name": "Qasir", "email": "not-an-email"},
        headers={"X-API-Key": "dev-key-replace-in-sprint-2"},
    )
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(e["loc"] == ["body", "email"] for e in errors)
```

---

**Q80: What is `pytest.fixture` and what is the difference between `scope="function"` and `scope="session"`?**

A `fixture` is a reusable setup/teardown function injected into tests. `scope="function"` (default) creates a new instance per test. `scope="session"` creates one instance for the entire test run — use it for expensive resources like DB connections that can be shared safely.

---

**Q81: How do you measure test coverage and what is the minimum acceptable threshold at senior level?**

```bash
# --- Using uv (recommended) ---
uv run pytest --cov=. --cov-report=term-missing --cov-fail-under=80

# --- Using poetry (existing codebases) ---
poetry run pytest --cov=. --cov-report=term-missing --cov-fail-under=80
```

80% is a commonly enforced minimum in UK production codebases. Critical paths (auth, payment, data mutation) should target 95%+.

---

### Mid to Senior Level (£70k–£90k)

**Q82: How do you structure a large FastAPI application — what folder layout do you use?**

Domain-driven structure:

```
app/
├── api/          # routers (route definitions only)
├── services/     # business logic (no HTTP concerns)
├── models/       # SQLAlchemy ORM models (Day 3)
├── schemas/      # Pydantic request/response models
├── db/           # session factory, engine
├── core/         # config, security, dependencies
└── main.py       # app factory
```

Routes call services; services call repositories; repositories call the DB. No business logic in route handlers.

---

**Q83: What is the difference between application-scoped and request-scoped resources?**

Application-scoped: created once in `lifespan`, shared across all requests (HTTP client, ML model, connection pool). Request-scoped: created per request via `Depends()` with `yield`, closed after the response (DB session, user context). Confusing the two causes data corruption — a shared DB session leaks transactions between requests.

---

**Q84: How do you handle async exception propagation in FastAPI middleware?**

Wrap `await call_next(request)` in a `try/except`. If an exception escapes your exception handlers, it surfaces here. Log it with a structured logger, set an appropriate status code, and return a `JSONResponse` — never let raw Python exceptions propagate to the ASGI (Asynchronous Server Gateway Interface) server.

```python
@app.middleware("http")
async def error_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.exception("Unhandled error", path=request.url.path)
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})
```

---

**Q85: What is `conftest.py` and where should it live in a FastAPI test suite?**

`conftest.py` is a pytest file that defines fixtures available to all tests in its directory and subdirectories. Put the `async_client` fixture and `dependency_overrides` setup here — not in individual test files. A root-level `conftest.py` covers the whole project; nested ones scope to their directory.

---

**Q86: How do you test background tasks in FastAPI?**

`BackgroundTasks` run after the response is sent — you cannot await them in a normal test. Patch the task function with `unittest.mock.patch` and assert it was called with the correct arguments.

```python
from unittest.mock import patch

async def test_create_user_sends_email(async_client: AsyncClient):
    with patch("routers.users._send_welcome_email") as mock_email:
        response = await async_client.post("/v1/users", json={...}, headers={...})
    assert response.status_code == 201
    mock_email.assert_called_once_with("q@example.com")
```

---

### Senior Level (£90k–£130k)

**Q87: How would you design a type-safe API client in Python?**

Use Pydantic models for requests/responses, generics for a reusable client, `httpx.AsyncClient` for async calls, retry decorators for transient failures, and structured logging.

```python
from typing import TypeVar
from pydantic import BaseModel
import httpx

T = TypeVar("T", bound=BaseModel)

class ApiClient:
    """ApiClient class docstring."""
    def __init__(self, base_url: str):
        """__init__ method docstring."""
        self._client = httpx.AsyncClient(base_url=base_url)

    async def get(self, path: str, model: type[T]) -> T:
        response = await self._client.get(path)
        response.raise_for_status()
        return model.model_validate(response.json())
```

---

**Q88: Explain your testing strategy for async Python code.**

`pytest-asyncio` with `asyncio_mode = "auto"` for async tests; `httpx.AsyncClient` with `ASGITransport` (Asynchronous Server Gateway Interface) for FastAPI integration tests; `dependency_overrides` for mocking DB and auth; `factory-boy` for test data generation; `unittest.mock.patch` for background tasks and external calls; coverage minimum 80% enforced in CI.

---

**Q89: How do you prevent a secret from being accidentally logged or serialised in Pydantic?**

Override `__repr__` and `__str__` on the field, or use `SecretStr` from Pydantic. `SecretStr` stores the value securely and renders as `'**********'` in logs and repr — the actual value is only accessible via `.get_secret_value()`.

```python
from pydantic import BaseModel, SecretStr

class UserCreate(BaseModel):
    """UserCreate class docstring."""
    email: str
    password: SecretStr  # never appears in logs or model_dump()
```

---

**Q90: How do you approach zero-downtime deployment for a FastAPI API with breaking schema changes?**

Use API versioning (`/v1`, `/v2`) to run old and new versions in parallel. Add fields in a backwards-compatible way first (old clients ignore new fields). Only remove or rename fields in a new version. Keep the old version live until all clients have migrated. Use feature flags or header-based routing in the API gateway during the transition.

---

## 🖥️ Working Code Artefact — `/users` CRUD API

> Self-contained, runnable with `fastapi dev main.py`. Uses an in-memory dict as the data store — Day 3 replaces this with async PostgreSQL.

### Project Structure

```
fastapi-users-api/
├── main.py
├── config.py
├── dependencies.py
├── auth/
│   └── jwt.py
├── routers/
│   └── users.py
├── schemas/
│   └── user.py
├── tests/
│   ├── conftest.py
│   └── test_users.py
├── .env
└── pyproject.toml
```

---

### `config.py`

```python
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings class docstring."""
    app_name: str = "Users API"
    app_version: str = "1.0.0"
    debug: bool = False
    allowed_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env"}

# Least Recently Used cache
@lru_cache
def get_settings() -> Settings:
    """get_settings function docstring."""
    return Settings()
```

---

### `schemas/user.py`

```python
from datetime import datetime
from pydantic import BaseModel, EmailStr, SecretStr, field_validator, ConfigDict


class UserCreate(BaseModel):
    """Request schema — no id, no timestamps, password stored as SecretStr."""
    name: str
    email: EmailStr
    password: SecretStr
    role: str = "user"

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        """name_not_empty method docstring."""
        v = v.strip()
        if not v:
            raise ValueError("Name must not be blank")
        return v

    @field_validator("role")
    @classmethod
    def valid_role(cls, v: str) -> str:
        """valid_role method docstring."""
        if v not in {"user", "admin"}:
            raise ValueError("role must be 'user' or 'admin'")
        return v


class UserUpdate(BaseModel):
    """Partial update schema — all fields optional for PATCH support."""
    name: str | None = None
    email: EmailStr | None = None
    role: str | None = None


class UserResponse(BaseModel):
    """Response schema — never exposes password or internal fields."""
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

---

### `auth/jwt.py`

```python
from datetime import datetime, timedelta, timezone
from typing import Any
import jwt  # PyJWT — replaces unmaintained python-jose

SECRET_KEY = "replace-with-env-var-in-sprint-2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(subject: str | int, extra: dict[str, Any] | None = None) -> str:
    """Create a signed JWT. subject is typically a user ID or email."""
    payload: dict[str, Any] = {
        "sub": str(subject),
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and verify a JWT.
    Raises jwt.ExpiredSignatureError or jwt.InvalidTokenError on failure.
    """
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

---

### `dependencies.py`

```python
from typing import Annotated
import jwt
from fastapi import Header, HTTPException, status
from auth.jwt import decode_access_token

# PEP 695 type aliases (Python 3.14) — import these in routers instead of raw Depends calls
# Full async DB aliases (AsyncSession) are added in Day 3


async def verify_api_key(x_api_key: Annotated[str, Header()] = "") -> None:
    """Day 2 API key guard. Sprint 2 replaces this with full JWT/OAuth2."""
    if x_api_key != "dev-key-replace-in-sprint-2":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )


async def get_current_user_id(authorization: Annotated[str, Header()] = "") -> str:
    """
    Extract and verify JWT from Authorization: Bearer <token> header.
    Raises 401 on missing, expired, or invalid tokens.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or malformed Authorization header",
        )
    token = authorization.removeprefix("Bearer ")
    try:
        payload = decode_access_token(token)
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

# Old style (very safe)
#CurrentUser: TypeAlias = Annotated[str, Depends(get_current_user_id)]

# PEP 695 type aliases — use these as parameter types in routers
type CurrentUser = Annotated[str, Depends(get_current_user_id)]
type PageSkip = Annotated[int, Query(ge=0)]
type PageLimit = Annotated[int, Query(ge=1, le=100)]
```

---

### `routers/users.py`

```python
from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Query
from schemas.user import UserCreate, UserUpdate, UserResponse
from dependencies import verify_api_key, get_current_user_id

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_api_key)],
)

# In-memory store — replaced by async PostgreSQL in Day 3
_db: dict[int, dict] = {}
_counter: int = 0

# PEP 695 type aliases for this router
type PageSkip = Annotated[int, Query(ge=0, description="Items to skip")]
type PageLimit = Annotated[int, Query(ge=1, le=100, description="Max items returned")]


def _send_welcome_email(email: str) -> None:
    """Background task — runs after response is sent to the client."""
    print(f"[background] Sending welcome email to {email}")


@router.get("/", response_model=list[UserResponse], summary="List all users")
async def list_users(
    skip: PageSkip = 0,
    limit: PageLimit = 20,
    role: Annotated[str | None, Query(description="Filter by role")] = None,
) -> list[dict]:
    users = list(_db.values())
    if role:
        users = [u for u in users if u.get("role") == role]
    return users[skip : skip + limit]


@router.get("/{user_id}", response_model=UserResponse, summary="Get a user by ID")
async def get_user(user_id: int) -> dict:
    user = _db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user


@router.post("/", response_model=UserResponse, status_code=201, summary="Create a user")
async def create_user(payload: UserCreate, background_tasks: BackgroundTasks) -> dict:
    global _counter
    _counter += 1
    user = {
        "id": _counter,
        "name": payload.name,
        "email": payload.email,
        "role": payload.role,
        "created_at": datetime.now(timezone.utc),
    }
    _db[_counter] = user
    background_tasks.add_task(_send_welcome_email, payload.email)
    return user


@router.put("/{user_id}", response_model=UserResponse, summary="Replace a user")
async def replace_user(user_id: int, payload: UserCreate) -> dict:
    if user_id not in _db:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    _db[user_id].update(
        {"name": payload.name, "email": payload.email, "role": payload.role, "id": user_id}
    )
    return _db[user_id]


@router.patch("/{user_id}", response_model=UserResponse, summary="Partially update a user")
async def patch_user(user_id: int, payload: UserUpdate) -> dict:
    if user_id not in _db:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    updates = payload.model_dump(exclude_unset=True)  # only fields explicitly sent
    _db[user_id].update(updates)
    return _db[user_id]


@router.delete("/{user_id}", status_code=204, summary="Delete a user")
async def delete_user(user_id: int) -> None:
    if user_id not in _db:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    del _db[user_id]
```

---

### `main.py`

```python
import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from config import get_settings
from routers.users import router as users_router

settings = get_settings()


def custom_operation_id(route: APIRoute) -> str:
    """SDK-friendly operation IDs — avoids default path-based names like list_users_v1_users_get."""
    tag = route.tags[0].lower().replace(" ", "_") if route.tags else "api"
    name = route.name.replace("_", "-")
    return f"{tag}:{name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle. Add DB pool and HTTP client in Day 3."""
    print(f"Starting {settings.app_name} v{settings.app_version}")
    yield
    print("Shutting down")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-grade user management API — Sprint 1 Day 2",
    lifespan=lifespan,
    generate_unique_id_function=custom_operation_id,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
)

# CORS — allow Next.js dev frontend; read from env in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key"],
)


@app.middleware("http")
async def request_timing_and_correlation(request: Request, call_next):
    """Adds X-Request-ID and X-Process-Time-Ms to every response."""
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-Ms"] = str(duration_ms)
    return response


app.include_router(users_router, prefix="/v1")


@app.get("/health", tags=["system"], include_in_schema=False)
async def health():
    return {"status": "ok", "version": settings.app_version}
```

---

### `.env`

```
APP_NAME=Users API
APP_VERSION=1.0.0
DEBUG=true
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

---

### Run Locally

```bash
# --- Using uv (recommended) ---
uv sync

# Development (auto-reload, Swagger UI at /docs)
uv run fastapi dev main.py

# Production (no reload)
uv run fastapi run main.py

# Health check
curl http://localhost:8000/health

# Create a user (debug mode, API key guard)
curl -X POST http://localhost:8000/v1/users \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-key-replace-in-sprint-2" \
  -d '{"name": "Qasir", "email": "q@example.com", "password": "secure123", "role": "user"}'

# --- Using poetry (existing codebases) ---
# poetry install
# poetry run fastapi dev main.py         # development
# poetry run fastapi run main.py         # production
# poetry run uvicorn main:app --reload   # legacy equivalent (still valid)
```

---

### `tests/conftest.py`

```python
import pytest
from httpx import AsyncClient, ASGITransport #(Asynchronous Server Gateway Interface)
from main import app
from auth.jwt import create_access_token

AUTH_HEADERS = {"X-API-Key": "dev-key-replace-in-sprint-2"}


@pytest.fixture
async def async_client():
    """Async test client using ASGI (Asynchronous Server Gateway Interface) transport — no network required."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
def auth_token() -> str:
    """auth_token function docstring."""
    return create_access_token(subject="test-user-1")


@pytest.fixture
def auth_headers(auth_token: str) -> dict[str, str]:
    """auth_headers function docstring."""
    return {**AUTH_HEADERS, "Authorization": f"Bearer {auth_token}"}
```

---

### `tests/test_users.py`

```python
import pytest
from httpx import AsyncClient
from unittest.mock import patch
from main import app


async def test_create_user(async_client: AsyncClient, auth_headers: dict):
    response = await async_client.post(
        "/v1/users",
        json={"name": "Qasir", "email": "q@example.com", "password": "secure123", "role": "user"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "q@example.com"
    assert data["role"] == "user"
    assert "id" in data
    assert "password" not in data  # response schema must never expose the password


async def test_get_user(async_client: AsyncClient, auth_headers: dict):
    create = await async_client.post(
        "/v1/users",
        json={"name": "Test", "email": "test@example.com", "password": "secure123"},
        headers=auth_headers,
    )
    user_id = create.json()["id"]
    response = await async_client.get(f"/v1/users/{user_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == user_id


async def test_get_user_not_found(async_client: AsyncClient, auth_headers: dict):
    response = await async_client.get("/v1/users/99999", headers=auth_headers)
    assert response.status_code == 404


async def test_patch_user_partial_update(async_client: AsyncClient, auth_headers: dict):
    create = await async_client.post(
        "/v1/users",
        json={"name": "Original", "email": "orig@example.com", "password": "secure123"},
        headers=auth_headers,
    )
    user_id = create.json()["id"]
    response = await async_client.patch(
        f"/v1/users/{user_id}",
        json={"name": "Updated"},  # only name — email must be unchanged
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"
    assert response.json()["email"] == "orig@example.com"


async def test_delete_user(async_client: AsyncClient, auth_headers: dict):
    create = await async_client.post(
        "/v1/users",
        json={"name": "ToDelete", "email": "del@example.com", "password": "secure123"},
        headers=auth_headers,
    )
    user_id = create.json()["id"]
    delete_response = await async_client.delete(f"/v1/users/{user_id}", headers=auth_headers)
    assert delete_response.status_code == 204
    get_response = await async_client.get(f"/v1/users/{user_id}", headers=auth_headers)
    assert get_response.status_code == 404

# {
#   "detail": [
#     {
#       "loc": ["body", "email"],
#       "msg": "value is not a valid email address",
#       "type": "value_error.email"
#     },
#     {
#       "loc": ["body", "password"],
#       "msg": "string does not match expected pattern",
#       "type": "value_error"
#     }
#   ]
# }
async def test_create_user_invalid_email(async_client: AsyncClient, auth_headers: dict):
    response = await async_client.post(
        "/v1/users",
        json={"name": "Qasir", "email": "not-an-email", "password": "secure123"},
        headers=auth_headers,
    )
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any(e["loc"] == ["body", "email"] for e in errors)


async def test_create_user_blank_name(async_client: AsyncClient, auth_headers: dict):
    response = await async_client.post(
        "/v1/users",
        json={"name": "   ", "email": "q@example.com", "password": "secure123"},
        headers=auth_headers,
    )
    assert response.status_code == 422


async def test_list_users_role_filter(async_client: AsyncClient, auth_headers: dict):
    await async_client.post(
        "/v1/users",
        json={"name": "Admin", "email": "admin@example.com", "password": "secure123", "role": "admin"},
        headers=auth_headers,
    )
    response = await async_client.get("/v1/users?role=admin", headers=auth_headers)
    assert response.status_code == 200
    assert all(u["role"] == "admin" for u in response.json())


async def test_create_user_triggers_background_email(async_client: AsyncClient, auth_headers: dict):
    with patch("routers.users._send_welcome_email") as mock_email:
        response = await async_client.post(
            "/v1/users",
            json={"name": "Qasir", "email": "bg@example.com", "password": "secure123"},
            headers=auth_headers,
        )
    assert response.status_code == 201
    mock_email.assert_called_once_with("bg@example.com")


async def test_missing_api_key_returns_401(async_client: AsyncClient):
    response = await async_client.post(
        "/v1/users",
        json={"name": "Qasir", "email": "q@example.com", "password": "secure123"},
    )
    assert response.status_code == 401
```

---

## ✅ Key Concepts

- **Separate request and response schemas** — `UserCreate` (input, with `SecretStr` password) and `UserResponse` (output, no password) are distinct models; never expose internal or write-only fields in responses
- **`Depends()` is composable** — chain dependencies (`get_db → get_current_user → require_admin`) to build clean auth hierarchies; every dependency is trivially overridable in tests
- **`lifespan` over deprecated `@app.on_event`** — use the `asynccontextmanager` pattern for all app-level resource management since FastAPI 0.95
- **CORS `allow_origins=["*"]` with credentials is rejected by browsers** — always read allowed origins from `pydantic-settings`, never hardcode them
- **`response_model` is not optional on routes that return DB objects** — omitting it means FastAPI returns the raw dict, potentially leaking internal fields

---

## ⚠️ Pitfalls

- Forgetting `model_config = ConfigDict(from_attributes=True)` on response schemas that map from SQLAlchemy ORM objects (Day 3) — causes `ValidationError` at runtime
- Using `def` instead of `async def` for routes that call async I/O — blocks the event loop and collapses throughput to one request at a time
- Setting `allow_origins=["*"]` with `allow_credentials=True` — browsers reject this per the CORS spec; it is also an OWASP A05 misconfiguration
- Using `BackgroundTasks` for retryable or critical jobs — it has no retry, timeout, or failure handling; use Celery or ARQ (Atomic Redis Queue) for those
- Not calling `model_dump(exclude_unset=True)` in `PATCH` handlers — overwrites all optional fields with `None` even when the client did not send them
- Leaving `openapi_url` enabled in production while hiding the Swagger UI — the schema is still publicly accessible at `/openapi.json`
- Using `python-jose` — unmaintained since 2023, open CVEs; use `PyJWT` instead

```python
# ARQ (Atomic Redis Queue)
from arq import create_pool
from arq.worker import func

@func
async def add(ctx, x, y):
    return x + y
```

---

## 🎯 Practice Exercises

**Exercise 1 — Add a `POST /v1/users/bulk` endpoint**

Accept `list[UserCreate]`, create all users in the in-memory store, trigger one background welcome email per user, and return `list[UserResponse]` with `status_code=201`. Write a test that asserts the correct number of background email calls.

**Exercise 2 — Add rate limiting per API key**

Using a `dict[str, int]` counter in module scope, track how many requests each API key has made. Return `429 Too Many Requests` if a key exceeds 100 requests. Reset the counter every 60 seconds using a background task triggered on startup. Write a test that triggers the limit.

---

## 📊 Quick Reference — FastAPI Decorator Arguments

| Argument                       | Type           | Purpose                                                       |
| ------------------------------ | -------------- | ------------------------------------------------------------- |
| `response_model`               | Pydantic model | Serialise and schema-document the response                    |
| `status_code`                  | int            | Override default `200` (use `201` for POST, `204` for DELETE) |
| `summary`                      | str            | Short label in Swagger UI                                     |
| `description`                  | str            | Full Markdown description in Swagger UI                       |
| `response_description`         | str            | Documents the success response body                           |
| `deprecated`                   | bool           | Marks the endpoint as deprecated in OpenAPI                   |
| `include_in_schema`            | bool           | `False` to hide from OpenAPI (e.g., internal health probes)   |
| `response_model_exclude_unset` | bool           | Omit fields not explicitly set in the response                |

---

---

## 🧪 Advanced / Senior-Level: Typed DataFrames (Optional)

> This section is not required for beginners. It targets senior engineers working in data-adjacent Python roles.

For FastAPI services that process or serve data pipelines, typed DataFrames are a senior-level differentiator. **`pandera`** allows you to define DataFrame schemas with full type annotations and runtime validation — complementing Pydantic's role at API boundaries with equivalent rigour at the data layer.

```python
import pandera as pa
from pandera.typing import DataFrame, Series

class UserDataSchema(pa.DataFrameModel):
    """UserDataSchema class docstring."""
    user_id: Series[int] = pa.Field(ge=1)
    email: Series[str]
    role: Series[str] = pa.Field(isin=["user", "admin"])

    class Config:
        """Config class docstring."""
        coerce = True

@pa.check_types
def filter_admins(df: DataFrame[UserDataSchema]) -> DataFrame[UserDataSchema]:
    """filter_admins function docstring."""
    return df[df["role"] == "admin"]
```

**When this matters:** data pipeline services, ML feature APIs, ETL endpoints. **At pure FastAPI CRUD roles:** knowledge is a differentiator, not a prerequisite.

---

## 🔧 Tooling Q&A — `uv` vs `poetry`

**What is `uv` and why is it the 2026 default?**
`uv` is a Rust-based all-in-one tool: Python version management, virtual environments, and dependency installation in a single binary. It is 10–100× faster than equivalent Python-based tools and replaces `pyenv` + `pip` + `venv` for all new projects in 2026.

```bash
# uv workflow for this project
uv python install 3.14
uv init fastapi-users-api
cd fastapi-users-api
uv add "fastapi[standard]" pydantic pydantic-settings PyJWT cryptography
uv add --dev ruff mypy pytest httpx pytest-cov pytest-asyncio
uv run fastapi dev main.py    # development
uv run fastapi run main.py    # production
```

**When would you still use `poetry`?**
When joining an existing codebase already using `poetry`, or when a team has established tooling and pipelines around it. `poetry` remains the standard alternative and is frequently seen in interviews — senior engineers know both.

**Should senior engineers know both `uv` and `poetry`?** YES.

---

## 📚 Additional Resources

| Resource                            | URL                                                          |
| ----------------------------------- | ------------------------------------------------------------ |
| FastAPI documentation               | https://fastapi.tiangolo.com/                                |
| FastAPI releases (version tracking) | https://github.com/fastapi/fastapi/releases                  |
| Pydantic v2 docs                    | https://docs.pydantic.dev/latest/                            |
| pydantic-settings                   | https://docs.pydantic.dev/latest/concepts/pydantic_settings/ |
| PyJWT documentation                 | https://pyjwt.readthedocs.io/en/stable/                      |
| OWASP Top 10                        | https://owasp.org/www-project-top-ten/                       |
| pytest-asyncio                      | https://pytest-asyncio.readthedocs.io/                       |
| uv documentation                    | https://docs.astral.sh/uv/                                   |
| Poetry documentation                | https://python-poetry.org/docs/                              |
| PEP 695 — Type Aliases              | https://peps.python.org/pep-0695/                            |
| PEP 593 — `Annotated`               | https://peps.python.org/pep-0593/                            |
| PEP 703 — Free-threading            | https://peps.python.org/pep-0703/                            |

---

## ✅ Today's Deliverable Checklist

By the end of today, you should have:

- [ ] Created a new `fastapi-users-api` project with `uv init` (or `poetry new` if working in an existing poetry codebase) using `fastapi[standard]`
- [ ] Configured `pyproject.toml` with `asyncio_mode = "auto"` for pytest
- [ ] Implemented `config.py` with `pydantic-settings` and `lru_cache`
- [ ] Implemented `schemas/user.py` with separate `UserCreate`, `UserUpdate`, `UserResponse` models
- [ ] Added `@field_validator` on `name` and `role`, with `SecretStr` on `password`
- [ ] Implemented `auth/jwt.py` using `PyJWT` (not `python-jose`)
- [ ] Implemented `dependencies.py` with `verify_api_key` and `get_current_user_id`
- [ ] Built `routers/users.py` with all five verbs (GET list, GET single, POST, PUT, PATCH, DELETE)
- [ ] Used PEP 695 `type` aliases for `PageSkip` and `PageLimit` in the router
- [ ] Added `role` query parameter filter to `GET /users`
- [ ] Built `main.py` with `lifespan`, `CORSMiddleware`, timing middleware, and `generate_unique_id_function`
- [ ] Disabled docs in production (`docs_url=None` when `debug=False`)
- [ ] Written `tests/conftest.py` with `async_client`, `auth_token`, and `auth_headers` fixtures
- [ ] Written `tests/test_users.py` covering create, get, patch, delete, 404, 422, role filter, and background task
- [ ] Confirmed `ruff check .` and `mypy .` pass with zero errors
- [ ] Confirmed `pytest --cov=. --cov-fail-under=80` passes
- [ ] Run `fastapi dev main.py` and verified Swagger UI at `http://localhost:8000/docs`

---

**Next Sprint Day:** Wed 22 Apr — PostgreSQL + Async SQLAlchemy: async engine, session factory, repository pattern, Alembic migrations. Wire the users API to a local PostgreSQL instance.

---

_This learning material is part of the 2026 Python · Azure · AI Engineering Roadmap targeting UK senior roles (£90k–£130k / £550–£750/day). Python 3.14 · uv · FastAPI · Pydantic v2 · PyJWT · ruff · mypy._
