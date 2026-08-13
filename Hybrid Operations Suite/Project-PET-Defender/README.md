\# Project-PET-Defender: Decoupled SIEM & Network Detection Lab 🐾🛡️

Project-PET-Defender is a custom-engineered, resource-optimized Security Information and Event Management (SIEM) and Network Security Monitoring (NSM) lab. Built on bare-metal hardware, this project showcases a manually decoupled deployment of the \*\*Wazuh Security Platform\*\* integrated with \*\*Grafana Alloy\*\*, \*\*Loki\*\*, and \*\*Zeek\*\* to establish continuous threat detection and network telemetry pipelines.

\---

\#\# 🏗️ Architecture & Component Flow

Due to local hardware constraints, the environment bypasses automated monolithic installation scripts. Instead, all components are manually provisioned, isolated, and optimized to run efficiently on resource-constrained systems.

\`\`\`text

              ┌──────────────────────────────────────────┐

              │          Bare-Metal Mainframe            │

              │   (Kali Purple / HP Pavilion 23 AIO)     │

              └────────────────────┬─────────────────────┘

                                   │

     ┌─────────────────────────────┼─────────────────────────────┐

     ▼                             ▼                             ▼

\[ Zeek Sensor \]              \[ Grafana Alloy \]            \[ Wazuh SIEM Suite \]

(Network Telemetry)          (Log Ingestion Engine)         (Host Auditing Core)

│                             │                             │

Tails raw network             Parses & labels              \- wazuh-indexer (DB)

traffic and writes            Zeek syslog sources          \- wazuh-manager (Sec)

connection/DNS logs.          ({log\_type="dns/conn"}).     \- wazuh-dashboard (UI)

│                             │                             │

└───────────────►             ▼                             ▼

\[ Grafana Loki (3100) \]     \[ Central Detection Matrix \]

(Structured Storage)          (Alerts & Hardening)

## **🛠️ Deployment Log & Hardware Troubleshooting**

Deploying enterprise-grade SIEM components on custom lab hardware required advanced Linux system administration and service engineering. Below are the key engineering challenges resolved during deployment:

### **1\. Bypassing Hardware Minimum Enforcements**

* **Symptom:** The installer halted with: `ERROR: Your system does not meet the recommended minimum hardware requirements of 4Gb of RAM and 2 CPU cores.`  
* **Root Cause:** Default install scripts enforce enterprise production baselines.  
* **Resolution:** Decoupled the stack and executed a **manual component installation workflow**, tuning the Java Virtual Machine (JVM) options to restrict the database cluster (`wazuh-indexer`) to a strict 1GB heap limit.

### **2\. Mitigating Systemd Initialization Timeouts (CPU/Java Bottleneck)**

* **Symptom:** Services failed to start, throwing generic systemd `result 'timeout'` exceptions after exactly 90 seconds.  
* **Root Cause:** The cryptographic database space generation under Java, as well as the Wazuh Manager's compilation of extensive XML rule definitions on boot, exceeded systemd's default 90-second wall-clock limit.  
* **Resolution:** Designed and deployed native systemd drop-in override configurations to extend the startup threshold allowance, giving the processor adequate room to initialize:

Bash

\# Override for Wazuh Indexer (Extended to 10 minutes)

sudo mkdir \-p /etc/systemd/system/wazuh-indexer.service.d

echo \-e "\[Service\]\\nTimeoutStartSec=600" | sudo tee /etc/systemd/system/wazuh-indexer.service.d/override.conf

\# Override for Wazuh Manager (Extended to 5 minutes)

sudo mkdir \-p /etc/systemd/system/wazuh-manager.service.d

echo \-e "\[Service\]\\nTimeoutStartSec=300" | sudo tee /etc/systemd/system/wazuh-manager.service.d/override.conf

\# Reload and restart services cleanly

sudo systemctl daemon-reload

sudo systemctl restart wazuh-indexer

sudo systemctl restart wazuh-manager

## **🔌 Observability & Network Telemetry Pipeline**

Once the host security matrix was secured, an independent network security monitoring pipeline was established to ingest network events.

### **1\. Zeek Network Telemetry**

Zeek (formerly Bro) passive network sensor sits on the interface, dumping detailed network action logs into `/opt/zeek/logs/current/`.

### **2\. Grafana Alloy Pipeline Ingestion**

Grafana Alloy was deployed to discover, parse, and ship Zeek network events into a local Loki instance (listening on port `3100`).

To resolve initial deployment permission errors blocking the agent, the system permissions were hardened and aligned:

Bash

\# Appended Alloy to the Zeek group and corrected folder traversal permissions

sudo usermod \-aG zeek alloy

sudo chmod 755 /opt/zeek/logs/current/

### **3\. Log Ingestion Configuration (`config.alloy`)**

# 🐾🛡️ Project-PET-Defender

## Decoupled SIEM & Network Detection Lab

## 📖 Project Overview

**Project-PET-Defender** is a custom-engineered, resource-optimized Security Information and Event Management (SIEM) and Network Security Monitoring (NSM) laboratory.

Built on **bare-metal hardware**, the project demonstrates a manually decoupled deployment of the **Wazuh Security Platform** integrated with **Grafana Alloy, Grafana Loki, and Zeek** to establish continuous host-security and network-telemetry pipelines.

The primary engineering challenge was operating enterprise-grade security tooling within a resource-constrained environment.

Rather than relying on a monolithic automated installation, the environment was manually provisioned, isolated, tuned, and validated component by component.

---

# 🏗️ Architecture & Component Flow

```text
┌─────────────────────────────────────────────┐
│             Bare-Metal Mainframe            │
│        Kali Purple / HP Pavilion 23 AIO     │
└──────────────────────┬──────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────────┐
│ Zeek Sensor  │ │ Grafana Alloy│ │ Wazuh SIEM Suite │
│              │ │              │ │                  │
│ Network      │ │ Log Ingestion│ │ Host Security    │
│ Telemetry    │ │ Engine       │ │ & Auditing       │
└──────┬───────┘ └──────┬───────┘ └────────┬─────────┘
       │                │                  │
       │                ▼                  ├─ wazuh-indexer
       │        ┌──────────────┐            ├─ wazuh-manager
       └───────►│ Grafana Loki │            └─ wazuh-dashboard
                │    :3100     │
                └──────┬───────┘
                       │
                       ▼
             ┌─────────────────────┐
             │ Central Detection   │
             │ & Observability     │
             │      Matrix         │
             └─────────────────────┘
