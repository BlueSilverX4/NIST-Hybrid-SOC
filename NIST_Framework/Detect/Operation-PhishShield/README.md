# Operation PhishShield: Automated End-to-End Phishing Telemetry & SIEM Pipeline

## 📌 Executive Summary
Operation PhishShield is an engineered, hardware-based defensive security project demonstrating an end-to-end telemetry pipeline for detecting and analyzing phishing threats. The architecture simulates a targeted credential-harvesting phishing attack, tracks local directory modifications via automated security agents, ships data over a credential-secured HTTPS connection into a local SIEM cluster, and visualizes live threat metrics on a centralized SOC analyst dashboard.

This repository is strictly organized to map engineering controls directly to the **NIST Cybersecurity Framework (CSF 2.0)**.

---

## 🛠️ Technology Stack & Architecture
* **OS Platform:** Kali Purple (Defensive Architecture Deployment)
* **Telemetry Agent:** Grafana Alloy (OpenTelemetry-compliant file monitoring pipeline)
* **SIEM Core:** Elasticsearch (Data modeling and secure document indexing over HTTPS)
* **Visualization Layer:** Grafana Server (SOC interface and dynamic indicator tracking)
* **Forensic Tooling:** CyberChef (Manual email header validation and IoC extraction)

---

## 🏛️ NIST Cybersecurity Framework Mapping

### 🔍 1. Detect (ID.DE) — Directory Telemetry & Ingestion
* **Implementation:** Configured `config.alloy` to monitor system endpoints for `.eml` threat artifacts. The agent automatically parses local paths and streams records to an enterprise SIEM cluster via an OpenTelemetry HTTP exporter (`otelcol.exporter.otlphttp`).
* **Artifact Location:** `[nist_detect/config.alloy]`

### 🚨 2. Respond (RS.AN) — Incident Triage & Data Extraction
* **Manual Analysis:** Leveraged CyberChef to manually extract external sender infrastructure, embedded phishing URLs, and targeted user domains from `simulation_test.eml`.
* **SIEM Automation:** Provisioned a strict Elastic Common Schema (ECS) definition over HTTPS (`soc-phishshield-logs`). Extracted structured triage telemetry via automated reporting features.
* **Artifact Location:** `[nist_respond/phishing_alert_telemetry.csv]`

---

## 🚀 Step-by-Step Implementation Summary

### Phase 1: Malware/Phishing Artifact Staging
1. Staged a baseline target email vector containing specific simulation flags (`email.authorized_test: true`) inside the scoped target path.

### Phase 2: Pipeline Engineering
1. Developed the Grafana Alloy tracking configuration utilizing standard block targeting components.
2. Validated syntax health using localized validation syntax (`alloy fmt`).

### Phase 3: SIEM Hardening & Verification
1. Deployed an API payload over HTTPS utilizing explicit schema layouts.
2. Successfully ran automated search validation routines to confirm schema readiness (`hits.total.value: 1`).

### Phase 4: Visualization & Metrics Tracking
1. Attached Grafana over TLS to the verified local engine using the `elasticsearch-1` connector block.
2. Created an enterprise-grade metric counter tracking high-severity alert indicator variables (`${__field.name}`).

---

## 📊 Operational Metrics & Visual Evidence
All technical milestones have been fully captured and validated through live visual checks. Evidence snapshots confirming successful pipeline integration, schema validation, and database operations are organized within the `[documentation/]` directory.
