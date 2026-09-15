from pathlib import Path

from .investigation.evidence_enrichment import enrich_evidence
from .investigation.timeline_visualization import render_timeline
from .assessment import assess_finding
from .case import EvidenceEvent, IncidentCase
from .case_report import export_case_report
from .closure import assess_closure
from .correlation import correlate_evidence
from .decision import evaluate_decision
from .detector import detect_ssh_bruteforce
from .exporter import export_response_plan
from .integrity import write_hash_file
from .investigation.assessment import assess_investigation
from .investigation.reconstruction import reconstruct_evidence_timeline
from .lessons_learned import assess_lessons
from .mitre import recommend_mitre
from .protocol import get_protocol_phase
from .recovery import assess_recovery
from .response import generate_response
from .scoring import calculate_threat_score
from .validation import validate_case


LOG_FILE = Path.home() / "Desktop/sec-agent/artifacts/auth.log"
CASE_ID = "BERSERK-001"
CASE_TITLE = "The Branded Host"


def load_logs() -> list[str]:
    """Load authentication logs used by the detection engine."""
    with LOG_FILE.open("r", encoding="utf-8") as file:
        return file.readlines()


def build_case(finding: dict) -> IncidentCase:
    """Convert a detector finding into a BERSERK incident case."""
    evidence_events = [
        EvidenceEvent(
            timestamp=event["timestamp"],
            username=event["username"],
            source_ip=event["source_ip"],
            port=event["port"],
            event=event["event"],
        )
        for event in finding["evidence"]
    ]

    return IncidentCase(
        case_id=CASE_ID,
        title=CASE_TITLE,
        severity=finding["severity"],
        confidence=finding["confidence"],
        primary_indicator=finding["indicator"],
        detection=finding["event"],
        attempts=len(evidence_events),
        evidence=evidence_events,
    )


def print_validation(validation) -> bool:
    """Display case validation results and return whether the case is valid."""
    print("\n--- BERSERK Case Validation ---")
    print(f"Case:       {validation.case_id}")
    print(f"Valid:      {validation.valid}")

    if validation.valid:
        print("Status:     VALIDATION_PASSED")
        print("Issues:     None")
        return True

    print("Status:     VALIDATION_FAILED")
    print("\nValidation Issues:")

    for number, issue in enumerate(validation.issues, start=1):
        print(f"[{number}] {issue}")

    print("\nPipeline halted due to validation failure.")
    return False


def print_correlation(case: IncidentCase) -> None:
    """Display evidence correlation results."""
    correlation = correlate_evidence(case)

    print("\n--- BERSERK Evidence Correlation ---")
    print(f"Source IP:        {correlation.source_ip}")
    print(f"Targeted Users:   {', '.join(correlation.targeted_usernames)}")
    print(f"Related Events:   {correlation.event_count}")
    print(f"Pattern:          {correlation.pattern}")


def print_assessment(case: IncidentCase) -> None:
    """Display finding assessment results."""
    assessment = assess_finding(case)

    print("\n--- BERSERK Finding Assessment ---")
    print(f"Pattern:          {assessment.pattern}")
    print(f"Severity:         {assessment.severity}")
    print(f"Confidence:       {assessment.confidence}")
    print(f"Rationale:        {assessment.rationale}")


def print_case_summary(case: IncidentCase) -> None:
    """Display the core incident case summary."""
    print("\n--- BERSERK Case Summary ---")
    print(f"Case ID:      {case.case_id}")
    print(f"Title:        {case.title}")
    print(f"Threat:       {case.detection}")
    print(f"Indicator:    {case.primary_indicator}")
    print(f"Attempts:     {len(case.evidence)}")
    print(f"Severity:     {case.severity}")
    print(f"Confidence:   {case.confidence}")
    print(f"Compromise:   {case.compromise_confirmed}")


def print_evidence(case: IncidentCase) -> None:
    """Display evidence associated with the case."""
    print("\n--- Evidence ---")

    for event in case.evidence:
        print(
            f"{event.timestamp} | "
            f"user={event.username} | "
            f"ip={event.source_ip} | "
            f"port={event.port}"
        )


def print_mitre(mitre) -> None:
    """Display MITRE ATT&CK recommendation."""
    print("\n--- MITRE ATT&CK Recommendation ---")

    if not mitre:
        print("No MITRE recommendation available.")
        return

    print(f"Technique:       {mitre['technique']}")
    print(f"Sub-technique:   {mitre['subtechnique']}")
    print(f"Name:             {mitre['name']}")
    print(f"Confidence:       {mitre['confidence']}")
    print("Status:           REQUIRES HUMAN VALIDATION")


