from berserk_core.investigation.case import IncidentCase
from berserk_core.investigation.timeline import TimelineEvent
from berserk_core.investigation.timeline_analysis import analyze_timeline


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


def test_timeline_analysis_counts_events():
    case = create_case()

    case.add_timeline_event(
        TimelineEvent(
            event_type="EVIDENCE",
            description="First SSH failure",
            timestamp="2026-08-03T08:14:22Z",
        )
    )

    case.add_timeline_event(
        TimelineEvent(
            event_type="EVIDENCE",
            description="Second SSH failure",
            timestamp="2026-08-03T08:14:25Z",
        )
    )

    analysis = analyze_timeline(case)

    assert analysis["event_count"] == 2


def test_timeline_analysis_identifies_time_range():
    case = create_case()

    case.add_timeline_event(
        TimelineEvent(
            event_type="EVIDENCE",
            description="First SSH failure",
            timestamp="2026-08-03T08:14:22Z",
        )
    )

    case.add_timeline_event(
        TimelineEvent(
            event_type="EVIDENCE",
            description="Last SSH failure",
            timestamp="2026-08-03T08:14:31Z",
        )
    )

    analysis = analyze_timeline(case)

    assert analysis["first_event"] == "2026-08-03T08:14:22Z"
    assert analysis["last_event"] == "2026-08-03T08:14:31Z"
    assert analysis["duration_seconds"] == 9.0


def test_timeline_analysis_counts_event_types():
    case = create_case()

    case.add_timeline_event(
        TimelineEvent(
            event_type="EVIDENCE",
            description="SSH failure",
            timestamp="2026-08-03T08:14:22Z",
        )
    )

    case.add_timeline_event(
        TimelineEvent(
            event_type="EVIDENCE",
            description="SSH failure",
            timestamp="2026-08-03T08:14:25Z",
        )
    )

    case.add_timeline_event(
        TimelineEvent(
            event_type="INVESTIGATION",
            description="Reviewed authentication logs",
            timestamp="2026-08-03T08:15:00Z",
        )
    )

    analysis = analyze_timeline(case)

    assert analysis["event_types"]["EVIDENCE"] == 2
    assert analysis["event_types"]["INVESTIGATION"] == 1


def test_empty_timeline_returns_zero_values():
    case = create_case()

    analysis = analyze_timeline(case)

    assert analysis["event_count"] == 0
    assert analysis["first_event"] is None
    assert analysis["last_event"] is None
    assert analysis["duration_seconds"] == 0
    assert analysis["event_types"] == {}