```

---

# 🧩 Component Responsibilities

| Component           | Role                                                       |
| ------------------- | ---------------------------------------------------------- |
| **Zeek**            | Passive network security monitoring and protocol telemetry |
| **Grafana Alloy**   | Log discovery, parsing, labeling, and forwarding           |
| **Grafana Loki**    | Centralized network-log storage                            |
| **Wazuh Indexer**   | SIEM data storage and search                               |
| **Wazuh Manager**   | Host-security analysis and alert processing                |
| **Wazuh Dashboard** | Security monitoring interface                              |
| **Grafana**         | Network telemetry visualization and LogQL analysis         |

---

# 🛠️ Deployment Engineering

Deploying the security stack on constrained hardware required manual Linux administration and service-level optimization.

The project focused on three major engineering challenges:

1. Hardware resource limitations
2. Slow Java-based service initialization
3. Network-log ingestion and permissions

---

# 1. 🧠 Bypassing Hardware Minimum Enforcement

### Challenge

The automated installation process halted with:

```text
ERROR: Your system does not meet the recommended minimum hardware requirements of 4Gb of RAM and 2 CPU cores.
```

### Root Cause

The default installation workflow enforced recommended enterprise deployment baselines that were not appropriate for the available laboratory hardware.

### Resolution

Instead of relying on the monolithic installation workflow, the environment was **manually decoupled**.

Individual components were installed and configured independently, allowing resources to be allocated according to the capabilities of the host.

The `wazuh-indexer` JVM heap was constrained to:

```text
1 GB
```

This reduced memory pressure and allowed the database component to operate within the available resources.

---

# 2. ⏱️ Systemd Initialization & Java Bottlenecks

### Challenge

Several services failed during startup with systemd timeout errors after approximately 90 seconds.

### Root Cause

The available CPU resources created extended initialization times for Java-dependent operations, including cryptographic database-space generation and Wazuh Manager startup processing.

### Resolution

Native systemd drop-in overrides were created to extend the permitted startup window.

## Wazuh Indexer

```bash
sudo mkdir -p /etc/systemd/system/wazuh-indexer.service.d

echo -e "[Service]\nTimeoutStartSec=600" | \
sudo tee /etc/systemd/system/wazuh-indexer.service.d/override.conf
```

The startup allowance was extended to **10 minutes**.

## Wazuh Manager

```bash
sudo mkdir -p /etc/systemd/system/wazuh-manager.service.d

echo -e "[Service]\nTimeoutStartSec=300" | \
sudo tee /etc/systemd/system/wazuh-manager.service.d/override.conf
```

The startup allowance was extended to **5 minutes**.

Services were then reloaded and restarted:

```bash
sudo systemctl daemon-reload

