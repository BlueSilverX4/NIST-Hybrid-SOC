from dataclasses import dataclass


@dataclass
class CorrelatedFinding:
    source_ip: str
    targeted_usernames: list[str]
    event_count: int
    pattern: str


def correlate_evidence(case) -> CorrelatedFinding:
    analysis = case.evidence_analysis()

    source_ips = analysis["source_ip_counts"]
    username_counts = analysis["username_counts"]
    event_type_counts = analysis["event_type_counts"]

    source_ip = max(
        source_ips,
        key=source_ips.get,
        default=None,
    )

    targeted_usernames = sorted(username_counts)

    event_count = sum(event_type_counts.values())

    pattern = "Unclassified Activity"

    if (
        event_count >= 3
        and source_ip
        and targeted_usernames
        and any(
            "authentication" in event_type.lower()
            for event_type in event_type_counts
        )
    ):
        pattern = "SSH Brute Force"

    return CorrelatedFinding(
        source_ip=source_ip,
        targeted_usernames=targeted_usernames,
        event_count=event_count,
        pattern=pattern,
    )
