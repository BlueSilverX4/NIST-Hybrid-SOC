#!/bin/bash

BASE_DIR="/home/brandongregg/Portfolios/Volatile_Mirage/hunting_web_shells"
VOL_DIR="$BASE_DIR/tools/volatility3"
MEM_DUMP="$BASE_DIR/ram_captures/webshell_execution.raw"

echo "===================================================="
echo "🛡️  Operation Ironclad: Web Shell Memory Hunter 🛡️"
echo "===================================================="
echo "[*] Pivoting to Volatility 3 engine..."
cd "$VOL_DIR" || exit

echo "[*] Executing full kernel process tree analysis..."
echo "----------------------------------------------------"
python3 vol.py -f "$MEM_DUMP" linux.pslist.PsList
