from berserk_core.investigation.case import (
    IncidentCase,
    EvidenceEvent,
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
        case_id="BERSERK-014",
        title="Evidence Intelligence Test",
        threat="SSH Brute Force",
        indicator="185.220.101.5",
        attempts=4,
        severity="HIGH",
        confidence="HIGH",
        evidence=evidence,
    )


def test_evidence_summary_identifies_source_ips():
    case = create_case()

    summary = case.evidence_summary()

    assert summary["source_ips"] == [
        "185.220.101.5"
    ]


def test_evidence_summary_identifies_targeted_usernames():
    case = create_case()

    summary = case.evidence_summary()

    assert summary["usernames"] == [
        "admin",
        "root",
    ]


def test_evidence_summary_identifies_ports():
    case = create_case()

    summary = case.evidence_summary()

    assert summary["ports"] == [
        42110,
        42112,
        42115,
        42118,
    ]


def test_evidence_summary_counts_events():
    case = create_case()

    summary = case.evidence_summary()

    assert summary["event_count"] == 4
