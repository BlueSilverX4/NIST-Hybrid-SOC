#!/bin/bash

# Automated Data Remanence & Forensic Verification Audit

if [ "$EUID" -ne 0 ]; then
  echo "[-] Error: Please run this script using sudo."
  exit 1
fi

read -p "[?] Enter the partition target to forensically audit (e.g., sdc1): " TARGET
DEV_PATH="/dev/$TARGET"

if [ ! -b "$DEV_PATH" ]; then
  echo "[-] Error: Device path $DEV_PATH not found."
  exit 1
fi

OUTPUT_FILE="$HOME/Desktop/Post_Wipe_Verification.txt"

echo "[*] Extracting raw binary strings from $DEV_PATH..."
echo "[*] Piping output structures directly to: $OUTPUT_FILE"
sudo strings "$DEV_PATH" > "$OUTPUT_FILE"

echo "[*] Running regex validation loops against target signatures..."
echo "------------------------------------------------"

KEYWORDS=("CIA secrets" "Sensitive_Data" "Confidential")
LEAKS_FOUND=0

for KEYWORD in "${KEYWORDS[@]}"; do
    echo -n "[*] Scanning for marker: '$KEYWORD' -> "
    MATCH_COUNT=$(grep -i -c "$KEYWORD" "$OUTPUT_FILE")
    
    if [ "$MATCH_COUNT" -gt 0 ]; then
        echo -e "\e[31m[!] CRITICAL LEAK ENCOUNTERED ($MATCH_COUNT matches found!)\e[0m"
        grep -i -n "$KEYWORD" "$OUTPUT_FILE"
        LEAKS_FOUND=$((LEAKS_FOUND + 1))
    else
        echo -e "\e[32m[+] Sterile (0 Matches)\e[0m"
    fi
done

echo "------------------------------------------------"
if [ "$LEAKS_FOUND" -eq 0 ]; then
    echo -e "\e[32m[+] AUDIT PASS: Compliance verified. Total device sterilization achieved.\e[0m"
else
    echo -e "\e[31m[-] AUDIT FAIL: Data remanence markers detected in unallocated space.\e[0m"
fi
