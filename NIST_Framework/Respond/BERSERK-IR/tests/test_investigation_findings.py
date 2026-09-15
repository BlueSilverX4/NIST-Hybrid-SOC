from berserk_core.investigation.case import (
    IncidentCase,
    EvidenceEvent,
)
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
        case_id="BERSERK-017",
        title="Investigation Findings Test",
        threat="SSH Brute Force",
        indicator="185.220.101.5",
        attempts=4,
        severity="HIGH",
        confidence="HIGH",
        evidence=evidence,
    )


def test_investigation_assessment_provides_evidence_findings():
    case = create_case()

    reconstruct_evidence_timeline(case)

    assessment = assess_investigation(case)

    assert assessment["event_count"] == 4
    assert assessment["repeated_activity"] is True
    assert assessment["multiple_users_targeted"] is True
    assert assessment["privileged_account_targeted"] is True


def test_investigation_assessment_preserves_timeline_duration():
    case = create_case()

    reconstruct_evidence_timeline(case)

    assessment = assess_investigation(case)

    assert assessment["duration_seconds"] == 9.0


def test_investigation_assessment_identifies_dominant_source():
    case = create_case()

    reconstruct_evidence_timeline(case)

    assessment = assess_investigation(case)

    assert assessment["dominant_source_ip"] == "185.220.101.5"

def test_empty_investigation_has_no_findings():
    case = IncidentCase(
        case_id="BERSERK-017",
        title="Empty Investigation",
        threat="Unknown",
        indicator=None,
        attempts=0,
        severity="LOW",
        confidence="LOW",
    )

    assessment = assess_investigation(case)

    assert assessment["event_count"] == 0
    assert assessment["repeated_activity"] is False
    assert assessment["targeted_users"] == []
    assert assessment["dominant_source_ip"] is None

def test_investigation_assessment_generates_findings():
    case = create_case()

    reconstruct_evidence_timeline(case)

    assessment = assess_investigation(case)

    assert "findings" in assessment
    assert isinstance(assessment["findings"], list)

    assert "Repeated authentication activity was observed." in assessment[
        "findings"
    ]

    assert "Multiple user accounts were targeted." in assessment[
        "findings"
    ]

    assert "The root account was targeted." in assessment[
        "findings"
    ]

    assert (
        "Dominant source IP identified: 185.220.101.5."
        in assessment["findings"]
    )


def test_empty_investigation_generates_no_findings():
    case = IncidentCase(
        case_id="BERSERK-017",
        title="Empty Investigation",
        threat="Unknown",
        indicator=None,
        attempts=0,
        severity="LOW",
        confidence="LOW",
    )

    assessment = assess_investigation(case)

    assert assessment["findings"] == []
