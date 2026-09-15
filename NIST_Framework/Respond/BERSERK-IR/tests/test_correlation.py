from berserk_core.investigation.case import (
    IncidentCase,
    EvidenceEvent,
)
from berserk_core.correlation import (
    CorrelatedFinding,
    correlate_evidence,
)


def create_case():
    evidence = [
        EvidenceEvent(
            timestamp="Aug 3 08:14:22",
            username="admin",
            source_ip="185.220.101.5",
            port=42110,
            event="Failed SSH Authentication",
        ),
        EvidenceEvent(
            timestamp="Aug 3 08:14:25",
            username="admin",
            source_ip="185.220.101.5",
            port=42112,
            event="Failed SSH Authentication",
        ),
        EvidenceEvent(
            timestamp="Aug 3 08:14:28",
            username="root",
            source_ip="185.220.101.5",
            port=42115,
            event="Failed SSH Authentication",
        ),
        EvidenceEvent(
            timestamp="Aug 3 08:14:31",
            username="root",
            source_ip="185.220.101.5",
            port=42118,
            event="Failed SSH Authentication",
        ),
    ]

    return IncidentCase(
        case_id="BERSERK-016",
        title="Correlation Test",
        threat="SSH Brute Force",
        indicator="185.220.101.5",
        attempts=4,
        severity="HIGH",
        confidence="HIGH",
        evidence=evidence,
    )


def test_correlation_returns_finding():
    case = create_case()

    finding = correlate_evidence(case)

    assert isinstance(finding, CorrelatedFinding)


def test_correlation_identifies_common_source():
    case = create_case()

    finding = correlate_evidence(case)

    assert finding.source_ip == "185.220.101.5"


def test_correlation_identifies_targeted_users():
    case = create_case()

    finding = correlate_evidence(case)

    assert finding.targeted_usernames == [
        "admin",
        "root",
    ]


def test_correlation_counts_related_events():
    case = create_case()

    finding = correlate_evidence(case)

    assert finding.event_count == 4


def test_correlation_identifies_attack_pattern():
    case = create_case()

    finding = correlate_evidence(case)

    assert finding.pattern == "SSH Brute Force"
