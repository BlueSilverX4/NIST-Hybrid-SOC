# Project Chaosdramon: Automated Incident Response & Scorched-Earth Containment

## Objective
To engineer an automated incident response pipeline that detects a high-severity simulated threat and triggers a programmatic "scorched-earth" containment protocol (isolation, process termination, and forensics snapshot).

## Milestones & Checklist
- [x] Phase 0: Workspace & Documentation Setup (`docs/screenshots/`)
- [X] Phase 1: Host-Based Telemetry & Sensor Configuration
- [X] Phase 2: Threat Simulation Scripting
- [X] Phase 3: Writing the "DigiCore" Response Automation (`chaosdramon_response.py`)
- [X] Phase 4: Local Telemetry & Verification Testing

# Project Chaosdramon: Automated Incident Response & Scorched-Earth Containment

## Executive Summary
**Project Chaosdramon** is an automated host-based incident response and telemetry pipeline designed to safeguard high-value assets (such as hospital Electronic Health Records or banking vaults) from automated brute-force breaches. Named after the heavily armed, autonomous fortress Digimon, the project simulates a "scorched-earth" containment protocol that executes instant network isolation, process termination, and forensic evidence gathering upon detecting threat telemetry thresholds.

---

## NIST Cybersecurity Framework (CSF) Alignment

This project maps directly to key pillars of the NIST Cybersecurity Framework to ensure structured, standards-compliant incident management:

| NIST CSF Function | Category / Control | Project Implementation |
| :--- | :--- | :--- |
| **Protect (PR)** | **Access Control (PR.AC)** & **Protective Technology (PR.PT)** | Hardening high-value vault boundaries and restricting unauthorized entry vectors. |
| **Detect (DE)** | **Anomalous Activity (DE.AE)** & **Continuous Monitoring (DE.CM)** | The host-based log sensor (`log_sensor.py`) continuously monitors authentication streams for suspicious spikes. |
| **Respond (RS)** | **Analysis (RS.AN)**, **Mitigation (RS.MI)**, & **Improvements (RS.IM)** | The automated "DigiCore" engine (`chaosdramon_response.py`) executes instant quarantine and forensic artifact dumping. |

---

## Project Architecture & Workflow
1. **The Sensor (`sensors/log_sensor.py`):** Tails telemetry logs in real-time, tracking failed authentication attempts against a rolling time window.
2. **The Invader (`scripts/simulate_attack.py`):** Generates structured multi-vector attack bursts to test sensor fidelity.
3. **The DigiCore Engine (`scripts/chaosdramon_response.py`):** Automatically invoked upon threshold breach to execute:
   - **Forensic Snapshot:** Dumps volatile states and connection artifacts to `logs/forensic_snapshot.txt`.
   - **Network Quarantine:** Simulates firewall rule deployment (`iptables` isolation) to sever attacker access.
   - **Vault Shielding:** Secures target databases against data exfiltration.

---

## Repository Structure
```text
project-chaosdramon/
├── sensors/
│   └── log_sensor.py          # Real-time authentication log monitor
├── scripts/
│   ├── simulate_attack.py     # Automated threat simulation tool
│   └── chaosdramon_response.py# Automated response & containment engine
├── logs/
│   ├── incident_response.log  # Action audit trail
│   └── forensic_snapshot.txt  # Captured evidence dump
├── docs/
│   └── screenshots/           # Milestone and execution captures
└── README.md                  # Project documentation & NIST alignment
Getting Started & Execution
Initialize the Sensor:

Bash
python3 sensors/log_sensor.py
Launch the Threat Simulation (in a separate terminal):

Bash
python3 scripts/simulate_attack.py
Review the Incident Audit Log:

Bash
cat logs/incident_response.log

--

### Next Steps for Your Portfolio
With your `README.md` updated, your directory structured, and all your execution screenshots saved inside `docs/screenshots/`, this project is fully ready to be initialized as a Git repository and pushed to your GitHub profile (`BlueSilverX4`)!
