from dataclasses import dataclass, field


@dataclass
class ResponsePlan:
    case_id: str
    indicator: str
    action: str
    mode: str
    playbook: str
    protocol_phase: str
    protocol_name: str
    human_approval_required: bool
    steps: list[str] = field(default_factory=list)
