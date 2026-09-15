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


def test_case_can_store_timeline_event():
    case = create_case()

    event = TimelineEvent(
        action="DETECTION",
        description="SSH authentication failure detected",
        timestamp="2026-08-03T08:14:22Z",
    )

    case.add_timeline_event(event)

    assert len(case.timeline) == 1
    assert case.timeline[0].action == "DETECTION"


def test_timeline_event_is_preserved_in_case_summary():
    case = create_case()

    event = TimelineEvent(
        action="DETECTION",
        description="SSH authentication failure detected",
        timestamp="2026-08-03T08:14:22Z",
    )

    case.add_timeline_event(event)

    summary = case.summary()

    assert "timeline" in summary
    assert len(summary["timeline"]) == 1
    assert summary["timeline"][0]["timestamp"] == "2026-08-03T08:14:22Z"
    assert summary["timeline"][0]["action"] == "DETECTION"

def test_timeline_events_are_kept_in_chronological_order():
    case = create_case()

    first_event = TimelineEvent(
        action="DETECTION",
        description="SSH authentication failure detected",
        timestamp="2026-08-03T08:14:22Z",
    )

    second_event = TimelineEvent(
        action="INVESTIGATION",
        description="Root account targeting identified",
        timestamp="2026-08-03T08:14:28Z",
    )

    third_event = TimelineEvent(
        action="ASSESSMENT",
        description="Repeated authentication activity confirmed",
        timestamp="2026-08-03T08:14:31Z",
    )

    case.add_timeline_event(first_event)
    case.add_timeline_event(second_event)
    case.add_timeline_event(third_event)

    summary = case.summary()

    timeline = summary["timeline"]

    assert len(timeline) == 3
    assert timeline[0]["timestamp"] == "2026-08-03T08:14:22Z"
    assert timeline[1]["timestamp"] == "2026-08-03T08:14:28Z"
    assert timeline[2]["timestamp"] == "2026-08-03T08:14:31Z"
