import re
import ipaddress
from typing import Dict, List, Set

class IOCExtractor:
    # Regex patterns for IOC detection
    IPV4_PATTERN = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    SHA256_PATTERN = r'\b[a-fA-F0-9]{64}\b'
    
    @staticmethod
    def is_public_ip(ip_str: str) -> bool:
        try:
            ip = ipaddress.ip_address(ip_str)
            return not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast)
        except ValueError:
            return False

    @classmethod
    def extract_from_text(cls, text: str) -> Dict[str, List[str]]:
        raw_ips = re.findall(cls.IPV4_PATTERN, text)
        hashes = list(set(re.findall(cls.SHA256_PATTERN, text)))
        
        # Filter for public IPs only
        public_ips = list(set([ip for ip in raw_ips if cls.is_public_ip(ip)]))
        
        return {
            "public_ips": public_ips,
            "hashes": hashes
        }
