# 🛰️ Snort 3 IDS Flow Visualizer

## Real-Time Network Traffic Analysis & Threat Intelligence Integration

## 📌 Project Overview

The **Snort 3 IDS Flow Visualizer** transforms raw Snort 3 intrusion-detection telemetry into a high-visibility network security dashboard.

Using **Filebeat, Elasticsearch, and Grafana**, the project creates a visualization pipeline that allows security analysts to identify high-volume network sources, understand traffic relationships between systems, and quickly investigate suspicious IP addresses through integrated threat-intelligence lookups.

The project demonstrates how raw IDS telemetry can be transformed into actionable network visibility for security operations.

---

# 🏗️ Architecture

```text
┌──────────────────────┐
│      Network         │
│      Traffic         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Snort 3        │
│   IDS / Detection    │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      Filebeat        │
│  Log Collection      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│    Elasticsearch     │
│  Security Telemetry  │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       Grafana        │
│ Flow Visualization   │
└──────────┬───────────┘
           │
           ▼
     Analyst Investigation
           │
           ▼
      VirusTotal Lookup
```

---

# 🛠️ Technology Stack

| Component          | Purpose                                          |
| ------------------ | ------------------------------------------------ |
| **Snort 3**        | Network Intrusion Detection System               |
| **Kali Purple**    | Security monitoring environment                  |
| **Filebeat**       | IDS log collection and forwarding                |
| **Elasticsearch**  | Security telemetry storage and search            |
| **Grafana**        | Visualization and analyst interface              |
| **Sankey Panel**   | Network traffic-flow visualization               |
| **VirusTotal API** | IP reputation and threat-intelligence enrichment |

---

# 🚀 Key Features

## 🔀 Sankey Traffic Flow

The Grafana dashboard visualizes traffic relationships between:

```text
Origin / Source IP
        │
        ▼
   Network Flow
        │
        ▼
Target / Asset IP
```

This provides analysts with a visual method for identifying:

* High-volume network sources
* Potential scanning activity
* Unusual source-to-target relationships
* Possible lateral movement patterns

---

## 📊 Advanced Data Transformations

Grafana transformations were used to combine disparate query results into a unified traffic view.

The transformation workflow includes:

```text
Source / Destination Data
          │
          ▼
     Join by Field
          │
          ▼
Add Field From Calculation
          │
          ▼
    Organize Fields
          │
          ▼
 Unified Traffic Metric
```

This approach allowed separate source and destination datasets to be combined into a visualization suitable for Sankey-based traffic analysis.

---

## 🔎 Click-to-Investigate

The dashboard includes custom **Grafana Data Links** that allow analysts to select an IP address directly from the visualization and initiate a reputation lookup through **VirusTotal**.

This creates a rapid investigation workflow:

```text
Suspicious IP
     │
     ▼
Grafana Dashboard
     │
     ▼
Analyst Clicks IP
     │
     ▼
VirusTotal Reputation Lookup
     │
     ▼
Threat Intelligence Context
```

---

## 🚦 Threshold-Based Visualization

Traffic-volume thresholds are used to help analysts quickly distinguish normal traffic from potentially suspicious high-volume activity.

The visualization uses threshold-driven node states to reduce analyst **log fatigue** and prioritize traffic relationships requiring additional investigation.

---

# 🔍 Identify Function

This project supports the **Identify** function of security operations by providing visibility into network assets and communication relationships.

Analysts can use the dashboard to answer questions such as:

* Which systems are communicating?
* Which source IPs generate the most traffic?
* Which assets receive unusually high volumes of traffic?
* What source-to-destination relationships exist?
* Which IP addresses warrant threat-intelligence investigation?

This establishes network context before deeper detection or incident-response activities begin.

---

# 🧠 Engineering Challenges

## Schema Auditing

Elasticsearch index mappings were audited to resolve **Field Not Found** errors.

The investigation involved identifying the correct JSON paths containing source and destination IP metadata so that Grafana queries could retrieve the expected network fields.

---

## Logic Merging

Grafana's individual query frames did not initially provide the unified dataset required by the visualization.

The problem was addressed through a transformation sequence:

```text
Query Results
     │
     ▼
Join by Field
     │
     ▼
Add Field From Calculation
     │
     ▼
Organize Fields
     │
     ▼
Unified Visualization Dataset
```

This allowed separate source and destination metrics to be combined into a single traffic-flow representation.

---

# 📂 Repository Contents

```text
/
├── dashboards/
│   └── snort-flow-visualizer.json
│
├── screenshots/
│   ├── dashboard/
│   └── threat-intelligence/
│
├── configs/
│   ├── filebeat.yml
│   └── snort/
│
└── README.md
```

### Dashboards

The exported Grafana dashboard is located at:

```text
dashboards/snort-flow-visualizer.json
```

The export can be imported into a compatible Grafana environment to reproduce the visualization.

### Screenshots

The screenshots directory contains visual validation of:

* The live traffic-flow dashboard
* Network relationships
* Threat-intelligence links

### Configurations

The `configs/` directory contains example configuration material for:

* Filebeat
* Snort 3

---

# 🔄 Analyst Workflow

```text
Network Traffic
      │
      ▼
    Snort 3
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
Traffic Analysis
      │
      ├───────────────┐
      ▼               ▼
High-Volume Flow   Suspicious IP
      │               │
      ▼               ▼
Network Context   VirusTotal
                      │
                      ▼
              Threat Intelligence
```

---

# 🛡️ Security Operations Value

This project demonstrates practical experience with:

* Network Security Monitoring
* IDS telemetry
* Elasticsearch
* Filebeat
* Grafana
* Network traffic visualization
* Grafana transformations
* Schema auditing
* Threat-intelligence enrichment
* IP reputation investigation
* Analyst-focused dashboard design

The project bridges the gap between **raw IDS telemetry and analyst-readable network intelligence**.

---

# 📸 Validation Evidence

Project evidence includes:

* Grafana traffic-flow dashboard screenshots
* Source-to-destination visualization
* Threat-intelligence investigation links
* Configuration examples
* Exported Grafana dashboard JSON

---

# 👤 Author

**Brandon Lawrence Gregg**

**Certifications:**

* Cybersecurity Certificate
* SQL Certificate
