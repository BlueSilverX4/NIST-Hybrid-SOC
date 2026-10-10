#!/usr/bin/env python3
"""
Playbook: ShieldStyle Active Hardening & Defense
Framework: Style_Change_Framework
Description: Executes host-level defensive hardening, applies iptables/ufw dynamic 
             drops for malicious IPs, and enforces local service mitigation rules.
NIST Mapping: Containment, Eradication & Recovery (SP 800-61) / SI-4 Monitoring (SP 800-53)
"""

import argparse
import ipaddress
import json
import logging
import os
import subprocess
import sys
from datetime import datetime

# Configure Structured Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [ShieldStyle] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)


def validate_ip(ip_str: str) -> str:
    """
    Validates the format of an IP address before passing to firewall rules.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return str(ip)
    except ValueError:
        logging.error(f"Invalid IP address supplied for mitigation: {ip_str}")
        sys.exit(1)


def execute_command(cmd_args: list, dry_run: bool = False) -> dict:
    """
    Executes CLI system utilities using safe list vectors to prevent shell injection.
    """
    printable_cmd = " ".join(cmd_args)
    if dry_run:
        logging.info(f"[DRY-RUN] Would execute: {printable_cmd}")
        return {"status": "SKIPPED", "stdout": "Dry-run mode active.", "returncode": 0}

    logging.info(f"Executing defense command: {printable_cmd}")
    try:
        result = subprocess.run(
            cmd_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )
        return {
            "status": "SUCCESS" if result.returncode == 0 else "FAILED",
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }
    except FileNotFoundError:
        logging.error(f"Binary not found: {cmd_args[0]}")
        return {"status": "ERROR", "error": f"{cmd_args[0]} not found in system PATH."}
    except Exception as e:
        logging.error(f"Execution error: {e}")
        return {"status": "ERROR", "error": str(e)}


def apply_iptables_block(block_ip: str, dry_run: bool = False) -> dict:
    """
    Applies an immediate DROP rule in iptables for the flagged source IP.
    """
    logging.info(f"--- Deploying Shield Barrier (iptables DROP) against: {block_ip} ---")
    cmd = ["sudo", "iptables", "-A", "INPUT", "-s", block_ip, "-j", "DROP"]
    return execute_command(cmd, dry_run=dry_run)


def apply_ufw_block(block_ip: str, dry_run: bool = False) -> dict:
    """
    Applies a deny rule in UFW (Uncomplicated Firewall) for the flagged source IP.
    """
    logging.info(f"--- Deploying Shield Barrier (UFW Deny) against: {block_ip} ---")
    cmd = ["sudo", "ufw", "deny", "from", block_ip, "to", "any"]
    return execute_command(cmd, dry_run=dry_run)


def export_shield_telemetry(block_ip: str, action_results: dict, output_path: str = None) -> dict:
    """
    Formats mitigation actions into a standard ShieldStyle telemetry payload.
    """
    artifact = {
        "playbook": "ShieldStyle_Active_Hardening",
        "timestamp": datetime.now().isoformat(),
        "mitigated_target": block_ip,
        "actions_taken": action_results,
        "status": "COMPLETED"
    }

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(artifact, f, indent=2)
        logging.info(f"ShieldStyle telemetry exported to: {output_path}")

    return artifact


def main():
    parser = argparse.ArgumentParser(
        description="ShieldStyle Playbook - Automated Defense & Firewall Hardening"
    )
    parser.add_argument("-b", "--block-ip", required=True, help="Source IP to isolate/block (e.g., 10.0.0.50)")
    parser.add_argument("--engine", choices=["iptables", "ufw"], default="iptables", help="Firewall engine to use")
    parser.add_argument("--dry-run", action="store_true", help="Simulate rule enforcement without modifying system firewall")
    parser.add_argument("-o", "--output", help="Path to export JSON telemetry artifact")

    args = parser.parse_args()

    # 1. Validate Target IP
    target_ip = validate_ip(args.block_ip)

    logging.info(f"Engaging ShieldStyle Hardening against source: {target_ip}")

    # 2. Execute Barrier Deployment
    if args.engine == "ufw":
        result = apply_ufw_block(target_ip, dry_run=args.dry_run)
    else:
        result = apply_iptables_block(target_ip, dry_run=args.dry_run)

    # 3. Export Telemetry Artifact
    export_shield_telemetry(
        block_ip=target_ip,
        action_results={args.engine: result},
        output_path=args.output
    )

    logging.info("ShieldStyle Playbook Execution Completed Successfully.")


if __name__ == "__main__":
    main()
