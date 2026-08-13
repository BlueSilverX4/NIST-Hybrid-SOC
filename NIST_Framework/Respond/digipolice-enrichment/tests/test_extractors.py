import unittest
from src.extractors import IOCExtractor
from src.kev import KEVMatcher

class TestIOCExtractor(unittest.TestCase):

    def test_public_ip_extraction(self):
        """Verify public IPs are extracted while private/loopback IPs are ignored."""
        sample_log = "Connection from 118.25.6.39 to internal host 192.168.1.50 and 127.0.0.1"
        iocs = IOCExtractor.extract_from_text(sample_log)
        
        self.assertIn("118.25.6.39", iocs["public_ips"])
        self.assertNotIn("192.168.1.50", iocs["public_ips"])
        self.assertNotIn("127.0.0.1", iocs["public_ips"])

    def test_sha256_hash_extraction(self):
        """Verify valid 64-character SHA256 hashes are extracted correctly."""
        sample_log = "Process executed hash=e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        iocs = IOCExtractor.extract_from_text(sample_log)
        
        self.assertEqual(len(iocs["hashes"]), 1)
        self.assertEqual(iocs["hashes"][0], "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")

    def test_cve_extraction_and_kev_matching(self):
        """Verify CVE extraction and matching against the CISA KEV catalog."""
        sample_log = "Exploit attempt targeting CVE-2021-44228 on web application"
        matcher = KEVMatcher()
        
        extracted_cves = matcher.extract_cves(sample_log)
        self.assertIn("CVE-2021-44228", extracted_cves)
        
        kev_matches = matcher.match_cves(extracted_cves)
        self.assertGreaterEqual(len(kev_matches), 1)
        self.assertEqual(kev_matches[0]["cveID"], "CVE-2021-44228")

if __name__ == "__main__":
    unittest.main()
