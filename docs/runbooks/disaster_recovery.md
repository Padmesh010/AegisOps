# Disaster Recovery Runbook

This document defines the operational recovery guidelines for the **AegisOps** platform.

---

## 1. RPO & RTO Objectives
*   **Recovery Point Objective (RPO)**: 15 minutes (maximum historical data loss limit allowed).
*   **Recovery Time Objective (RTO)**: 1 hour (maximum offline system restoration period allowed).

---

## 2. Backup Schedule Heuristics
*   **Database backups**: Run automated pg_dump scripts daily via CRON scheduled runs, storing snapshots in isolated S3 storage buckets.
*   **Configuration snapshots**: Commit all dashboard layouts and alert parameters changes directly to the Git repository.

---

## 3. Step-by-Step Restoration Operations

### Phase A: DB Cluster Restoration
1.  Deploy a new Postgres pod instance:
    ```bash
    helm install aegisops-db bitnami/postgresql --values deploy/helm/values.yaml
    ```
2.  Locate the latest backup file from storage:
    ```bash
    aws s3 cp s3://aegisops-backups/db_backup_latest.sql .
    ```
3.  Execute the restore script targeting the database cluster:
    ```bash
    ./deploy/scripts/restore.sh db_backup_latest.sql
    ```

### Phase B: Frontend & API Deployment Re-deployment
1.  Re-deploy Helm chart applications:
    ```bash
    helm upgrade --install aegisops deploy/helm/ --values deploy/helm/values.yaml
    ```
2.  Validate API availability:
    ```bash
    curl -f http://api.aegisops.io/api/v1/health/readiness
    ```
