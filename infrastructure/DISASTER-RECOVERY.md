# Disaster Recovery and Backup Restore

This document defines the Disaster Recovery (DR) plan for the Job Discovery platform, ensuring minimal data loss and rapid recovery in the event of catastrophic failure.

## Recovery Targets
- **RPO (Recovery Point Objective)**: <= 15 minutes (maximum acceptable data loss).
- **RTO (Recovery Time Objective)**: <= 1 hour (maximum acceptable downtime).

## Backup Strategy
- **PostgreSQL**: Continuous WAL (Write-Ahead Logging) archiving to blob storage + daily full snapshots.
- **Redis**: RDB snapshots every 15 minutes (cache only, acceptable to lose transient state).
- **Terraform state**: Remote state locked and versioned in secure cloud storage.
- **Docker images**: Immutable tagged images stored in container registry.
- **Prompts**: Versioned inside the Git repository (`prompts/`).

## Restore Workflow
In the event of a total region failure, the following 7 steps are executed:
1. Declare DR event and page engineers.
2. Update DNS/Traffic Manager to route to the failover region.
3. Provision new infrastructure via Terraform (`terraform apply` in secondary region).
4. Restore PostgreSQL from the latest snapshot and apply WAL logs up to the point of failure.
5. Deploy the latest tagged Docker container to the new environment.
6. Run smoke tests and database consistency checks.
7. Open traffic to users and declare DR complete.

## DR Validation
- **Quarterly drills**: Simulated failovers conducted every 3 months.
- **Automated recovery validation**: Nightly automated restores to isolated dev environments to verify backup integrity.
- **Consistency checks**: Scripts run post-restore to ensure relational integrity and pgvector alignment.
- **Runbooks**: Maintained and tested step-by-step guides for engineers on call.
