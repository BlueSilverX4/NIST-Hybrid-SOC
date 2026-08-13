import json
import re
import os
from typing import List, Dict, Any

class KEVMatcher:
    CVE_PATTERN = r'\bCVE-\d{4}-\d{4,7}\b'

    def __init__(self, catalog_path: str = "config/cisa_kev.json"):
        self.catalog_path = catalog_path
        self.vulnerabilities = self._load_catalog()

    def _load_catalog(self) -> Dict[str, Dict[str, Any]]:
        """Loads the CISA KEV JSON catalog and indexes entries by CVE ID."""
        if not os.path.exists(self.catalog_path):
            print(f"[!] Warning: KEV catalog not found at {self.catalog_path}")
            return {}

        try:
            with open(self.catalog_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            # Index by cveID for O(1) fast lookup
            catalog = {}
            for item in data.get("vulnerabilities", []):
                cve_id = item.get("cveID")
                if cve_id:
                    catalog[cve_id.upper()] = item
            return catalog
        except Exception as e:
            print(f"[!] Error loading KEV catalog: {e}")
            return {}

    def extract_cves(self, text: str) -> List[str]:
        """Extracts unique CVE IDs from raw log text."""
        matches = re.findall(self.CVE_PATTERN, text, re.IGNORECASE)
        return list(set([cve.upper() for cve in matches]))

    def match_cves(self, cve_list: List[str]) -> List[Dict[str, Any]]:
        """Cross-references a list of CVE IDs against the loaded CISA KEV catalog."""
        results = []
        for cve in cve_list:
            if cve in self.vulnerabilities:
                results.append(self.vulnerabilities[cve])
        return results
