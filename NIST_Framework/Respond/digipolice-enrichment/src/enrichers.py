import os
import requests
from typing import Dict, Any

class ThreatEnricher:
    def __init__(self):
        self.abuseipdb_key = os.getenv("ABUSEIPDB_API_KEY")
        self.virustotal_key = os.getenv("VIRUSTOTAL_API_KEY")

    def check_ip_abuseipdb(self, ip: str) -> Dict[str, Any]:
        """Queries AbuseIPDB API v2 for IP reputation and geolocation metadata."""
        if not self.abuseipdb_key or self.abuseipdb_key == "your_abuseipdb_api_key_here":
            return {
                "ip": ip,
                "status": "API Key Missing",
                "score": 0,
                "country": "N/A",
                "isp": "N/A",
                "total_reports": 0
            }

        url = "https://api.abuseipdb.com/api/v2/check"
        headers = {
            "Accept": "application/json",
            "Key": self.abuseipdb_key
        }
        params = {
            "ipAddress": ip,
            "maxAgeInDays": "90"
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json().get("data", {})
                return {
                    "ip": ip,
                    "status": "Success",
                    "score": data.get("abuseConfidenceScore", 0),
                    "country": data.get("countryCode", "Unknown"),
                    "isp": data.get("isp", "Unknown"),
                    "domain": data.get("domain", "N/A"),
                    "total_reports": data.get("totalReports", 0)
                }
            elif response.status_code == 429:
                return {"ip": ip, "status": "Rate Limited (429)", "score": 0, "country": "N/A", "isp": "N/A", "total_reports": 0}
            else:
                return {"ip": ip, "status": f"HTTP {response.status_code}", "score": 0, "country": "N/A", "isp": "N/A", "total_reports": 0}
        except Exception as e:
            return {"ip": ip, "status": f"Error: {str(e)}", "score": 0, "country": "N/A", "isp": "N/A", "total_reports": 0}

    def check_hash_virustotal(self, file_hash: str) -> Dict[str, Any]:
        """Queries VirusTotal API v3 for SHA256 detection ratios and threat tags."""
        if not self.virustotal_key or self.virustotal_key == "your_virustotal_api_key_here":
            return {
                "hash": file_hash,
                "status": "API Key Missing",
                "positives": 0,
                "total_engines": 0,
                "tags": [],
                "meaningful_name": "N/A"
            }

        url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
        headers = {
            "accept": "application/json",
            "x-apikey": self.virustotal_key
        }

        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                attr = response.json().get("data", {}).get("attributes", {})
                stats = attr.get("last_analysis_stats", {})
                
                malicious = stats.get("malicious", 0)
                total = sum(stats.values()) if stats else 0
                tags = attr.get("tags", [])[:5] # Extract top 5 tags
                meaningful_name = attr.get("meaningful_name", "N/A")

                return {
                    "hash": file_hash,
                    "status": "Success",
                    "positives": malicious,
                    "total_engines": total,
                    "tags": tags,
                    "meaningful_name": meaningful_name
                }
            elif response.status_code == 404:
                return {"hash": file_hash, "status": "Clean / Not Found", "positives": 0, "total_engines": 0, "tags": [], "meaningful_name": "N/A"}
            elif response.status_code == 429:
                return {"hash": file_hash, "status": "Rate Limited (429)", "positives": 0, "total_engines": 0, "tags": [], "meaningful_name": "N/A"}
            else:
                return {"hash": file_hash, "status": f"HTTP {response.status_code}", "positives": 0, "total_engines": 0, "tags": [], "meaningful_name": "N/A"}
        except Exception as e:
            return {"hash": file_hash, "status": f"Error: {str(e)}", "positives": 0, "total_engines": 0, "tags": [], "meaningful_name": "N/A"}
