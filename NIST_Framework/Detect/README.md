# 🛡️ SOC Investigation Workbench

### Modular SOC Telemetry, Investigation & Threat Intelligence Platform

The **SOC Investigation Workbench** is a modular, open-source cybersecurity telemetry and threat intelligence microservice suite deployed on Kali Linux.

The workbench demonstrates an end-to-end SOC investigation workflow by capturing real-time network telemetry with **Zeek**, forwarding structured logs through **Grafana Alloy**, aggregating telemetry in **Grafana Loki**, visualizing network activity through **Grafana dashboards**, and enriching externally routable IP addresses through a custom **Flask / VirusTotal API v3 microservice**.

The project focuses on practical SOC investigation workflows, structured telemetry, analyst-driven visualization, and API-based threat intelligence enrichment.

---

## 🏗️ Architecture Overview

```text
                     ┌─────────────────────────┐
                     │  Local Network / wlan0  │
                     └────────────┬────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    Zeek NSM     │
                         │                 │
                         │ JSON Telemetry  │
                         │ conn.log        │
                         │ dns.log         │
                         │ ssl.log         │
                         └────────┬────────┘
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │    Grafana Alloy    │
                       │                     │
                       │ Log Collection &    │
                       │ Forwarding Engine   │
                       └──────────┬──────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │   Grafana Loki  │
                         │                 │
                         │ Log Aggregation │
                         │ + LogQL         │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     Grafana     │
                         │                 │
                         │ SOC Investigation│
                         │   Dashboards    │
                         └────────┬────────┘
                                  │
                         Data Links / Cell
                           Click-Through
                                  │
                                  ▼
                  ┌─────────────────────────────┐
                  │     threat_intel.py        │
                  │                             │
                  │ Flask REST API Microservice │
                  │                             │
                  │ IP Filtering & Sanitization │
                  └──────────────┬──────────────┘
                                 │
                                 ▼
                       ┌─────────────────────┐
                       │   VirusTotal API v3 │
                       │                     │
                       │ IP Reputation       │
                       │ Threat Intelligence │
                       └─────────────────────┘

🔄 Investigation Workflow
The workbench follows a simple telemetry-to-intelligence workflow:
Network Traffic
      │
      ▼
    Zeek
      │
      │ Structured JSON Logs
      ▼
 Grafana Alloy
      │
      │ Log Forwarding
      ▼
    Loki
      │
      │ LogQL Queries
      ▼
   Grafana
      │
      │ Analyst Investigation
      │
      ▼
 Public Destination IP
      │
      │ Data Link
      ▼
 threat_intel.py
      │
      │ IP Validation
      │ Internal / Multicast Filtering
      ▼
 VirusTotal API v3
      │
      ▼
 Reputation / Threat Intelligence

📁 Repository Structure
.
├── config/
│   └── alloy-config.alloy
│       # Grafana Alloy pipeline configuration
│
├── dashboards/
│   └── *.json
│       # Exported Grafana dashboard templates
│
├── logs/
│   ├── core_investigation_panels_dashboard.json
│   ├── Live DNS Resolution Activity-data-*.csv
│   └── Outbound Network Connections & Protocols-logs-*.txt
│       # Investigation exports and supporting evidence
│
├── screenshots/
│   ├── 01_zeek_listening.png
│   ├── 02_dns_conn_logs.png
│   ├── 03_running_config_alloy.png
│   ├── 04_loki_explore_success.png
│   ├── 05_outbound_network_connections_protocols_dashboard.png
│   ├── 06_live_dns_resolution_activity_dashboard.png
│   ├── 07_non-private_destination_ip_traffic_volume_dashboard.png
│   ├── 08_core_investigation_panels_dashboard.png
│   └── 09_data_link_result.png
│       # Execution and evidence verification screenshots
│
└── scripts/
    ├── enrich_zeek_logs.py
    │   # Batch Zeek log enrichment utility
    │
    ├── threat_intel.py
    │   # Flask REST threat intelligence microservice
    │
    ├── requirements.txt
    │   # Python dependencies
    │
    └── *.log
        # Live Zeek telemetry logs

⚙️ Component Details
1. 🔎 Network Security Monitoring — Zeek
Zeek is configured to monitor the active wireless interface and produce structured JSON telemetry.
Example:
sudo zeek -i wlan0 LogAscii::use_json=T

The resulting telemetry can include network activity such as:
- Connection metadata
- DNS requests
- SSL/TLS connections
- Source and destination addresses
- Source and destination ports
- Network protocols
- Connection states
Example Zeek log sources:
conn.log
dns.log
ssl.log

The JSON output provides structured telemetry that can be consumed by downstream log-processing components.
2. 📡 Telemetry Ingestion — Grafana Alloy
Grafana Alloy acts as the telemetry collection and forwarding layer.
The Alloy pipeline:
Zeek Logs
   │
   ▼
File Collection
   │
   ▼
JSON Parsing
   │
   ▼
Label Assignment
   │
   ▼
Grafana Loki

Zeek telemetry is collected from local log files and forwarded to Loki.
A service="zeek" label is used to identify the telemetry source within the Loki pipeline.
3. 🗄️ Log Aggregation — Grafana Loki
Grafana Loki provides centralized log aggregation and LogQL-based querying.
The workbench uses Loki to make Zeek telemetry available to Grafana investigation panels.
Typical workflow:
Zeek
  │
  ▼
Alloy
  │
  ▼
Loki :3100
  │
  ▼
LogQL
  │
  ▼
Grafana Panels

This allows the analyst to move from raw telemetry into structured investigation views.
4. 📊 SOC Investigation Dashboards
Grafana provides the primary analyst-facing visualization layer.
The project includes dashboards for investigating:
- Outbound network connections
- Network protocols
- DNS resolution activity
- Destination IP traffic
- Core investigation panels
- Public destination IP addresses
The dashboards are designed to provide progressively more useful context:
Raw Telemetry
     │
     ▼
Aggregated Activity
     │
     ▼
Investigation Panel
     │
     ▼
Destination IP
     │
     ▼
Threat Intelligence

5. 🧠 Threat Intelligence Microservice
The threat_intel.py service is a custom Flask microservice that provides IP reputation lookups through the VirusTotal API v3.
The service listens locally:
127.0.0.1:5000

Start the service:
cd scripts
source venv/bin/activate

export VT_API_KEY="YOUR_VIRUSTOTAL_API_KEY"

python3 threat_intel.py

🔐 IP Filtering & Sanitization
Before an address is submitted to VirusTotal, the service validates the IP using Python's standard ipaddress library.
The service filters addresses such as:
- RFC 1918 private IPv4 addresses
- Loopback addresses
- Multicast addresses
- Broadcast addresses
- IPv6 addresses, where excluded by the service's lookup policy
This prevents unnecessary external API requests and avoids attempting to enrich addresses that are not appropriate for public IP reputation lookup.
Example:
Incoming IP
     │
     ▼
Python ipaddress validation
     │
     ├── Private ────────► Skip
     ├── Loopback ───────► Skip
     ├── Multicast ──────► Skip
     ├── IPv6 ───────────► Skip
     │
     └── Public IPv4
              │
              ▼
       VirusTotal API v3

🔗 REST Endpoint Support
The microservice supports both path-based and query-string lookup routes.
Path Parameter
/lookup/ip/<address>

Example:
curl -s http://127.0.0.1:5000/lookup/ip/8.8.8.8

Query Parameter
/lookup/ip?address=<address>

Example:
curl -s "http://127.0.0.1:5000/lookup/ip?address=8.8.8.8"

🔬 Grafana Data Link Investigation
One of the key technical lessons from this project involved the difference between Grafana Logs panels and Grafana Table panels when working with structured Loki telemetry.
Logs Panel Behavior
Grafana Logs panels primarily display Loki entries as a stream of log lines.
When structured JSON is represented as a raw log stream, field-level Data Link interpolation cannot always bind directly to individual JSON properties in the way an analyst might expect.
For example, variables such as:
${__value.raw}

or:
${__data.fields.dest_ip}

may not provide reliable cell-level access when the underlying visualization is simply rendering the complete log line.
Appropriate Use Case
Logs panels are well suited for high-velocity, terminal-style telemetry streams.
For example:
| line_format "{{.src_ip}} queried {{.query}}"

This produces a readable investigation stream such as:
192.168.1.50 queried example.com
192.168.1.50 queried google.com
192.168.1.50 queried api.example.net

📋 Table Panel Behavior
Converting the Loki result into a structured Table panel provides a different investigation model.
Instead of treating the result as a stream of complete log lines, Grafana can expose individual fields as table columns.
Example fields:
id_orig_h
id_resp_h
query
service
proto

This makes individual destination IP values available for field-level interaction.
🔗 Cell-Level Threat Intelligence Data Links
A Field Override can be applied to destination IP columns to create an analyst-driven Data Link.
Example endpoint:
http://127.0.0.1:5000/lookup/ip/${__value.raw}

The resulting workflow becomes:
Grafana Table
     │
     │ Click Destination IP
     ▼
Data Link
     │
     ▼
127.0.0.1:5000
     │
     ▼
threat_intel.py
     │
     ▼
VirusTotal API v3
     │
     ▼
IP Reputation Result

This allows an analyst to move from network telemetry to threat intelligence without manually copying an IP address between applications.
🚀 Verification & Testing
Backend Endpoint Verification
Test the Flask service against a public IPv4 address:
curl -s http://127.0.0.1:5000/lookup/ip/8.8.8.8

A successful response should contain fields similar to:
{
  "as_owner": "Google LLC",
  "country": "US",
  "harmless_count": 55,
  "ip": "8.8.8.8",
  "malicious_count": 0,
  "reputation": 562,
  "suspicious_count": 0
}

VirusTotal reputation and detection counts are dynamic and may change over time. The values above represent an example response structure rather than guaranteed current results.

🔐 Internal IP Pre-Filtering Verification
Test the service with an internal address:
curl -s http://127.0.0.1:5000/lookup/ip/192.168.1.157

Expected behavior:
{
  "ip": "192.168.1.157",
  "reason": "Internal, loopback, or multicast IP addresses are not indexed by VirusTotal.",
  "status": "skipped"
}

The important validation is the:
"status": "skipped"

response, demonstrating that private network addresses are filtered locally rather than unnecessarily submitted for external enrichment.
🧪 Evidence & Verification
The project includes screenshots documenting the major stages of the pipeline.
Evidence	Demonstrates
01_zeek_listening.png	Zeek network monitoring
02_dns_conn_logs.png	DNS and connection telemetry
03_running_config_alloy.png	Grafana Alloy configuration
04_loki_explore_success.png	Successful Loki ingestion
05_outbound_network_connections_protocols_dashboard.png	Outbound connection visualization
06_live_dns_resolution_activity_dashboard.png	DNS activity visualization
07_non-private_destination_ip_traffic_volume_dashboard.png	Public destination IP analysis
08_core_investigation_panels_dashboard.png	Core SOC investigation dashboard
09_data_link_result.png	Grafana-to-threat-intelligence click-through


🧰 Technology Stack
Component	Technology
Operating System	Kali Linux
Network Security Monitoring	Zeek
Telemetry Collection	Grafana Alloy
Log Aggregation	Grafana Loki
Visualization	Grafana
Threat Intelligence	VirusTotal API v3
Microservice	Python / Flask
IP Validation	Python ipaddress
API Testing	curl
Primary Language	Python 3


🎯 SOC Skills Demonstrated
This project demonstrates practical experience with:
- Network security monitoring
- Zeek telemetry collection
- JSON log processing
- Security telemetry pipelines
- Grafana Alloy configuration
- Grafana Loki log aggregation
- LogQL investigation
- Grafana dashboard development
- SOC investigation workflows
- Destination IP analysis
- Threat intelligence enrichment
- REST API development
- Flask microservices
- IP address validation
- API integration
- Grafana Data Links
- Analyst workflow automation
- Evidence collection and verification
🧠 Key Engineering Lessons
1. Structured telemetry improves investigation workflows
Producing JSON telemetry allows downstream systems to work with individual fields instead of relying exclusively on raw text searches.
2. Visualization type affects investigation capability
A Logs panel and a Table panel may expose the same underlying telemetry differently. Table-based visualization can be more appropriate when analysts need field-level interaction.
3. Threat intelligence should be selectively queried
Filtering private, loopback, multicast, and otherwise unsupported addresses before making external API requests reduces unnecessary lookups and preserves API quota.
4. Analyst workflows benefit from contextual enrichment
A Grafana Data Link can bridge the gap between:
Detection
   ↓
Investigation
   ↓
Indicator
   ↓
Threat Intelligence

without requiring the analyst to manually copy indicators between tools.
🔐 Security Considerations
Never commit API credentials to source control.
Use environment variables or another appropriate secret-management mechanism:
export VT_API_KEY="YOUR_VIRUSTOTAL_API_KEY"

Recommended .gitignore entries:
venv/
__pycache__/
*.pyc
*.log
.env

If API credentials have accidentally been committed to a public repository, revoke or rotate them immediately.
🧭 Future Development
Potential extensions to the workbench include:
- Additional Zeek protocol dashboards
- Automated IOC extraction
- Additional threat intelligence providers
- IOC caching
- Rate-limit handling
- Analyst case tracking
- Automated alert generation
- Sigma rule generation
- Wazuh integration
- Additional Loki investigation views
- Structured incident reports
- SOC case management integration
⚠️ Defensive Use Disclaimer
This project is intended for authorized cybersecurity research, education, monitoring, and defensive SOC laboratory environments.
Network monitoring and threat intelligence functionality should only be deployed against systems and networks for which appropriate authorization has been obtained.
📜 License
Add your preferred open-source license here if you intend to distribute this project under an open-source license.
🛡️ Project Summary
                 SOC INVESTIGATION WORKBENCH

 Network Traffic
       │
       ▼
     ZEEK
       │
       ▼
   GRAFANA ALLOY
       │
       ▼
   GRAFANA LOKI
       │
       ▼
     GRAFANA
       │
       ▼
  Analyst Investigation
       │
       ▼
 Destination IP
       │
       ▼
 THREAT_INTEL.PY
       │
       ▼
 VIRUSTOTAL API
       │
       ▼
 Threat Intelligence

Observe → Collect → Aggregate → Investigate → Enrich → Document
