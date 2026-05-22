# Learning: Step 14 - Auth & RBAC (Role-Based Access Control)

## Learning Objectives
- Learn how to secure FastAPI routes using JSON Web Tokens (JWT).
- Understand how to invalidate stateless JWTs securely using a Redis Denylist.
- Master Role-Based Access Control (RBAC) via FastAPI Dependencies.

## Technical Details

### 1. Redis Denylist Architecture
JWTs are fundamentally stateless; once signed, they are valid until their expiration date. 
To support features like instantaneous "Logout" or "Force Revoke", we use a Redis Denylist:
- Upon logout, the JWT's unique `jti` (JWT ID) is inserted into Redis with a Time-To-Live (TTL) matching the token's remaining lifespan.
- The `get_current_user` dependency in `backend/auth.py` checks Redis *before* trusting a valid signature. If the `jti` exists in the cache, it raises an HTTP 401 Unauthorized.

### 2. Dependency Injection for RBAC
We implemented role-based protection using FastAPI's `Depends` system in `backend/rbac.py`:
- `RequireAuthenticated`: A base class dependency that extracts the JWT, verifies its signature and algorithms (`pyjwt[crypto]`), checks the Redis Denylist, and injects the `User` object into the route.
- `RequireAdmin`: Inherits from `RequireAuthenticated` but adds a subsequent check: `if user.role != "admin"`. It raises an HTTP 403 Forbidden if the user is a standard user trying to access an admin route.

This pattern keeps the actual route handlers (`routers/*.py`) completely clean of authorization logic.
