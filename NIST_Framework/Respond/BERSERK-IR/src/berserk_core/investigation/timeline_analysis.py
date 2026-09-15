from datetime import datetime


def _parse_timestamp(
    timestamp: str,
    year: int | None = None,
) -> datetime:
    """Parse ISO-8601 and syslog-style timeline timestamps."""

    normalized = timestamp.strip()

    try:
        return datetime.fromisoformat(
            normalized.replace("Z", "+00:00")
        )
    except ValueError:
        pass

    if year is None:
        year = datetime.now().year

    return datetime.strptime(
        f"{year} {normalized}",
        "%Y %b %d %H:%M:%S",
    )




def analyze_timeline(case) -> dict:
    """
    Analyze the reconstructed investigation timeline.

    Returns objective timeline statistics without modifying
    the incident case.
    """

    events = list(case.timeline)

    if not events:
        return {
            "event_count": 0,
            "first_event": None,
            "last_event": None,
            "duration_seconds": 0,
            "event_types": {},
        }

    ordered_events = sorted(
        events,
        key=lambda event: event.timestamp,
    )

    first_event = ordered_events[0]
    last_event = ordered_events[-1]

    first_timestamp = _parse_timestamp(first_event.timestamp)
    last_timestamp = _parse_timestamp(last_event.timestamp)

    duration_seconds = (
        last_timestamp - first_timestamp
    ).total_seconds()

    event_types = {}

    for event in ordered_events:
        event_type = event.event_type or event.action or "UNKNOWN"
        event_types[event_type] = (
            event_types.get(event_type, 0) + 1
        )

    return {
        "event_count": len(ordered_events),
        "first_event": first_event.timestamp,
        "last_event": last_event.timestamp,
        "duration_seconds": duration_seconds,
        "event_types": event_types,
    }


def analyze_attack_pattern(case) -> dict:
    """
    Identify simple behavioral patterns from timeline evidence.

    The analysis is descriptive only and does not make a
    containment or response decision.
    """

    events = list(case.timeline)

    if not events:
        return {
            "repeated_activity": False,
            "targeted_users": [],
            "multiple_users_targeted": False,
            "privileged_account_targeted": False,
            "dominant_source_ip": None,
        }

    descriptions = [
        event.description
        for event in events
        if event.description
    ]

    source_ips = []
    users = []

    for description in descriptions:
        parts = [
            part.strip()
            for part in description.split("|")
        ]

        for part in parts:
            if part.startswith("source="):
                source_ips.append(
                    part.split("=", 1)[1]
                )

            elif part.startswith("user="):
                users.append(
                    part.split("=", 1)[1]
                )

    unique_users = sorted(set(users))

    source_counts = {}

    for source_ip in source_ips:
        source_counts[source_ip] = (
            source_counts.get(source_ip, 0) + 1
        )

    dominant_source_ip = (
        max(
            source_counts,
            key=source_counts.get,
        )
        if source_counts
        else None
    )

    return {
        "repeated_activity": len(events) >= 2,
        "targeted_users": unique_users,
        "multiple_users_targeted": len(unique_users) >= 2,
        "privileged_account_targeted": (
            "root" in unique_users
        ),
        "dominant_source_ip": dominant_source_ip,
    }
