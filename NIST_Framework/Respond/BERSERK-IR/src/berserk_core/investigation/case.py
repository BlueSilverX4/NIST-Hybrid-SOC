from dataclasses import dataclass

from berserk_core.investigation.timeline import TimelineEvent


@dataclass
class EvidenceEvent:
    timestamp: str
    username: str
    source_ip: str
    port: int
    event: str

    def summary(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "username": self.username,
            "source_ip": self.source_ip,
            "port": self.port,
            "event": self.event,
        }


class IncidentCase:
    def __init__(
        self,
        case_id: str,
        title: str,
        severity: str,
        confidence: str,
        threat: str = None,
        indicator: str = None,
        attempts: int = 0,
        primary_indicator: str = None,
        detection: str = None,
        evidence: list = None,
    ):
        self.case_id = case_id
        self.title = title

        # Support both the original API and the newer test/API names.
        self.threat = threat if threat is not None else detection
        self.indicator = (
            indicator
            if indicator is not None
            else primary_indicator
        )

        # Public aliases used by reporting and validation.
        self.detection = (
            detection
            if detection is not None
            else self.threat
        )

        self.primary_indicator = (
            primary_indicator
            if primary_indicator is not None
            else self.indicator
        )

        self.attempts = attempts
        self.severity = severity
        self.confidence = confidence

        self.evidence = list(evidence) if evidence is not None else []
        self.timeline = []
        self.status = "OPEN"

        # Investigation state.
        self.compromise_confirmed = False

    def add_evidence(self, evidence: str) -> None:
        self.evidence.append(evidence)

    def evidence_summary(self) -> dict:
        source_ips = sorted({
            evidence.source_ip
            for evidence in self.evidence
            if hasattr(evidence, "source_ip")
            and evidence.source_ip
        })

        usernames = sorted({
            evidence.username
            for evidence in self.evidence
            if hasattr(evidence, "username")
            and evidence.username
        })

        ports = sorted({
            evidence.port
            for evidence in self.evidence
            if hasattr(evidence, "port")
            and evidence.port is not None
        })

        return {
            "source_ips": source_ips,
            "usernames": usernames,
            "ports": ports,
            "event_count": len(self.evidence),
        }

    def evidence_analysis(self) -> dict:
        from collections import Counter

        event_type_counts = Counter(
            evidence.event
            for evidence in self.evidence
            if hasattr(evidence, "event") and evidence.event
        )

        username_counts = Counter(
            evidence.username
            for evidence in self.evidence
            if hasattr(evidence, "username") and evidence.username
        )

        source_ip_counts = Counter(
            evidence.source_ip
            for evidence in self.evidence
            if hasattr(evidence, "source_ip") and evidence.source_ip
        )

        most_targeted_username = (
            username_counts.most_common(1)[0][0]
            if username_counts
            else None
        )

        dominant_source_ip = (
            source_ip_counts.most_common(1)[0][0]
            if source_ip_counts
            else None
        )

        repeated_authentication = (
            event_type_counts.get(
                "Failed SSH Authentication",
                0,
            ) >= 2
        )

        return {
           "event_type_counts": event_type_counts,
           "event_types": event_type_counts,
           "username_counts": username_counts,
           "source_ip_counts": source_ip_counts,
           "most_targeted_username": most_targeted_username,
           "dominant_source_ip": dominant_source_ip,
           "repeated_authentication": repeated_authentication,
        }

    def close(self) -> None:
        self.status = "CLOSED"

    def add_timeline_event(self, event: TimelineEvent) -> None:
        self.timeline.append(event)

        self.timeline.sort(
            key=lambda item: item.timestamp
        )

    def record_investigation_activity(
        self,
        description: str,
    ) -> TimelineEvent:
        event = TimelineEvent.create(
            event_type="INVESTIGATION",
            description=description,
        )

        self.add_timeline_event(event)

        return event

    def get_timeline_events(
        self,
        event_type: str,
    ) -> list:
        return [
            event
            for event in self.timeline
            if event.event_type == event_type
        ]

    def get_timeline_events_between(
        self,
        start_timestamp: str,
        end_timestamp: str,
    ) -> list:
        return [
            event
            for event in self.timeline
            if start_timestamp <= event.timestamp <= end_timestamp
        ]

    def summary(self) -> dict:
        return {
            "case_id": self.case_id,
            "title": self.title,
            "threat": self.threat,
            "indicator": self.indicator,
            "attempts": self.attempts,
            "severity": self.severity,
            "confidence": self.confidence,
            "status": self.status,
            "evidence": [
                evidence.summary()
                if hasattr(evidence, "summary")
                else evidence
                for evidence in self.evidence
            ],
            "timeline": [
                {
                    "event_type": event.event_type,
                    "action": event.event_type,
                    "description": event.description,
                    "timestamp": getattr(
                        event,
                        "timestamp",
                        None,
                    ),
                }
                for event in self.timeline
            ],
        }
