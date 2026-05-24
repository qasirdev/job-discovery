import sys

content = """
# Security Standards

This document outlines the security architecture of the Job Discovery platform.

## Agent Isolation & Prompt Injection Defense
All LLM inputs from user-generated content (e.g. scraped CVs, job descriptions) must pass through `security_agent.py`. The agent strips HTML via bleach, checks for prompt injection triggers, and verifies OWASP standards.

## OWASP Middleware
`OWASPMiddleware` intercepts requests to validate content limits and enforce basic RBAC on `/api/v1/admin/*` endpoints.

## Circuit Breakers
Agents are wrapped in tenacity-based circuit breakers that open after repeated failures, routing problematic payloads to the Dead Letter Queue (DLQ).

## Authorization
JWT validation is required for specific endpoints. The `admin-claim` must be present in the headers for admin routes.
"""

with open("docs/SECURITY.md", "w") as f:
    f.write(content)

