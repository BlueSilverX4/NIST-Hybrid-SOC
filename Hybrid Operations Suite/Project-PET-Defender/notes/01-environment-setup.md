# Lab Initialization & Pre-Deployment Logs

## Host Mainframe Environment
- **Platform:** Bare-metal HP Pavilion 23
- **Operating System:** Kali Purple (Debian-based Rolling Release)
- **Role:** Central SIEM Mainframe (Wazuh Manager, Indexer, Dashboard)

## Deployment Obstacles & Troubleshooting

### Log Entry 01: Host Compatibility Warning
- **Symptom:** Script outputted: `WARNING: The current system does not match with the list of recommended systems.`
- **Root Cause:** Kali Purple is built on Debian Testing/Rolling branches, which falls outside of Wazuh’s enterprise production target whitelist.
- **Resolution:** Acknowledged and safe to bypass; package dependencies remain fully compatible.

### Log Entry 02: Hardware Resource Constraint Error
- **Symptom:** Script halted with: `ERROR: Your system does not meet the recommended minimum hardware requirements of 4Gb of RAM and 2 CPU cores.`
- **Root Cause:** The default installer enforces corporate-level production hardware minimums.
- **Resolution:** Switched to a manual component installation workflow to allow micro-configurations of system resources.

### Log Entry 03: Systemd Initialization Timeout (CPU Constraint)
- **Symptom:** Service failed to start with a generic systemd `result 'timeout'` exception after precisely 90 seconds.
- **Root Cause:** The underlying customized Java security framework requires significant processing overhead during its very first initialization. The host CPU required roughly ~3 minutes to fully provision internal cryptographic database spaces, tripping systemd's default 90-second execution wall-clock limit.
- **Resolution:** Created a native systemd drop-in override directory and extended the startup threshold allowance parameter to 10 minutes (600 seconds) to ensure the hardware had adequate breathing room to stand up:
  ```bash
  sudo mkdir -p /etc/systemd/system/wazuh-indexer.service.d
  echo -e "[Service]\nTimeoutStartSec=600" | sudo tee /etc/systemd/system/wazuh-indexer.service.d/override.conf
  sudo systemctl daemon-reload
  sudo systemctl restart wazuh-indexer

### Log Entry 04: Systemd Initialization Timeout (CPU Constraint)
- **Symptom:** Service failed to start with a generic systemd `result 'timeout'` exception after precisely 90 seconds.
- **Root Cause:** The underlying customized Java security framework requires significant processing overhead during its very first initialization. The host CPU required roughly ~3 minutes to fully provision internal cryptographic database spaces, tripping systemd's default 90-second execution wall-clock limit.
- **Resolution:** Created a native systemd drop-in override directory and extended the startup threshold allowance parameter to 10 minutes (600 seconds) to ensure the hardware had adequate breathing room to stand up:
  ```bash
  sudo mkdir -p /etc/systemd/system/wazuh-indexer.service.d
  echo -e "[Service]\TimeoutStartSec=600" | sudo tee /etc/systemd/system/wazuh-indexer.service.d/override.conf
  sudo systemctl daemon-reload
  sudo systemctl restart wazuh-indexer

## Next Phase: Provisioning the Wazuh Manager Core

With the indexing engine safely holding down the fort, the next piece of the puzzle is installing the **Wazuh Manager** itself. This is the application daemon that parses incoming security events from your GPD Win's Parrot OS node, compares them against rules, and decides when to trigger defensive automations.

Since we are rocking a manual installation route due to our hardware customizations, let's grab and install the manager binary package cleanly:

```bash
cd ~/Portfolios/Project-PET-Defender/scripts

# 1. Download the unified manager component
wget -4 https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-manager/wazuh-manager_4.14.5-1_amd64.deb

# 2. Force install the local binary package
sudo dpkg -i wazuh-manager_4.14.5-1_amd64.deb

# 3. Fire it up and check if its footprint starts smoothly
sudo systemctl daemon-reload
sudo systemctl enable wazuh-manager
sudo systemctl start wazuh-manager
sudo systemctl status wazuh-manager

### Log Entry 04: Wazuh Manager Initialization Timeout (Sub-Daemon Latency)
- **Symptom:** Service installation succeeded, but startup initializations halted with systemd `result 'timeout'`.
- **Root Cause:** The manager spins up multiple micro-daemons simultaneously. The primary analysis engine (`wazuh-analysisd`) requires extensive processing capacity to compile XML rule definitions on boot. This process exceeded systemd's standard script validation timer, leading to a false-positive failure state while the process was still running in the background.
- **Resolution:** Terminated the lingering background processes, built a custom drop-in systemd configuration directory for the manager service, and extended the startup parameter allowance to 5 minutes (`300s`):
  ```bash
  sudo pkill -f wazuh-
  sudo mkdir -p /etc/systemd/system/wazuh-manager.service.d
  echo -e "[Service]\nTimeoutStartSec=300" | sudo tee /etc/systemd/system/wazuh-manager.service.d/override.conf
  sudo systemctl daemon-reload
  sudo systemctl start wazuh-manager
Status: SUCCESSFUL. Core manager online, spawning 200+ task threads, validated utilizing systemctl status.


---

### Next Phase: The Final Core Component — The Dashboard

You have successfully stood up the database storage layer (`wazuh-indexer`) and the processing logic engine (`wazuh-manager`). Now, we just need to install the **Wazuh Dashboard** so you can access the graphical user interface via HTTPS on port 443!

Let's fetch the final package and get it onto your server:

```bash
cd ~/Portfolios/Project-PET-Defender/scripts

# 1. Download the frontend web dashboard binary
wget -4 https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-dashboard/wazuh-dashboard_4.14.5-1_amd64.deb

# 2. Extract and force install the binary package
sudo dpkg -i wazuh-dashboard_4.14.5-1_amd64.deb

## Deployment Status Summary

| Component | Role | Runtime | Status | Resource Target |
| :--- | :--- | :--- | :--- | :--- |
| **wazuh-indexer** | DB Cluster | Java (JVM) | 🟢 ACTIVE | Tuned to 1GB Heap Limit |
| **wazuh-manager** | Analytics | C/Python | 🟢 ACTIVE | Default Array Threads |
| **wazuh-dashboard**| Frontend | Node.js | 🟢 ACTIVE | Native (~230MB Peak) |

### Phase 1 Conclusion
All local architectural components have been successfully decoupled from the automated enterprise script installation method, manually provisioned, optimized for resource-constrained lab environments via customized JVM options and extended systemd timeouts, and cryptographically verified. The central detection matrix is ready to ingest endpoint telemetry.

## Engineering Log: Telemetry Ingestion Pipeline
**Date:** July 13, 2026
**Component:** Observability & Log Orchestration (NIST Detect / Respond)

### Completed Objectives:
1. **Loki Daemon Activation:** Verified local log backend listening state via loopback port `3100`.
2. **Grafana Alloy Pipeline Configuration:** 
   - Constructed standard `config.alloy` to discover and tail native Zeek logs (`/opt/zeek/logs/current/*.log`).
   - Implemented dynamic string parsing via regex stages to extract log names (`dns`, `conn`) automatically into `log_type` labels.
3. **Access Control & Permissions:** Remedied deployment permission blocks by appending the `alloy` user to the `zeek` system group and applying absolute execution bits (`755`) to the directory stack traversal path.
4. **Data Aggregation & Visualization:**
   - Isolated historical log-backfill timing characteristics using tight window analysis.
   - Built a custom **LogQL** dashboard tracing internal reverse-DNS querying spikes (`{log_type="dns"}`) and TCP connection anomalies (`{log_type="conn"}`).
