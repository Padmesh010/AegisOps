#!/bin/bash
set -e

# Configuration settings
BACKUP_DIR="/var/backups/aegisops"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/db_backup_${TIMESTAMP}.sql"

echo "Starting database snapshot dump operation..."
mkdir -p "${BACKUP_DIR}"

# Execute PostgreSQL pg_dump
# Uses standard PG password injected via env parameters configurations
pg_dump -h db -U admin -d aegisops -F c -f "${BACKUP_FILE}"

echo "Database snapshot saved successfully to: ${BACKUP_FILE}"

# Keep only the last 7 daily backup snapshots (pruning older files)
find "${BACKUP_DIR}" -name "db_backup_*.sql" -mtime +7 -delete
echo "Cleanup of expired backup snapshots complete."
