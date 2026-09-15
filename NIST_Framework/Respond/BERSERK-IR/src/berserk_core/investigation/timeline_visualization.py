from .timeline_analysis import (
    analyze_attack_pattern,
    analyze_timeline,
)


def render_timeline(case) -> str:
    """
    Render the reconstructed investigation timeline
    as a deterministic terminal-friendly string.

    This function does not modify the incident case.
    """

    timeline_analysis = analyze_timeline(case)
    attack_pattern = analyze_attack_pattern(case)

    lines = [
        "--- BERSERK Attack Timeline ---",
        f"Case: {case.case_id}",
        f"Events: {timeline_analysis['event_count']}",
    ]

    duration = timeline_analysis["duration_seconds"]

    lines.append(
        f"Duration: {duration:.1f} seconds"
    )

    lines.append("")

    if not case.timeline:
        lines.append("No timeline events reconstructed.")
    else:
        for event in case.timeline:
            timestamp = event.timestamp

            # Display only the time portion when using
            # ISO-8601 timestamps.
            if "T" in timestamp:
                time_display = timestamp.split("T", 1)[1]
                time_display = time_display.rstrip("Z")
            else:
                time_display = timestamp

            lines.append(
                f"{time_display}  ●  {event.event_type}"
            )
            lines.append(
                f"           {event.description}"
            )
            lines.append("")

    lines.append(
        f"Attack Window: {duration:.1f} seconds"
    )

    dominant_source = attack_pattern["dominant_source_ip"]

    lines.append(
        "Dominant Source: "
        f"{dominant_source or 'None identified'}"
    )

    targeted_users = attack_pattern["targeted_users"]

    lines.append(
        "Targeted Accounts: "
        f"{', '.join(targeted_users) if targeted_users else 'None identified'}"
    )

    return "\n".join(lines)
