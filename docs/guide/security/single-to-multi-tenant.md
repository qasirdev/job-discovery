# Transitioning from Single-User Bridge to Multi-Tenant Auth

## Overview

The AI-Powered Job Discovery Platform is built from day one with enterprise-grade security primitives, including Role-Based Access Control (RBAC) and database-level Row Level Security (RLS). 

However, to accelerate the delivery of **MVP 1**, the application currently operates in a single-tenant mode using a "Single-User Bridge Strategy." This document explains how the bridge works and how the platform will transition to a fully multi-tenant architecture in **MVP 2 and MVP 3**.

---

## 1. The `SINGLE_USER_ID` Bridge (MVP 1)

In MVP 1, there is no login screen or user authentication flow. Instead, the application simulates a logged-in user.

### How it works:
*   **Environment Variable:** The `.env` file defines a constant UUID: `SINGLE_USER_ID=00000000-0000-0000-0000-000000000000`.
*   **Backend Middleware (`backend/middleware/auth.py`):** The backend intercepts all incoming requests. Since no valid JWT is provided by the frontend, the middleware injects the `SINGLE_USER_ID` as the subject (`sub`) of the request.
*   **Simulated Roles:** To ensure the user can perform all necessary actions (saving jobs, uploading CVs, viewing applications) without being blocked by the existing RBAC system, the middleware automatically attaches the `"admin"` role to this user session.
*   **Data Persistence:** Every record created in the database—from User Profiles to Saved Jobs—is tied to `00000000-0000-0000-0000-000000000000`.

### Why use this strategy?
It allows frontend and backend developers to build the core AI features (Scraping, Ranking, Cover Letter generation) against a robust permission architecture without the overhead of building login screens, password resets, and session management for MVP 1.

---

## 2. Full Multi-Tenant Login (MVP 2–3)

As the platform moves into MVP 2 and MVP 3, the `SINGLE_USER_ID` bridge will be dismantled in favor of real authentication.

### Supabase Auth & JWTs
*   **Frontend Integration:** A login and registration UI will be added to the Next.js frontend. Upon login, Supabase Auth will issue a secure JSON Web Token (JWT).
*   **Backend Validation:** The frontend will pass this JWT in the `Authorization: Bearer <token>` header on every API request. The FastAPI backend will use `pyjwt[crypto]` to cryptographically verify the token's signature against Supabase.
*   **Token Denylist:** Redis will be used to maintain a denylist for revoked or expired JWTs to prevent replay attacks.

### Dynamic Role Assignments (RBAC)
Instead of a hardcoded `"admin"` role, the backend will extract the exact role assigned to the user from the JWT payload.
*   **`user` / `authenticated`:** Standard access for job seekers. Can only read/write their own data.
*   **`admin`:** Can access administrative routes (like the DLQ dashboard or schedule controls).
*   **`service_role`:** Used exclusively for agent-to-agent communication or system-level bypasses (e.g., cron jobs scraping jobs in the background).

### Row Level Security (RLS) Enforcement
The PostgreSQL database already has RLS policies configured. Once the real JWTs are passed through the connection context, the database will automatically enforce that a logged-in `user` can only query rows where `user_id == current_user_id`.

---

## 3. Migration Plan for Existing Data

When the switch to multi-tenant is flipped, the data tied to `00000000-0000-0000-0000-000000000000` will become inaccessible to new, legally authenticated users.

**Data Migration Options:**
1.  **Start Fresh (Recommended for Dev/Staging):** Truncate the tables and allow the first real user to onboard naturally.
2.  **Re-assignment:** Create a data migration script that updates the `user_id` of all records belonging to `00000000-0000-0000-0000-000000000000` to the new UUID of the system administrator or the first registered user.
