from berserk_core.investigation.case import (
    EvidenceEvent,
    IncidentCase,
)
from berserk_core.investigation.reconstruction import (
    reconstruct_evidence_timeline,
)
from berserk_core.investigation.evidence_enrichment import (
    enrich_evidence,
)


def create_case():
    case = IncidentCase(
        case_id="BERSERK-001",
        title="The Branded Host",
        threat="SSH Brute Force",
        indicator="185.220.101.5",
        attempts=4,
        severity="HIGH",
        confidence="HIGH",
    )

    case.evidence = [
        EvidenceEvent(
            timestamp="2026-08-03T08:14:22Z",
            username="admin",
            source_ip="185.220.101.5",
            port=42110,
            event="Failed SSH Authentication",
        ),
        EvidenceEvent(
            timestamp="2026-08-03T08:14:25Z",
            username="admin",
            source_ip="185.220.101.5",
            port=42112,
            event="Failed SSH Authentication",
        ),
        EvidenceEvent(
            timestamp="2026-08-03T08:14:28Z",
            username="root",
            source_ip="185.220.101.5",
            port=42115,
            event="Failed SSH Authentication",
        ),
        EvidenceEvent(
            timestamp="2026-08-03T08:14:31Z",
            username="root",
            source_ip="185.220.101.5",
            port=42118,
            event="Failed SSH Authentication",
        ),
    ]

    return case


def test_enrichment_classifies_ipv4_indicator():
    case = create_case()

    enrichment = enrich_evidence(case)

    assert enrichment["indicator"] == "185.220.101.5"
    assert enrichment["indicator_type"] == "IPv4 Address"


def test_enrichment_counts_evidence():
    case = create_case()

    enrichment = enrich_evidence(case)

    assert enrichment["evidence_count"] == 4


def test_enrichment_identifies_time_range():
    case = create_case()

    reconstruct_evidence_timeline(case)

    enrichment = enrich_evidence(case)

    assert enrichment["first_seen"] == "2026-08-03T08:14:22Z"
    assert enrichment["last_seen"] == "2026-08-03T08:14:31Z"
    assert enrichment["duration_seconds"] == 9.0


def test_enrichment_identifies_targeted_accounts():
    case = create_case()

    enrichment = enrich_evidence(case)

    assert enrichment["targeted_accounts"] == [
        "admin",
        "root",
    ]


def test_enrichment_identifies_observed_ports():
    case = create_case()

    enrichment = enrich_evidence(case)

    assert enrichment["observed_ports"] == [
        42110,
        42112,
        42115,
        42118,
    ]


def test_enrichment_identifies_observed_events():
    case = create_case()

    enrichment = enrich_evidence(case)

    assert enrichment["observed_events"] == [
        "Failed SSH Authentication",
    ]


def test_enrichment_builds_attack_context():
    case = create_case()

    reconstruct_evidence_timeline(case)

    enrichment = enrich_evidence(case)

    assert "Repeated authentication failures" in (
        enrichment["attack_context"]
    )

    assert "Multiple accounts targeted" in (
        enrichment["attack_context"]
    )

    assert "Privileged account targeted" in (
        enrichment["attack_context"]
    )


def test_enrichment_requires_human_validation():
    case = create_case()

    enrichment = enrich_evidence(case)

    assert enrichment["confidence"] == "HIGH"
    assert enrichment["human_validation_required"] is True


def test_enrichment_handles_empty_evidence():
    case = IncidentCase(
        case_id="BERSERK-EMPTY",
        title="Empty Case",
        threat="Unknown",
        indicator=None,
        attempts=0,
        severity="LOW",
        confidence="LOW",
    )

    enrichment = enrich_evidence(case)

    assert enrichment["indicator"] is None
    assert enrichment["indicator_type"] == "Unknown"
    assert enrichment["evidence_count"] == 0
    assert enrichment["first_seen"] is None
    assert enrichment["last_seen"] is None
    assert enrichment["duration_seconds"] == 0
    assert enrichment["targeted_accounts"] == []
    assert enrichment["observed_ports"] == []
    assert enrichment["observed_events"] == []
    assert enrichment["attack_context"] == []
    assert enrichment["human_validation_required"] is True


def test_enrichment_does_not_modify_case():
    case = create_case()

    reconstruct_evidence_timeline(case)

    before = [
        (
            event.event_type,
            event.description,
            event.timestamp,
        )
        for event in case.timeline
    ]

    enrich_evidence(case)

    after = [
        (
            event.event_type,
            event.description,
            event.timestamp,
        )
        for event in case.timeline
    ]

    assert after == before
