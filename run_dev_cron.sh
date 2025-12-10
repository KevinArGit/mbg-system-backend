#!/bin/bash

# This script simulates the cron job for development purposes.
# Run it in a SEPARATE terminal window.

# Ensure DATABASE_URL is set in this terminal session if not already
# Example: export DATABASE_URL="postgresql://user:password@host:5432/dbname?sslmode=require"

DATABASE_URL="postgresql://neondb_owner:npg_gE0FuUrIAD7X@ep-twilight-term-a1j7pbr6-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
PROJECT_DIR="/home/kevin/Projects/mbg-system-backend"
VENV_PATH="${PROJECT_DIR}/.venv/bin"
LOG_FILE="${PROJECT_DIR}/cron_dev.log" # Output logs to a file within your project

echo "Starting development cron job simulator. Press Ctrl+C to stop."
echo "Logs for this simulator will be written to ${LOG_FILE}"

while true; do
    echo "--- Running process-logs at $(date) ---" | tee -a "$LOG_FILE"
    cd "$PROJECT_DIR" && FLASK_APP=run.py "${VENV_PATH}/flask" process-logs >> "$LOG_FILE" 2>&1
    echo "--- Finished process-logs ---" | tee -a "$LOG_FILE"
    
    echo "Sleeping for 1 minute..." | tee -a "$LOG_FILE"
    sleep 60 # Sleep for 1 minute (60 seconds)
done
