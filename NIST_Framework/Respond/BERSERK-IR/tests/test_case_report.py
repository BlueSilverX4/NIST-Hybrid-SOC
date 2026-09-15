import sys
from pathlib import Path

sys.path.insert(
    0,
    str(
        Path(__file__).resolve().parents[1]
        / "src"
        / "berserk_core"
    )
)

from case import EvidenceEvent, IncidentCase
from case_report import export_case_report
from mitre import recommend_mitre
from scoring import calculate_threat_score
from decision import evaluate_decision
from response import generate_response
from protocol import get_protocol_phase
from recovery import assess_recovery
from closure import assess_closure
from lessons_learned import assess_lessons

from berserk_core.investigation.assessment import (
    assess_investigation,
)
from berserk_core.investigation.reconstruction import (
    reconstruct_evidence_timeline,
)


def create_case():
    evidence = [
        EvidenceEvent(
            timestamp="Aug 3 08:14:22",
            username="admin",
            source_ip="185.220.101.5",
            port=42110,
            event="Failed SSH Authentication",
        )
    ]

    return IncidentCase(
        case_id="BERSERK-TEST",
        title="Test Case",
        severity="HIGH",
        confidence="HIGH",
        primary_indicator="185.220.101.5",
        detection="SSH Brute Force",
        evidence=evidence,
    )


def test_case_report_generation(tmp_path):
    case = create_case()

    mitre = recommend_mitre(case.detection)
    threat_score = calculate_threat_score(case)
    decision = evaluate_decision(case, threat_score)
    protocol = get_protocol_phase(decision["action"])
    response = generate_response(case, decision, protocol)
    recovery = assess_recovery(case)
    closure = assess_closure(case, recovery)
    lessons = assess_lessons(case)

    report_file = export_case_report(
        case,
        mitre,
        threat_score,
        decision,
        response,
        recovery,
        closure,
        lessons,
        report_dir=tmp_path,
    )

    assert report_file.exists()

    content = report_file.read_text(
        encoding="utf-8"
    )

    assert "BERSERK-TEST" in content
    assert "SSH Brute Force" in content
    assert "185.220.101.5" in content


def test_case_report_includes_investigation_assessment(tmp_path):
    case = create_case()

    reconstruct_evidence_timeline(case)

    investigation = assess_investigation(case)

    mitre = recommend_mitre(case.detection)
    threat_score = calculate_threat_score(case)
    decision = evaluate_decision(case, threat_score)
    protocol = get_protocol_phase(decision["action"])
    response = generate_response(case, decision, protocol)
    recovery = assess_recovery(case)
    closure = assess_closure(case, recovery)
    lessons = assess_lessons(case)

    report_file = export_case_report(
        case,
        mitre,
        threat_score,
        decision,
        response,
        recovery,
        closure,
        lessons,
        investigation=investigation,
        report_dir=tmp_path,
    )

    assert report_file.exists()

    content = report_file.read_text(
        encoding="utf-8"
    )

    assert "investigation" in content
    assert "event_count" in content
    assert "duration_seconds" in content
    assert "dominant_source_ip" in content
    assert "findings" in content
    assert "185.220.101.5" in content
