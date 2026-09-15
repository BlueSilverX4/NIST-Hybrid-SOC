from berserk_core.investigation.timeline import TimelineEvent


def test_timeline_event_has_event_type():
    event = TimelineEvent(
        timestamp="2026-08-03T08:14:22Z",
        event_type="DETECTION",
        description="SSH authentication failure detected",
    )

    assert event.event_type == "DETECTION"


def test_timeline_event_summary_preserves_event_type():
    event = TimelineEvent(
        timestamp="2026-08-03T08:14:22Z",
        event_type="DETECTION",
        description="SSH authentication failure detected",
    )

    summary = event.summary()

    assert summary["event_type"] == "DETECTION"