sudo systemctl restart wazuh-indexer
sudo systemctl restart wazuh-manager
```

This provided the processor with additional time to complete service initialization.

---

# 🌐 Network Observability Pipeline

After stabilizing the host-security components, an independent network-monitoring pipeline was established.

```text
Zeek
  │
  │ Network Telemetry
  ▼
/opt/zeek/logs/current/
  │
  ▼
Grafana Alloy
  │
  │ Parse + Label + Forward
  ▼
Grafana Loki :3100
  │
  ▼
Grafana
  │
  ▼
Network Security Analysis
```

---

# 1. 🔎 Zeek Network Telemetry

**Zeek** operates as the passive network sensor and continuously produces detailed network-security logs.

The resulting telemetry is written to:

```text
/opt/zeek/logs/current/
```

The pipeline focuses on Zeek logs including:

```text
conn.log
dns.log
```

These provide visibility into network connections and DNS activity.

---

# 2. 📡 Grafana Alloy Ingestion

**Grafana Alloy** was deployed to discover, parse, and forward Zeek telemetry into the local Loki instance.

Initial permission issues prevented the collector from accessing the Zeek log directory.

The issue was resolved by aligning Linux group membership and directory permissions:

```bash
sudo usermod -aG zeek alloy

sudo chmod 755 /opt/zeek/logs/current/
```

This allowed Alloy to access the telemetry while maintaining controlled filesystem permissions.

---

# 3. ⚙️ Alloy Pipeline Configuration

The collector monitors Zeek's active log directory:

```text
/opt/zeek/logs/current/*.log
```

A simplified representation of the ingestion pipeline:

```text
local.file_match
       │
       ▼
loki.source.file
       │
       ▼
Regex Processing
       │
       ▼
Dynamic Labels
       │
       ▼
loki.write
       │
       ▼
Grafana Loki
```

The pipeline dynamically identifies the Zeek log type and assigns a corresponding `log_type` label.

Example labels include:

```text
log_type="dns"
log_type="conn"
```

This allows the resulting telemetry to be queried independently through LogQL.

---

# 📈 Threat Detection Use Cases

The structured Zeek telemetry enables several network-security monitoring use cases.

## 🔎 DNS Activity Monitoring

```text
{log_type="dns"}
```

Used to monitor DNS activity and identify unusual spikes or patterns that may warrant investigation, including potential beaconing or DNS-based data-transfer behavior.

---

## 🔗 TCP Connection Monitoring

```text
{log_type="conn"}
```

Used to analyze successful and failed network connections and investigate patterns associated with:

* System profiling
* Internal port scanning
* Unusual outbound connections
* Abnormal connection volumes

These queries provide analysts with a structured view of network behavior without requiring direct analysis of raw Zeek files.

---

# 🧪 Purple Team Value

Project-PET-Defender demonstrates the relationship between multiple defensive security layers:

```text
┌──────────────────┐
│ Host Telemetry   │
│      Wazuh       │
└────────┬─────────┘
         │
         │
         ▼
┌──────────────────┐
│ Network Telemetry│
│      Zeek        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Log Collection   │
│  Grafana Alloy   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Log Storage      │
│      Loki        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Visualization    │
│     Grafana      │
└──────────────────┘
```

The result is a decoupled security-monitoring architecture capable of providing both **host-level and network-level visibility**.

---

# 🏆 Key Defensive Skills Demonstrated

## Linux Performance & Systemd Engineering

* Diagnosed service startup failures
* Tuned Java resource allocation
* Modified systemd service timeouts
* Stabilized slow-starting services
* Managed resource constraints

## Manual SIEM Administration

* Manually provisioned Wazuh components
* Operated Indexer, Manager, and Dashboard independently
* Avoided reliance on monolithic installation workflows
* Tuned the SIEM for constrained hardware

## Network Security Monitoring

* Deployed Zeek as a passive network sensor
* Collected DNS and connection telemetry
* Built a centralized network-log pipeline
* Created structured LogQL queries for investigation

## Observability Engineering

* Integrated Grafana Alloy with Zeek
* Forwarded telemetry into Loki
* Applied dynamic log-type labeling
* Established centralized network observability

## Linux Security & Permissions

* Managed service accounts and groups
* Corrected filesystem access issues
* Applied controlled directory permissions
* Maintained separation between telemetry collection and system components

---

# 🎯 Project Goals

Project-PET-Defender was built to demonstrate:

* Practical SIEM deployment
* Network Security Monitoring
* Linux administration
* Resource-constrained security engineering
* Security telemetry pipelines
* Host and network visibility
* Service resilience
* Manual infrastructure engineering
* Purple Team defensive validation

---

# 📜 License

This project is intended for educational and cybersecurity portfolio purposes.
