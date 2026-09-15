import json
from dataclasses import asdict
from pathlib import Path

try:
    from .response_plan import ResponsePlan
except ImportError:
    from response_plan import ResponsePlan


REPORT_DIR = (
    Path(__file__).resolve().parents[2]
    / "reports"
    / "incident_reports"
)


def export_response_plan(plan: ResponsePlan) -> Path:
    """
    Export a ResponsePlan as a JSON incident artifact.
    """

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = REPORT_DIR / f"{plan.case_id}-response.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(
            asdict(plan),
            file,
            indent=4
        )

    return output_file
