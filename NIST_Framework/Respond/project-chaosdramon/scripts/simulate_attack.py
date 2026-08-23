#!/usr/bin/env python3
import time
import sys

TARGET_LOG = "mock_auth.log"
ATTACKER_IP = "192.168.1.50"

def simulate_bruteforce():
    print(f"[*] Launching simulated threat from IP: {ATTACKER_IP}")
    print(f"[*] Targeting log stream: {TARGET_LOG}")
    
    # Simulate a rapid burst of failed SSH login attempts
    burst_count = 4
    for i in range(1, burst_count + 1):
        log_entry = f"Failed password for invalid user root from {ATTACKER_IP} port 22 ssh2 [ATTACK #{i}]"
        
        with open(TARGET_LOG, "a") as f:
            f.write(log_entry + "\n")
            
        print(f"[+] Sent attack packet {i}/{burst_count}...")
        time.sleep(0.5)  # Short delay between attempts to trigger the sensor's time window
        
    print("[*] Threat simulation burst completed.")

if __name__ == "__main__":
    simulate_bruteforce()
