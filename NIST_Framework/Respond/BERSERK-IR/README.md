# BERSERK-IR

## Black Swordsman Incident Response Framework

A defensive incident-response laboratory combining deterministic detection, investigation, evidence enrichment, MITRE ATT&CK mapping, response decisioning, evidence integrity, and Loki/Grafana observability.

> **BERSERK-IR** uses Berserk-inspired terminology as a presentation layer over a conventional incident-response workflow. The underlying methodology remains focused on practical SOC and incident-response processes.

---

## Project Overview

BERSERK-IR is a Python-based incident-response laboratory designed to simulate the investigation of a suspected SSH brute-force attack.

The project demonstrates how security telemetry can move through a structured workflow:

**Detection → Investigation → Evidence Enrichment → MITRE ATT&CK Mapping → Threat Assessment → Response Decision → Recovery → Reporting → Observability**

The project emphasizes deterministic analysis, reproducible evidence handling, human validation, and clear separation between automated recommendations and analyst decisions.

---

## Objectives

The primary objectives of BERSERK-IR are to demonstrate practical incident-response capabilities through a reproducible security investigation.

The project focuses on:

- Detecting repeated SSH authentication failures.
- Identifying and correlating related security events.
- Reconstructing an attack timeline from available evidence.
- Enriching evidence using locally observed characteristics.
- Mapping observed activity to MITRE ATT&CK.
- Calculating threat severity and confidence.
- Separating automated recommendations from human approval.
- Generating structured incident-response reports.
- Preserving evidence integrity through hashing and verification.
- Exporting incident telemetry for centralized observability.
- Visualizing investigation data through Loki and Grafana.
- Validating the project through automated Python tests.

The goal is not to automatically declare an attacker or take irreversible action. Instead, BERSERK-IR demonstrates a controlled workflow where automation assists the analyst while final response decisions remain subject to human validation.

---

## Incident Scenario

### Case BERSERK-001 — The Branded Host

BERSERK-IR investigates a simulated SSH brute-force incident involving repeated authentication failures from a single external IP address.

| Field | Value |
|---|---|
| Case ID | `BERSERK-001` |
| Case Title | **The Branded Host** |
| Threat | SSH Brute Force |
| Indicator | `185.220.101.5` |
| Authentication Attempts | `4` |
| Targeted Accounts | `admin`, `root` |
| Severity | `HIGH` |
| Confidence | `HIGH` |
| Attack Window | `9 seconds` |
| MITRE ATT&CK | `T1110.001 — Password Guessing` |
| Response Decision | `INVESTIGATE` |
| Human Approval | Required |
| Compromise Status | `NO_COMPROMISE_OBSERVED` |

### Observed Activity

The investigation identified four failed SSH authentication events associated with the same source indicator:

```text
Aug 03 08:14:22  admin  port 42110
Aug 03 08:14:25  admin  port 42112
Aug 03 08:14:28  root   port 42115
Aug 03 08:14:31  root   port 42118
```

The events demonstrate a progression from repeated authentication attempts against the `admin` account to attempts against the privileged `root` account.

### Investigation Outcome

Based on the available evidence, BERSERK-IR determined:

- Four failed SSH authentication attempts were observed.
- All four events were associated with `185.220.101.5`.
- Multiple accounts were targeted.
- The privileged `root` account was targeted.
- The activity occurred within a 9-second window.
- The observed behavior was consistent with password-guessing activity.
- MITRE ATT&CK mapping identified `T1110.001 — Password Guessing`.
- No successful compromise was observed in the available evidence.
- The automated response recommendation was `INVESTIGATE`.
- Human validation was required before taking further response action.

> **Evidence Note:** `185.220.101.5` is treated as an observed indicator within this laboratory scenario. BERSERK-IR does not independently establish that the IP address belongs to a malicious actor.

### Case Classification

The incident was retained as an investigation candidate rather than automatically declared a confirmed compromise.

This distinction is intentional. BERSERK-IR is designed to assist an analyst by identifying patterns, organizing evidence, and producing recommendations while keeping final investigative and response decisions under human control.

---

## Architecture

BERSERK-IR uses a modular Python-based incident-response pipeline. The investigation engine processes evidence, produces structured case data, and then exports selected incident telemetry into a local observability pipeline.

### Core Investigation Flow

```text
Security Evidence
       │
       ▼
Detection Engine
       │
       ▼
Incident Case
       │
       ├──► Threat Scoring
       │
       ├──► Investigation & Timeline
       │
       ├──► Evidence Enrichment
       │
       ├──► MITRE ATT&CK Mapping
       │
       ├──► Response Decision
       │
       └──► Case Report
                │
                ▼
          Evidence Integrity
```

### Observability Pipeline

