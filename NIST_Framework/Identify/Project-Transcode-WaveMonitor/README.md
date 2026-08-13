# Project Transcode: Wave World Monitor (Project-3)

An electromagnetic wave tracking framework and wireless asset discovery architecture mapped explicitly to the **Identify (Asset Management)** function of the NIST Cybersecurity Framework.

## 🛰️ Portfolio Overview
This project targets the security of 802.11 wireless infrastructure, utilizing bare-metal RF sniffing hardware to discover local wireless assets, catalog access point baselines, and audit hidden infrastructure signatures.

## 🔍 Wireless Reconnaissance & Threat Analysis

Using a physical Alfa monitoring interface running passive 802.11 frame captures, the sensor mapped local wireless infrastructure and isolated unencrypted management frames.

### 🛰️ Identified Rogue Wave Vectors
The following access points were flagged for broadcasting an open security posture (`OPN`) without active ESSID string lengths, representing unauthorized or rogue physical infrastructure vectors:

| Target BSSID | Channel | Configuration | Risk Classification |
| :--- | :---: | :---: | :--- |
| `AC:EC:85:9E:1D:76` | 6 | OPN (Hidden) | Rogue Access Point / Evil Twin Vector |
| `C0:36:53:0C:71:C8` | 6 | OPN (Hidden) | Rogue Access Point / Evil Twin Vector |
| `AC:EC:85:9D:8F:76` | 6 | OPN (Hidden) | Rogue Access Point / Evil Twin Vector |

### 🌐 The Star Force Interpretation (Lore Toggle)
*   **The Status:** Rogue signals detected echoing across Channel 6 of the Wave Road! 
*   **The Threat:** These unencrypted, faceless broadcast frames match the signatures of foreign EM viruses trying to destabilize the district's networks. By isolating their physical MAC addresses, the Star Carrier can target and isolate the rogue frequencies before real-world electronic device malfunctions occur.

## ⚙️ Automated Log Pipeline Architecture

To transition the deployment from manual batch inspection to real-time telemetry streaming, a data pipeline was engineered using the Grafana Alloy orchestration framework.

*   **Log Forwarder:** `alloy_wireless_pipeline.alloy` monitors active local CSV exports.
*   **Parsing Layer:** Regex pattern extraction isolates the 802.11 physical MAC layer boundaries, pulling `bssid`, `channel`, and `privacy` properties inline.
*   **Log Ingestion Backend:** Streams structured tokens over internal loopback ports to a local Loki aggregation platform for immediate analytical indexing.

### 🚀 Pipeline Verification Command
To dry-run test the pipeline schema locally against target infrastructure dumps:
```bash
alloy run alloy_wireless_pipeline.alloy

# Project Transcode: WaveMonitor Pipeline

A resource-optimized wireless observability and threat-hunting pipeline deployed on bare-metal architecture. This project captures raw radio frequency (RF) spectrum frames, parses local telemetry, and ships structured labels into a centralized visualization platform to identify rogue access points and signal anomalies.

## 🛠️ System Architecture & NIST Mapping

This deployment is structured deliberately around the core functions of the **NIST Cybersecurity Framework (CSF)** to demonstrate enterprise-aligned engineering constraints on limited local hardware.

+--------------------------------------------------------------------------+
|                                 DETECT                                   |
|  [ Alfa Wireless Card ] -> [ airodump-ng ] -> [ Raw CSV Telemetry ]       |
|                                                                          |
|                                 IDENTIFY                                 |
|               [ Grafana Alloy Engine ] (Regex Parsing / Labelling)       |
|                                                                          |
|                                 PROTECT                                  |
|         [ Loki Ingestion ] Engine Engine Engine (Kernel zRAM Compression)|
+--------------------------------------------------------------------------+


### 📋 Identify (ID) — Asset & Data Flow Inventory
* **ID.AM-2 (Physical Asset Inventory):** Logged and mapped 57 unique RF endpoints into an active tracking repository (`data/`), establishing an operational baseline for local wireless footprints.
* **ID.AM-4 (Data Flow Mapping):** Explicitly mapped the ingest pipeline data flow within `alloy_wireless_pipeline.alloy`, tracing raw radio packet collection (`data_exports/`) through the Grafana Alloy ingestion engine to localized database sinks.

### 🛡️ Protect (PR) — Hardware Constraints & Optimization
* **Environment:** Deployed entirely on bare-metal infrastructure (HP Pavilion 23, 3.4 GiB RAM) to avoid the compute virtualization overhead of traditional hypervisors.
* **Memory Hardening (zRAM):** To ensure maximum system availability and protect the low-spec machine from disk-swapping latency spikes during deep packet manipulation, a kernel-level compressed swap layer (`/dev/zram0`) was initialized.
* **Performance Metric:** Achieved an active **2.5x data-to-compression ratio** via the `lz4` compression engine, allowing concurrent operations of the OS, network capture cards, and the full observability stack without experiencing system degradation.

---

## ⚙️ Configuration Deployment

### Grafana Alloy Pipeline (`alloy_wireless_pipeline.alloy`)
```alloy
local.file_match "wireless_logs" {
    path_targets = [{
        __address__ = "localhost",
        __path__    = "/home/brandongregg/Portfolios/Project-Transcode-WaveMonitor/data_exports/wave_capture-01.csv",
        job         = "wave-world-monitor",
    }]
}

loki.source.file "wave_sensor_stream" {
    targets    = local.file_match.wireless_logs.targets
    forward_to = [loki.process.parse_wireless_csv.receiver]
}

loki.process "parse_wireless_csv" {
    stage.regex {
        expression = "^(?P<bssid>[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}),\\s*[^,\\s]*,\\s*[^,\\s]*,\\s*(?P<channel>\\d+),\\s*[^,\\s]*,\\s*(?P<privacy>[A-Za-z0-9]+)"
    }
    stage.labels {
        values = {
            bssid   = "bssid",
            channel = "channel",
            privacy = "privacy",
        }
    }
    forward_to = [loki.write.local_loki_sink.receiver]
}

loki.write "local_loki_sink" {
    endpoint {
        url = "[http://127.0.0.1:3100/loki/api/v1/push](http://127.0.0.1:3100/loki/api/v1/push)"
    }
}