def print_threat_judgment(threat_score: dict) -> None:
    """Display threat scoring results."""
    print("\n--- BERSERK Threat Judgment ---")
    print(f"Risk Score:      {threat_score['score']}")
    print(f"Recommended:     {threat_score['severity']}")

    print("\nRisk Factors:")
    for factor in threat_score["factors"]:
        print(f"- {factor}")

    print("\nStatus:          REQUIRES HUMAN VALIDATION")


def print_decision(decision: dict) -> None:
    """Display decision gate results."""
    print("\n--- BERSERK Decision Gate ---")
    print(f"Recommended Action: {decision['action']}")
    print(f"Reason:             {decision['reason']}")
    print(f"Human Approval:     {decision['requires_human_approval']}")


def print_protocol(protocol) -> None:
    """Display Black Swordsman Protocol mapping."""
    print("\n--- Black Swordsman Protocol Mapping ---")

    if not protocol:
        print("No protocol phase mapped.")
        return

    print(f"Phase:       {protocol['phase']}")
    print(f"Name:        {protocol['name']}")
    print(f"Objective:   {protocol['objective']}")

    print("\nProtocol Tasks:")
    for number, task in enumerate(protocol["tasks"], start=1):
        print(f"[{number}] {task}")


def run_response_engine(
    case: IncidentCase,
    decision: dict,
    protocol,
):
    """Generate, export, and hash the response plan."""
    response = generate_response(case, decision, protocol)

    response_file = export_response_plan(response)
    integrity_file = write_hash_file(response_file)

    print("\n--- BERSERK Response Engine ---")
    print(f"Case:       {response.case_id}")
    print(f"Indicator:  {response.indicator}")
    print(f"Action:     {response.action}")
    print(f"Mode:       {response.mode}")
    print(f"Playbook:   {response.playbook}")
    print(f"Phase:      {response.protocol_phase}")
    print(f"Protocol:   {response.protocol_name}")
    print(f"Human Approval: {response.human_approval_required}")

    print("\nRecommended Response Steps:")
    for number, step in enumerate(response.steps, start=1):
        print(f"[{number}] {step}")

    print("\nNo system changes performed.")
    print(f"\nResponse artifact: {response_file}")
    print(f"Integrity hash:    {integrity_file}")

    return response


def print_recovery(recovery) -> None:
    """Display recovery assessment."""
    print("\n--- BERSERK Recovery Assessment ---")
    print(f"Case:                  {recovery.case_id}")
    print(f"Status:                {recovery.status}")
    print(f"Compromise Confirmed:  {recovery.compromise_confirmed}")
    print(f"Containment Required:  {recovery.containment_required}")
    print(f"Recovery Required:     {recovery.recovery_required}")

    print("\nRecovery Notes:")
    for number, note in enumerate(recovery.notes, start=1):
        print(f"[{number}] {note}")


def print_closure(closure) -> None:
    """Display closure assessment."""
    print("\n--- BERSERK Closure Assessment ---")
    print(f"Case:                  {closure.case_id}")
    print(f"Status:                {closure.status}")
    print(f"Closure Eligible:      {closure.closure_eligible}")
    print(f"Human Approval:        {closure.human_approval_required}")
    print(f"Reason:                {closure.reason}")


def print_lessons(lessons) -> None:
    """Display lessons-learned assessment."""
    print("\n--- BERSERK Campfire ---")
    print(f"Case:                  {lessons.case_id}")
    print(f"Status:                {lessons.status}")

    sections = [
        ("What Worked", lessons.what_worked),
        ("What Failed", lessons.what_failed),
        ("Detection Review", lessons.detection_source),
        ("Early Detection", lessons.early_detection),
        ("Playbook Review", lessons.playbook_effectiveness),
        ("Detection Tuning", lessons.detection_tuning),
        ("Defensive Improvements", lessons.defensive_improvements),
    ]

    for title, items in sections:
        print(f"\n{title}:")
        for number, item in enumerate(items, start=1):
            print(f"[{number}] {item}")


def print_investigation_timeline(case: IncidentCase) -> None:
    """Display the reconstructed investigation timeline."""
    print("\n--- BERSERK Investigation Timeline ---")

    if not case.timeline:
        print("No investigation timeline events recorded.")
        return

    for number, event in enumerate(case.timeline, start=1):
        print(
            f"[{number}] "
            f"{event.timestamp} | "
            f"{event.event_type} | "
            f"{event.description}"
        )


