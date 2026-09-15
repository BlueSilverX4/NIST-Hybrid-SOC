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


def test_case_can_retrieve_events_by_type():
    case = create_case()

    detection = TimelineEvent(
        timestamp="2026-08-03T08:14:22Z",
        event_type="DETECTION",
        description="SSH authentication failure detected",
    )

    investigation = TimelineEvent(
        timestamp="2026-08-03T08:15:00Z",
        event_type="INVESTIGATION",
        description="Root account targeting identified",
    )

    case.add_timeline_event(detection)
    case.add_timeline_event(investigation)

    events = case.get_timeline_events("DETECTION")

    assert len(events) == 1
    assert events[0].event_type == "DETECTION"


def test_case_returns_empty_list_for_unknown_event_type():
    case = create_case()

    event = TimelineEvent(
        timestamp="2026-08-03T08:14:22Z",
        event_type="DETECTION",
        description="SSH authentication failure detected",
    )

    case.add_timeline_event(event)

    events = case.get_timeline_events("RECOVERY")

    assert events == []
