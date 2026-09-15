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


def test_case_can_retrieve_events_within_time_range():
    case = create_case()

    first = TimelineEvent(
        timestamp="2026-08-03T08:14:22Z",
        event_type="DETECTION",
        description="SSH authentication failure detected",
    )

    second = TimelineEvent(
        timestamp="2026-08-03T08:14:28Z",
        event_type="INVESTIGATION",
        description="Root account targeting identified",
    )

    third = TimelineEvent(
        timestamp="2026-08-03T08:15:30Z",
        event_type="ASSESSMENT",
        description="Repeated authentication activity confirmed",
    )

    case.add_timeline_event(first)
    case.add_timeline_event(second)
    case.add_timeline_event(third)

    events = case.get_timeline_events_between(
        "2026-08-03T08:14:20Z",
        "2026-08-03T08:14:30Z",
    )

    assert len(events) == 2
    assert events[0].event_type == "DETECTION"
    assert events[1].event_type == "INVESTIGATION"


def test_case_returns_empty_list_when_no_events_match_time_range():
    case = create_case()

    event = TimelineEvent(
        timestamp="2026-08-03T08:14:22Z",
        event_type="DETECTION",
        description="SSH authentication failure detected",
    )

    case.add_timeline_event(event)

    events = case.get_timeline_events_between(
        "2026-08-03T09:00:00Z",
        "2026-08-03T10:00:00Z",
    )

    assert events == []
