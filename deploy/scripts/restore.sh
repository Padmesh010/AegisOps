#!/bin/bash
set -e

BACKUP_FILE=$1

if [ -z "${BACKUP_FILE}" ]; then
    echo "Usage: $0 /path/to/backup_file.sql"
    exit 1
fi

if [ ! -f "${BACKUP_FILE}" ]; then
    echo "Error: target restore snapshot not found: ${BACKUP_FILE}"
    exit 1
fi

echo "Initiating database snapshot restoration: ${BACKUP_FILE}..."

# Drop and recreate database schema cleanly
PGPASSWORD=securepassword dropdb -h db -U admin aegisops || true
PGPASSWORD=securepassword createdb -h db -U admin aegisops

# Restore using pg_restore
PGPASSWORD=securepassword pg_restore -h db -U admin -d aegisops "${BACKUP_FILE}"

echo "Database snapshot restored successfully."
