from dataclasses import dataclass


@dataclass
class ClosureAssessment:
    case_id: str
    closure_eligible: bool
    status: str
    reason: str
    human_approval_required: bool


def assess_closure(case, recovery):
    """
    Determine whether an incident case is eligible for closure.

    Closure requires:
    - No confirmed compromise
    - No containment required
    - No recovery required
    """

    if (
        not case.compromise_confirmed
        and not recovery.containment_required
        and not recovery.recovery_required
    ):
        return ClosureAssessment(
            case_id=case.case_id,
            closure_eligible=True,
            status="READY_FOR_CLOSURE",
            reason="No compromise, containment, or recovery activity remains.",
            human_approval_required=True,
        )

    return ClosureAssessment(
        case_id=case.case_id,
        closure_eligible=False,
        status="REMAINS_OPEN",
        reason="Additional incident-response activity is required.",
        human_approval_required=True,
    )
