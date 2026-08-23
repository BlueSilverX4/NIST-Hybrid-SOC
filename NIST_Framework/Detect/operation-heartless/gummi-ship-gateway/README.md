# Module: Gummi Ship Gateway (NDR Telemetry Pipeline)

## Overview
**Gummi Ship Gateway** serves as the Network Detection and Response (NDR) telemetry tier for **Operation Heartless**. It passively monitors network traffic using **Zeek**, converts logs into structured JSON, streams telemetry into **Loki** via **Grafana Alloy**, and evaluates real-time threat detection rules using **Loki Ruler**.

---

## Directory Structure
gummi-ship-gateway/
├── configs/
│   ├── config.alloy              # Grafana Alloy pipeline configuration
│   ├── promtail_gummi_ship.yml   # Backup Promtail ingestion spec
│   └── zeek_local.zeek           # Custom Zeek script forcing JSON output
├── data/                         # Query export snapshots (TXT, JSON, CSV)
├── logs/                         # Active Zeek log outputs & Alloy positions
│   ├── conn.log
│   ├── dns.log
│   └── data-alloy/               # Alloy position tracking files
├── rules/
│   └── network_alerts.yaml       # Loki Ruler detection rules (Port Scan / Recon)
└── screenshots/                  # Verified portfolio proof artifacts
├── 04_alloy_zeek_telemetry_ingestion_running.png
├── 05_grafana_zeek_network_stream_explore.png
└── 06_grafana_network_port_scan_alert_firing.png


---

## Architecture & Data Flow

1. **Traffic Capture (Zeek):**
   * Sniffs network interfaces and produces structured JSON telemetry (`conn.log`, `dns.log`).
   * Configured via `configs/zeek_local.zeek` to enforce JSON formatting and timestamping.

2. **Telemetry Forwarding (Grafana Alloy):**
   * `loki.source.file` scrapes live Zeek JSON logs.
   * `loki.process` extracts fields (`service`, `id.orig_h`, `id.resp_h`, `id.resp_p`) and applies labels (`realm="gummi-ship-gateway"`, `log_type="zeek_conn"`).
   * Streamed directly to Loki on `http://127.0.0.1:3100/loki/api/v1/push`.

3. **Ingestion & Alerting (Loki & Loki Ruler):**
   * **LogQL Exploration:** Log streams are queried in Grafana using `{realm="gummi-ship-gateway"}`.
   * **Rule Evaluation:** `rules/network_alerts.yaml` defines `GummiShipPotentialPortScan`, triggering when connection attempts cross volume thresholds within a 1-minute window.

---

## Detection Engineering

### Rule: `GummiShipPotentialPortScan`
* **File:** `rules/network_alerts.yaml`
* **Target:** `{realm="gummi-ship-gateway", log_type="zeek_conn"}`
* **Logic:** Detects recon probes scanning across multiple TCP/UDP ports.
* **Validation:** Verified via targeted `nmap -Pn -sS -p 4400-4415 <target_ip>` scans.

---

## Portfolio Evidence
* `screenshots/04_alloy_zeek_telemetry_ingestion_running.png`: Grafana Alloy actively scraping and shipping Zeek JSON logs.
* `screenshots/05_grafana_zeek_network_stream_explore.png`: LogQL live stream visualization in Grafana Explore.
* `screenshots/06_grafana_network_port_scan_alert_firing.png`: Loki Ruler firing the port scan alert upon detecting Nmap probe activity.

---
*Developed by Brandon Gregg (BlueSilverX4) for Operation Heartless.*
