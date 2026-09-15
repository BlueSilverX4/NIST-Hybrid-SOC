import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src" / "berserk_core")
)

from case import EvidenceEvent, IncidentCase
from decision import evaluate_decision
from scoring import calculate_threat_score
from response import generate_response
from protocol import get_protocol_phase


def create_test_case():
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
        case_id="BERSERK-001",
        title="The Branded Host",
        severity="HIGH",
        confidence="HIGH",
        primary_indicator="185.220.101.5",
        detection="SSH Brute Force",
        evidence=evidence,
    )


def test_high_risk_case_requires_investigation():
    case = create_test_case()

    threat_score = calculate_threat_score(case)
    decision = evaluate_decision(case, threat_score)

    assert threat_score["severity"] == "HIGH"
    assert decision["action"] == "INVESTIGATE"
    assert decision["requires_human_approval"] is True


def test_response_plan_is_simulation_only():
    case = create_test_case()

    threat_score = calculate_threat_score(case)
    decision = evaluate_decision(case, threat_score)
    protocol = get_protocol_phase(decision["action"])

    response = generate_response(case, decision, protocol)

    assert response.case_id == "BERSERK-001"
    assert response.indicator == "185.220.101.5"
    assert response.action == "INVESTIGATE"
    assert response.mode == "SIMULATION"
    assert response.human_approval_required is True
    assert len(response.steps) > 0
