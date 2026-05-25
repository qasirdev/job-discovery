# Data Ownership and Portability

This document defines the data ownership and portability guarantees for users of the Job Discovery platform, ensuring compliance with privacy standards and giving users full control over their data.

## Export Capabilities

Users have the right to export their data at any time. The system provides exact export formats per resource:
- **CVs**: PDF / DOCX
- **Applications**: JSON / CSV
- **Cover Letters**: Markdown / PDF
- **Interview Packs**: Markdown / PDF
- **Recruiter Interactions**: JSON

## Deletion Capabilities

When a user requests account deletion, the system guarantees the exact propagation targets are purged:
- **PostgreSQL records**: All relational data linked to `user_id`
- **pgvector embeddings**: All associated vector embeddings
- **Redis caches**: All cached sessions and temporary data
- **Object storage**: Uploaded files and generated PDFs
- **Observability metadata**: Anonymised or removed from tracing logs

## GDPR Compliance

The platform strictly adheres to GDPR compliance requirements:
- **Right to Export**: Automated self-service data export.
- **Right to Deletion**: Full cascading deletes across all storage layers.
- **Consent Withdrawal**: Instant pausing of background processing and AI agents.
- **Retention Policies**: Explicit limits on how long data is stored before auto-purging.
- **Audit Logging**: Immutable logs of data access and modifications for security review.