```text
BERSERK-001-case.json
        │
        ▼
   Loki Exporter
        │
        ▼
BERSERK-001-loki.jsonl
        │
        ▼
    Grafana Alloy
        │
        ▼
       Loki
        │
        ▼
     Grafana
```

### Architecture Components

| Component | Purpose |
|---|---|
| Python Detection Engine | Identifies repeated SSH authentication failures |
| Incident Case Model | Represents the investigation and associated evidence |
| Investigation Modules | Reconstruct and analyze the incident timeline |
| Evidence Enrichment | Adds locally derived context to observed evidence |
| MITRE ATT&CK Mapping | Maps observed behavior to ATT&CK techniques |
| Threat Scoring | Calculates severity and confidence |
| Decision Engine | Produces an automated response recommendation |
| Response Module | Defines appropriate response actions |
| Case Report Generator | Produces structured incident documentation |
| Integrity Module | Supports evidence hashing and verification |
| Loki Exporter | Converts case data into telemetry events |
| Grafana Alloy | Collects and forwards incident telemetry |
| Loki | Stores and queries incident telemetry |
| Grafana | Visualizes the investigation through dashboards |

---

## Detection

BERSERK-IR begins with deterministic detection of repeated SSH authentication failures.

The detection engine analyzes authentication evidence and looks for repeated failed login attempts associated with the same source indicator. Rather than relying on a single event, the engine evaluates the observed activity as a pattern.

### Detection Logic

The current case produced the following detection result:

```text
Case ID:       BERSERK-001
Threat:        SSH Brute Force
Indicator:     185.220.101.5
Attempts:      4
Severity:      HIGH
Confidence:    HIGH
Compromise:    False

---

## Investigation

After detection, BERSERK-IR transitions into structured investigation.

The investigation workflow reconstructs the observed authentication activity into a timeline, analyzes the attack pattern, and produces an assessment of the available evidence.

### Timeline Reconstruction

The investigation engine reconstructs related evidence events in chronological order.

For BERSERK-001, the observed activity was:

```text
Aug 03 08:14:22  admin  port 42110
Aug 03 08:14:25  admin  port 42112
Aug 03 08:14:28  root   port 42115
Aug 03 08:14:31  root   port 42118

---

## Evidence Enrichment

BERSERK-IR performs local evidence enrichment after the initial investigation.

The enrichment process derives additional context from the evidence already available to the case. It does not contact external threat-intelligence services or automatically classify the indicator as malicious.

### Enrichment Results

For BERSERK-001, the enrichment process identified:

```text
Indicator:          185.220.101.5
Indicator Type:     IPv4 Address
Evidence Count:     4
First Seen:         Aug 03 08:14:22
Last Seen:          Aug 03 08:14:31
Duration:           9 seconds
Targeted Accounts:  admin, root
Observed Ports:     42110, 42112, 42115, 42118
Observed Event:     Failed SSH Authentication
Confidence:         HIGH

---

## MITRE ATT&CK Mapping

BERSERK-IR maps observed attack behavior to the MITRE ATT&CK framework as part of the investigation workflow.

For BERSERK-001, the observed repeated authentication failures were mapped to:

```text
Tactic:        Credential Access
Technique:     T1110 — Brute Force
Sub-technique: T1110.001 — Password Guessing
Confidence:    HIGH
Status:        REQUIRES HUMAN VALIDATION

---

## Threat Assessment & Decisioning

BERSERK-IR evaluates the collected evidence to produce a structured threat assessment and response recommendation.

The assessment combines detection results, investigation findings, and contextual evidence rather than relying on a single indicator.

### Threat Assessment

For BERSERK-001, the resulting assessment was:

```text
Severity:        HIGH
Confidence:      HIGH
Threat:          SSH Brute Force
Indicator:       185.220.101.5
Attempts:        4
Compromise:      False

---

## Response & Recovery

BERSERK-IR translates the investigation findings into a structured response recommendation.

The response workflow is designed to support analyst-led incident handling rather than automatically performing irreversible containment actions.

### Response Strategy

For BERSERK-001, the recommended action was:

```text
Decision:            INVESTIGATE
Severity:            HIGH
Human Approval:      REQUIRED
Compromise Observed: NO

---

## Evidence Integrity

BERSERK-IR includes an evidence-integrity workflow for generated incident-response artifacts.

The integrity module uses SHA-256 hashing to provide a deterministic way to verify whether a generated artifact has changed after it was recorded.

### Integrity Artifact

For BERSERK-001, the response artifact is accompanied by a SHA-256 checksum:

