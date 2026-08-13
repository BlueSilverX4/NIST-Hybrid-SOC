# Project: Operation Crimson Echo 🩸

## 📌 Incident Overview

During a routine host security inspection of a critical Linux deployment, an unauthorized modification was detected within the system's scheduling infrastructure. Further investigation revealed the presence of a malicious cron-based persistence mechanism designed to maintain recurring execution privileges on the compromised host.

This project documents the detection, tracking, and root-cause analysis of a **Linux Cron Backdoor** using native Linux auditing capabilities, file system forensics, and timeline analysis to identify the adversary's persistence technique and determine how the malicious task was deployed.

---

## 🎯 Investigation Objectives

* Identify unauthorized persistence mechanisms
* Locate and analyze malicious scheduled tasks
* Determine execution frequency and privilege level
* Trace the origin of configuration modifications
* Correlate audit telemetry with file system artifacts
* Produce a complete DFIR triage report

---

## 🛠️ Tooling & Environment

| Category             | Tool                                      |
| -------------------- | ----------------------------------------- |
| Operating System     | Kali Purple                               |
| Host Telemetry       | auditd                                    |
| Event Querying       | ausearch                                  |
| File System Analysis | stat                                      |
| Persistence Analysis | cron.d inspection                         |
| Target Environment   | Linux Host Undergoing Persistence Staging |

---

## 🔎 Key Investigative Findings

### 1. Persistence Mechanism Discovery

Analysis of the system scheduling infrastructure revealed a malicious cron job designed to execute with root-level privileges every sixty seconds.

#### Malicious Artifact

```bash
* * * * * root /opt/imperium/update_check.sh
```

#### File Location

```text
/etc/cron.d/system_update
```

#### Assessment

The cron task provided an automated persistence mechanism, ensuring continuous execution of an attacker-controlled script regardless of user activity or service restarts.

---

### 2. Payload Analysis

Further examination of the referenced script identified behavior consistent with reverse shell deployment and command-and-control communications.

#### Observed Behavior

* Executed every 60 seconds
* Ran with root privileges
* Generated outbound network connections
* Maintained attacker access following reboot or logout events

#### External Infrastructure

```text
192.168.111.148:4444
```

#### Impact

The persistence mechanism enabled recurring privileged execution and remote access to the compromised host.

---

### 3. Kernel-Level Audit Tracking (auditd)

Linux Audit Framework telemetry was leveraged to reconstruct the deployment timeline of the malicious persistence artifact.

#### Detection Methodology

Using auditd and ausearch, kernel-level events were queried to identify modifications made to sensitive scheduling directories.

Example workflow:

```bash
ausearch -f /etc/cron.d/system_update
```

#### Evidence Recovered

* Modification timestamp
* Process ID (PID)
* User ID (UID)
* Executable responsible for file creation
* Audit event records associated with deployment

#### Outcome

Audit records provided direct attribution to the process responsible for creating the unauthorized cron configuration file.

---

## 📂 Repository Structure

```text
operation-crimson-echo/
│
├── screenshots/
│   ├── 01_persistence_deployment.png
│   ├── 02_auditd_detection_trigger.png
│   └── 03_stat_binary_triage.png
│
├── triage_analysis_report.txt
└── README.md
```

---

## 📸 Visual Evidence

### 01 — Persistence Deployment

Initial deployment of the malicious cron configuration responsible for recurring task execution.

### 02 — Auditd Detection Trigger

Kernel audit event demonstrating modification activity within monitored scheduling paths.

### 03 — File System Metadata Triage

MACB timestamp analysis using stat to establish artifact creation and modification chronology.

---

## 🧪 Investigation Workflow

### Phase 1 — Artifact Discovery

* Enumerated cron scheduling locations
* Identified unauthorized configuration files
* Validated execution frequency and privilege level

### Phase 2 — Audit Correlation

* Queried auditd event records
* Reconstructed deployment timeline
* Identified responsible process metadata

### Phase 3 — File System Forensics

* Collected MACB timestamps
* Validated creation and modification chronology
* Correlated host telemetry with audit records

### Phase 4 — Persistence Assessment

* Analyzed payload execution behavior
* Confirmed outbound communications
* Determined persistence objective and impact

---

## 📊 Investigation Summary

| Finding                          | Result |
| -------------------------------- | ------ |
| Persistence Mechanism Located    | ✅ Yes  |
| Malicious Cron Job Identified    | ✅ Yes  |
| Audit Trail Recovered            | ✅ Yes  |
| Responsible Process Tracked      | ✅ Yes  |
| Reverse Shell Activity Confirmed | ✅ Yes  |
| Root Cause Established           | ✅ Yes  |

---

## 🚀 Downloads

### Evidence Package

Store investigation artifacts within GitHub Releases and update the links below accordingly.

Included artifacts may contain:

* DFIR Triage Report
* Auditd Event Logs
* Timeline Analysis Notes
* Persistence Samples
* Investigation Screenshots


---

## ⚠️ Disclaimer

This project was conducted within a controlled laboratory environment for educational, defensive security, and incident response training purposes. All artifacts, techniques, and demonstrations are intended solely for authorized security assessments and forensic investigations.

---

## 👨‍💻 Author

DFIR • Linux Forensics • Threat Hunting • Incident Response

**Operation Crimson Echo** demonstrates how Linux auditing, persistence hunting, and file system forensics can be combined to identify, trace, and attribute malicious scheduled-task backdoors within enterprise environments.
