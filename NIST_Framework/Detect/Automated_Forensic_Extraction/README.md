## 🔎 Project Overview

This project demonstrates a high-efficiency approach to **network forensics using Zeek (formerly Bro)**. Raw PCAP data was processed into protocol-specific logs to identify and investigate a **NetSupport RAT infection** on a corporate network while operating within a resource-constrained environment with **4 GB of RAM**.

The investigation focused on identifying the infected host, associated user account, network identity, and malicious command-and-control (C2) communication.

---

## 🛡️ NIST CSF Alignment

The investigation aligns with the following **NIST Cybersecurity Framework (CSF)** functions:

* **Detect (DE):** Automated identification of malicious C2 communication.
* **Respond (RS):** Forensic characterization of the infected host and compromised user account.

---

## 🧰 Technical Skills Demonstrated

* **Network Security Monitoring:** Parsing and analyzing network traffic through Zeek-generated logs.
* **Linux Engineering:** CLI-based automation, log processing, and environment configuration.
* **Incident Response:** Correlating Layer 2 (MAC), Layer 3 (IP), and Layer 7 (identity/application) information to identify the affected endpoint and user.

---

## 🚨 Investigation Findings

| Artifact           | Finding             |
| ------------------ | ------------------- |
| **Host Name**      | `DESKTOP-TEYQ2NR`   |
| **User Account**   | `Brad Rolf (brolf)` |
| **Victim IP**      | `10.2.28.88`        |
| **MAC Address**    | `00:19:d1:b2:4d:ad` |
| **MAC Vendor**     | Intel Corp          |
| **C2 Destination** | `45.131.214.85:443` |
| **Malware**        | NetSupport RAT      |

The investigation identified network communication from the affected endpoint to the documented C2 destination associated with the **NetSupport RAT** infection.

---

## 🔬 Investigation Methodology

### 1. Ingestion

Raw PCAP data was processed through **Zeek** to extract protocol-specific forensic artifacts and generate structured network logs.

### 2. Analysis

Command-line tools including `zeek-cut` and `grep` were used to filter and examine relevant **DHCP, Kerberos, and HTTP** logs.

### 3. Correlation

The extracted artifacts were correlated across multiple network layers to map the malicious connection back to a specific physical device and its authenticated user.

```text
Raw PCAP
   │
   ▼
  Zeek
   │
   ├── DHCP Logs ──────► Host / MAC Identification
   │
   ├── Kerberos ───────► User / Identity Correlation
   │
   └── HTTP / Network ─► C2 Communication
              │
              ▼
       Incident Correlation
              │
              ▼
     NetSupport RAT Finding

