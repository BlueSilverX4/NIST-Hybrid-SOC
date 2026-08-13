# Incident Post-Mortem Report
**Incident ID:** IR-2026-0516A  
**Date:** May 16, 2026  
**Lead Analyst:** Brandon Lawrence Gregg  
**Status:** CLOSED / MITIGATED  

---

## 1. Incident Summary
* **Threat Classification:** Infrastructure Reconnaissance / Authentication Flooding
* **Target System:** Physical Kali Purple Endpoint Node (WSL Subsystem Architecture)
* **Source IP:** [Insert Attacker IP here, e.g., 192.168.1.X or Localhost Loopback]
* **Impact Rating:** Low (Threat successfully isolated during reconnaissance phase)

---

## 2. Timeline of Events (NIST Lifecycle)

| Timestamp (EST) | Phase | Description |
| :--- | :--- | :--- |
| **00:00:01** | **Detection** | Zeek engine logs an abrupt spike in connection attempts via `conn.log`. |
| **00:00:02** | **Analysis** | Python automation script detects the threshold breach (>5 anomalous events within a 3-second window). |
| **00:00:02.5**| **Containment** | Script automatically triggers system command to drop all future packets from Source IP. |
| **00:00:03** | **Eradication** | Active network connections from malicious host dropped by `iptables` at the kernel boundary. |
| **00:00:10** | **Recovery** | Analyst verified system integrity, network throughput normal, and sensor functionality green. |

---

## 3. Investigative Findings & Technical Evidence
Analysis of the Zeek connection tables indicated structural pattern metrics consistent with automated scanning or protocol flooding. 

### Core Log Evidence (Zeek Extract):
```text
# Fields: ts uid id.orig_h id.orig_p id.resp_h id.resp_p proto service duration
1715850001.12  Cxyz123  [Attacker_IP]  54321  [Target_IP]  22  tcp  -  0.002
1715850001.15  Cxyz124  [Attacker_IP]  54322  [Target_IP]  22  tcp  -  0.001
