# Auto# 🛡️ Automated Threat Detection & Incident Response Lab

A Blue Team portfolio project demonstrating a **closed-loop incident detection and automated containment system**.

The lab uses a Kali Purple environment running **Zeek Network Security Analytics** alongside a custom **Python orchestration engine** to detect network-layer attacks and automatically initiate defensive containment.

---

## 📊 Executive Summary

| Category              | Details                                                                  |
| --------------------- | ------------------------------------------------------------------------ |
| **Objective**         | Detect and automatically contain an active network infrastructure threat |
| **Detection**         | Lightweight signature and behavioral analysis                            |
| **Network Sensor**    | Zeek Network Security Monitor                                            |
| **Automation Engine** | Python 3                                                                 |
| **Enforcement**       | Linux Netfilter / `iptables`                                             |
| **Framework**         | NIST SP 800-61 Rev. 2                                                    |
| **Measured MTTC**     | **Under 2.5 seconds**                                                    |

### Key Achievement

The automated response workflow reduced the measured **mean time to containment (MTTC)** from a manual-response process taking minutes to **under 2.5 seconds** through automated defensive scripting.

---

## 🛠️ Production Stack & Topology

### Defensive Environment

* **Operating System:** Kali Purple
* **Architecture:** WSL environment
* **Network Sensor / NTA:** Zeek Network Security Monitor
* **Response Automation:** Python 3
* **Log Processing:** Automated Zeek log parsing
* **Enforcement Point:** Linux Netfilter (`iptables`)

### Detection & Response Flow

```text
┌───────────────────────────────────┐
│         Attack Source Node       │
└─────────────────┬─────────────────┘
                  │
                  │ 1. Network Attack
                  ▼
┌────────────────────────────────────────────┐
│             Kali Purple Target             │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │ 2. Zeek Network Sensor              │  │
│  │    Inspects packets → conn.log       │  │
│  └──────────────────┬───────────────────┘  │
│                     │                      │
│                     ▼                      │
│  ┌──────────────────────────────────────┐  │
│  │ 3. Python Response Engine           │  │
│  │    Parses logs → evaluates threshold │  │
│  └──────────────────┬───────────────────┘  │
│                     │                      │
│                     ▼                      │
│  ┌──────────────────────────────────────┐  │
│  │ 4. Linux Netfilter                  │  │
│  │    iptables → DROP rule             │  │
│  └──────────────────────────────────────┘  │
│                                            │
└────────────────────────────────────────────┘
```

---

## 🔄 Closed-Loop Response

The core workflow follows four stages:

```text
Network Attack
      │
      ▼
Zeek Detection
      │
      ▼
Python Analysis
      │
      ▼
Threshold Breach
      │
      ▼
Automated Containment
      │
      ▼
iptables DROP
```

This creates a closed defensive loop in which network telemetry is converted into an automated containment action without requiring manual intervention.
