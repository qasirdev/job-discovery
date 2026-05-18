# Security

- **Authentication**: JWT based auth powered by Supabase.
- **Authorization**: Role-based access control (RBAC) restricts endpoints.
- **Prompt Injection**: Mitigated by the SecurityAgent running OWASP validation on all scraped text before hitting the LLM.