def print_investigation_assessment(assessment: dict) -> None:
    """Display the investigation assessment."""
    print("\n--- BERSERK Investigation Assessment ---")
    print(f"Events:              {assessment['event_count']}")
    print(f"First Event:         {assessment['first_event']}")
    print(f"Last Event:          {assessment['last_event']}")
    print(f"Duration:            {assessment['duration_seconds']} seconds")
    print(f"Repeated Activity:   {assessment['repeated_activity']}")
    print(
        f"Targeted Users:      "
        f"{', '.join(assessment['targeted_users']) or 'None'}"
    )
    print(f"Multiple Users:      {assessment['multiple_users_targeted']}")
    print(f"Privileged Target:   {assessment['privileged_account_targeted']}")
    print(
        f"Dominant Source IP:  "
        f"{assessment['dominant_source_ip'] or 'None'}"
    )

    print("Event Types:")
    for event_type, count in assessment["event_types"].items():
        print(f"  - {event_type}: {count}")

    print("Findings:")

    for index, finding in enumerate(
        assessment["findings"],
        start=1,
    ):
        print(f"  [{index}] {finding}")

def main() -> None:
    """Run the complete BERSERK-IR incident response pipeline."""
    print("\n=== BERSERK-IR DETECTION ENGINE ===\n")

    # 1. Load telemetry
    try:
        logs = load_logs()
    except FileNotFoundError:
        print(f"ERROR: Log file not found: {LOG_FILE}")
        return
    except OSError as exc:
        print(f"ERROR: Unable to read log file: {exc}")
        return

    # 2. Detection
    findings = detect_ssh_bruteforce(logs)

    if not findings:
        print("No suspicious SSH activity detected.")
        return

    finding = findings[0]

    # 3. Case creation
    case = build_case(finding)

    # 4. Investigation reconstruction
    reconstruct_evidence_timeline(case)

    # 5. Investigation assessment
    investigation = assess_investigation(case)
    print_investigation_assessment(investigation)

    # 6. Timeline visualization
    timeline_output = render_timeline(case)
    print(timeline_output)

    # 7. Evidence enrichment
    enrichment = enrich_evidence(case)

    print("\n--- BERSERK Evidence Enrichment ---")
    print(f"Indicator:             {enrichment['indicator']}")
    print(f"Indicator Type:        {enrichment['indicator_type']}")
    print(f"Evidence Count:        {enrichment['evidence_count']}")
    print(f"First Seen:            {enrichment['first_seen']}")
    print(f"Last Seen:             {enrichment['last_seen']}")
    print(f"Duration:              {enrichment['duration_seconds']} seconds")
    print(
        f"Targeted Accounts:     "
        f"{', '.join(enrichment['targeted_accounts']) or 'None'}"
    )
    print(
        f"Observed Ports:        "
        f"{', '.join(map(str, enrichment['observed_ports'])) or 'None'}"
    )
    print(
        f"Observed Events:       "
        f"{', '.join(enrichment['observed_events']) or 'None'}"
    )

    print("Attack Context:")
    for number, context in enumerate(
        enrichment["attack_context"],
        start=1,
    ):
        print(f"  [{number}] {context}")

    print(
        f"Confidence:            {enrichment['confidence']}"
    )
    print(
        f"Human Validation:      "
        f"{enrichment['human_validation_required']}"
    )


    # 8. Case validation
    validation = validate_case(case)

    # 8. Evidence correlation
    print_correlation(case)

    # 9. Finding assessment
    print_assessment(case)

    # 10. MITRE ATT&CK mapping
    mitre = recommend_mitre(case.detection)
    print_mitre(mitre)

    # 11. Threat scoring
    threat_score = calculate_threat_score(case)
    print_threat_judgment(threat_score)

    # 12. Decision gate
    decision = evaluate_decision(case, threat_score)
    print_decision(decision)

    # 13. Case summary
    print_case_summary(case)
    print_evidence(case)

    # 14. Black Swordsman Protocol
    protocol = get_protocol_phase(decision["action"])
    print_protocol(protocol)

    # 15. Response engine
    response = run_response_engine(case, decision, protocol)

    # 16. Recovery assessment
    recovery = assess_recovery(case)
    print_recovery(recovery)

    # 17. Closure assessment
    closure = assess_closure(case, recovery)
    print_closure(closure)

    # 18. Lessons learned
    lessons = assess_lessons(case)
    print_lessons(lessons)

    # 19. Final case report
    case_report_file = export_case_report(
    case,
    mitre,
    threat_score,
    decision,
    response,
    recovery,
    closure,
    lessons,
    investigation=investigation,
    enrichment=enrichment,
)

    print("\n--- BERSERK Case Report ---")
    print(f"Case Report: {case_report_file}")

    print("\n=== BERSERK-IR PIPELINE COMPLETE ===\n")


if __name__ == "__main__":
    main()
