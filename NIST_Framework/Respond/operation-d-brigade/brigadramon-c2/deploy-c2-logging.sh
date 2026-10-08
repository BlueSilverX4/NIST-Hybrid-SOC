#!/usr/bin/env bash
# operation-d-brigade/brigadramon-c2/deploy-c2-logging.sh

if [ "$EUID" -ne 0 ]; then
  echo "[-] Please run as root: sudo ./deploy-c2-logging.sh"
  exit 1
fi

C2_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONF_SRC="$C2_DIR/50-brigadramon.conf"
CONF_DEST="/etc/rsyslog.d/50-brigadramon.conf"

echo "[+] Deploying Brigadramon C2 Rsyslog Configuration..."

# Copy configuration to rsyslog directory
cp "$CONF_SRC" "$CONF_DEST"

# Touch log file and ensure appropriate permissions
touch /var/log/brigadramon-c2.log
chmod 644 /var/log/brigadramon-c2.log

# Restart rsyslog service
systemctl restart rsyslog

echo "[+] Brigadramon C2 Logging active -> Listening on /var/log/brigadramon-c2.log"
