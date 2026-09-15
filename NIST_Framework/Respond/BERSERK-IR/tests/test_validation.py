import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src" / "berserk_core")
)

from case import EvidenceEvent, IncidentCase
from validation import validate_case

def create_valid_case():
    evidence = [
        EvidenceEvent(
            timestamp="Aug 3 08:14:22",
            username="admin",
            source_ip="185.220.101.5",
            port=42110,
            event="Failed SSH Authentication",
        )
    ]

    return IncidentCase(
        case_id="BERSERK-001",
        title="The Branded Host",
        severity="HIGH",
        confidence="HIGH",
        primary_indicator="185.220.101.5",
        detection="SSH Brute Force",
        evidence=evidence,
    )


def test_valid_case_passes_validation():
    case = create_valid_case()

    result = validate_case(case)

    assert result.valid is True
    assert result.issues == []


def test_missing_indicator_fails_validation():
    case = create_valid_case()
    case.primary_indicator = ""

    result = validate_case(case)

    assert result.valid is False
    assert "Primary indicator is missing." in result.issues


def test_missing_evidence_fails_validation():
    case = create_valid_case()
    case.evidence = []

    result = validate_case(case)

    assert result.valid is False
    assert "No evidence events are attached to the case." in result.issues
