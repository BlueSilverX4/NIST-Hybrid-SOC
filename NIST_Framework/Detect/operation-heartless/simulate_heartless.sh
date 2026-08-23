#!/bin/bash

LOG_FILE="sample_auth.log"

echo "[*] Injecting 5 rapid SSH failed login entries into $LOG_FILE..."

# Generate current ISO/syslog timestamp
TIMESTAMP=$(date +"%b %d %H:%M:%S")

# Burst 5 failed password attempts
for i in {1..5}; do
    echo "$TIMESTAMP target-node sshd[$(shuf -i 1000-9999 -n 1)]: Failed password for invalid user heartless_$i from 192.168.1.100 port $(shuf -i 30000-60000 -n 1) ssh2" >> "$LOG_FILE"
    sleep 0.2
done

echo "[+] Injected 5 entries into $LOG_FILE successfully."
