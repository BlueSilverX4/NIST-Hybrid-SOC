from dataclasses import dataclass


@dataclass
class ValidationResult:
    case_id: str
    valid: bool
    issues: list[str]


def validate_case(case) -> ValidationResult:
    issues = []

    if not case.case_id:
        issues.append("Case ID is missing.")

    if not case.primary_indicator:
        issues.append("Primary indicator is missing.")

    if not case.detection:
        issues.append("Detection type is missing.")

    if not case.evidence:
        issues.append("No evidence events are attached to the case.")

    for event in case.evidence:
        if not event.timestamp:
            issues.append("Evidence event is missing a timestamp.")

        if not event.source_ip:
            issues.append("Evidence event is missing a source IP.")

        if not event.username:
            issues.append("Evidence event is missing a username.")

    return ValidationResult(
        case_id=case.case_id,
        valid=len(issues) == 0,
        issues=issues,
    )
