import re
from collections import Counter


FAILED_SSH_PATTERN = re.compile(
    r"^(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+).*?"
    r"Failed password for "
    r"(?:invalid user )?(?P<username>\S+) "
    r"from (?P<source_ip>\S+) "
    r"port (?P<port>\d+)"
)


def extract_ssh_evidence(log_lines):
    """
    Extract structured evidence from SSH authentication failures.
    """

    evidence = []

    for line in log_lines:
        match = FAILED_SSH_PATTERN.search(line)

        if match:
            evidence.append(
                {
                    "timestamp": match.group("timestamp"),
                    "username": match.group("username"),
                    "source_ip": match.group("source_ip"),
                    "port": int(match.group("port")),
                    "event": "Failed SSH Authentication",
                }
            )

    return evidence


def detect_ssh_bruteforce(log_lines, threshold=3):
    """
    Detect repeated SSH authentication failures.
    """

    evidence = extract_ssh_evidence(log_lines)

    attempts = Counter(
        event["source_ip"]
        for event in evidence
    )

    findings = []

    for source_ip, count in attempts.items():
        if count >= threshold:

            related_events = [
                event
                for event in evidence
                if event["source_ip"] == source_ip
            ]

            findings.append(
                {
                    "indicator": source_ip,
                    "event": "SSH Brute Force",
                    "failed_attempts": count,
                    "severity": "HIGH",
                    "confidence": "HIGH",
                    "evidence": related_events,
                }
            )

    return findings
