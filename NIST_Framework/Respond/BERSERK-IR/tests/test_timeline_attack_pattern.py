from berserk_core.investigation.case import IncidentCase
from berserk_core.investigation.timeline import TimelineEvent
from berserk_core.investigation.timeline_analysis import analyze_attack_pattern


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


def test_attack_pattern_detects_repeated_activity():
    case = create_case()

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

    analysis = analyze_attack_pattern(case)

    assert analysis["repeated_activity"] is True


def test_attack_pattern_detects_multiple_targeted_users():
    case = create_case()

    add_event(
        case,
        "2026-08-03T08:14:22Z",
        "Failed SSH Authentication | source=185.220.101.5 | user=admin | port=42110",
    )

    add_event(
        case,
        "2026-08-03T08:14:28Z",
        "Failed SSH Authentication | source=185.220.101.5 | user=root | port=42115",
    )

    analysis = analyze_attack_pattern(case)

    assert analysis["targeted_users"] == ["admin", "root"]
    assert analysis["multiple_users_targeted"] is True


def test_attack_pattern_detects_privileged_account_targeting():
    case = create_case()

    add_event(
        case,
        "2026-08-03T08:14:28Z",
        "Failed SSH Authentication | source=185.220.101.5 | user=root | port=42115",
    )

    analysis = analyze_attack_pattern(case)

    assert analysis["privileged_account_targeted"] is True


def test_attack_pattern_identifies_dominant_source():
    case = create_case()

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

    analysis = analyze_attack_pattern(case)

    assert analysis["dominant_source_ip"] == "185.220.101.5"
