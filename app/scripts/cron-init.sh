#!/bin/bash

PROJECT_PATH=$(pwd)
SCRIPT_PATH="$PROJECT_PATH/scripts/backup.sh"
LOG_FILE="$PROJECT_PATH/log/cron.log"


log_install() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] CRON_SETUP: $1" | tee -a "$LOG_FILE"
}

chmod +x "$SCRIPT_PATH"
mkdir -p "$(dirname "$LOG_FILE")"

crontab -l > mycron 2>/dev/null || true

if grep -q "$SCRIPT_PATH" mycron; then
    log_install "Task is already registered."
else
    echo "0 3 * * * cd $PROJECT_PATH && $SCRIPT_PATH >> $LOG_FILE 2>&1" >> mycron
    crontab mycron
    log_install "Task has been registered(03:00 daily)."
fi

rm mycron
