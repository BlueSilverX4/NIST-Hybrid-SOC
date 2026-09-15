from berserk_core.assessment import (
    FindingAssessment,
    assess_finding,
)
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
        title="Finding Assessment Test",
        threat="SSH Brute Force",
        indicator="185.220.101.5",
        attempts=4,
        severity="HIGH",
        confidence="HIGH",
        evidence=evidence,
    )


def test_finding_assessment_identifies_ssh_brute_force():
    case = create_case()

    finding = assess_finding(case)

    assert isinstance(finding, FindingAssessment)
    assert finding.pattern == "SSH Brute Force"


def test_finding_assessment_preserves_severity():
    case = create_case()

    finding = assess_finding(case)

    assert finding.severity == "HIGH"


def test_finding_assessment_preserves_confidence():
    case = create_case()

    finding = assess_finding(case)

    assert finding.confidence == "HIGH"


def test_finding_assessment_contains_rationale():
    case = create_case()

    finding = assess_finding(case)

    assert "Repeated SSH authentication failures" in finding.rationale
