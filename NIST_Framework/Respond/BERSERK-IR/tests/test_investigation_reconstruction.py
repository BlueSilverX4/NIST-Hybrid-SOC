from berserk_core.investigation.case import EvidenceEvent, IncidentCase
from berserk_core.investigation.reconstruction import (
    reconstruct_evidence_timeline,
)


def create_case():
    case = IncidentCase(
        case_id="BERSERK-001",
        title="The Branded Host",
        threat="SSH Brute Force",
        indicator="185.220.101.5",
        attempts=4,
        severity="HIGH",
        confidence="HIGH",
    )

    case.evidence = [
        EvidenceEvent(
            timestamp="2026-08-03T08:14:28Z",
            username="root",
            source_ip="185.220.101.5",
            port=42115,
            event="Failed SSH Authentication",
        ),
        EvidenceEvent(
            timestamp="2026-08-03T08:14:22Z",
            username="admin",
            source_ip="185.220.101.5",
            port=42110,
            event="Failed SSH Authentication",
        ),
    ]

    return case


def test_reconstruct_evidence_timeline_creates_events():
    case = create_case()

    timeline = reconstruct_evidence_timeline(case)

    assert len(timeline) == 2
    assert timeline[0].event_type == "EVIDENCE"
    assert timeline[1].event_type == "EVIDENCE"


def test_reconstruction_preserves_evidence_timestamp():
    case = create_case()

    timeline = reconstruct_evidence_timeline(case)

    assert timeline[0].timestamp == "2026-08-03T08:14:22Z"


def test_reconstruction_keeps_events_chronological():
    case = create_case()

    timeline = reconstruct_evidence_timeline(case)

    assert timeline[0].timestamp == "2026-08-03T08:14:22Z"
    assert timeline[1].timestamp == "2026-08-03T08:14:28Z"


def test_reconstruction_includes_evidence_context():
    case = create_case()

    timeline = reconstruct_evidence_timeline(case)

    assert "185.220.101.5" in timeline[0].description
    assert "admin" in timeline[0].description
    assert "42110" in timeline[0].description
