from berserk_core.investigation.case import EvidenceEvent, IncidentCase
from berserk_core.investigation.reconstruction import (
    reconstruct_evidence_timeline,
)


def create_case():
    return IncidentCase(
        case_id="BERSERK-001",
        title="The Branded Host",
        threat="SSH Brute Force",
        indicator="185.220.101.5",
        attempts=2,
        severity="HIGH",
        confidence="HIGH",
        evidence=[
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
        ],
    )


def test_reconstruction_integrates_with_incident_case():
    case = create_case()

    reconstruct_evidence_timeline(case)

    assert len(case.timeline) == 2
    assert case.timeline[0].timestamp == "2026-08-03T08:14:22Z"
    assert case.timeline[1].timestamp == "2026-08-03T08:14:28Z"


def test_reconstructed_timeline_is_present_in_case_summary():
    case = create_case()

    reconstruct_evidence_timeline(case)

    summary = case.summary()

    assert len(summary["timeline"]) == 2
    assert summary["timeline"][0]["event_type"] == "EVIDENCE"
    assert "185.220.101.5" in summary["timeline"][0]["description"]
