# 🛡️ Snort 3 IDS — Custom Signature & Network Monitoring Lab

## 📋 Project Overview

This project demonstrates the deployment and validation of **Snort 3** as an Intrusion Detection System (IDS) on a Linux environment.

The objective was to establish real-time network visibility and develop a custom detection signature capable of identifying specific network traffic patterns, with **ICMP/Ping traffic** used as the primary detection scenario.

The lab focuses on practical IDS deployment, signature engineering, network-interface tuning, troubleshooting, and controlled detection validation.

---

## 🎯 Objectives

* Deploy Snort 3 as a network intrusion detection sensor.
* Engineer a custom ICMP detection signature.
* Configure the network interface for packet visibility.
* Troubleshoot Snort configuration and dependency issues.
* Generate controlled network traffic to validate detection.
* Confirm that alerts are generated successfully.

---

## 🏆 Technical Achievements

### Custom Rule Engineering

Developed and validated a functional **ICMP detection signature** designed to identify network reconnaissance and ping activity.

### Troubleshooting Hardcoded Dependencies

Identified and resolved a configuration issue involving a missing `ips.rules` file.

A placeholder bypass was implemented so the Snort parser could successfully load the custom detection configuration and continue initialization.

### Network Interface Tuning

Configured the network interface for improved packet visibility by:

* Disabling GRO/LRO offloading where required
* Enabling Promiscuous Mode
* Preparing the interface for live packet inspection

These adjustments helped ensure that the IDS sensor could observe the expected network traffic.

### Detection Verification

The detection engine was validated by generating ICMP traffic from external mobile devices connected to the same subnet.

Successful traffic generation resulted in Snort alerts, confirming that the custom detection workflow was operational.

---

# 🧰 Environment & Tools

| Component         | Purpose                                 |
| ----------------- | --------------------------------------- |
| **Kali Linux**    | IDS deployment environment              |
| **Snort 3.12+**   | Intrusion Detection System              |
| **ethtool**       | Network-interface configuration         |
| **tcpdump**       | Packet capture and traffic verification |
| **iproute2**      | Network configuration and inspection    |
| **Grafana**       | Security-event visualization            |
| **Elasticsearch** | Grafana data source                     |

The lab was tested across the documented **WSL/physical Kali environment** configurations.

---

# ⚙️ Detection Workflow

```text
Network Traffic
      │
      ▼
Network Interface
      │
      ▼
Snort 3 Sensor
      │
      ▼
Custom ICMP Signature
      │
      ▼
Detection Alert
      │
      ▼
Snort Alert Logs
      │
      ▼
Visualization / Investigation
```

---

# 🔧 Configuration Validation

Before starting live detection, validate the Snort configuration:

```bash
sudo snort -c /etc/snort/snort.lua -T
```

A successful configuration test confirms that Snort can parse the configured rules and initialize the detection engine.

---

# 🌐 Live Network Monitoring

Start Snort in live-capture mode:

```bash
sudo snort \
  -c /etc/snort/snort.lua \
  -i wlan0 \
  --daq afpacket \
  -l /var/log/snort \
  -A alert_fast
```

### Configuration Components

| Option           | Function                                    |
| ---------------- | ------------------------------------------- |
| `-c`             | Specifies the Snort configuration           |
| `-i wlan0`       | Selects the monitoring interface            |
| `--daq afpacket` | Uses the AFPacket packet-acquisition method |
| `-l`             | Specifies the Snort log directory           |
| `-A alert_fast`  | Enables fast alert output                   |

---

# 🧪 Detection Validation

The detection was validated by generating ICMP/Ping traffic from external mobile devices connected to the same subnet.

```text
External Device
      │
      │ ICMP / Ping
      ▼
Kali Network Interface
      │
      ▼
Snort 3 IDS
      │
      ▼
Custom ICMP Signature
      │
      ▼
Alert Generated
      │
      ▼
/var/log/snort
```

The successful alert generation demonstrated that the Snort sensor was able to observe the traffic and match it against the custom detection logic.

---

# 🔍 Investigation & Troubleshooting

This lab also provided hands-on experience troubleshooting an IDS deployment rather than simply running a preconfigured sensor.

### Configuration Dependency Issue

A missing `ips.rules` dependency prevented the Snort parser from loading the intended configuration.

The issue was investigated and resolved using a placeholder bypass, allowing the parser to proceed and the custom rules to load.

### Network Visibility

Network-interface configuration was reviewed to ensure that the sensor could observe the expected traffic.

This included:

* Reviewing interface state
* Configuring Promiscuous Mode
* Adjusting GRO/LRO settings
* Verifying traffic visibility with packet-capture tooling

---

# 🛡️ SOC Detection Value

This Snort exercise demonstrates practical experience with:

* Intrusion Detection Systems
* Network Security Monitoring
* Custom signature engineering
* ICMP traffic analysis
* Packet capture
* Network-interface configuration
* IDS troubleshooting
* Alert validation
* Security visualization

It also complements the endpoint-focused detection work in **DigiPolice-SOC v2** by adding a network-based detection layer.

```text
                 DigiPolice SOC
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
     Endpoint Data             Network Data
          │                         │
       Wazuh                     Snort
          │                         │
          └────────────┬────────────┘
                       ▼
                 SOC Investigation
```

---

# 📌 Lab Outcome

The lab successfully demonstrated:

* ✅ Snort 3 deployment
* ✅ Custom ICMP detection
* ✅ Configuration troubleshooting
* ✅ Network-interface tuning
* ✅ Live packet inspection
* ✅ Controlled alert generation
* ✅ External-device detection validation
* ✅ Integration with the broader SOC monitoring workflow
