# Data Ownership and Portability

## Overview

This document outlines the data ownership, portability, and GDPR compliance policies for the AI-Powered Job Discovery Platform (MVP 3). It ensures that users have full control over their data, including the right to export, delete, and manage consent.

## Export Capabilities per Resource

Users can export their data at any time in the following formats:

*   **CVs (Resumes):** PDF, DOCX
*   **Applications:** JSON, CSV
*   **Cover Letters:** Markdown, PDF
*   **Interview Packs:** Markdown, PDF
*   **Recruiter Interactions:** JSON

## Deletion Capabilities and Propagation Targets

When a user requests data deletion, the platform ensures complete removal across all systems. The deletion propagates to the following targets:

*   **PostgreSQL records:** All relational data (user profile, saved jobs, applications, recruiter interactions) is hard-deleted.
*   **pgvector embeddings:** Vector representations of CVs and user profiles used for AI matching are deleted.
*   **Redis caches:** Any cached session data or temporary user data is evicted.
*   **Object storage:** Uploaded files (CVs, cover letters) are permanently removed from S3/blob storage.
*   **Observability metadata:** PII is scrubbed from logs and traces (though anonymized aggregate metrics may be retained).

## GDPR Compliance Requirements

The platform is designed to be fully GDPR compliant:

*   **Right to Export (Data Portability):** Users can download all their data in structured, commonly used, and machine-readable formats (as outlined above).
*   **Right to Deletion (Right to be Forgotten):** Users can permanently delete their account and all associated data, triggering the propagation described above.
*   **Consent Withdrawal:** Users can withdraw consent for specific AI processing activities at any time (e.g., stop AI from analyzing specific documents).
*   **Retention Policies:** Data is only retained for as long as necessary to provide the service. Inactive accounts may be subject to automated deletion after a predefined period (e.g., 2 years of inactivity) with prior notification.
*   **Audit Logging:** All data access, modifications, and consent changes are logged for security and compliance auditing.

## Consent Revocability and Transparency

*   **Consent Revocability:** Active "living contracts" for AI agents can be managed and revoked via the user dashboard (`/settings/consent`).
*   **Transparency of Data Flows:** Users are provided with clear visibility into how their data is used by different AI agents (e.g., the RAG agent accessing their CV).
*   **Fine-grained Personalization:** Users have granular control over what data the AI can access. For example, a user can exclude specific data folders, past jobs, or certain skills from being used by the RAG agent for context generation.
