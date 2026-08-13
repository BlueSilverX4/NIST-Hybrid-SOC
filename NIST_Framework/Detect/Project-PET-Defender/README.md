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

The collector monitors the network logs and dynamically structures them into custom indexed labels:

Code snippet

// Grafana Alloy pipeline configuration snippet

local.file\_match "zeek\_logs" {

  path\_targets \= \[{"\_\_path\_\_" \= "/opt/zeek/logs/current/\*.log"}\]

}

loki.source.file "zeek\_ingest" {

  targets    \= local.file\_match "zeek\_logs".targets

  forward\_to \= \[loki.write.local\_loki.receiver\]

}

// Applies regex stages to dynamically extract 'dns' or 'conn' into log\_type labels

stage.regex {

  expression \= "/opt/zeek/logs/current/(?P\<log\_type\>\\\\w+)\\\\.log"

}

stage.labels {

  values \= {

    log\_type \= "log\_type",

  }

}

## **📈 Threat Detection Use Cases**

Using structured LogQL dashboards, the pipeline actively parses and visualizes network activity:

* **Reverse-DNS Query Anomalies (`{log_type="dns"}`):** Monitors for sudden spikes in external DNS queries, highlighting potential DNS exfiltration attempts or beaconing behaviors.  
* **TCP Connection Tracking (`{log_type="conn"}`):** Traces failed and successful connection volumes to map system profiling, internal port scanning, and anomalous outbound communication.

## **🏆 Key Defensive Skills Demonstrated**

* **Linux Performance Tuning & Systemd Engineering:** Diagnosed low-level process behaviors under CPU constraints and customized systemd environments to stabilize slow-starting Java services.  
* **Manual SIEM Administration:** Hand-provisioned independent SIEM components (Indexer, Manager, Dashboard) as a decoupled architecture instead of relying on helper scripts.  
* **Network Observability Integration:** Engineered an agent-based log forwarding pipeline utilizing Grafana Alloy, Loki, and Zeek, applying proper Linux POSIX permission/group alignment to safeguard sensitive system data.

