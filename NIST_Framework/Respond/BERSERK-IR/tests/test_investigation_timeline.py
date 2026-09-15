import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from berserk_core.investigation.timeline import TimelineEvent


def test_timeline_event_creation():
    event = TimelineEvent.create(
        "EVIDENCE_REVIEW",
        "Reviewed SSH authentication failures.",
    )

    assert event.action == "EVIDENCE_REVIEW"
    assert event.description == "Reviewed SSH authentication failures."
    assert event.timestamp


def test_timeline_event_summary():
    event = TimelineEvent.create(
        "INDICATOR_REVIEW",
        "Reviewed source IP associated with the activity.",
    )

    summary = event.summary()

    assert summary["action"] == "INDICATOR_REVIEW"
    assert summary["description"] == "Reviewed source IP associated with the activity."
    assert summary["timestamp"] == event.timestamp
