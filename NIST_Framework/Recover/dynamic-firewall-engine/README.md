# Dynam# 🛡️ Dynamic Threat-Response Firewall Engine

## Automated Incident Containment & Security Recovery Automation

## 📋 Project Overview

The **Dynamic Threat-Response Firewall Engine** is a custom security orchestration tool designed to automate defensive response actions during a security incident.

The system monitors security telemetry in real time, identifies malicious indicators, and dynamically updates Linux firewall rules to contain suspicious activity.

The project demonstrates how automated response tooling can reduce manual intervention time and help restore a controlled security posture after a detected threat.

---

# 🎯 Objectives

The primary goals of this project are:

* Automate security response actions
* Monitor security event streams
* Detect malicious indicators from logs
* Dynamically modify firewall controls
* Reduce manual containment time
* Demonstrate incident lifecycle automation

---

# 🏗️ Architecture

```text id="wz0b6t"
Security Event
      │
      ▼
IDS / Log Source
      │
      ▼
ids_alerts.log
      │
      ▼
Python Response Engine
      │
      ▼
Threat Indicator Detection
      │
      ▼
iptables Firewall Update
      │
      ▼
Threat Containment
      │
      ▼
Recovered Defensive State
```

---

# 🧰 Technology Stack

| Component             | Purpose                             |
| --------------------- | ----------------------------------- |
| **Linux**             | Host security environment           |
| **Python 3**          | Automation and orchestration engine |
| **iptables**          | Dynamic firewall enforcement        |
| **Docker Networking** | Container-aware firewall management |
| **Security Logs**     | Threat detection input source       |

---

# 📂 Project Evidence Log

## Phase 1 — Baseline Configuration

### Description

Established the initial firewall state before automated response actions were enabled.

The baseline captured the existing Linux firewall configuration under Docker-managed networking conditions.

### Status

✅ Completed

### Evidence

```text
docs/evidence/setup/baseline_rules.txt
```

---

# Phase 2 — Detection & Automated Response

## Description

A Python-based monitoring engine was developed to continuously analyze:

```text
logs/ids_alerts.log
```

When the responder detects a:

```text
[CRITICAL] MALICIOUS
```

pattern, it automatically injects a firewall block rule into the Docker-aware firewall chain:

```text
DOCKER-USER
```

---

## Response Workflow

```text id="1z5m4h"
Malicious Indicator Detected
            │
            ▼
Python Log Parser
            │
            ▼
Threat Pattern Matched
            │
            ▼
Source IP Extracted
            │
            ▼
iptables DROP Rule Created
            │
            ▼
Network Access Blocked
```

---

## Validation

The automated response system was validated by successfully blocking:

```text
192.168.1.105
```

The resulting firewall state was verified through inspection of the active `iptables` rules.

### Status

✅ Completed

### Evidence

```text
docs/evidence/results/final_automation_test.png
```

---

# ⚙️ How to Run

## 1. Prepare Log Directory

Ensure the monitoring directory exists:

```bash
mkdir -p logs
```

Verify permissions allow the responder to read the log source.

---

## 2. Start the Responder

```bash
python3 scripts/responder.py
```

---

## 3. Simulate an Alert Event

Append a test malicious event:

```bash
echo "[CRITICAL] MALICIOUS source=192.168.1.105" >> logs/ids_alerts.log
```

The responder should detect the event and create a firewall containment rule.

---

# 🔧 Installation & Requirements

## Prerequisites

* Linux operating system
* Python 3.x
* `iptables` or `nftables` support
* Root/Sudo privileges

Root privileges are required because the responder modifies kernel-level firewall controls.

---

# 🔄 Incident Recovery Workflow

```text id="4q7ywv"
Security Incident
        │
        ▼
Threat Identified
        │
        ▼
Automated Containment
        │
        ▼
Firewall State Updated
        │
        ▼
Threat Isolated
        │
        ▼
Controlled Environment Restored
        │
        ▼
Recovery Documentation
```

---

# 🛡️ NIST CSF Alignment

## Respond (RS)

Supports:

* Automated response actions
* Threat containment
* Security orchestration

## Recover (RC)

Supports:

* Restoration of defensive controls
* Returning systems to a controlled state
* Maintaining operational resilience after security events

---

# 🧠 Skills Demonstrated

This project demonstrates experience with:

* Incident response automation
* Firewall management
* Python security tooling
* Linux administration
* Threat containment
* Security orchestration
* Log-based detection
* Network defense
* Recovery workflow design

---

# 📌 Project Outcome

The Dynamic Threat-Response Firewall Engine successfully demonstrates how security telemetry can trigger automated defensive actions.

By connecting detection input with automated firewall enforcement, the project reduces response latency and provides a foundation for future SOAR-style security automation.
