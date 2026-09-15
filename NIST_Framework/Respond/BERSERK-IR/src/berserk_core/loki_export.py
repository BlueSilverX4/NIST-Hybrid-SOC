from __future__ import annotations

import json
from pathlib import Path


def build_loki_events(case_report: dict) -> list[dict]:
    """Build lightweight Loki telemetry from an existing BERSERK case report."""

    case = case_report["case"]
    investigation = case_report.get("investigation", {})
    mitre = case_report.get("mitre", {})
    decision = case_report.get("decision", {})
    recovery = case_report.get("recovery", {})

    return [
        {
            "case_id": case["case_id"],
            "event": "detection",
            "threat": case["threat"],
            "severity": case["severity"],
            "indicator": case["indicator"],
            "attempts": case["attempts"],
        },
        {
            "case_id": case["case_id"],
            "event": "investigation",
            "events": investigation.get("event_count", 0),
            "duration_seconds": investigation.get("duration_seconds", 0.0),
            "repeated_activity": investigation.get(
                "repeated_activity", False
            ),
        },
        {
            "case_id": case["case_id"],
            "event": "indicator",
            "indicator": case["indicator"],
        },
        {
            "case_id": case["case_id"],
            "event": "accounts",
            "accounts": investigation.get("targeted_users", []),
        },
        {
            "case_id": case["case_id"],
            "event": "mitre",
            "technique": mitre.get("technique"),
            "subtechnique": mitre.get("subtechnique"),
            "name": mitre.get("name"),
        },
        {
            "case_id": case["case_id"],
            "event": "decision",
            "decision": decision.get("action"),
            "human_approval_required": decision.get(
                "requires_human_approval", True
            ),
        },
        {
            "case_id": case["case_id"],
            "event": "compromise",
            "status": recovery.get("status"),
            "confirmed": recovery.get("compromise_confirmed", False),
        },
    ]


def export_loki_events(
    case_report_path: str | Path,
    output_path: str | Path,
) -> Path:
    """Export BERSERK case data as JSONL telemetry for Loki/Alloy."""

    case_report_path = Path(case_report_path)
    output_path = Path(output_path)

    with case_report_path.open("r", encoding="utf-8") as file:
        case_report = json.load(file)

    events = build_loki_events(case_report)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        for event in events:
            file.write(json.dumps(event, separators=(",", ":")) + "\n")

    return output_path


if __name__ == "__main__":
    export_loki_events(
        "reports/incident_reports/BERSERK-001-case.json",
        "reports/incident_reports/BERSERK-001-loki.jsonl",
    )

    print(
        "BERSERK Loki telemetry exported to "
        "reports/incident_reports/BERSERK-001-loki.jsonl"
    )
