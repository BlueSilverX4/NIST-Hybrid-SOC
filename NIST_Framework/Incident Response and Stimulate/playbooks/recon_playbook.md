# Incident Response Playbook: Network Reconnaissance & Port Scanning

## 1. Incident Overview
- **Playbook ID:** IR-PB-101
- **Threat Category:** Reconnaissance / Unauthorized Scanning
- **Objective:** Identify, analyze, and mitigate unauthorized network discovery or high-volume DNS traffic anomalies targeting or originating from the local asset network interface.

---

## 2. Preparation (The Security Stack)
To successfully execute this playbook, the following baseline infrastructure must be active:
- **Network Sensor:** Zeek Network Security Monitor bound to the active physical interface (`wlan0`).
- **Telemetry Storage:** Data spooled directly to `/opt/zeek/spool/zeek/`.
- **Parsing Automation:** Custom Python utility (`dns_analyzer.py`) configured to extract indicators of compromise (IoCs).

---

## 3. Detection & Analysis (The Trigger)
An incident is officially declared if the network telemetry exhibits either of the following indicators:
1. **Volume Spike:** A single source IP initiates more than 15 distinct connection or lookup requests within a 30-second window.
2. **Anomalous Domains:** Frequent queries to external, unverified, or high-risk endpoints.

### Triage Actions:
1. Access the live sensor telemetry.
2. Execute the Python parsing automation tool to isolate the top talking IP addresses.
3. Verify if the traffic is a legitimate administrative action or an active probe.

---

## 4. Containment (Stopping the Threat)
Once a malicious scanning or reconnaissance source is identified, containment actions must be taken immediately to prevent potential follow-up exploitation phases:

- **Manual Containment:** Isolate the offending IP address using the native Linux firewall:
  ```bash
  sudo ufw block from [OFFENDING_IP]
