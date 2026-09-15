from berserk_core.investigation.timeline import TimelineEvent
from berserk_core.investigation.case import IncidentCase


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


def test_case_can_record_investigation_activity():
    case = create_case()

    event = case.record_investigation_activity(
        "Reviewed SSH authentication logs for additional failures."
    )

    assert event.event_type == "INVESTIGATION"
    assert event.description == (
        "Reviewed SSH authentication logs for additional failures."
    )
    assert len(case.timeline) == 1


def test_investigation_activity_is_preserved_in_summary():
    case = create_case()

    case.record_investigation_activity(
        "Reviewed SSH authentication logs for additional failures."
    )

    summary = case.summary()

    assert len(summary["timeline"]) == 1
    assert summary["timeline"][0]["event_type"] == "INVESTIGATION"
    assert summary["timeline"][0]["description"] == (
        "Reviewed SSH authentication logs for additional failures."
    )
