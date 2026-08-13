# 🛡️ Operation: Log Armor

## Host-Based Linux Security Telemetry & Authentication Threat Hunt

### 🎯 Objective

Operation **Log Armor** demonstrates host-based log analysis, event auditing, and detection engineering principles on a **Kali Purple physical host**.

The lab simulates an adversary attempting to:

* Brute-force local authentication
* Access an invalid account context
* Violate `sudo` privilege boundaries

The investigation then identifies the authentication and privilege-related telemetry written to the system's persistent authentication logs.

---

## 🛠️ Toolset & Environment

| Component      | Purpose                                  |
| -------------- | ---------------------------------------- |
| **OS**         | Kali Purple — physical bare-metal system |
| **Log Source** | `/var/log/auth.log`                      |
| **`su`**       | Authentication simulation                |
| **`sudo`**     | Privilege-boundary simulation            |
| **`grep`**     | Log pattern extraction and triage        |
| **`tail`**     | Recent telemetry inspection              |

---

# 📑 Phase 1 — Adversary Simulation

Two security events were generated locally to establish a verifiable detection baseline.

## 1. Authentication Brute-Force Simulation

An attempt was made to spawn a shell under a non-existent account context:

```bash
su sigma_compromise
```

### Expected Detection Objective

Identify the attempted use of an unknown account and locate the resulting authentication failure within `/var/log/auth.log`.

---

## 2. Privilege Escalation Violation

An attempt was made to execute a root-access command using an invalid operator identity:

```bash
sudo -u invalid_operator ls /root
```

### Expected Detection Objective

Identify the invalid operator request while determining which authenticated user actually initiated the command.

---

# 🔎 Phase 2 — Threat Hunting & Log Triage

The investigation focused on extracting the generated authentication events from:

```text
/var/log/auth.log
```

The `grep` utility was used with the `-a` / `--text` option during the investigation to force matching data to be processed as text.

---

## Query 1 — Extracting the Target Identity Loop

```bash
sudo grep -a "sigma_compromise" /var/log/auth.log
```

### Analysis

The system recorded the attempted use of the unknown account, producing an authentication failure event suitable for investigation.

The key detection objective was confirming that the attempted account identifier appeared within the authentication telemetry.

---

## Query 2 — Dissecting the `sudo` Policy Breach

```bash
sudo grep -a "invalid_operator" /var/log/auth.log
```

The investigation produced telemetry containing the following structure:

```text
10:32:51.385543-04:00 DESKTOP-TTT5P7O sudo: brandongregg :
unknown user invalid_operator ;
TTY=pts/0 ;
PWD=/home/brandongregg/Desktop/Log_Armor ;
USER=invalid_operator ;
```

This single event provides several useful investigation fields.

---

# 📊 Key Telemetry Takeaways for SOC Operations

## 1. The Core Five Fields

High-fidelity authentication telemetry can provide multiple pieces of investigative context:

| Field             | Investigation Question                |
| ----------------- | ------------------------------------- |
| **Timestamp**     | When did the event occur?             |
| **Host**          | Where did the event occur?            |
| **Actor Account** | Who initiated the action?             |
| **TTY Session**   | Which terminal/session originated it? |
| **PWD**           | What working directory was active?    |

These fields allow an analyst to move beyond simply identifying that an authentication event occurred and begin reconstructing the activity surrounding it.

---

## 2. True Actor Attribution

The `sudo -u invalid_operator` attempt requested an invalid target identity, but the authentication telemetry still identified the authenticated actor that initiated the request:

```text
brandongregg
```

This demonstrates an important detection principle:

> **Requested identity and authenticated actor are not necessarily the same identity.**

Correlating both values can help analysts distinguish attempted impersonation or unauthorized privilege requests from legitimate administrative activity.

---

## 3. Log Integrity & Centralized Monitoring

Local tools such as `grep` and `tail` provide fast investigation capabilities, but local authentication logs should not be treated as the only source of evidence.

For a production SOC, authentication telemetry should be forwarded to centralized monitoring infrastructure so analysts can investigate events even if an attacker attempts to modify or remove local evidence.

In the DigiPolice-SOC v2 environment, this concept connects directly to the broader logging pipeline:

```text
Linux Authentication Logs
          │
          ▼
        Wazuh
          │
          ▼
    Security Alert
          │
          ▼
    Grafana Alloy
          │
          ▼
         Loki
          │
          ▼
       Grafana
          │
          ▼
   SOC Investigation
```

---

# 🧪 Detection Validation

The Log Armor investigation demonstrates the following detection workflow:

```text
Adversary Simulation
        │
        ▼
Authentication Event
        │
        ▼
/var/log/auth.log
        │
        ▼
Log Triage
        │
        ▼
Identity Correlation
        │
        ▼
Detection Analysis
        │
        ▼
SOC Investigation
```

### Evidence Preserved

* Authentication event output
* `sudo` telemetry
* Terminal command history
* Extracted log entries
* Investigation notes
* Local terminal captures

All analytical evidence, text extractions, and terminal captures are preserved locally within the repository.

---

# 🛡️ SOC Detection Value

Operation Log Armor demonstrates practical skills in:

* Linux authentication monitoring
* Host-based threat hunting
* `sudo` activity analysis
* Privilege escalation detection
* Log triage
* User attribution
* Terminal/session correlation
* Detection engineering
* SOC evidence preservation

The exercise also provides a foundation for turning manually identified authentication patterns into **Wazuh rules, Sigma detections, and centralized Grafana/Loki investigations**.
