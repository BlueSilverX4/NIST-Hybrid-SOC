# Project RAIL-BEAST // Dual-Pipeline Blue Team Monitoring Console

An operational defensive security architecture utilizing **Grafana Alloy**, **Loki**, and **Prometheus** to ingest, parse, and visualize high-fidelity Network IDS telemetry alongside infrastructure performance metrics.

---

## 📐 Architecture Overview

* **Telemetry Ingestion:** Grafana Alloy dynamically tracks local Snort NIDS logging pipelines (`alert_fast.txt`).
* **Log Aggregation:** High-volume text logs are structured, indexed, and pushed to a centralized Loki data cluster.
* **Infrastructure Telemetry:** cAdvisor monitors bare-metal Docker container sockets, passing numeric performance parameters straight to Prometheus.
* **Visualization Layer:** A unified Grafana operations dashboard pairs live intrusion events alongside real-time hardware tracking.

---

## 📁 Repository Structure

```text
Project RAIL-BEAST/
├── docker-compose.yml           # Multi-container service orchestrator
├── alloy-host-config.alloy      # Log ingestion routing rules
├── prometheus.yml               # Telemetry scraper configuration
├── snort_logs/                  # Host directory for active NIDS logs
│   └── alert_fast.txt           # Live Snort telemetry targeted by Alloy
├── snort_rules/                 # Active network intrusion signatures
│   └── local.rules              # Customized detection parameters
├── screenshots/                 # Operational verification logs
└── backup_pre_hybrid/           # Legacy baseline configurations
