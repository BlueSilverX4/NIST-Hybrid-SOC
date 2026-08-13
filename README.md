# 🔵 NIST-Hybrid-SOC  
A unified cybersecurity engineering lab integrating **NIST Framework modules** and the **Hybrid Operations Suite**.  
This repository showcases hands-on SOC pipelines, detection engineering projects, threat hunting exercises, and operational resilience labs built by **BlueSilverX4**.

---

## 📘 Overview  
This repo is designed as a **portfolio-grade SOC engineering showcase**, demonstrating real-world defensive operations across:

- **NIST Detect**
- **NIST Respond**
- **Hybrid SOC Architecture**
- **Threat Hunting**
- **Log Analysis**
- **Incident Simulation**
- **Dashboarding & Telemetry**
- **Automation & Pipeline Engineering**

All modules are built and tested inside a hybrid environment using **Zeek**, **Snort**, **Promtail**, **Loki**, **Grafana**, **Elastic**, and custom BlueBuster tooling.

---

## 📂 Project Index  
A complete index of all NIST-aligned and Hybrid SOC modules included in this repository.

---

### 🔹 NIST Framework — Detect

- **Automated Forensic Extraction**  
  Zeek logs, packet captures, forensic case study, investigation summary, and triage screenshots.

- **Operation PhishShield**  
  Email ingestion pipeline, Alloy config validation, SIEM ingestion proof, phishing telemetry.

- **Project RAIL-BEAST**  
  TrainNet chaos simulation, Snort detection, Loki ingestion, Prometheus metrics, honeypot telemetry.

- **Violatile Mirage**  
  Web shell hunting, auditd triggers, persistence deployment, triage analysis report.

- **Snort3 IDS Automated Detection**  
  Snort3 rules, Lua configs, alert pipelines, dashboard screenshots, and detection documentation.

- **Log Armor**  
  Authentication failure exposure, defensive hardening, and SIEM visualization.

- **Hunting Web Shells**  
  SQLi exploit vector analysis, network traffic triage, kernel-level web shell indicators.

---

### 🔹 NIST Framework — Respond

- **Discord Bot SOC Automation**  
  Automated alerting and SOC workflow orchestration.

- **Sec-Agent**  
  Lightweight host telemetry agent for hybrid SOC pipelines.

- **SOC-AI Project**  
  AI-assisted triage and automated detection logic.

---

### 🔹 Hybrid Operations Suite

- **Hardware Guardian Mini-SOC**  
  Modular SOC dashboard, Filebeat configs, sanitized logs, operational resilience documentation.

- **Operation Ironclad**  
  Attacker POV evidence, Zeek logs, Promtail configs, time-series spike analysis, SIEM ingestion proof.

- **Project PET Defender**  
  Wazuh deployment, Zeek anomaly detection, DNS spike analysis, environment setup notes.

---

### 🔹 Evidence, Logs & Telemetry

- **Zeek Logs** — conn, dns, http, kerberos, ssl, weird, x509  
- **Snort Alerts** — fast alerts, custom rules, Lua configs  
- **Prometheus Metrics** — container CPU, cAdvisor, Snort pipeline flush  
- **Grafana Dashboards** — SIEM ingestion, anomaly detection, metrics visualization  
- **Honeypot Telemetry** — Cowrie SSH brute force, internal recon, battle lines  
- **Packet Captures** — forensic PCAPs, DVWA exploit traffic, TrainNet chaos simulation

---

### 🔹 Documentation & Reports

- **Operational Resilience Reports**  
- **Forensic Case Studies**  
- **Triage Analysis Reports**  
- **Environment Setup Notes**  
- **Detection Engineering Documentation**  
- **Dashboard Exports & Configs**

---

## 🚀 BlueBuster Sync & Release Pipeline  
This repository is maintained using the **BlueBuster Sync Pipeline**, which:

- Selectively syncs NIST + Hybrid Suite modules  
- Auto-removes nested git repos  
- Auto-tags releases (`v1.0.x`)  
- Auto-generates release notes  
- Packages artifacts into downloadable `.zip` bundles  
- Uploads releases directly to GitHub

This ensures every update is clean, versioned, and portfolio-ready.

---

## 📊 Dashboards & Telemetry  
Many modules include:

- Grafana dashboards  
- Prometheus metrics  
- Loki log streams  
- Snort alerts  
- Zeek connection logs  
- DNS anomaly charts  
- Honeypot telemetry  
- Operational resilience visualizations

These demonstrate real-world SOC observability and detection engineering.

---

## 🛠 Technologies Used

- **Zeek**
- **Snort3**
- **Promtail / Loki**
- **Grafana**
- **Elastic Stack**
- **Wazuh**
- **Prometheus**
- **Cowrie Honeypot**
- **Custom BlueBuster scripts**

---

## 📦 Releases  
All releases are automatically generated using the BlueBuster Release Builder:

- Auto-versioned (`v1.0.x`)
- Includes zipped artifacts
- Includes commit-based release notes

Download the latest release from the **Releases** tab.

---

## 👤 Author  
**Brandon Gregg (BlueSilverX4)**  
Cybersecurity Engineer • SOC Pipeline Architect • Detection Engineer  
Bronx, NY

---

## 🔵 BlueBuster Motto  
> *“Defensive engineering is an art — build boldly.”*
