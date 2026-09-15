import json
from dataclasses import asdict
from pathlib import Path


REPORT_DIR = (
    Path.home()
    / "Desktop/BERSERK-IR/reports/incident_reports"
)


def export_case_report(
    case,
    mitre,
    threat_score,
    decision,
    response,
    recovery,
    closure,
    lessons,
    investigation=None,
    enrichment=None,
    report_dir=None,
):
    """
    Export the complete BERSERK incident lifecycle
    as a structured JSON case report.

    Args:
        case: Incident case.
        mitre: MITRE ATT&CK mapping.
        threat_score: Threat assessment.
        decision: Decision gate result.
        response: Response assessment.
        recovery: Recovery assessment.
        closure: Closure assessment.
        lessons: Lessons learned assessment.
        investigation: Investigation assessment.
        report_dir: Optional output directory.

    Returns:
        Path to the generated case report.
    """

    output_dir = (
        Path(report_dir)
        if report_dir is not None
        else REPORT_DIR
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    report = {
        "case": case.summary(),
        "investigation": investigation or {},
        "evidence_enrichment": enrichment or {},
        "mitre": mitre,
        "threat_assessment": threat_score,
        "decision": decision,
        "response": asdict(response),
        "recovery": asdict(recovery),
        "closure": asdict(closure),
        "lessons_learned": asdict(lessons),
    }

    output_file = (
        output_dir
        / f"{case.case_id}-case.json"
    )

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=4,
            default=str,
        )

    return output_file
