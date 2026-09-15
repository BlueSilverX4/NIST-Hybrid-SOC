from dataclasses import dataclass


@dataclass
class RecoveryAssessment:
    case_id: str
    status: str
    compromise_confirmed: bool
    containment_required: bool
    recovery_required: bool
    notes: list[str]


def assess_recovery(case) -> RecoveryAssessment:

    if case.compromise_confirmed:
        return RecoveryAssessment(
            case_id=case.case_id,
            status="RECOVERY_REQUIRED",
            compromise_confirmed=True,
            containment_required=True,
            recovery_required=True,
            notes=[
                "Confirmed compromise requires containment.",
                "Affected assets must be assessed for recovery.",
                "Evidence preservation should continue.",
            ],
        )

    return RecoveryAssessment(
        case_id=case.case_id,
        status="NO_COMPROMISE_OBSERVED",
        compromise_confirmed=False,
        containment_required=False,
        recovery_required=False,
        notes=[
            "Malicious authentication activity was detected.",
            "No successful attacker authentication was observed.",
            "No recovery action is currently required.",
        ],
    )
