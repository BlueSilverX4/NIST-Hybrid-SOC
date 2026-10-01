import json
import os
import requests
import ipaddress

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, "conn.log")
VT_SERVICE_URL = "http://127.0.0.1:5000/lookup/ip/"

seen_ips = set()

if not os.path.exists(LOG_PATH):
    print(f"[!] Error: {LOG_PATH} not found.")
    exit(1)

with open(LOG_PATH, "r") as f:
    for line in f:
        if line.startswith("#"):
            continue
        try:
            data = json.loads(line)
            dest_ip = data.get("id.resp_h")
            
            if dest_ip and dest_ip not in seen_ips:
                try:
                    ip_obj = ipaddress.ip_address(dest_ip)
                    # Skip non-public, multicast, and IPv6 addresses locally
                    if ip_obj.is_private or ip_obj.is_multicast or ip_obj.is_reserved or ip_obj.is_loopback or ip_obj.version == 6:
                        continue
                except ValueError:
                    continue

                seen_ips.add(dest_ip)
                print(f"[*] Querying Threat Intel for External IP: {dest_ip}")
                try:
                    res = requests.get(f"{VT_SERVICE_URL}{dest_ip}")
                    if res.status_code == 200:
                        print(f"    [+] Result: {res.json()}")
                    else:
                        print(f"    [-] API Error ({res.status_code}): {res.text}")
                except requests.exceptions.ConnectionError:
                    print("    [!] Connection refused. Ensure threat_intel.py is running on port 5000.")
        except json.JSONDecodeError:
            continue
