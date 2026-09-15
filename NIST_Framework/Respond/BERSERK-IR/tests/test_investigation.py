from berserk_core.investigation.case import IncidentCase


def test_incident_case_creation():
    case = IncidentCase(
        case_id="BERSERK-001",
        title="The Branded Host",
        threat="SSH Brute Force",
        indicator="185.220.101.5",
        attempts=4,
        severity="HIGH",
        confidence="HIGH",
    )

    assert case.case_id == "BERSERK-001"
    assert case.threat == "SSH Brute Force"
    assert case.severity == "HIGH"
    assert case.status == "OPEN"


def test_evidence_can_be_added():
    case = IncidentCase(
        case_id="BERSERK-002",
        title="Test Incident",
        threat="SSH Brute Force",
        indicator="192.168.1.100",
        attempts=5,
        severity="MEDIUM",
        confidence="HIGH",
    )

    case.add_evidence("Multiple failed SSH authentication attempts")

    assert len(case.evidence) == 1
    assert "SSH authentication" in case.evidence[0]


def test_case_can_be_closed():
    case = IncidentCase(
        case_id="BERSERK-003",
        title="Closure Test",
        threat="SSH Brute Force",
        indicator="10.0.0.50",
        attempts=3,
        severity="LOW",
        confidence="MEDIUM",
    )

    case.close()

    assert case.status == "CLOSED"
