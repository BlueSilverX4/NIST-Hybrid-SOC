from berserk_core.investigation.case import IncidentCase
from berserk_core.investigation.reconstruction import (
    reconstruct_evidence_timeline,
)
from berserk_core.investigation.timeline_visualization import (
    render_timeline,
)
from berserk_core.investigation.case import EvidenceEvent


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
            timestamp="2026-08-03T08:14:22Z",
            username="admin",
            source_ip="185.220.101.5",
            port=42110,
            event="Failed SSH Authentication",
        ),
        EvidenceEvent(
            timestamp="2026-08-03T08:14:25Z",
            username="admin",
            source_ip="185.220.101.5",
            port=42112,
            event="Failed SSH Authentication",
        ),
        EvidenceEvent(
            timestamp="2026-08-03T08:14:28Z",
            username="root",
            source_ip="185.220.101.5",
            port=42115,
            event="Failed SSH Authentication",
        ),
        EvidenceEvent(
            timestamp="2026-08-03T08:14:31Z",
            username="root",
            source_ip="185.220.101.5",
            port=42118,
            event="Failed SSH Authentication",
        ),
    ]

    return case


def test_render_timeline_contains_case_metadata():
    case = create_case()
    reconstruct_evidence_timeline(case)

    output = render_timeline(case)

    assert "--- BERSERK Attack Timeline ---" in output
    assert "Case: BERSERK-001" in output
    assert "Events: 4" in output
    assert "Duration: 9.0 seconds" in output


def test_render_timeline_contains_event_details():
    case = create_case()
    reconstruct_evidence_timeline(case)

    output = render_timeline(case)

    assert "08:14:22" in output
    assert "08:14:31" in output
    assert "Failed SSH Authentication" in output
    assert "185.220.101.5" in output
    assert "user=admin" in output
    assert "user=root" in output


def test_render_timeline_contains_attack_summary():
    case = create_case()
    reconstruct_evidence_timeline(case)

    output = render_timeline(case)

    assert "Attack Window: 9.0 seconds" in output
    assert "Dominant Source: 185.220.101.5" in output
    assert "Targeted Accounts: admin, root" in output


def test_render_timeline_handles_empty_timeline():
    case = create_case()

    output = render_timeline(case)

    assert "Events: 0" in output
    assert "Duration: 0.0 seconds" in output
    assert "No timeline events reconstructed." in output
    assert "Dominant Source: None identified" in output
    assert "Targeted Accounts: None identified" in output


def test_render_timeline_does_not_modify_case():
    case = create_case()
    reconstruct_evidence_timeline(case)

    before = [
        (
            event.event_type,
            event.description,
            event.timestamp,
        )
        for event in case.timeline
    ]

    render_timeline(case)

    after = [
        (
            event.event_type,
            event.description,
            event.timestamp,
        )
        for event in case.timeline
    ]

    assert after == before
