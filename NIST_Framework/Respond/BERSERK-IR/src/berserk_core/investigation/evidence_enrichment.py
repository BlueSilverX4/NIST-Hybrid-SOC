from ipaddress import ip_address

from .timeline_analysis import (
    analyze_attack_pattern,
    analyze_timeline,
)


def _classify_indicator(indicator: str | None) -> str:
    """Classify the primary case indicator."""

    if not indicator:
        return "Unknown"

    try:
        parsed = ip_address(indicator)

        if parsed.version == 4:
            return "IPv4 Address"

        return "IPv6 Address"

    except ValueError:
        return "Unknown"


def _extract_targeted_accounts(evidence) -> list[str]:
    """Extract unique targeted usernames from evidence."""

    return sorted(
        {
            event.username
            for event in evidence
            if event.username
        }
    )


def enrich_evidence(case) -> dict:
    """
    Enrich existing case evidence with structured investigation context.

    This function performs local evidence enrichment only.
    It does not contact external threat-intelligence services
    and does not modify the incident case.
    """

    timeline_analysis = analyze_timeline(case)
    attack_pattern = analyze_attack_pattern(case)

    evidence = case.evidence

    observed_ports = sorted(
        {
            event.port
            for event in evidence
            if event.port is not None
        }
    )

    observed_events = sorted(
        {
            event.event
            for event in evidence
            if event.event
        }
    )

    targeted_accounts = _extract_targeted_accounts(
        evidence
    )

    attack_context = []

    if attack_pattern["repeated_activity"]:
        attack_context.append(
            "Repeated authentication failures"
        )

    if (
        len(targeted_accounts) > 1
    ):
        attack_context.append(
            "Multiple accounts targeted"
        )

    if "root" in targeted_accounts:
        attack_context.append(
            "Privileged account targeted"
        )

    return {
        "indicator": case.indicator,
        "indicator_type": _classify_indicator(
            case.indicator
        ),
        "evidence_count": len(evidence),
        "first_seen": timeline_analysis["first_event"],
        "last_seen": timeline_analysis["last_event"],
        "duration_seconds": (
            timeline_analysis["duration_seconds"]
        ),
        "targeted_accounts": targeted_accounts,
        "observed_ports": observed_ports,
        "observed_events": observed_events,
        "attack_context": attack_context,
        "confidence": case.confidence,
        "human_validation_required": True,
    }
