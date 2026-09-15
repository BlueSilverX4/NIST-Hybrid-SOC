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
        case_id="BERSERK-015",
        title="Evidence Analysis Test",
        threat="SSH Brute Force",
        indicator="185.220.101.5",
        attempts=4,
        severity="HIGH",
        confidence="HIGH",
        evidence=evidence,
    )


def test_event_type_counts():
    case = create_case()

    analysis = case.evidence_analysis()

    assert analysis["event_types"] == {
        "Failed SSH Authentication": 4
    }


def test_username_counts():
    case = create_case()

    analysis = case.evidence_analysis()

    assert analysis["username_counts"] == {
        "admin": 2,
        "root": 2,
    }


def test_source_ip_counts():
    case = create_case()

    analysis = case.evidence_analysis()

    assert analysis["source_ip_counts"] == {
        "185.220.101.5": 4
    }


def test_most_targeted_username():
    case = create_case()

    analysis = case.evidence_analysis()

    assert analysis["most_targeted_username"] in {
        "admin",
        "root",
    }


def test_dominant_source_ip():
    case = create_case()

    analysis = case.evidence_analysis()

    assert analysis["dominant_source_ip"] == "185.220.101.5"


def test_repeated_authentication_detected():
    case = create_case()

    analysis = case.evidence_analysis()

    assert analysis["repeated_authentication"] is True
