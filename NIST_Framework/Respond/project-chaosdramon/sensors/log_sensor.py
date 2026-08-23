#!/usr/bin/env python3
import time
import os
import re
import json
import subprocess

CONFIG_FILE = "configs/sensor_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    # Default fallback if config is missing
    return {
        "sensor": {"log_file": "mock_auth.log", "threshold": 3, "time_window_seconds": 10}
    }

config = load_config()
LOG_FILE = config["sensor"]["log_file"]
THRESHOLD = config["sensor"]["threshold"]
TIME_WINDOW = config["sensor"]["time_window_seconds"]

failed_attempts = []

def monitor_logs():
    global failed_attempts
    
    print(f"[*] Initializing Project Chaosdramon Sensor...")
    print(f"[*] Loaded configuration from {CONFIG_FILE}")
    print(f"[*] Tailing telemetry from: {LOG_FILE} (Threshold: {THRESHOLD} failures in {TIME_WINDOW}s)")
    
    active_log = LOG_FILE if os.path.exists(LOG_FILE) else "mock_auth.log"
    if not os.path.exists(active_log):
        with open(active_log, "w") as f:
            f.write("# Mock Auth Log Initialized\n")
            
    with open(active_log, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            
            if "Failed password" in line or "authentication failure" in line:
                print(f"[ALERT] Detected suspicious authentication event: {line.strip()}")
                current_time = time.time()
                failed_attempts.append(current_time)
                
                failed_attempts = [t for t in failed_attempts if current_time - t <= TIME_WINDOW]
                
                if len(failed_attempts) >= THRESHOLD:
                    print("\n[!] ----------------------------------------------------")
                    print("[!] THRESHOLD BREACHED: Multiple authentication failures!")
                    print("[!] INITIATING CHAOSDRAMON PROTOCOL SIGNAL...")
                    print("[!] ----------------------------------------------------\n")
                    
                    try:
                        subprocess.run(["python3", "scripts/chaosdramon_response.py"])
                    except Exception as e:
                        print(f"[!] Error triggering response script: {e}")
                        
                    failed_attempts = []

if __name__ == "__main__":
    try:
        monitor_logs()
    except KeyboardInterrupt:
        print("\n[*] Sensor shut down safely.")
