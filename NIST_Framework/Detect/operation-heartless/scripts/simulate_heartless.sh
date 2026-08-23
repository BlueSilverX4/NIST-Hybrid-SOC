#!/bin/bash
# Operation Heartless - Telemetry Generator

LOG_FILE="../logs/sample_auth.log"

echo "[i] Generating simulated Heartless threat activity..."

# Low severity - Shadow alert
echo "$(date '+%b %d %H:%M:%S') target-node sshd[1234]: Failed password for invalid user heartless_spawn from 192.168.1.100 port 45678 ssh2" >> "$LOG_FILE"

# Critical severity - Darkside alert
echo "$(date '+%b %d %H:%M:%S') target-node sudo: heartless_spawn : TTY=pts/0 ; PWD=/home/user ; USER=root ; COMMAND=/bin/bash" >> "$LOG_FILE"

echo "[+] Simulated telemetry written to $LOG_FILE"
