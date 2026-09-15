from dataclasses import dataclass


@dataclass
class FindingAssessment:
    pattern: str
    severity: str
    confidence: str
    rationale: str


def assess_finding(case) -> FindingAssessment:
    analysis = case.evidence_analysis()

    if analysis["repeated_authentication"]:
        return FindingAssessment(
            pattern="SSH Brute Force",
            severity=case.severity,
            confidence=case.confidence,
            rationale=(
                "Repeated SSH authentication failures were observed "
                "against multiple targeted accounts."
            ),
        )

    return FindingAssessment(
        pattern="Unclassified Activity",
        severity=case.severity,
        confidence=case.confidence,
        rationale=(
            "Available evidence does not match a known attack pattern."
        ),
    )
