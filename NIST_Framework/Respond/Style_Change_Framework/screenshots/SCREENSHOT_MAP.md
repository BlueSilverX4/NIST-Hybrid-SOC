# Style Change Framework — Portfolio Screenshot Map

This document indexes the 14 visual verification artifacts in `screenshots/`. Each screenshot is mapped to its corresponding module, verification objective, operational role, and relevant NIST SP 800-61 / SP 800-53 references.

These artifacts provide visual evidence of the framework's architecture, telemetry processing, security automation, and observability pipeline.

## 📸 Master Screenshot Index

| ID | Screenshot | Category / Module | Verification Objective | NIST References |
|:--:|---|---|---|---|
| 01 | `01_folder_structure.png` | Architecture | **Framework Directory Layout:** Documents repository initialization, module directories, and workspace organization through `init_framework.sh`. | SP 800-53: CM-2, CM-8 |
| 02 | `02_guts_nmap_hydra.png` | Playbook / GutsStyle | **Reconnaissance and Containment:** Illustrates Nmap reconnaissance and simulated SSH brute-force telemetry associated with firewall containment workflows. | SP 800-61: Incident handling; SP 800-53: IR-4, SC-7 |
| 03 | `03_hubstyle_telemetry.png` | HubStyle Core | **Central Event Orchestration:** Shows `core_orchestrator.py` processing event payloads and producing normalized JSON artifacts. | SP 800-53: AU-2, IR-5 |
| 04 | `04_element_heat_volatility.png` | Element / Heat | **Memory-Forensics Telemetry:** Demonstrates parsing Volatility 3 output, including process and network artifacts, into structured host telemetry. | SP 800-53: IR-4, SI-4 |
| 05 | `05_element_aqua_web_application_api_security.png` | Element / Aqua | **Web and API Security Ingestion:** Illustrates ingestion of web vulnerability scan findings and API security alerts into normalized security events. | SP 800-53: RA-5, SI-4 |
| 06 | `06_element_elec_network_packet_inspection.png` | Element / Elec | **Network Packet Inspection:** Demonstrates `tshark`-based protocol analysis and network traffic inspection. | SP 800-53: AU-12, SI-4 |
| 07 | `07_element_wood_identity_directory_service.png` | Element / Wood | **Identity and Directory Telemetry:** Documents processing of authentication, Kerberos, LDAP, and account-privilege activity. | SP 800-53: AU-2, IA-2 |
| 08 | `08_shield_openvas_ufw.png` | Playbook / ShieldStyle | **Perimeter Hardening:** Illustrates vulnerability findings feeding a firewall-hardening workflow. | SP 800-53: SC-7, SI-2 |
| 09 | `09_custom_yara_msf.png` | Playbook / CustomStyle | **YARA Signature Validation:** Documents custom YARA rule generation or validation using controlled Metasploit-related test artifacts. | SP 800-53: SI-3, IR-4 |
| 10 | `10_team_bloodhound_impacket.png` | Playbook / TeamStyle | **Lateral-Movement Investigation:** Illustrates correlating BloodHound-derived relationship data with Impacket-related activity. | SP 800-53: IR-4, CA-7 |
| 11 | `11_loki_explore.png` | Observability / Loki | **Log Pipeline Verification:** Shows Grafana Loki Explore querying the `{job="wazuh_alerts"}` stream. | SP 800-53: AU-6, IR-5 |
| 12 | `12_hubstyle_soar_live_ingest_stream_dashboard.png` | Observability / Dashboard | **Panel 1 — Live Ingest Stream:** Displays raw or decoded SOAR events associated with the `style_framework` telemetry pipeline. | SP 800-53: AU-6, IR-5 |
| 13 | `13_hubstyle_high_severity_ingest_spikes_dashboard.png` | Observability / Dashboard | **Panel 2 — High-Severity Spikes:** Visualizes high-severity alert activity over time. | SP 800-53: IR-5, SI-4 |
| 14 | `14_top_targeted_host_ips_dashboard.png` | Observability / Dashboard | **Panel 3 — Target Host Breakdown:** Aggregates target-related IP fields to visualize the distribution of security events across hosts. | SP 800-53: IR-4, SI-4 |

> **Evidence note:** NIST references identify relevant control areas; a screenshot alone does not establish compliance. Descriptions should match the behavior actually demonstrated by each artifact.

---

## Reproduction and Verification

Run commands from the repository root unless otherwise noted. Confirm that each script supports the specified arguments before using them.

### 1. Framework Architecture — Screenshot 01

```bash
./init_framework.sh
```

### 2. Core Telemetry and Playbooks — Screenshots 02–10

```bash
# HubStyle Core
python3 hub_style/core_orchestrator.py --simulate-guts --dry-run

# Heat: Volatility telemetry
python3 elements/heat/heat_volatility.py --dry-run

# Aqua: web and API telemetry
python3 elements/aqua/aqua_telemetry.py --simulate

# Elec: network packet telemetry
python3 elements/elec/elec_tshark.py --dry-run

# Wood: identity and directory telemetry
python3 elements/wood/wood_identity.py --simulate

# ShieldStyle: firewall hardening
python3 playbooks/shield_style/shield_hardening.py --simulate

# CustomStyle: YARA workflow
python3 playbooks/custom_style/custom_yara_engine.py --simulate

# TeamStyle: lateral-movement investigation
python3 playbooks/team_style/team_pivot_tracker.py --simulate
```

These are documented invocation examples, not proof that every script supports those flags. Check `--help` if an argument is rejected. Screenshot 02 may require a separate GutsStyle demonstration.

### 3. Observability Pipeline — Screenshots 11–14

Append a synthetic event to the framework log:

```bash
printf '%s [INFO] [HubStyle Core] ALERT INGESTED | Severity: HIGH | Type: BRUTE_FORCE | Target: 192.168.1.105\n' \
  "$(date '+%Y-%m-%d %H:%M:%S')" \
  | sudo tee -a /var/log/style_framework/events.log
```

Check for a corresponding Wazuh alert:

```bash
sudo grep -F 'style_framework' \
  /var/ossec/logs/alerts/alerts.json \
  | tail -n 5
```

A written log entry confirms the test event was recorded. A matching Wazuh alert confirms alert processing. Loki ingestion and Grafana visualization must be verified separately.

### 4. Evidence Verification Checklist

- [X] All 14 screenshot files exist and match the index.
- [X] Each screenshot shows the relevant command, output, or dashboard.
- [X] Simulations are identified as simulations, not live detections.
- [X] Wazuh ingestion and alert generation are verified independently.
- [X] Loki labels and Grafana queries match the deployed configuration.
- [X] NIST references are mappings, not certifications or compliance claims.

---

## Portfolio Objective

The screenshot collection documents the Style Change Framework as a modular defensive security project covering event normalization, security telemetry, investigation workflows, incident response concepts, and centralized observability.

Together, these artifacts provide reviewers with a visual trail from framework structure and individual telemetry modules through event processing and SOC dashboard verification.
