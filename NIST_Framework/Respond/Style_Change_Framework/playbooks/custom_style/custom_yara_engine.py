#!/usr/bin/env python3
"""
Playbook: CustomStyle Dynamic YARA Rule Generation & Detection Testing
Framework: Style_Change_Framework
Description: Auto-generates customized YARA detection rules from target IOC strings/bytes
             and scans target files to verify detection signatures.
NIST Mapping: Post-Incident Activity & Threat Hunting (SP 800-53 / SI-4 Monitoring)
"""

import argparse
import json
import logging
import os
import re
import subprocess
import sys
from datetime import datetime

# Configure Structured Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [CustomStyle] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)


def sanitize_rule_name(raw_name: str) -> str:
    """
    Sanitizes rule names to ensure strict YARA identifier compatibility.
    """
    clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', raw_name)
    if clean_name[0].isdigit():
        clean_name = f"rule_{clean_name}"
    return clean_name


def generate_yara_rule(rule_name: str, target_strings: list, author: str = "CustomStyle_SOAR") -> str:
    """
    Constructs a syntactically valid YARA detection rule string.
    """
    clean_name = sanitize_rule_name(rule_name)
    date_str = datetime.now().strftime("%Y-%m-%d")

    string_definitions = []
    for idx, s in enumerate(target_strings):
        string_definitions.append(f'        $str_{idx} = "{s}" ascii wide nocase')

    strings_block = "\n".join(string_definitions)

    yara_template = f"""rule {clean_name} {{
    meta:
        author = "{author}"
        date = "{date_str}"
        description = "Auto-generated CustomStyle detection rule"
        framework = "Style_Change_Framework"

    strings:
{strings_block}

    condition:
        any of ($str_*)
}}
"""
    return yara_template


def run_yara_scan(rule_file: str, target_file: str, dry_run: bool = False) -> dict:
    """
    Executes the YARA CLI tool against a target file using the generated rule.
    """
    if dry_run:
        logging.info(f"[DRY-RUN] Would execute: yara {rule_file} {target_file}")
        return {
            "status": "SKIPPED",
            "matches": [f"CustomStyle_Mock_Rule {target_file}"],
            "returncode": 0
        }

    cmd = ["yara", rule_file, target_file]
    logging.info(f"Executing YARA scan: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )
        matches = result.stdout.strip().splitlines() if result.stdout else []
        return {
            "status": "MATCH_FOUND" if matches else "NO_MATCH",
            "matches": matches,
            "returncode": result.returncode,
            "stderr": result.stderr.strip()
        }
    except FileNotFoundError:
        logging.error("YARA binary not found in PATH. Install yara via 'sudo apt install yara'.")
        return {"status": "ERROR", "error": "yara executable missing"}
    except Exception as e:
        logging.error(f"YARA scan execution failed: {e}")
        return {"status": "ERROR", "error": str(e)}


def export_custom_telemetry(rule_name: str, rule_path: str, scan_results: dict, output_path: str = None) -> dict:
    """
    Exports CustomStyle YARA generation and detection results into a SOAR artifact.
    """
    artifact = {
        "playbook": "CustomStyle_YARA_Engine",
        "timestamp": datetime.now().isoformat(),
        "rule_name": rule_name,
        "rule_path": rule_path,
        "detection_results": scan_results,
        "status": "COMPLETED"
    }

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(artifact, f, indent=2)
        logging.info(f"CustomStyle telemetry exported to: {output_path}")

    return artifact


def main():
    parser = argparse.ArgumentParser(
        description="CustomStyle Playbook - Dynamic YARA Rule Generation & Detection Testing"
    )
    parser.add_argument("-n", "--name", default="CustomThreat_Detection", help="YARA rule name identifier")
    parser.add_argument("-s", "--strings", nargs="+", default=["cmd.exe /c", "eval(base64_decode"], help="Space-separated list of strings to detect")
    parser.add_argument("-t", "--target-file", help="Path to file to scan with generated rule")
    parser.add_argument("-r", "--rule-out", default="playbooks/custom_style/generated_rule.yar", help="Path to write the generated YARA rule")
    parser.add_argument("--dry-run", action="store_true", help="Simulate YARA scan execution")
    parser.add_argument("-o", "--output", help="Path to export JSON telemetry artifact")

    args = parser.parse_args()

    logging.info(f"Initiating CustomStyle YARA Engine for Rule: {args.name}")

    # 1. Auto-Generate YARA Rule File
    yara_content = generate_yara_rule(args.name, args.strings)
    
    os.makedirs(os.path.dirname(os.path.abspath(args.rule_out)), exist_ok=True)
    with open(args.rule_out, "w") as f:
        f.write(yara_content)
    logging.info(f"Generated YARA rule written to: {args.rule_out}")

    # 2. Execute YARA Scan if target file is provided
    scan_results = {}
    if args.target_file:
        if not os.path.exists(args.target_file) and not args.dry_run:
            logging.error(f"Target file for scanning not found: {args.target_file}")
            sys.exit(1)
        scan_results = run_yara_scan(args.rule_out, args.target_file, dry_run=args.dry_run)
    else:
        scan_results = {"status": "RULE_GENERATED_ONLY"}

    # 3. Export Telemetry
    export_custom_telemetry(
        rule_name=args.name,
        rule_path=args.rule_out,
        scan_results=scan_results,
        output_path=args.output
    )

    logging.info("CustomStyle YARA Engine Execution Completed Successfully.")


if __name__ == "__main__":
    main()
