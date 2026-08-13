import sys
import json
import os
from dotenv import load_dotenv

from src.extractors import IOCExtractor
from src.enrichers import ThreatEnricher
from src.kev import KEVMatcher
from src.reporter import MarkdownReporter

def main():
    # Load API keys from .env file
    load_dotenv()

    # Determine input payload path
    if len(sys.argv) > 1:
        alert_path = sys.argv[1]
    else:
        alert_path = "input/sample_alert.json"

    if not os.path.exists(alert_path):
        print(f"[!] Error: Alert file not found at '{alert_path}'")
        sys.exit(1)

    print(f"[*] Loading alert payload from: {alert_path}")
    with open(alert_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Parse JSON summary for context if valid JSON
    try:
        alert_json = json.loads(raw_text)
        rule_desc = alert_json.get("rule", {}).get("description", "Generic Alert")
        agent_name = alert_json.get("agent", {}).get("name", "Unknown Agent")
        alert_summary = f"Rule: **{rule_desc}** | Agent: `{agent_name}`"
    except json.JSONDecodeError:
        alert_summary = "Raw unstructured log payload ingested."

    # 1. Extract IOCs
    print("[+] Extracting Indicators of Compromise (IOCs)...")
    iocs = IOCExtractor.extract_from_text(raw_text)
    
    kev_matcher = KEVMatcher()
    extracted_cves = kev_matcher.extract_cves(raw_text)

    print(f"    └─ Public IPs Found : {len(iocs['public_ips'])} -> {iocs['public_ips']}")
    print(f"    └─ SHA256 Hashes   : {len(iocs['hashes'])} -> {iocs['hashes']}")
    print(f"    └─ CVE Identifiers : {len(extracted_cves)} -> {extracted_cves}")

    # 2. Enrich Telemetry via OSINT APIs
    print("[+] Querying OSINT APIs & Threat Intel Feeds...")
    enricher = ThreatEnricher()

    ip_results = []
    for ip in iocs['public_ips']:
        print(f"    └─ [AbuseIPDB] Checking IP: {ip}...")
        ip_results.append(enricher.check_ip_abuseipdb(ip))

    hash_results = []
    for h in iocs['hashes']:
        print(f"    └─ [VirusTotal] Checking Hash: {h[:16]}...")
        hash_results.append(enricher.check_hash_virustotal(h))

    # 3. Match CISA KEV Catalog
    print("[+] Cross-referencing CISA Known Exploited Vulnerabilities...")
    kev_results = kev_matcher.match_cves(extracted_cves)
    print(f"    └─ Matches Found    : {len(kev_results)}")

    # 4. Generate Markdown Triage Report
    print("[+] Generating Markdown Triage Report...")
    report_md = MarkdownReporter.generate_report(
        alert_summary=alert_summary,
        ip_results=ip_results,
        hash_results=hash_results,
        kev_results=kev_results
    )

    # Ensure output directory exists
    output_dir = "output/reports"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "triage_report.md")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_md)

    print(f"\n[✔] SUCCESS: Triage report generated at '{output_path}'!")

if __name__ == "__main__":
    main()
