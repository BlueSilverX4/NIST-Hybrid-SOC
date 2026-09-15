from pathlib import Path

try:
    from .response_plan import ResponsePlan
except ImportError:
    from response_plan import ResponsePlan

PLAYBOOK_FILE = (
    Path(__file__).resolve().parents[2]
    / "playbooks"
    / "black_swordsman_protocol.md"
)


def load_playbook():
    """
    Load the BERSERK-IR Black Swordsman Protocol.
    """

    if not PLAYBOOK_FILE.exists():
        raise FileNotFoundError(
            f"Playbook not found: {PLAYBOOK_FILE}"
        )

    return PLAYBOOK_FILE.read_text(encoding="utf-8")


def generate_response(case, decision, protocol):
    """
    Generate a structured defensive response plan.

    Phase 9 operates in simulation mode.
    No system changes are performed.
    """

    playbook = load_playbook()

    action = decision["action"]

    if action == "INVESTIGATE":

        steps = [
            "Review SSH authentication failures",
            "Review targeted accounts",
            "Check for successful authentication",
            "Review related network and web activity",
            "Determine whether containment is necessary",
        ]

    elif action == "CONTAIN_PENDING_APPROVAL":

        steps = [
            "Validate malicious activity",
            "Review affected accounts",
            "Prepare indicator containment",
            "Obtain analyst approval",
            "Execute containment only after approval",
        ]

    elif action == "CONTAIN":

        steps = [
            "Confirm compromise",
            "Isolate affected system",
            "Review compromised accounts",
            "Preserve forensic evidence",
            "Begin recovery procedures",
        ]

    elif action == "MONITOR":

        steps = [
            "Continue monitoring the indicator",
            "Increase authentication logging",
            "Look for additional related events",
        ]

    else:

        steps = [
            "Document finding",
            "Continue routine monitoring",
        ]

    return ResponsePlan(
        case_id=case.case_id,
        indicator=case.primary_indicator,
        action=action,
        mode="SIMULATION",
        playbook="Black Swordsman Incident Response Protocol",
        protocol_phase=protocol["phase"],
        protocol_name=protocol["name"],
        human_approval_required=decision["requires_human_approval"],
        steps=steps,
    )
