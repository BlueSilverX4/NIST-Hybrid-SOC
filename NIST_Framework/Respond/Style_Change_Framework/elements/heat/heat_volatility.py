#!/usr/bin/env python3
"""
Element: Heat Element (Linux / Host OS Forensics)
Framework: Style_Change_Framework
Description: Executes Volatility 3 plugins against host memory dumps to analyze
             process trees, network connections, and loaded kernel modules.
"""

import argparse
import json
import logging
import os
import subprocess
import sys
from datetime import datetime

# Configure Structured Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [Element:Heat] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)


def verify_volatility_installation() -> str:
    """
    Checks whether Volatility 3 is available in PATH or accessible via Python module.
    Returns the command invocation string.
    """
    # Check for CLI executable 'vol' or 'volatility3'
    for binary in ["vol", "volatility3", "vol.py"]:
        try:
            res = subprocess.run([binary, "-h"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if res.returncode == 0:
                logging.info(f"Volatility 3 framework detected using binary: '{binary}'")
                return binary
        except FileNotFoundError:
            continue

    logging.warning("Volatility 3 CLI binary not found directly in PATH. Fallback to 'python3 -m volatility3.cli'")
    return f"{sys.executable} -m volatility3.cli"


def run_volatility_plugin(vol_cmd: str, mem_dump: str, plugin: str, OS_type: str, dry_run: bool = False) -> dict:
    """
    Executes a specific Volatility 3 plugin against a memory image and captures JSON/Text output.
    """
    # Format plugin name based on OS type (linux or windows)
    full_plugin = f"{OS_type}.{plugin}"
    
    # Base command array
    if " " in vol_cmd:
        cmd_args = vol_cmd.split() + ["-f", mem_dump, full_plugin]
    else:
        cmd_args = [vol_cmd, "-f", mem_dump, full_plugin]

    printable_cmd = " ".join(cmd_args)

    if dry_run:
        logging.info(f"[DRY-RUN] Would execute Volatility plugin: {printable_cmd}")
        return {
            "plugin": full_plugin,
            "status": "SKIPPED",
            "output": "Dry-run mode active. No memory analysis performed."
        }

    logging.info(f"Executing Volatility 3 plugin: {full_plugin}")
    try:
        result = subprocess.run(
            cmd_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=600
        )
        return {
            "plugin": full_plugin,
            "status": "SUCCESS" if result.returncode == 0 else "FAILED",
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }
    except FileNotFoundError:
        logging.error(f"Failed to execute command: {printable_cmd}")
        return {"plugin": full_plugin, "status": "ERROR", "error": "Volatility 3 executable not found."}
    except subprocess.TimeoutExpired:
        logging.error(f"Plugin execution timed out: {full_plugin}")
        return {"plugin": full_plugin, "status": "TIMEOUT", "error": "Analysis timed out after 600s."}


def analyze_memory_dump(mem_dump: str, OS_type: str, dry_run: bool = False) -> dict:
    """
    Runs a standard triage suite of Volatility 3 plugins corresponding to the Heat Element.
    """
    logging.info(f"--- Initiating Heat Element Memory Triage on: {mem_dump} ---")
    vol_cmd = verify_volatility_installation()

    # Plugins to run based on OS targeted
    if OS_type.lower() == "linux":
        plugins = ["pslist.PsList", "netstat.NetStat", "lsmod.Lsmod"]
    else:
        plugins = ["pslist.PsList", "netscan.NetScan", "modules.Modules"]

    analysis_results = {}
    for plugin in plugins:
        res = run_volatility_plugin(vol_cmd, mem_dump, plugin, OS_type, dry_run=dry_run)
        analysis_results[plugin] = res

    return analysis_results


def export_heat_telemetry(mem_dump: str, analysis_data: dict, output_path: str = None) -> dict:
    """
    Formats memory findings into a standardized Heat Element SOAR telemetry payload.
    """
    artifact = {
        "element": "Heat",
        "domain": "Host OS & Memory Forensics",
        "timestamp": datetime.now().isoformat(),
        "memory_file": mem_dump,
        "plugin_results": analysis_data,
        "status": "COMPLETED"
    }

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(artifact, f, indent=2)
        logging.info(f"Heat Element telemetry exported to: {output_path}")

    return artifact


def main():
    parser = argparse.ArgumentParser(
        description="Heat Element - Volatility 3 Host Memory Analysis Module"
    )
    parser.add_argument("-f", "--file", required=True, help="Path to raw RAM/memory dump file (e.g., mem.raw, vmem)")
    parser.add_argument("--os", default="linux", choices=["linux", "windows"], help="Target OS type for plugins (default: linux)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate Volatility execution without parsing file")
    parser.add_argument("-o", "--output", help="Path to save JSON telemetry output artifact")

    args = parser.parse_args()

    # Validate Memory Dump File existence if not dry-run
    if not args.dry_run and not os.path.exists(args.file):
        logging.error(f"Memory dump file not found: {args.file}")
        sys.exit(1)

    # 1. Run Memory Analysis Suite
    analysis_results = analyze_memory_dump(args.file, args.os, dry_run=args.dry_run)

    # 2. Export Telemetry
    export_heat_telemetry(args.file, analysis_results, output_path=args.output)

    logging.info("Heat Element Memory Forensics Completed Successfully.")


if __name__ == "__main__":
    main()
