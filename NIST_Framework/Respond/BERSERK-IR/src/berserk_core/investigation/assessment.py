from .timeline_analysis import (
    analyze_attack_pattern,
    analyze_timeline,
)


def _generate_findings(
    timeline_analysis: dict,
    attack_pattern: dict,
) -> list[str]:
    """Generate descriptive findings from investigation analysis."""

    findings = []

    if attack_pattern["repeated_activity"]:
        findings.append(
            "Repeated authentication activity was observed."
        )

    if attack_pattern["multiple_users_targeted"]:
        findings.append(
            "Multiple user accounts were targeted."
        )

    if attack_pattern["privileged_account_targeted"]:
        findings.append(
            "The root account was targeted."
        )

    if attack_pattern["dominant_source_ip"]:
        findings.append(
            "Dominant source IP identified: "
            f"{attack_pattern['dominant_source_ip']}."
        )

    if timeline_analysis["event_count"] > 0:
        findings.append(
            f"{timeline_analysis['event_count']} investigation "
            "events were reconstructed."
        )

    if timeline_analysis["duration_seconds"] > 0:
        findings.append(
            "Observed activity occurred within a "
            f"{timeline_analysis['duration_seconds']}-second window."
        )

    return findings


def assess_investigation(case) -> dict:
    """
    Combine timeline and attack-pattern analysis
    into a read-only investigation assessment.

    This function does not modify the incident case
    or its timeline.
    """

    timeline_analysis = analyze_timeline(case)
    attack_pattern = analyze_attack_pattern(case)

    findings = _generate_findings(
        timeline_analysis,
        attack_pattern,
    )

    return {
        "event_count": timeline_analysis["event_count"],
        "first_event": timeline_analysis["first_event"],
        "last_event": timeline_analysis["last_event"],
        "duration_seconds": timeline_analysis["duration_seconds"],
        "event_types": timeline_analysis["event_types"],
        "repeated_activity": attack_pattern["repeated_activity"],
        "targeted_users": attack_pattern["targeted_users"],
        "multiple_users_targeted": (
            attack_pattern["multiple_users_targeted"]
        ),
        "privileged_account_targeted": (
            attack_pattern["privileged_account_targeted"]
        ),
        "dominant_source_ip": (
            attack_pattern["dominant_source_ip"]
        ),
        "findings": findings,
    }
