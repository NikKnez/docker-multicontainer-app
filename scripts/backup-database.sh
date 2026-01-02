#!/bin/bash
# Backup PostgreSQL database

set -euo pipefail

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup-$TIMESTAMP.sql"

mkdir -p "$BACKUP_DIR"

echo "Starting database backup..."

docker-compose exec -T postgres pg_dump -U appuser appdb > "$BACKUP_FILE"

echo "Backup completed: $BACKUP_FILE"
echo "Size: $(du -h "$BACKUP_FILE" | cut -f1)"

# Keep only last 7 backups
ls -t "$BACKUP_DIR"/backup-*.sql | tail -n +8 | xargs -r rm

echo "Old backups cleaned up"
