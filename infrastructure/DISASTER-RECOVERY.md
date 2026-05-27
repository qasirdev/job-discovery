# Disaster Recovery and Backup Restore

## Overview

This document outlines the Disaster Recovery (DR) and backup restore procedures for the AI-Powered Job Discovery Platform. It ensures data resilience and minimal downtime in the event of a catastrophic failure.

## Target Metrics

*   **Recovery Point Objective (RPO):** <= 15 minutes. This is the maximum acceptable amount of data loss.
*   **Recovery Time Objective (RTO):** <= 1 hour. This is the maximum acceptable downtime before the system must be restored to full operation.

## Backup Strategy per Component

*   **PostgreSQL (Database & pgvector):** Continuous WAL (Write-Ahead Logging) archiving to secure object storage (e.g., S3), plus daily full backups. Ensures point-in-time recovery to within the 15-minute RPO.
*   **Redis (Cache & Queues):** AOF (Append Only File) persistence enabled, with periodic snapshots (RDB) backed up daily. Note that session cache loss is acceptable, but queue states are persisted.
*   **Terraform State:** State files are stored remotely in secure, versioned object storage (e.g., AWS S3 or Azure Blob Storage) with state locking enabled (e.g., DynamoDB).
*   **Docker Images:** All production images are signed and stored in a secure, replicated container registry (e.g., ACR or ECR).
*   **Prompts (`prompts/` directory):** Prompt configurations and version history are stored in the git repository and deployed alongside the codebase. Git serves as the backup mechanism.

## Restore Workflow (7 Steps)

In the event of a total system failure, the following 7-step restore workflow must be executed:

1.  **Declare Incident and Isolate:** Acknowledge the outage, declare a DR event, and isolate the compromised environment to prevent further data corruption.
2.  **Restore Infrastructure:** Run `terraform apply` using the latest uncorrupted remote state to provision clean infrastructure in the recovery region/environment.
3.  **Restore Database (PostgreSQL):** Restore the latest daily full backup, then replay the WAL logs up to the exact point of failure (or latest uncorrupted point-in-time).
4.  **Restore Cache (Redis):** Restore the latest Redis RDB snapshot and start the Redis service.
5.  **Deploy Application Images:** Pull the latest signed Docker images from the container registry and deploy them to the newly provisioned infrastructure (ECS Fargate/Azure Container Apps).
6.  **Verify Data Integrity:** Run automated consistency checks to ensure the database and embeddings match, and that critical data (users, auth, applications) is intact.
7.  **Update DNS and Verify Routing:** Switch DNS records to point to the new recovery environment and perform end-to-end synthetic health checks before routing user traffic.

## DR Validation

To ensure the reliability of this plan, the following validation measures are enforced:

*   **Quarterly Drills:** Full DR failover drills are conducted every quarter to test the RTO and RPO targets in a staging environment.
*   **Automated Recovery Validation:** Nightly backup validation processes automatically spin up temporary databases from backups and run basic integrity queries.
*   **Consistency Checks:** Regular scripts check for consistency between relational data and pgvector embeddings.
*   **Runbooks:** Detailed, step-by-step technical runbooks are maintained and reviewed monthly.
