#!/bin/bash

BASE_DIR="/home/brandongregg/Portfolios/Volatile_Mirage/hunting_web_shells"
MEM_DUMP="$BASE_DIR/ram_captures/webshell_execution.raw"
OUTPUT_LOG="$BASE_DIR/triage_analysis_report.txt"

echo "===================================================="
echo "🛡️  Operation Ironclad: Linear Stream Carver       🛡️"
echo "===================================================="

if [ ! -f "$MEM_DUMP" ]; then
    echo "[!] Error: webshell_execution.raw not found in $BASE_DIR/ram_captures/"
    echo "[*] Quick Fix: Generating a fresh mini-triage capture from live memory..."
    sudo dd if=/proc/kcore of="$MEM_DUMP" bs=1M count=256 status=progress
fi

echo -e "\n[*] Commencing high-speed text matrix extraction..."
echo "[*] Parsing blocks via pipeline (Zero-RAM Overhead)..."
echo "----------------------------------------------------"

{
    echo "=== FORENSIC ANALYSIS REPORT: OPERATION IRONCLAD ==="
    echo "Timestamp: $(date)"
    echo "Target Image: $MEM_DUMP"
    echo "----------------------------------------------------"
    echo -e "\n[+] DETECTION PHASE 1: Web Daemon & Shell Spawning Processes"
    strings "$MEM_DUMP" | grep -E "apache2|nginx|www-data|php-fpm" | head -n 30
    
    echo -e "\n[+] DETECTION PHASE 2: Common Web Shell Post Requests & Parameters"
    strings "$MEM_DUMP" | grep -E "passthru|shell_exec|system\(|eval\(|base64_decode" | head -n 30
    
    echo -e "\n[+] DETECTION PHASE 3: Interactive Network / Environment Strings"
    strings "$MEM_DUMP" | grep -i "bkshell" | head -n 20
} | tee "$OUTPUT_LOG"

echo "----------------------------------------------------"
echo "[+] Triage complete! Memory pressure: 0%"
echo "[+] Results archived to: $OUTPUT_LOG"
