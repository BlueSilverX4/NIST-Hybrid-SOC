# 📡 Vigil-Net: NIST-Aligned Observability Hub

## 📋 Overview

**Vigil-Net** is a centralized telemetry and observability platform engineered to provide granular visibility into containerized microservices.

The platform combines container orchestration, metric collection, time-series storage, and visualization to provide real-time insight into:

* System health
* Container resource utilization
* Filesystem usage
* Network performance
* Infrastructure trends
* Operational anomalies

The project demonstrates how a lightweight observability stack can provide centralized visibility across a containerized environment.

---

# 🏗️ Architectural Design

Vigil-Net follows a modular observability architecture built around four primary components:

| Component                | Technology     | Purpose                                                        |
| ------------------------ | -------------- | -------------------------------------------------------------- |
| **Orchestration**        | Docker Compose | Manages service lifecycle and network isolation                |
| **Metric Collection**    | cAdvisor       | Collects container-level CPU, memory, and filesystem telemetry |
| **Time-Series Database** | Prometheus     | Scrapes and persists infrastructure metrics                    |
| **Visualization**        | Grafana        | Provides dashboards, monitoring, and alerting                  |

### Architecture Flow

```text
┌──────────────────────────────┐
│      Containerized Apps      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│           cAdvisor           │
│ CPU • Memory • Filesystem    │
│ Container Telemetry          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          Prometheus          │
│ Metrics Scraping & Storage   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│           Grafana            │
│ Dashboards • Monitoring      │
│ Alerting • Visualization     │
└──────────────────────────────┘
```

Docker Compose manages the overall service lifecycle and provides an isolated `vigil-net` bridge network for communication between the observability components.

---

# 🛡️ NIST Cybersecurity Framework Alignment

Vigil-Net supports multiple functions of the **NIST Cybersecurity Framework (CSF)**.

## Identify (ID)

Provides visibility into the containerized environment by monitoring assets and infrastructure resources.

This supports:

* Asset awareness
* Infrastructure visibility
* Resource inventory
* Operational situational awareness

## Detect (DE)

Provides continuous monitoring of infrastructure metrics, allowing operators to identify:

* Abnormal resource utilization
* Performance degradation
* Container health issues
* Unexpected infrastructure behavior

The observability pipeline therefore provides a foundation for identifying operational anomalies before they develop into larger infrastructure or security problems.

---

# 📁 Project Structure

```text
.
├── docker-compose.yml       # Container orchestration
├── prometheus/              # Prometheus configuration and data
├── grafana-data/            # Persistent Grafana state
├── dashboards/              # Exported Grafana dashboards
│   └── vigil-dashboard.json
└── README.md                # Project documentation
```

---

# 🐳 Container Networking

Docker Compose manages the Vigil-Net service lifecycle and establishes the dedicated:

```text
vigil-net
```

bridge network.

This provides an isolated communication layer for the observability components while allowing Prometheus to collect metrics from the configured targets.

---

# 📊 Observability Workflow

```text
Containerized Services
        │
        ▼
     cAdvisor
        │
        │ Container Metrics
        ▼
    Prometheus
        │
        │ Time-Series Data
        ▼
     Grafana
        │
        ├── System Health
        ├── CPU Utilization
        ├── Memory Usage
        ├── Filesystem Usage
        └── Network Performance
```

This pipeline transforms raw container telemetry into centralized dashboards suitable for operational monitoring and investigation.

---

# 🧪 Engineering Challenges

Development of Vigil-Net included hands-on infrastructure troubleshooting and configuration work involving:

* Docker networking
* Container DNS resolution
* PromQL query development
* Multi-container metric collection
* Persistent Grafana configuration
* Dashboard development
* Infrastructure documentation

These challenges helped reinforce practical Linux, Docker, monitoring, and observability engineering skills.

---

# 📈 Dashboarding

Grafana provides the primary visualization layer for Vigil-Net.

The project includes an exported dashboard model:

```text
dashboards/
└── vigil-dashboard.json
```

The dashboard is designed to provide centralized visibility into container health and resource utilization.

---

# 🔮 Future Roadmap

## Data Retention & Resource Management

The next development phase focuses on implementing explicit **Prometheus data-retention policies** and automated cleanup procedures.

Planned improvements include:

1. Configure Prometheus TSDB retention parameters.
2. Establish appropriate telemetry storage limits.
3. Implement automated cleanup procedures.
4. Monitor storage utilization over time.
5. Document retention decisions for reproducibility.

These improvements will help balance observability depth with the storage constraints of a lightweight infrastructure environment.

---

# 🧠 Skills Demonstrated

Vigil-Net demonstrates practical experience with:

* Docker Compose
* Container Networking
* Linux Infrastructure
* cAdvisor
* Prometheus
* PromQL
* Grafana
* Infrastructure Monitoring
* Observability Engineering
* Metrics Collection
* Dashboard Development
* NIST CSF Alignment
* Technical Documentation

---

# 📌 Project Status

**Active observability and infrastructure monitoring project.**

Current focus:

* ✅ Container orchestration
* ✅ Metrics collection
* ✅ Prometheus integration
* ✅ Grafana visualization
* ✅ Dashboard development
* ✅ NIST CSF alignment
* 🔄 Data-retention optimization
* 🔄 Automated telemetry cleanup
