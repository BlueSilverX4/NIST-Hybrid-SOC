from typing import List, Dict, Any

class MarkdownReporter:
    @staticmethod
    def generate_report(
        alert_summary: str,
        ip_results: List[Dict[str, Any]],
        hash_results: List[Dict[str, Any]],
        kev_results: List[Dict[str, Any]]
    ) -> str:
        
        md = []
        md.append("# 🛡️ Automated Incident Triage & Threat Intelligence Report\n")
        md.append(f"**Alert Context:** {alert_summary}\n")
        md.append("---\n")

        # 1. IP Enrichment Section
        md.append("## 🌐 IP Reputation & Geolocation (AbuseIPDB)\n")
        if ip_results:
            md.append("| IP Address | Status | Abuse Score | Country | ISP / Domain | Reports |")
            md.append("| :--- | :--- | :--- | :--- | :--- | :--- |")
            for ip in ip_results:
                score = ip.get("score", 0)
                badge = "🔴 HIGH" if score > 50 else ("🟡 MED" if score > 15 else "🟢 LOW")
                md.append(f"| `{ip['ip']}` | {ip['status']} | {score}% ({badge}) | {ip.get('country', 'N/A')} | {ip.get('isp', 'N/A')} | {ip.get('total_reports', 0)} |")
        else:
            md.append("*No public IP indicators identified in alert payload.*")
        md.append("\n---\n")

        # 2. File Hash Enrichment Section
        md.append("## 🔍 Hash Analysis & Malware Intelligence (VirusTotal)\n")
        if hash_results:
            md.append("| SHA256 Hash | Status | Detections | Primary Name | Threat Tags |")
            md.append("| :--- | :--- | :--- | :--- | :--- |")
            for h in hash_results:
                positives = h.get("positives", 0)
                total = h.get("total_engines", 0)
                tags = ", ".join([f"`{t}`" for t in h.get("tags", [])]) or "None"
                ratio = f"{positives}/{total}" if total > 0 else "0/0"
                badge = "🔴 MALICIOUS" if positives > 5 else ("🟡 SUSPICIOUS" if positives > 0 else "🟢 CLEAN")
                
                md.append(f"| `{h['hash'][:16]}...` | {h['status']} | {ratio} ({badge}) | {h.get('meaningful_name', 'N/A')} | {tags} |")
        else:
            md.append("*No file hash indicators identified in alert payload.*")
        md.append("\n---\n")

        # 3. CISA KEV Matches Section
        md.append("## 🚨 CISA Known Exploited Vulnerabilities (KEV) Matches\n")
        if kev_results:
            md.append("| CVE ID | Vulnerability Name | Vendor/Project | Product | Action Due |")
            md.append("| :--- | :--- | :--- | :--- | :--- |")
            for kev in kev_results:
                md.append(f"| **{kev.get('cveID')}** | {kev.get('vulnerabilityName')} | {kev.get('vendorProject')} | {kev.get('product')} | `{kev.get('dueDate')}` |")
        else:
            md.append("*No CISA Known Exploited Vulnerabilities detected.*")
        md.append("\n---\n")

        # 4. Analyst Recommendations
        md.append("## 📌 Incident Action Plan")
        md.append("1. **Network Containment:** Block active high-confidence malicious IPs at the gateway firewall.")
        md.append("2. **Endpoint Isolation:** Quarantine hosts exhibiting matching hash indicators.")
        md.append("3. **Patch Prioritization:** Expedite remediation for identified CISA KEV CVEs.")

        return "\n".join(md)
