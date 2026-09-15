from .timeline import TimelineEvent


def reconstruct_evidence_timeline(case):
    """
    Reconstruct the investigation timeline from case evidence.

    Existing evidence timestamps are preserved so the resulting
    timeline reflects the chronological order of observed activity.
    """

    for evidence in case.evidence:
        timestamp = getattr(evidence, "timestamp", "")
        username = getattr(evidence, "username", "")
        source_ip = getattr(evidence, "source_ip", "")
        port = getattr(evidence, "port", None)
        event = getattr(evidence, "event", "")

        description = (
            f"{event} | "
            f"source={source_ip} | "
            f"user={username} | "
            f"port={port}"
        )

        timeline_event = TimelineEvent(
            event_type="EVIDENCE",
            description=description,
            timestamp=timestamp,
        )

        case.add_timeline_event(timeline_event)

    return case.timeline