```text
BERSERK-001-response.json
BERSERK-001-response.json.sha256

---

## Loki + Grafana Observability

BERSERK-IR extends the incident-response workflow with a local observability pipeline using Grafana Alloy, Loki, and Grafana.

The purpose of this layer is to transform structured incident data into searchable telemetry and provide a visual investigation interface.

### Telemetry Pipeline

The case report is converted into compact JSONL telemetry events by the BERSERK-IR Loki exporter.

```text
BERSERK-001-case.json
        │
        ▼
   Loki Exporter
        │
        ▼
BERSERK-001-loki.jsonl
        │
        ▼
    Grafana Alloy
        │
        ▼
       Loki
        │
        ▼
     Grafana

---

## Testing

BERSERK-IR includes automated tests covering the core incident-response workflow.

The test suite validates functionality across detection, investigation, case reporting, evidence enrichment, timeline visualization, and related components.

### Test Execution

The full test suite can be executed with:

```bash
PYTHONPATH=src python3 -m pytest tests/ -q

---

## Repository Structure

The project is organized around the incident-response workflow and separates source code, tests, documentation, reports, dashboards, and evidence screenshots.

```text
BERSERK-IR/
├── dashboards/
│   └── grafana/
│       └── BERSERK-IR-Incident-Response-Dashboard.json
├── playbooks/
│   ├── black_swordsman_protocol.md
│   ├── case_001_dragonslayer_response.md
│   ├── case_001_mitre_analysis.md
│   └── case_001_threat_judgment.md
├── reports/
│   ├── dashboard/
│   │   └── BERSERK-001-loki-query.json
│   └── incident_reports/
│       ├── BERSERK-001-case.json
│       ├── BERSERK-001-loki.jsonl
│       ├── BERSERK-001-response.json
│       ├── BERSERK-001-response.json.sha256
│       └── CASE-001_The_Branded_Host.md
├── screenshots/
│   ├── 01-environment/
│   ├── 02-detection/
│   ├── 03-investigation/
│   ├── 04-mitre/
│   ├── 05-response/
│   ├── 06-dashboard/
│   └── 07-challenge/
├── src/
│   └── berserk_core/
├── tests/
├── case.md
├── .gitignore
└── README.md

---

## Key Skills Demonstrated

BERSERK-IR demonstrates practical cybersecurity and incident-response skills across the full investigation lifecycle.

### Security Operations

- Security event detection and triage
- SSH authentication monitoring
- Behavioral pattern analysis
- Incident classification
- Threat severity and confidence assessment
- Investigation prioritization

### Incident Response

- Incident timeline reconstruction
- Evidence correlation and analysis
- Response decisioning
- Human-in-the-loop validation
- Recovery considerations
- Structured incident reporting

### Threat Intelligence & Frameworks

- MITRE ATT&CK technique mapping
- Evidence-based attack characterization
- Local evidence enrichment
- Indicator analysis

### Security Engineering

- Python-based security automation
- Modular incident-response architecture
- Automated testing with pytest
- Evidence integrity with SHA-256
- Structured JSON and JSONL telemetry
- Reproducible analysis workflows

### SIEM & Observability

- Grafana Alloy telemetry collection
- Loki log aggregation and querying
- Grafana dashboard development
- Log parsing and labeling
- Security telemetry visualization

### Analyst Mindset

The project emphasizes evidence-driven investigation, reproducibility, documentation, and human oversight.

Automation is used to reduce repetitive analysis and organize evidence while keeping consequential investigative and response decisions under analyst control.


---


## Limitations & Future Improvements

BERSERK-IR is a local incident-response laboratory and is intentionally scoped for reproducibility, learning, and portfolio demonstration.

### Current Limitations

- Analysis is based on a controlled local evidence set.
- Evidence enrichment uses locally derived context rather than external threat-intelligence services.
- Response actions are recommendations and are not automatically executed against production systems.
- Loki and Grafana provide local observability rather than a production-scale SIEM deployment.
- The current case represents a focused SSH brute-force scenario rather than a broad collection of attack types.

### Future Improvements

Potential future development includes:

- Additional detection rules and attack scenarios
- Expanded MITRE ATT&CK coverage
- Additional log sources and telemetry formats
- Automated regression and edge-case testing
- Increased test coverage toward 100%
- Additional evidence-integrity verification
- Expanded dashboard visualizations
- Controlled containment integrations with explicit analyst approval
- Additional SOC playbooks and incident types

The project can therefore continue evolving from a focused incident-response laboratory into a broader security-operations training environment.


---

## Disclaimer

BERSERK-IR is an educational and portfolio-oriented security laboratory.

The project is designed for controlled environments and should not be interpreted as a production-ready incident-response platform or as a substitute for organizational security procedures, forensic processes, or professional security guidance.

All simulated indicators, attack activity, and response decisions are used for defensive training and demonstration purposes.
