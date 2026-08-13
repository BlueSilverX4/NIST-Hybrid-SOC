\# Project-Scilab-Firewall: UnderNet Hunter 🌐🛡️

An end-to-end host-based firewall telemetry and security monitoring pipeline. This project captures raw Linux kernel firewall drops (\`NETPOLICE\_DROP\`), processes them through an enterprise-grade ingestion agent, and visualizes live threat intelligence on a dynamic Grafana SOC dashboard.

\---

\#\# 🏗️ Architecture Overview

The telemetry pipeline is built using the following modern open-source observability stack:

\[ Linux Kernel /dev/kmsg \] │ ▼ (Reads raw firewall syslog drops) \[ Grafana Alloy \] │ ▼ (Applies Regex, parses metadata, extracts labels) \[ Grafana Loki \] (Aggregates and stores structured logs) │ ▼ (Runs real-time LogQL queries) \[ Grafana Dashboard \] (SOC Isolation Deck Visuals)

1\. \*\*Sensor & Enforcer:\*\* Linux iptables rules configured to drop unauthorized traffic, tagging dropped packets with the prefix \`NETPOLICE\_DROP\`.  
2\. \*\*Collector:\*\* \*\*Grafana Alloy\*\* tails the system kernel log buffer (\`/dev/kmsg\`), isolates firewall events, parses nested networking values using regex, and structures them into indexed labels.  
3\. \*\*Log Database:\*\* \*\*Grafana Loki\*\* ingests and indexes the parsed events.  
4\. \*\*Visualization:\*\* \*\*Grafana SOC Dashboard\*\* queries Loki in real-time using LogQL to visualize security incidents.

\---

\#\# 📊 SOC Dashboard Visuals

Our custom dashboard provides an immediate tactical overview of incoming threats:

\* \*\*🚨 Target: Port 4444 Shell Drops (Time Series):\*\* Tracks high-risk connection attempts targeting port 4444—frequently associated with reverse-shell payloads.  
\* \*\*🌐 Top Attacking Threat Sources (Pie Chart):\*\* Aggregates and displays a real-time percentage distribution of attacking source IPs.  
\* \*\*🌐 Protocol Breakdown (Stat Panel):\*\* Tracks the split of transport layers (TCP, UDP, ICMP) to identify if an attacker is running ping sweeps or active port scans.

\---

\#\# 🚀 Telemetry Pipeline & Parsing Logic

To keep database ingestion lightweight and hyper-focused, Grafana Alloy filters out OS clutter at the edge. Below is the custom stage block used to extract raw IP headers, transport protocols, and target ports:

\`\`\`alloy  
// Grafana Alloy pipeline parsing snippet  
stage.regex {  
    expression \= "SRC=(?P\<src\_ip\>\[\\\\d\\\\.\]+) DST=(?P\<dst\_ip\>\[\\\\d\\\\.\]+) .\* PROTO=(?P\<protocol\>\\\\w+)"  
}  
stage.regex {  
    expression \= "DPT=(?P\<dst\_port\>\\\\d+)"  
}  
stage.labels {  
    values \= {  
        src\_ip   \= "",  
        protocol \= "",  
        dst\_port \= "",  
    }  
}

## **🧪 Simulation & Validation**

To test and validate the pipeline in a safe sandbox environment, a custom multi-protocol attack simulation script (`simulate_attacks.sh`) was developed to inject raw mock firewall hits directly into the kernel ring buffer:

Bash  
\# Run the attack simulator  
sudo bash simulate\_attacks.sh

### **Script Output:**

Plaintext  
\[-\] Starting UnderNet Attack Simulator... Press \[CTRL+C\] to stop.  
\[+\] Injected Drop: SRC=192.168.1.157 | PROTO=UDP | DST\_PORT=4444  
\[+\] Injected Drop: SRC=1.1.168.192   | PROTO=TCP | DST\_PORT=4673  
\[+\] Injected Drop: SRC=10.0.0.15     | PROTO=ICMP| DST\_PORT=4444

## **🛠️ Key Takeaways & Defensive Skills Demonstrated**

* **Data Engineering & Filtering:** Avoided database bloat by filtering out noisy system logs at the ingestion layer, minimizing Loki indexing costs.  
* **Structured Parsing:** Developed robust regular expressions to extract key network fields (Source IP, Destination IP, Protocol, Destination Port) from unstructured kernel messages.  
* **Observability & Analytics:** Configured dashboard metrics using precise LogQL range aggregations down to `[5s]` intervals for ultra-low latency alerting.

