from berserk_core.investigation.assessment import (
    assess_investigation,
)
from berserk_core.investigation.case import IncidentCase
from berserk_core.investigation.timeline import TimelineEvent


def create_case():
    return IncidentCase(
        case_id="BERSERK-001",
        title="The Branded Host",
        threat="SSH Brute Force",
        indicator="185.220.101.5",
        attempts=4,
        severity="HIGH",
        confidence="HIGH",
    )


def add_event(case, timestamp, description):
    case.add_timeline_event(
        TimelineEvent(
            event_type="EVIDENCE",
            description=description,
            timestamp=timestamp,
        )
    )


def add_four_evidence_events(case):
    add_event(
        case,
        "2026-08-03T08:14:22Z",
        "Failed SSH Authentication | source=185.220.101.5 | user=admin | port=42110",
    )

    add_event(
        case,
        "2026-08-03T08:14:25Z",
        "Failed SSH Authentication | source=185.220.101.5 | user=admin | port=42112",
    )

    add_event(
        case,
        "2026-08-03T08:14:28Z",
        "Failed SSH Authentication | source=185.220.101.5 | user=root | port=42115",
    )

    add_event(
        case,
        "2026-08-03T08:14:31Z",
        "Failed SSH Authentication | source=185.220.101.5 | user=root | port=42118",
    )


def test_empty_case_returns_empty_investigation_assessment():
    case = create_case()

    assessment = assess_investigation(case)

    assert assessment["event_count"] == 0
    assert assessment["repeated_activity"] is False
    assert assessment["targeted_users"] == []
    assert assessment["privileged_account_targeted"] is False
    assert assessment["dominant_source_ip"] is None


def test_investigation_assessment_combines_timeline_analysis():
    case = create_case()

    add_four_evidence_events(case)

    assessment = assess_investigation(case)

    assert assessment["event_count"] == 4
    assert assessment["repeated_activity"] is True
    assert assessment["targeted_users"] == ["admin", "root"]
    assert assessment["privileged_account_targeted"] is True
    assert assessment["dominant_source_ip"] == "185.220.101.5"


def test_investigation_assessment_does_not_modify_timeline():
    case = create_case()

    add_four_evidence_events(case)

    before = list(case.timeline)

    assess_investigation(case)

    assert case.timeline == before
