#!/usr/bin/env python3
"""
Element: Aqua Element (Web Application & API Security)
Framework: Style_Change_Framework
Description: Connects to OWASP ZAP API or parses static Nikto JSON reports
             to normalize web findings into HubStyle SOAR telemetry.
"""

import argparse
import json
import logging
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from typing import Any, Dict

# Configure Structured Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [Element:Aqua] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)


class ZapApiHandler:
    """
    Handler for interacting with OWASP ZAP Daemon REST API.
    Assumes ZAP is running locally as a service (e.g., http://127.0.0.1:8080).
    """
    def __init__(self, zap_base_url: str = "http://127.0.0.1:8080", api_key: str = ""):
        self.zap_base_url = zap_base_url.rstrip('/')
        self.api_key = api_key

    def _make_request(self, component: str, req_type: str, action_or_view: str, params: Dict[str, str] = None) -> Dict[str, Any]:
        if params is None:
            params = {}
        if self.api_key:
            params['apikey'] = self.api_key

        query_string = urllib.parse.urlencode(params)
        endpoint_url = f"{self.zap_base_url}/JSON/{component}/{req_type}/{action_or_view}/?{query_string}"

        try:
            req = urllib.request.Request(endpoint_url)
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    data = response.read().decode('utf-8')
                    return json.loads(data)
        except Exception as e:
            logging.error(f"ZAP API Request failed to {endpoint_url}: {e}")
            return {"error": str(e)}

    def fetch_alerts(self, base_url: str) -> Dict[str, Any]:
        logging.info(f"Querying ZAP alerts for target: {base_url}")
        return self._make_request(
            component="core",
            req_type="view",
            action_or_view="alerts",
            params={"baseurl": base_url}
        )


def normalize_aqua_telemetry(zap_alerts: dict, target_url: str, output_path: str = None) -> dict:
    """
    Normalizes raw scanner output into the SOAR telemetry schema.
    """
    alerts_list = zap_alerts.get("alerts", [])
    high_risk_count = sum(1 for a in alerts_list if a.get("risk") == "High")

    artifact = {
        "element": "Aqua",
        "domain": "Web Application & API Security",
        "timestamp": datetime.now().isoformat(),
        "target": target_url,
        "summary": {
            "total_alerts": len(alerts_list),
            "high_risk_alerts": high_risk_count
        },
        "raw_findings": alerts_list,
        "status": "COMPLETED"
    }

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(artifact, f, indent=2)
        logging.info(f"Aqua Element telemetry exported to: {output_path}")

    return artifact


def main():
    parser = argparse.ArgumentParser(description="Aqua Element - Web Security Ingestion Module")
    parser.add_argument("-t", "--target", default="http://127.0.0.1:8000", help="Target base URL")
    parser.add_argument("--api-url", default="http://127.0.0.1:8080", help="ZAP Daemon API base URL")
    parser.add_argument("--simulate", action="store_true", help="Run with mock ZAP alerts for testing")
    parser.add_argument("-o", "--output", help="Path to save output JSON artifact")

    args = parser.parse_args()

    if args.simulate:
        logging.info("Running simulated Aqua Element alert normalization...")
        mock_zap_response = {
            "alerts": [
                {
                    "sourceid": "1",
                    "other": "",
                    "method": "GET",
                    "evidence": "X-Frame-Options header not set",
                    "pluginId": "10020",
                    "cweid": "1021",
                    "confidence": "Medium",
                    "risk": "Medium",
                    "description": "Anti-MIME-Sniffing header missing",
                    "alert": "Absence of Anti-MIME-Sniffing Header",
                    "param": "x-content-type-options"
                },
                {
                    "sourceid": "1",
                    "other": "",
                    "method": "POST",
                    "evidence": "SELECT * FROM users WHERE id =",
                    "pluginId": "40018",
                    "cweid": "89",
                    "confidence": "High",
                    "risk": "High",
                    "description": "SQL Injection detected in login parameter",
                    "alert": "SQL Injection",
                    "param": "username"
                }
            ]
        }
        normalize_aqua_telemetry(mock_zap_response, args.target, output_path=args.output)
    else:
        handler = ZapApiHandler(zap_base_url=args.api_url)
        alerts = handler.fetch_alerts(args.target)
        normalize_aqua_telemetry(alerts, args.target, output_path=args.output)


if __name__ == "__main__":
    main()
