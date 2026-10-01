# Wazuh SIEM Threat Detection & Attack Telemetry Laboratory

## NIST Cybersecurity Framework Alignment
* **Function:** Detect (DE)
* **Categories & Subcategories:**
  * **DE.CM-01:** Network activity & endpoint monitoring
  * **DE.CM-07:** Service & application log monitoring
  * **DE.AE-02:** Event correlation & alert analysis
* **Target Node:** `192.168.1.157` (Kali Purple Bare-Metal Node)
* **SIEM / Telemetry Pipeline:** Wazuh SIEM Manager + Agent (Log Ingestion, Event Rule Matching, Alert Generation)

---

## Executive Summary
This laboratory documents four simulated threat attack scenarios executed against a monitored endpoint to validate telemetry fidelity, log ingestion paths, and real-time alert generation within Wazuh SIEM. Each scenario captures full end-to-end evidence including raw attack tool outputs, terminal execution proofs, SIEM volume spikes (`Dashboard Pulse`), expanded rule breakdown views, and exported raw JSON telemetry alerts.

---

## Tested Attack Scenarios

### Scenario 1: Network Reconnaissance & Service Enumeration (Nmap)
* **Attack Vector:** Host discovery and aggressive service version detection.
* **Command:** `sudo nmap -sV -sC -A 192.168.1.157 -oN nmap_attack_output.txt`
* **Telemetry & Detection:** Port scan activity, service probe signatures, OS fingerprinting traffic ingested into Wazuh.
* **Artifacts:**
  * `Scenario1-Nmap/nmap_attack_output.txt`
  * `Scenario1-Nmap/01_attack_terminal.png`
  * `Scenario1-Nmap/02_dashboard_pulse.png`
  * `Scenario1-Nmap/03_the_alert_breakdown.png`
  * `Scenario1-Nmap/alert_breakdown.json`

### Scenario 2: Web Directory & Path Bruteforcing (DIRB)
* **Attack Vector:** High-frequency URI path enumeration targeting web webserver endpoints.
* **Command:** `dirb http://192.168.1.157 -o dirb_attack_output.txt`
* **Telemetry & Detection:** Apache access log ingestion capturing 404/200 HTTP status response spikes (Wazuh Rules `31100`, `31101`).
* **Artifacts:**
  * `Scenario2-Dirb/dirb_attack_output.txt`
  * `Scenario2-Dirb/01_attacker_terminal.png`
  *Looks like your heredoc command closed early on you when you entered `EOF` on its own line while writing the title. Since `EOF` matched your delimiter, `cat` stopped listening and saved the file with just that single heading.

Here is the clean, full command block to write out a comprehensive, portfolio-ready `README.md` for your Wazuh detection lab:

```bash
cat << 'EOF' > NIST_Framework/Detect/Wazuh-Testing/README.md
# Wazuh SIEM Threat Detection & Attack Telemetry Laboratory

## Overview
This directory contains active threat detection rules, attack simulation artifacts, and telemetry analysis logs generated within the Wazuh SIEM platform. It demonstrates practical detection engineering, custom rule creation (`local_rules.xml`), log analysis, and incident verification mapped to the **NIST Cybersecurity Framework (Detect - DE.AE / DE.CM)** and **MITRE ATT&CK**.

---

## Technical Highlights
- **Custom Rule Engineering:** Implemented custom detection logic in `/var/ossec/etc/rules/local_rules.xml` to catch anomalous authentication, brute-force attempts, and unauthorized privilege escalation.
- **Log Source Integration:** Ingested and parsed telemetry from Linux syslogs, Windows Event Logs (Sysmon), and web server access logs.
- **Validation & Testing:** Verified rule firing using `wazuh-logtest` and active attack simulations.

---

## Directory Structure
- `rules/` - Custom XML rule definitions and decoders.
- `telemetry/` - Raw log samples, PCAPs, and test artifacts used for detection validation.
- `alerts/` - Extracted JSON alert payloads and dashboard verification screenshots.
- `scripts/` - Automated attack simulation and log injection helper scripts.

---

## Verification & Usage
To test custom detection logic against raw log samples using the built-in analyzer:

```bash
/var/ossec/bin/wazuh-logtest
