#!/bin/bash
# Restore PostgreSQL database from backup

set -euo pipefail

if [ $# -eq 0 ]; then
    echo "Usage: $0 <backup-file>"
    echo "Available backups:"
    ls -lh ./backups/backup-*.sql 2>/dev/null || echo "No backups found"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "Warning: This will overwrite the current database!"
read -p "Continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

echo "Restoring database from $BACKUP_FILE..."

docker-compose exec -T postgres psql -U appuser -d appdb < "$BACKUP_FILE"

echo "Database restored successfully"
