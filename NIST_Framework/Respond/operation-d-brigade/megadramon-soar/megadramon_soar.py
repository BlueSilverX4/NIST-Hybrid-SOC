#!/usr/bin/env python3
"""
Operation D-Brigade: Megadramon SOAR Containment Engine
Listens for Guardromon log entries and dynamically injects iptables drop rules.
"""

import os
import re
import subprocess
import sys
import time

LOG_FILE = "/var/log/brigadramon-c2.log"
TRIGGER_PREFIX = "[GUARDROMON-DROP]"
BLOCKED_IPS = set()


def check_root():
    """Ensure script is executed with root privileges to modify iptables."""
    if os.geteuid() != 0:
        print("[-] Megadramon requires root privileges to manipulate iptables.")
        print("    Run with: sudo python3 megadramon_soar.py")
        sys.exit(1)


def block_ip(ip_address):
    """Executes Megadramon Containment: Appends a dynamic iptables rule to drop all traffic from IP."""
    if ip_address in BLOCKED_IPS:
        return

    print(
        f"[!] Megadramon Triggered: ERADICATION ATTACK against offensive IP -> {ip_address}"
    )

    # Check if rule already exists in iptables
    check_cmd = ["iptables", "-C", "INPUT", "-s", ip_address, "-j", "DROP"]
    check_result = subprocess.run(
        check_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    if check_result.returncode != 0:
        # Rule does not exist; insert drop rule at top of INPUT chain
        block_cmd = ["iptables", "-I", "INPUT", "1", "-s", ip_address, "-j", "DROP"]
        res = subprocess.run(block_cmd, capture_output=True, text=True)

        if res.returncode == 0:
            print(
                f"[+] Megadramon Containment Successful: IP {ip_address} blocked on INPUT chain."
            )
            BLOCKED_IPS.add(ip_address)
        else:
            print(
                f"[-] Error executing iptables rule for {ip_address}: {res.stderr}"
            )
    else:
        print(f"[*] IP {ip_address} is already in the iptables block list.")
        BLOCKED_IPS.add(ip_address)


def monitor_logs():
    """Tails the system log file continuously to intercept Guardromon drop events."""
    print(f"[+] Megadramon SOAR Engine active. Monitoring {LOG_FILE}...")

    # Regex to extract IPv4 source address from syslog packet logs
    ip_regex = re.compile(r"SRC=([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})")

    try:
        with open(LOG_FILE, "r") as f:
            # Move file pointer to the end to avoid processing old historical logs
            f.seek(0, os.SEEK_END)

            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    continue

                if TRIGGER_PREFIX in line:
                    match = ip_regex.search(line)
                    if match:
                        src_ip = match.group(1)
                        # Ignore local loopback triggers
                        if src_ip != "127.0.0.1":
                            block_ip(src_ip)
    except KeyboardInterrupt:
        print("\n[*] Megadramon SOAR Engine standing down.")
    except FileNotFoundError:
        print(f"[-] Log file {LOG_FILE} not found. Ensure rsyslog is running.")


if __name__ == "__main__":
    check_root()
    monitor_logs()
