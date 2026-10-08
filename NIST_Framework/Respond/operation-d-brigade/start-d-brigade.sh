#!/usr/bin/env bash
# ==============================================================================
# Operation D-Brigade: Master Pipeline Orchestrator
# Applies Guardromon firewall rules and launches Megadramon SOAR engine.
# ==============================================================================

# Ensure script is executed with root privileges
if [ "$EUID" -ne 0 ]; then
  echo "[-] Error: Operation D-Brigade orchestrator requires root privileges."
  echo "    Please run with: sudo ./start-d-brigade.sh"
  exit 1
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUARDROMON_SCRIPT="$PROJECT_ROOT/guardromon-perimeter/guardromon-firewall.sh"
MEGADRAMON_SCRIPT="$PROJECT_ROOT/megadramon-soar/megadramon_soar.py"

echo "================================================================="
echo "       OPERATION D-BRIGADE: METAL EMPIRE SOC DEFENSE GRID        "
echo "================================================================="

# 1. Verify required scripts exist
if [ ! -f "$GUARDROMON_SCRIPT" ]; then
  echo "[-] Error: Guardromon script not found at $GUARDROMON_SCRIPT"
  exit 1
fi

if [ ! -f "$MEGADRAMON_SCRIPT" ]; then
  echo "[-] Error: Megadramon script not found at $MEGADRAMON_SCRIPT"
  exit 1
fi

# 2. Deploy Guardromon Perimeter Rules
echo ""
echo "[1/2] Deploying Guardromon Heavy Armor Perimeter Rules..."
chmod +x "$GUARDROMON_SCRIPT"
bash "$GUARDROMON_SCRIPT"

if [ $? -eq 0 ]; then
  echo "[+] Guardromon Perimeter Baseline successfully activated."
else
  echo "[-] Error deploying Guardromon firewall rules."
  exit 1
fi

# 3. Launch Megadramon SOAR Engine
echo ""
echo "[2/2] Booting Megadramon Automated SOAR Containment Engine..."
echo "[+] Press Ctrl+C at any time to stand down the D-Brigade defense grid."
echo "================================================================="
echo ""

python3 "$MEGADRAMON_SCRIPT"
