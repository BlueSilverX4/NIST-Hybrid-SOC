import os
from datetime import datetime

# Define paths (Adjust the output directory to wherever your portfolio lives)
ZEEK_DNS_LOG = "/opt/zeek/spool/zeek/dns.log"
OUTPUT_DIR = "/home/brandongregg/portfolio_evidence"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "dns_incident_report.txt")

def analyze_logs():
    # Create the output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"[+] Created directory: {OUTPUT_DIR}")

    if not os.path.exists(ZEEK_DNS_LOG):
        print(f"[-] Error: {ZEEK_DNS_LOG} not found. Is Zeek running?")
        return

    print("[*] Analyzing Zeek DNS logs for potential recon activity...")
    
    with open(ZEEK_DNS_LOG, "r") as log_file, open(OUTPUT_FILE, "w") as report:
        # Write a professional header for the portfolio artifact
        report.write("==================================================\n")
        report.write(f"INCIDENT EVIDENCE REPORT - GENERATED {datetime.now()}\n")
        report.write("Source Sensor: Zeek Network Security Monitor (wlan0)\n")
        report.write("==================================================\n\n")
        report.write(f"{'TIMESTAMP':<25} | {'SOURCE IP':<15} | {'QUERIED DOMAIN'}\n")
        report.write("-" * 75 + "\n")

        entry_count = 0
        for line in log_file:
            # Skip Zeek header lines
            if line.startswith("#"):
                continue
            
            # Zeek logs are tab-separated
            fields = line.strip().split("\t")
            
            # Standard Zeek dns.log layout structure check
            if len(fields) >= 10:
                ts = fields[0]      # Epoch timestamp
                src_ip = fields[2]  # Source IP address
                query = fields[9]   # Domain queried
                
                # Convert epoch time to human-readable format
                readable_ts = datetime.fromtimestamp(float(ts)).strftime('%Y-%m-%d %H:%M:%S')
                
                # Filter out empty or local multicast noise if desired
                if query != "-" and not query.endswith(".local"):
                    report.write(f"{readable_ts:<25} | {src_ip:<15} | {query}\n")
                    entry_count += 1

        print(f"[+] Success! Parsed {entry_count} activities.")
        print(f"[+] Evidence file saved safely to: {OUTPUT_FILE}")

if __name__ == "__main__":
    analyze_logs()
