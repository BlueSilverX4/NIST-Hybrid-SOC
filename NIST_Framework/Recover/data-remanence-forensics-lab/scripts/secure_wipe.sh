#!/bin/bash

# Secure Block Device Sanitization Script
# Updated with Portfolio Storage Fail-Safe Integration

if [ "$EUID" -ne 0 ]; then
  echo "[-] Error: Please run this script using sudo."
  exit 1
fi

echo "[*] Current Active Block Devices:"
lsblk -o NAME,SIZE,TYPE,LABEL,MOUNTPOINTS
echo "------------------------------------------------"

read -p "[?] Enter the partition target to securely wipe (e.g., sdc1): " TARGET
DEV_PATH="/dev/$TARGET"

if [ ! -b "$DEV_PATH" ]; then
  echo "[-] Error: Device node $DEV_PATH does not exist."
  exit 1
fi

# ==========================================================
#                      FAIL-SAFE CHECK
# ==========================================================
# Extract the unique volume label of the chosen partition
TARGET_LABEL=$(lsblk -o LABEL -n "$DEV_PATH" 2>/dev/null | xargs)

# CRITICAL PROTECTION: Change "BGREGG_LAB" if your actual drive has a different name
PROTECTED_NAME="BGREGG_LAB"

if [[ "$TARGET_LABEL" == "$PROTECTED_NAME" ]]; then
    echo -e "\n\e[31m[-] CRITICAL SAFETY HALT: Selected target matches protected volume: [$TARGET_LABEL]\e[0m"
    echo "[-] Execution automatically aborted to protect repository assets from accidental loss."
    exit 1
fi
# ==========================================================

echo "[*] Analyzing mount layout for $DEV_PATH..."

if mountpoint -q /run/media/*/"$TARGET" 2>/dev/null || grep -q "$DEV_PATH" /proc/mounts; then
    echo "[!] Target is currently active or locked by system application threads."
    echo "[*] Initiating defensive lazy unmount sequence..."
    sudo umount -l "$DEV_PATH"
    sleep 2
fi

echo "[+] Target isolated. Commencing sequential physical block scrambling..."
echo "[!] WARNING: This will permanently scramble all data structures on $DEV_PATH!"
read -p "[?] Are you absolutely sure you want to proceed? (y/N): " CONFIRM

if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
    sudo shred -v -n 1 "$DEV_PATH"
    echo "[+] Block sanitization sequence completed successfully."
else
    echo "[-] Operation aborted by user."
    exit 0
fi
