# 🛡️ Hardware Guardian: Modular Mini-SOC & Threat Detection Lab

## 📖 Executive Summary

**Hardware Guardian** is a resource-optimized Security Operations Center (SOC) lab designed for real-time system auditing, security telemetry collection, and threat detection.

The project demonstrates the deployment and operation of a multi-component Blue Team monitoring environment on **resource-constrained hardware**, while maintaining service stability, centralized visibility, and usable security telemetry.

The lab combines endpoint auditing, network intrusion detection, centralized log collection, search, and visualization into a modular SOC architecture.

---

# 🛠️ Technical Stack & Environment

| Category                | Technology                              |
| ----------------------- | --------------------------------------- |
| **Host Hardware**       | HP Pavilion 23 — Dual-Core CPU, 4GB RAM |
| **Operating System**    | Kali Purple via WSL/Docker              |
| **SIEM & Monitoring**   | Elasticsearch, Filebeat, Grafana        |
| **Intrusion Detection** | Snort                                   |
| **Endpoint Auditing**   | `auditd`                                |
| **Log Collection**      | Filebeat                                |
| **Visualization**       | Grafana Dashboards                      |
| **Version Control**     | GitHub                                  |

---

# 🧩 Project Architecture

```text id="9n2h4s"
┌──────────────────────┐
│    System Events     │
│  Files • Processes   │
│   Network Activity   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   auditd / Snort     │
│ Endpoint + Network   │
│      Telemetry       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Filebeat       │
│   Log Collection     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    Elasticsearch     │
│ Storage + Search     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Grafana        │
│ Visualization + SOC  │
│      Monitoring      │
└──────────────────────┘
```

---

# 🧭 NIST Cybersecurity Framework Alignment

Hardware Guardian supports multiple NIST Cybersecurity Framework functions because the lab spans the broader security-monitoring lifecycle.

## 🔍 Identify

Provides operational visibility into the environment through:

* Asset monitoring
* System-call auditing
* Endpoint telemetry
* Infrastructure monitoring

## 🛡️ Protect

Demonstrates defensive infrastructure practices including:

* Controlled log-shipping architecture
* JVM heap optimization
* Resource allocation
* Service stability tuning
* Operational hardening

## 🚨 Detect

Provides continuous monitoring of:

* Socket activity
* File activity
* Service logs
* System activity
* Network security events

Grafana dashboards provide centralized visibility into the resulting security telemetry.

---

# 🔧 Engineering Challenges & Resolutions

A major objective of Hardware Guardian was demonstrating **operational resilience under hardware and resource constraints**.

---

## 🧠 Memory Bottlenecks

### Challenge

Elasticsearch experienced instability associated with excessive swap activity and limited available RAM.

### Resolution

* Tuned Elasticsearch JVM heap allocation to `1g`
* Implemented automated cache-clearing procedures
* Reduced memory overhead across Docker/WSL services
* Monitored system resource utilization during operation

These changes improved stability within the constrained hardware environment.

---

# 🔁 Service Recovery Failures

### Challenge

Services repeatedly produced:

```text id="b7i5xj"
start request repeated too quickly
```

This occurred during failed service startup and configuration issues.

### Resolution

* Reset `systemd` failure counters
* Corrected Filebeat `auditd` fileset configuration
* Validated service dependencies
* Reviewed service startup order
* Re-tested the monitoring pipeline after configuration changes

---

# ⏱️ Latency Optimization

### Challenge

Grafana generated:

```text id="6n0y1q"
Context Deadline Exceeded
```

during periods of heavy disk swapping and delayed Elasticsearch responses.

### Resolution

* Increased Grafana API timeout to `120s`
* Optimized query execution
* Reduced infrastructure contention
* Stabilized dashboard retrieval under constrained hardware conditions

---

# 🧪 Purple Team Validation

Hardware Guardian was validated through a controlled security-event simulation designed to confirm the end-to-end telemetry pipeline.

## Test Action

A file creation and deletion event was generated:

```bash id="g4w9e0"
sudo touch /etc/audit_success_test
sudo rm /etc/audit_success_test
```

This created observable endpoint activity that could be followed through the monitoring pipeline.

---

## 📡 Detection Workflow

```text id="j8w7a5"
Controlled Security Event
          │
          ▼
        auditd
          │
          ▼
       Filebeat
          │
          ▼
    Elasticsearch
          │
          ▼
       Grafana
          │
          ▼
   Analyst Visibility
```

---

# 📊 Monitoring Results

The validation successfully demonstrated:

* ✅ Real-time event ingestion
* ✅ Filebeat telemetry collection
* ✅ Elasticsearch indexing
* ✅ Grafana visualization
* ✅ End-to-end SOC visibility

The environment captured **more than 8.56K security events** during active monitoring.

This provided measurable evidence that the monitoring stack remained operational while processing security telemetry on constrained hardware.

---

# 📂 Repository Contents

```text id="uy9z1c"
/config
├── filebeat.yml
└── Grafana dashboard JSON models

/data
├── Sample CSV exports
└── Security telemetry datasets

/evidence
├── Service status screenshots
├── Log ingestion proof
└── Dashboard visualizations
```

---

# 📸 Evidence & Validation

Recommended project evidence includes:

* Grafana dashboard overview
* Elasticsearch index health
* Filebeat service status
* Snort alert generation
* Docker container status
* `auditd` log captures
* Active SOC monitoring metrics
* Purple Team validation results

These artifacts provide visual and operational evidence of the monitoring pipeline.

---

# 🎯 Skills Demonstrated

Hardware Guardian demonstrates practical experience with:

* Blue Team Operations
* Purple Team Validation
* SOC Engineering
* SIEM Deployment
* Threat Detection
* Log Analysis
* Incident Monitoring
* Linux Administration
* Elasticsearch Optimization
* Grafana Dashboard Engineering
* Filebeat Configuration
* `auditd`
* Snort
* Resource-Constrained Infrastructure
* Service Recovery
* Security Telemetry Engineering

---

# 🔐 Security Concepts Demonstrated

The project demonstrates:

* Real-time telemetry ingestion
* Endpoint auditing
* Network intrusion detection
* Event correlation
* Security monitoring pipelines
* Log-forwarding architecture
* Infrastructure resilience
* Detection engineering
* Service recovery operations
* Resource-constrained SOC engineering
* Purple Team validation

---

# 📈 Future Improvements

Planned enhancements include:

* [ ] Suricata integration
* [ ] Sigma rule support
* [ ] Automated Discord/Slack alerting
* [ ] Threat-intelligence enrichment
* [ ] Elastic Security detection rules
* [ ] Containerized SOC deployment automation
* [ ] MITRE ATT&CK technique mapping
* [ ] Expanded Purple Team attack simulations

---

# 📌 Project Goals

Hardware Guardian was built to demonstrate:

* Practical SOC deployment skills
* Operational troubleshooting ability
* Security engineering under hardware limitations
* Real-world monitoring and telemetry workflows
* Blue Team analytical thinking
* Purple Team validation methodology
* Infrastructure resilience

---

# 📜 License

This project is intended for educational and cybersecurity portfolio purposes.

---

### 🛡️ System Monitoring in Action

