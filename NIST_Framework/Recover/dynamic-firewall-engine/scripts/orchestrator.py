import time
import json
import re
from firewall_manager import apply_block

# Load Config
with open("configs/config.json", "r") as f:
    config = json.load(f)

def monitor():
    print(f"[*] Starting Security Orchestrator...")
    with open(config["log_file"], "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if config["threat_keyword"] in line:
                ip = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                if ip:
                    ip_addr = ip.group(1)
                    print(f"[!] Threat Found: {ip_addr}. Applying Block...")
                    if apply_block(ip_addr, config["target_chain"]):
                        print(f"[+] Success: {ip_addr} is now blocked.")
            time.sleep(0.1)

if __name__ == "__main__":
    monitor()
