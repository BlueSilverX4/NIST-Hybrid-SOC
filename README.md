# 🔵 NIST-Hybrid-SOC  
A unified cybersecurity engineering lab integrating **NIST Framework modules** and the **Hybrid Operations Suite**.  
This repository contains hands-on SOC pipelines, detection engineering projects, threat hunting exercises, and operational resilience labs built by **BlueSilverX4**.

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

## 🧩 Repository Structure

### **NIST_Framework/**
Contains multiple NIST-aligned detection and response projects:

- **Automated Forensic Extraction**  
  Full packet analysis, Zeek logs, case study documentation, and forensic triage.

- **Operation PhishShield**  
  Email ingestion pipeline, Alloy config validation, SIEM dashboards, and phishing telemetry.

- **Project RAIL-BEAST**  
  TrainNet chaos simulation, Snort detection, Loki ingestion, Prometheus metrics, and honeypot telemetry.

- **Violatile Mirage**  
  Web shell hunting, auditd detection triggers, persistence analysis, and triage reports.

- **Snort3 IDS Automated Detection**  
  Snort3 rules, Lua configs, alert pipelines, and dashboard screenshots.

- **Log Armor**  
  Authentication failure exposure and defensive hardening.

…and more.

---

### **Hybrid Operations Suite/**
A modular SOC environment designed for hybrid host + network telemetry:

- **Hardware Guardian Mini-SOC**  
  Modular SOC dashboard, Filebeat configs, sanitized logs, and operational resilience documentation.

- **Operation Ironclad**  
  Attacker POV evidence, Zeek logs, Promtail configs, time-series spike analysis, and SIEM ingestion proof.

- **Project PET Defender**  
  Wazuh deployment, Zeek anomaly detection, DNS spike analysis, and environment setup notes.

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
