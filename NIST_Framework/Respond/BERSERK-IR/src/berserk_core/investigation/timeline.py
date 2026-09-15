from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class TimelineEvent:
    action: str | None = None
    description: str = ""
    timestamp: str = ""
    event_type: str | None = None

    def __post_init__(self):
        if self.event_type is None:
            self.event_type = self.action

        if self.action is None:
            self.action = self.event_type

    @classmethod
    def create(
        cls,
        action: str | None = None,
        description: str = "",
        event_type: str | None = None,
    ):
        resolved_type = event_type or action

        return cls(
            action=resolved_type,
            event_type=resolved_type,
            description=description,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def summary(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "action": self.action,
            "event_type": self.event_type,
            "description": self.description,
        }
