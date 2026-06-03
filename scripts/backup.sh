#!/bin/bash

export $(grep -v '^#' .env | xargs)


BACKUP_DIR="./backups"
LOG_FILE="./log/backup.log" 
KEEP_DAYS=7
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")
BACKUP_NAME="backup_${TIMESTAMP}.sql.gz"

mkdir -p "$BACKUP_DIR"
mkdir -p "$(dirname "$LOG_FILE")"


log_message() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log_message "Starting backup process for ${POSTGRES_DB}..."


if docker-compose exec -T db pg_dump -U ${POSTGRES_RIGHTFUL_USER} ${POSTGRES_DB} | gzip > "${BACKUP_DIR}/${BACKUP_NAME}"; then
    log_message "SUCCESS: Backup created: ${BACKUP_NAME}"
else
    log_message "ERROR: Backup failed! Check docker-compose logs db"
    exit 1
fi


log_message "Cleaning up backups older than ${KEEP_DAYS} days..."
find "$BACKUP_DIR" -name "backup_*.sql.gz" -type f -mtime +${KEEP_DAYS} -exec rm {} \; -print | while read -r file; do
    log_message "REMOVED OLD BACKUP: $file"
done

log_message "Backup process finished"
