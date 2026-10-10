# ⚡ Style Change Framework — NIST-Hybrid-SOAR

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python)
![Wazuh](https://img.shields.io/badge/Wazuh-v4.7.5-blue?style=flat&logo=wazuh)
![Grafana](https://img.shields.io/badge/Grafana-Loki%20%2F%20Alloy-orange?style=flat&logo=grafana)
![Architecture](https://img.shields.io/badge/Architecture-SOAR%20%2F%20Incident%20Response-red?style=flat)
![NIST](https://img.shields.io/badge/NIST-SP%20800--61%20%7C%20800--53-green?style=flat)

A modular, event-driven **Security Orchestration, Automation, and Response (SOAR)** framework built for Kali Linux environments.

Inspired by the *Mega Man Battle Network* franchise, the **Style Change Framework** organizes security telemetry, forensic analysis, and defensive response into a modular architecture. Its central orchestration engine coordinates specialized **Elemental Modifiers** for telemetry ingestion and **Style Playbooks** for containment, hardening, and threat investigation.

The project integrates Python-based automation with a defensive observability pipeline built around **Wazuh SIEM, Grafana Alloy, Grafana Loki, and Grafana dashboards**.

The objective is to demonstrate how modular security tools can work together to support incident detection, investigation, response, and operational visibility within a resource-conscious home lab.

---

## 🏛️ 1. System Architecture

The framework separates three primary responsibilities:

- **Central Orchestration:** HubStyle receives and normalizes security events.
- **Domain-Specific Analysis:** Elemental modules process host, web, network, and identity telemetry.
- **Tactical Response:** Style Playbooks implement defensive workflows and response actions.

### Telemetry and Response Pipeline

```text
                  SECURITY TELEMETRY
                          |
                          v
             +--------------------------+
             |     HubStyle Core        |
             |  core_orchestrator.py    |
             |  Event Dispatch &        |
             |  Normalization           |
             +------------+-------------+
                          |
             +------------+-------------+
             |                          |
             v                          v
    +------------------+       +-------------------+
    | Elemental        |       | Style Playbooks   |
    | Modifiers        |       |                   |
    +------------------+       +-------------------+
    | Heat             |       | GutsStyle         |
    | Aqua             |       | ShieldStyle       |
    | Elec             |       | CustomStyle       |
    | Wood             |       | TeamStyle         |
    +--------+---------+       +---------+---------+
             |                           |
             +-------------+-------------+
                           |
                           v
           /var/log/style_framework/events.log
                           |
                 +---------+---------+
                 |                   |
                 v                   v
          +-------------+     +----------------+
          | Grafana     |     | Wazuh Manager  |
          | Alloy       |     | Decoder & Rule |
          |             |     | Engine         |
          +------+------+     +--------+-------+
                 |                     |
                 |              alerts.json
                 |                     |
                 +----------+----------+
                            |
                            v
                     +-------------+
                     | Grafana Loki|
                     +------+------+
                            |
                            v
                     +-------------+
                     | Grafana SOC |
                     | Dashboards  |
                     +-------------+
```

### Central Event Log

The framework's primary event stream is:

```text
/var/log/style_framework/events.log
```

Wazuh processes framework events using custom decoders and rules. Grafana Alloy collects configured log streams and forwards them to Loki, where Grafana dashboards provide operational visibility.

**Pipeline objective:** Normalize security telemetry, generate meaningful SIEM alerts, and make relevant event data available for investigation and response workflows.

---

## 🧠 2. Central Orchestration — HubStyle

**Location:** `hub_style/core_orchestrator.py`

HubStyle is the central Python orchestration engine.

Its responsibilities include:

- Ingesting framework security events.
- Evaluating event severity and incident categories.
- Coordinating Elemental Modifiers and Style Playbooks.
- Writing standardized event records to the central framework log.
- Supporting module simulations and dry-run workflows.

### Central Telemetry Destination

```text
/var/log/style_framework/events.log
```

HubStyle provides the coordination layer between specialized telemetry processors and defensive response modules.

The modular design makes it possible to test individual components without requiring every workflow to execute a live containment action.

---

## 🔥 3. Elemental Modifiers — Domain Ingestion

Elemental Modifiers represent specialized telemetry ingestion and analysis modules.

| Element | Module | Security Domain | Primary Function |
|---|---|---|---|
| **Heat** | `elements/heat/` | Memory forensics | Wraps Volatility 3 workflows and parses memory-analysis output, including process and network information. |
| **Aqua** | `elements/aqua/` | Web and API security | Converts OWASP ZAP API responses and Nikto findings into structured SOAR events. |
| **Elec** | `elements/elec/` | Network inspection | Invokes `tshark` to inspect packets, calculate protocol hierarchies, and flag traffic anomalies. |
| **Wood** | `elements/wood/` | Identity and directory services | Normalizes identity-related telemetry, including Kerberos ticket-granting ticket (TGT) and LDAP events. |

### Heat Element — Memory Forensics

**Script:** `elements/heat/heat_volatility.py`

Processes Volatility 3 output to support memory-forensics workflows, including process-tree and network-connection analysis.

### Aqua Element — Web and API Security

**Script:** `elements/aqua/aqua_telemetry.py`

Transforms web application and API security findings into structured events that can be consumed by the broader framework.

### Elec Element — Network Packet Inspection

**Script:** `elements/elec/elec_tshark.py`

Uses `tshark` to inspect network traffic, summarize protocol activity, and identify traffic patterns requiring further investigation.

### Wood Element — Identity and Directory Services

**Script:** `elements/wood/wood_identity.py`

Processes identity-related events, with an emphasis on Kerberos and LDAP telemetry normalization.

---

## ⚔️ 4. Style Playbooks — Tactical Response

Style Playbooks represent the framework's defensive response layer.

| Playbook | Module | Tactical Objective |
|---|---|---|
| **GutsStyle** | `playbooks/guts_style/` | Rapid containment through process termination and network isolation workflows. |
| **ShieldStyle** | `playbooks/shield_style/` | Host-level firewall hardening using `iptables` and `ufw`. |
| **CustomStyle** | `playbooks/custom_style/` | Generate and validate YARA rules against target files. |
| **TeamStyle** | `playbooks/team_style/` | Track multi-node incidents and represent directional pivot relationships associated with potential lateral movement. |

### GutsStyle — Rapid Containment

**Script:** `playbooks/guts_style/guts_containment.py`

Provides a containment workflow intended to support rapid response to identified threats, including process termination and network isolation.

### ShieldStyle — Firewall Hardening

**Script:** `playbooks/shield_style/shield_hardening.py`

Supports host-level firewall enforcement and dynamic blocking workflows using `iptables` and `ufw`.

### CustomStyle — Threat Signatures

**Script:** `playbooks/custom_style/custom_yara_engine.py`

Provides a YARA rule-generation and validation workflow for file-focused threat investigation.

### TeamStyle — Multi-Node Investigation

**Script:** `playbooks/team_style/team_pivot_tracker.py`

Organizes incident relationships into directional pivot topologies to help investigators examine potential movement between systems.

**Operational distinction:** A playbook defines a response procedure; an incident record captures the event and actions taken. Dry-run output demonstrates workflow execution without necessarily proving that a live host was contained.

---

## 🛡️ 5. Wazuh Decoder and Rule Engine

The framework uses custom Wazuh decoders and rules to interpret standardized HubStyle telemetry and generate higher-severity alerts.

### Custom Decoder

**Configuration:** `/var/ossec/etc/decoders/local_decoder.xml`

The decoder uses `windows-date-format` as its parent and extracts the severity, event type, and target IP from matching HubStyle events.

```xml
<decoder name="style_framework">
  <parent>windows-date-format</parent>
  <use_own_name>true</use_own_name>
  <prematch offset="after_parent" type="pcre2">\[INFO\]\s+\[HubStyle Core\]\s+ALERT INGESTED</prematch>
  <regex offset="after_parent" type="pcre2">Severity:\s*([A-Za-z]+)\s*\|\s*Type:\s*([A-Za-z0-9_-]+)\s*\|\s*Target:\s*((?:[0-9]{1,3}\.){3}[0-9]{1,3})</regex>
  <order>severity,event_type,srcip</order>
</decoder>
```

### Custom Rule Chain

**Configuration:** `/var/ossec/etc/rules/local_rules.xml`

The custom rules provide a two-stage alerting workflow:

1. Rule `100200` identifies telemetry decoded as `style_framework`.
2. Rule `100201` raises the alert level to 10 when the decoded severity is `HIGH` or `CRITICAL`.

```xml
<group name="style_framework,soar_alert,">
  <rule id="100200" level="3">
    <decoded_as>style_framework</decoded_as>
    <description>Style Framework Telemetry Ingested</description>
  </rule>

  <rule id="100201" level="10">
    <if_sid>100200</if_sid>
    <field name="severity">HIGH|CRITICAL</field>
    <description>High/Critical Event Ingested by HubStyle Orchestrator</description>
    <mitre>
      <id>T1110.001</id>
    </mitre>
  </rule>
</group>
```

The resulting Wazuh alerts are written to:

```text
/var/ossec/logs/alerts/alerts.json
```

**Configuration note:** The MITRE ATT&CK mapping above is retained from the original configuration. Validate that the selected technique is appropriate for the event type and recognized by the installed Wazuh version before presenting it as verified coverage.

---

## 📊 6. Grafana SOC Dashboards

Grafana provides a visualization layer for framework telemetry collected in Loki.

The documented dashboard pipeline uses the Loki job label:

```logql
{job="wazuh_alerts"}
```

### Panel 1 — Live Ingest Stream

Displays live and structured SOAR telemetry associated with the Style Change Framework.

```logql
{job="wazuh_alerts"} |= "style_framework"
```

### Panel 2 — Ingest Activity Over Time

Tracks the frequency of framework-related events over the selected interval.

```logql
sum(
  count_over_time(
    {job="wazuh_alerts"} |= "style_framework" [$__interval]
  )
)
```

### Panel 3 — Top Targeted Host IPs

Aggregates events by the extracted `data_srcip` field to show which target addresses appear most frequently in the selected data.

```logql
sum by (data_srcip) (
  count_over_time(
    {job="wazuh_alerts"} |= "style_framework" | json [$__interval]
  )
)
```

**Dashboard objectives:**

- Observe incoming framework events.
- Review event volume over time.
- Identify frequently targeted hosts.
- Verify that telemetry is visible in the downstream observability layer.

These queries depend on the actual labels and JSON fields present in Loki. Confirm the extracted field names against the ingested records when troubleshooting a panel that returns no data.

---

## 📁 7. Repository Structure

```text
Style_Change_Framework/
├── README.md
├── init_framework.sh
│
├── docs/
│   ├── Style_Change_Framework_Dashboard.json
│   ├── hubstyle_soar_live_ingest_stream_dashboard.csv
│   ├── hubstyle_soar_live_ingest_stream_dashboard.txt
│   ├── hubstyle_high-severity_ingest_spikes-dashboard.csv
│   ├── top_targeted_host_ips_dashboard.csv
│   └── Logs-2026-10-08 23_19_35.json
│
├── hub_style/
│   ├── core_orchestrator.py
│   └── telemetry_ingest/
│
├── elements/
│   ├── aqua/
│   │   ├── aqua_telemetry.py
│   │   ├── aqua_telemetry.json
│   │   └── aqua_auto_telemetry.json
│   │
│   ├── elec/
│   │   ├── elec_tshark.py
│   │   ├── elec_telemetry.json
│   │   └── elec_auto_telemetry.json
│   │
│   ├── heat/
│   │   ├── heat_volatility.py
│   │   ├── heat_telemetry.json
│   │   └── heat_auto_telemetry.json
│   │
│   └── wood/
│       ├── wood_identity.py
│       ├── wood_telemetry.json
│       └── wood_auto_telemetry.json
│
├── playbooks/
│   ├── custom_style/
│   │   ├── custom_yara_engine.py
│   │   ├── auto_generated.yar
│   │   └── generated_rule.yar
│   │
│   ├── guts_style/
│   │   └── guts_containment.py
│   │
│   ├── shield_style/
│   │   └── shield_hardening.py
│   │
│   └── team_style/
│       └── team_pivot_tracker.py
│
└── screenshots/
    ├── 01_folder_structure.png
    ├── 02_guts_nmap_hydra.png
    ├── 03_hubstyle_telemetry.png
    ├── 04_element_heat_volatility.png
    ├── 05_element_aqua_web_application_api_security.png
    ├── 06_element_elec_network_packet_inspection.png
    ├── 07_element_wood_identity_directory_service.png
    ├── 08_shield_openvas_ufw.png
    ├── 09_custom_yara_msf.png
    ├── 10_team_bloodhound_impacket.png
    ├── 11_loki_explore.png
    ├── 12_hubstyle_soar_live_ingest_stream_dashboard.png
    ├── 13_hubstyle_high_severity_ingest_spikes_dashboard.png
    ├── 14_top_targeted_host_ips_dashboard.png
    └── SCREENSHOT_MAP.md
```

The layout above reflects the supplied repository inventory. Confirm it against the current checkout before treating it as an exhaustive listing.

---

## 🚀 8. Execution and Quickstart

### Prerequisites

The documented environment includes:

- Python 3.10 or newer
- Wazuh Manager
- Grafana Alloy
- Grafana Loki
- Grafana
- `tshark`
- YARA
- `iptables`
- `ufw`

Install the additional system packages on a compatible Debian-based system:

```bash
sudo apt update
sudo apt install -y tshark yara iptables ufw
```

Wazuh, Loki, Alloy, and Grafana require their own installation and configuration; the package command above does not install the full observability stack.

### Step 1 — Initialize the Framework

From the repository root:

```bash
chmod +x init_framework.sh
./init_framework.sh
```

This runs the framework's environment initialization script.

### Step 2 — Test the Style Playbooks

Run the documented dry-run simulations:

```bash
# GutsStyle — Rapid containment
python3 hub_style/core_orchestrator.py --simulate-guts --dry-run

# ShieldStyle — Firewall hardening
python3 hub_style/core_orchestrator.py --simulate-shield --dry-run

# CustomStyle — YARA rule workflow
python3 hub_style/core_orchestrator.py --simulate-custom --dry-run

# TeamStyle — Multi-node pivot tracking
python3 hub_style/core_orchestrator.py --simulate-team --dry-run
```

These commands are the documented simulation interfaces. Verify that the corresponding flags are supported by the current script version.

### Step 3 — Run Individual Element Modules

Each Elemental Modifier can be invoked independently using its documented interface.

```bash
# Heat — Memory forensics
python3 elements/heat/heat_volatility.py \
  -f sample_memory.raw \
  --dry-run \
  -o elements/heat/heat_telemetry.json

# Aqua — Web and API security
python3 elements/aqua/aqua_telemetry.py \
  --simulate \
  -o elements/aqua/aqua_telemetry.json

# Elec — Network packet inspection
python3 elements/elec/elec_tshark.py \
  --dry-run \
  -o elements/elec/elec_telemetry.json

# Wood — Identity and directory services
python3 elements/wood/wood_identity.py \
  --simulate \
  -o elements/wood/wood_telemetry.json
```

The Heat command requires an appropriate memory image at the specified path. The Elec module also depends on the input and options supported by its implementation.

### Step 4 — Generate a Test Security Event

Append a formatted sample event to the framework log:

```bash
echo "$(date +'%Y-%m-%d %H:%M:%S') [INFO] [HubStyle Core] ALERT INGESTED | Severity: HIGH | Type: BRUTE_FORCE | Target: 192.168.1.105" \
  | sudo tee -a /var/log/style_framework/events.log
```

This injects a test record into the local log file. It does not, by itself, prove that the entire pipeline is operational.

Verify each stage independently:

1. Confirm that the event appears in `events.log`.
2. Confirm that Wazuh decodes the event.
3. Confirm that the expected custom rule fires.
4. Confirm that the resulting record appears in `alerts.json`.
5. Confirm that Alloy forwards the configured log stream to Loki.
6. Confirm that the event appears in Grafana Explore and the dashboard panels.

This stage-by-stage approach makes it easier to identify whether a failure originates in event formatting, decoding, rule matching, log collection, or visualization.

---

## 📸 9. Portfolio Screenshots and Verification

The screenshot collection documents the framework's structure, module demonstrations, SIEM integration, and Grafana dashboards.

| Screenshot | Evidence |
|---|---|
| `01_folder_structure.png` | Repository layout and framework organization |
| `02_guts_nmap_hydra.png` | GutsStyle and security-tool workflow evidence |
| `03_hubstyle_telemetry.png` | HubStyle telemetry processing |
| `04_element_heat_volatility.png` | Heat memory-forensics module |
| `05_element_aqua_web_application_api_security.png` | Aqua web/API security module |
| `06_element_elec_network_packet_inspection.png` | Elec packet-inspection module |
| `07_element_wood_identity_directory_service.png` | Wood identity and directory-services module |
| `08_shield_openvas_ufw.png` | ShieldStyle and firewall-related evidence |
| `09_custom_yara_msf.png` | CustomStyle YARA workflow |
| `10_team_bloodhound_impacket.png` | TeamStyle and multi-node investigation tools |
| `11_loki_explore.png` | Loki log-ingestion and exploration evidence |
| `12_hubstyle_soar_live_ingest_stream_dashboard.png` | Live ingest stream dashboard |
| `13_hubstyle_high_severity_ingest_spikes_dashboard.png` | Event-frequency dashboard |
| `14_top_targeted_host_ips_dashboard.png` | Targeted-host aggregation dashboard |

For the complete mapping of screenshot artifacts to commands, modules, and verification objectives, see:

[`screenshots/SCREENSHOT_MAP.md`](screenshots/SCREENSHOT_MAP.md)

The screenshots are intended to provide supporting evidence for the implementation. Where a screenshot demonstrates a simulation or dry run, it should be described as such rather than as proof of successful live containment.

---

## 🏛️ 10. NIST Alignment

The framework is organized around incident-handling activities and security controls associated with the following references.

### NIST SP 800-61 Rev. 2 — Computer Security Incident Handling Guide

The project's stated alignment covers:

- **Detection and Analysis:** Heat, Aqua, and Elec telemetry-processing workflows.
- **Containment, Eradication, and Recovery:** GutsStyle and ShieldStyle response workflows.
- **Post-Incident Activity:** CustomStyle and TeamStyle investigation and analysis workflows.

These are project-level mappings to incident-handling activities, not a claim of formal compliance or certification.

### NIST SP 800-53 Rev. 5 — Security and Privacy Controls

| Control | Project Mapping |
|---|---|
| **IR-4 — Incident Handling** | Coordinated response and containment playbooks |
| **IR-5 — Incident Monitoring** | Incident-event processing and monitoring |
| **SI-4 — System Monitoring** | Endpoint, network, and security telemetry ingestion |
| **SC-7 — Boundary Protection** | Host firewall hardening and network containment workflows |

The mappings describe the intended relationship between project capabilities and the cited control objectives. Actual implementation coverage should be verified against the relevant control requirements.

---

## 🛡️ 11. Security and Ethical Use

This repository is intended for educational cybersecurity research, defensive lab development, and incident-response demonstrations.

- Run security tools only against systems you own or are explicitly authorized to test.
- Review containment actions before enabling live execution.
- Use dry-run modes when validating orchestration logic.
- Confirm firewall changes and isolation actions before applying them to a production or remote host.
- Preserve relevant telemetry and document the results of each test.
- Validate generated YARA rules before relying on them for detection.

Automated response should remain bounded by authorization, validation, and the operational requirements of the environment.

---

## 🏁 12. Project Takeaway

The **Style Change Framework** brings together modular telemetry ingestion, Python orchestration, SIEM alerting, and Grafana-based observability in a single NIST-informed defensive lab.

Its central design principle is to separate specialized analysis from tactical response while keeping both connected through a standardized event pipeline.

The project demonstrates practical exploration of:

- Modular SOAR architecture
- Security-event normalization
- Wazuh custom decoders and rules
- Network and memory-forensics workflows
- Web/API security telemetry
- Identity-event processing
- Firewall hardening and containment workflows
- YARA rule generation and validation
- Loki-based telemetry exploration
- Grafana SOC dashboards
- Evidence-oriented project documentation

**From telemetry to investigation, and from investigation to controlled response — the framework turns individual security modules into a coordinated defensive workflow.**
