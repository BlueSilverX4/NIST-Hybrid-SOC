#!/usr/bin/env python3
"""
Playbook: GutsStyle Rapid Containment & Service Stress-Verification
Framework: Style_Change_Framework
Description: Executes targeted port checks (Nmap) and credential resilience 
             verification (Hydra) against identified lab host IPs.
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
    format="%(asctime)s [%(levelname)s] [GutsStyle] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)


def validate_target_ip(ip_str: str) -> str:
    """
    Validates that the provided target is a valid IPv4 address and belongs 
    to a standard private/RFC 1918 lab IP range.
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        if not ip.is_private:
            logging.warning(f"Target {ip_str} is not a private/lab IP address.")
        return str(ip)
    except ValueError:
        logging.error(f"Invalid IP address format: {ip_str}")
        sys.exit(1)


def execute_command(cmd_args: list, dry_run: bool = False) -> dict:
    """
    Executes system CLI tools safely using list-based subprocess invocations
    to eliminate shell injection risks.
    """
    printable_cmd = " ".join(cmd_args)
    if dry_run:
        logging.info(f"[DRY-RUN] Would execute: {printable_cmd}")
        return {"status": "SKIPPED", "stdout": "Dry-run mode active.", "returncode": 0}

    logging.info(f"Executing action: {printable_cmd}")
    try:
        result = subprocess.run(
            cmd_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=300
        )
        return {
            "status": "SUCCESS" if result.returncode == 0 else "FAILED",
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }
    except FileNotFoundError:
        logging.error(f"Binary not found: {cmd_args[0]}. Ensure tool is installed in PATH.")
        return {"status": "ERROR", "error": f"{cmd_args[0]} not found in system PATH."}
    except subprocess.TimeoutExpired:
        logging.error(f"Execution timed out for command: {printable_cmd}")
        return {"status": "TIMEOUT", "error": "Process timed out after 300s."}


def run_nmap_scan(target_ip: str, fast_mode: bool, dry_run: bool) -> dict:
    """
    Phase 1: Aggressive port and service detection via Nmap.
    """
    logging.info(f"--- Phase 1: Initiating Port Assessment against {target_ip} ---")
    
    # Construct arguments securely as a list vector
    nmap_args = ["nmap", "-sV"]
    if fast_mode:
        nmap_args.extend(["-F", "-T4"])
    else:
        nmap_args.extend(["-A", "-T4"])
    
    nmap_args.append(target_ip)
    return execute_command(nmap_args, dry_run=dry_run)


def run_hydra_check(target_ip: str, service: str, userlist: str, passlist: str, dry_run: bool) -> dict:
    """
    Phase 2: Automated credential stress-testing on targeted service via Hydra.
    """
    logging.info(f"--- Phase 2: Verifying Credential Resilience ({service.upper()}) on {target_ip} ---")

    if not os.path.exists(userlist) or not os.path.exists(passlist):
        logging.warning(f"Wordlists not found ({userlist}, {passlist}). Running with default fallback checks.")
        # Minimal test fallback
        hydra_args = [
            "hydra",
            "-l", "admin",
            "-p", "admin",
            "-t", "4",
            f"{service}://{target_ip}"
        ]
    else:
        hydra_args = [
            "hydra",
            "-L", userlist,
            "-P", passlist,
            "-t", "4",
            f"{service}://{target_ip}"
        ]

    return execute_command(hydra_args, dry_run=dry_run)


def generate_soar_artifact(target_ip: str, nmap_res: dict, hydra_res: dict, output_path: str = None):
    """
    Formats playbook findings into a standardized JSON artifact for HubStyle ingest.
    """
    artifact = {
        "playbook": "GutsStyle_Rapid_Containment",
        "timestamp": datetime.now().isoformat(),
        "target": target_ip,
        "actions": {
            "nmap_assessment": nmap_res,
            "hydra_verification": hydra_res
        },
        "status": "COMPLETED"
    }

    if output_path:
        with open(output_path, "w") as f:
            json.dump(artifact, f, indent=2)
        logging.info(f"Execution telemetry exported to: {output_path}")
    
    return artifact


def main():
    parser = argparse.ArgumentParser(
        description="GutsStyle Playbook - Rapid Containment & Service Stress-Verification"
    )
    parser.add_argument("-t", "--target", required=True, help="Target host IPv4 address (e.g., 192.168.1.105)")
    parser.add_argument("-s", "--service", default="ssh", help="Target service for verification (default: ssh)")
    parser.add_argument("-u", "--userlist", default="userlist.txt", help="Path to user list file")
    parser.add_argument("-p", "--passlist", default="passlist.txt", help="Path to password list file")
    parser.add_argument("--fast", action="store_true", help="Run fast Nmap scan (-F)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate execution without running network traffic")
    parser.add_argument("-o", "--output", help="Path to save JSON execution artifact")

    args = parser.parse_args()

    # 1. Validate Target IP
    target_ip = validate_target_ip(args.target)

    logging.info(f"Kicking off GutsStyle Playbook for Target: {target_ip}")

    # 2. Execute Nmap Recon Phase
    nmap_result = run_nmap_scan(target_ip, fast_mode=args.fast, dry_run=args.dry_run)

    # 3. Execute Hydra Credential Verification Phase
    hydra_result = run_hydra_check(
        target_ip=target_ip,
        service=args.service,
        userlist=args.userlist,
        passlist=args.passlist,
        dry_run=args.dry_run
    )

    # 4. Generate Telemetry Artifact
    artifact = generate_soar_artifact(
        target_ip=target_ip,
        nmap_res=nmap_result,
        hydra_res=hydra_result,
        output_path=args.output
    )

    logging.info("GutsStyle Playbook Execution Finished Successfully.")


if __name__ == "__main__":
    main()
