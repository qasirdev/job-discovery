# Disaster Recovery and Backup Restore

## Overview

This document outlines the Disaster Recovery (DR) and backup restore procedures for the AI-Powered Job Discovery Platform. It ensures data resilience and minimal downtime in the event of a catastrophic failure.

## Target Metrics

*   **Recovery Point Objective (RPO):** <= 15 minutes. This is the maximum acceptable amount of data loss.
*   **Recovery Time Objective (RTO):** <= 1 hour. This is the maximum acceptable downtime before the system must be restored to full operation.

> **⚠️ Supabase Pro Plan Required:** Point-in-time recovery (PITR) is only available on the Supabase Pro plan or above. Confirm plan tier includes PITR before production go-live.

## Backup Strategy per Component

*   **PostgreSQL (Database & pgvector):** Continuous WAL (Write-Ahead Logging) archiving via Supabase PITR (Pro plan required). Ensures point-in-time recovery to within the 15-minute RPO.
*   **Redis (Cache & Queues):** AOF (Append Only File) persistence enabled (`appendonly yes`, `appendfsync everysec` in redis.conf), with periodic RDB snapshots. Session cache loss is acceptable; DLQ queue states are persisted via AOF.
*   **Terraform State:** State files stored remotely in versioned object storage (AWS S3 or Azure Blob) with state locking (DynamoDB / Azure Table Storage).
*   **Docker Images:** All production images are signed (cosign) and stored in ACR/ECR. Images are tagged by Git SHA for precise version pinning.
*   **Prompts (`prompts/` directory):** Prompt configurations are in git — restore by deploying the correct git tag.

### Redis AOF Configuration (redis.conf)

```conf
appendonly yes
appendfsync everysec
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

## Restore Workflow (7 Steps)

In the event of a total system failure, execute the following steps **in order**. All commands are verified against the staging environment.

### Step 1 — Declare Incident and Isolate

```bash
# Pause all Temporal workflows to prevent new work from starting
# (requires TEMPORAL_SERVER_URL set in environment)
temporal workflow list --namespace default | grep Running | awk '{print $1}' | \
  xargs -I{} temporal workflow terminate --workflow-id {} --reason "DR event declared"
```

### Step 2 — Restore Infrastructure via Terraform

```bash
cd infrastructure/terraform/azure
terraform init
# Use the stored state from Azure Blob (configured in backend block)
terraform apply -var-file=prod.tfvars -auto-approve
```

### Step 3 — Restore Database (PostgreSQL via Supabase PITR)

```bash
# Supabase PITR restore — requires Supabase Pro plan and CLI >= 1.150.0
# Replace <project_ref> and <recovery_timestamp> with actual values
supabase db restore \
  --project-ref <project_ref> \
  --recovery-target-time "2026-01-01T12:00:00Z"

# Verify row counts after restore
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM jobs;"
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM applications;"
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM cv_chunks;"  # pgvector embeddings
```

### Step 4 — Restore Cache (Redis AOF)

```bash
# Stop Redis, copy the AOF backup from object storage, restart
# Assumes backup stored in Azure Blob Storage
az storage blob download \
  --account-name <storage_account> \
  --container-name redis-backups \
  --name appendonly-latest.aof \
  --file /data/appendonly.aof

# Restart Redis with AOF replay
redis-server /etc/redis/redis.conf --appendonly yes
redis-cli PING  # Should return PONG
```

### Step 5 — Deploy Application Images

```bash
# Pull latest signed Docker image (tagged by Git SHA from DR runbook)
RECOVERY_SHA="<git_sha_from_last_known_good_deployment>"
docker pull acrjobdiscovery.azurecr.io/job-discovery:${RECOVERY_SHA}

# Verify cosign signature before running
cosign verify \
  --certificate-identity-regexp=.* \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com \
  acrjobdiscovery.azurecr.io/job-discovery:${RECOVERY_SHA}

# Deploy to Azure Container Apps
az containerapp update \
  --name job-discovery \
  --resource-group rg-job-discovery-prod \
  --image acrjobdiscovery.azurecr.io/job-discovery:${RECOVERY_SHA}
```

### Step 6 — Verify Data Integrity

```bash
# Run automated consistency checks
docker exec job-discovery uv run python -m backend.admin.run_evals --agent all --fast

# Check pgvector embeddings match job count
psql "$DATABASE_URL" -c "
  SELECT
    (SELECT COUNT(*) FROM jobs) AS total_jobs,
    (SELECT COUNT(DISTINCT job_id) FROM cv_chunks) AS jobs_with_embeddings;
"
```

### Step 7 — Update DNS and Verify Routing

```bash
# Switch DNS A record to recovery environment IP
# (Replace with actual DNS provider CLI — example uses Azure DNS)
az network dns record-set a update \
  --resource-group rg-dns \
  --zone-name yourdomain.com \
  --record-set-name api \
  --set "aRecords[0].ipv4Address=<recovery_ip>"

# End-to-end health check
curl -f https://api.yourdomain.com/health
curl -f https://api.yourdomain.com/api/v1/jobs?limit=1
```

## DR Validation

To ensure the reliability of this plan, the following validation measures are enforced:

*   **Quarterly Drills:** Full DR failover drills conducted quarterly against the staging environment to test RTO and RPO targets.
*   **Automated Recovery Validation:** Nightly backup validation spins up temporary databases from backups and runs Step 6 integrity queries automatically.
*   **Consistency Checks:** Regular scripts check consistency between relational data and pgvector embeddings.
*   **Runbooks:** This document serves as the primary runbook. Commands are re-verified on every quarterly drill. Stale commands are updated before sign-off.

