# INCIDENT DETECTION REPORT: Operation Ironclad

**Date:** May 19, 2026  
**Analyst:** Brandon Lawrence Gregg  
**Status:** Closed / Remediated  

---

## 1. Executive Summary
On May 19, 2026, at approximately 21:27 EDT, the local Network Intrusion Monitoring system (Zeek) flagged an anomalous spike in connection volume targeting the primary security operations asset (Kali Purple host at `192.168.1.157`). A single internal asset initiated tens of thousands of rapid connection requests over an 18-minute window, indicating active network reconnaissance. 

## 2. Threat Actor Profile
* **Source IP:** `192.168.1.61` (Identified as GPD Win 1 running Parrot OS)
* **Target IP:** `192.168.1.157` (Kali Purple Monitoring Engine)
* **Total Connection Attempts:** 78,350 unique socket requests
* **Protocol Distribution:** High-volume TCP SYN sweeps alongside selective UDP probes.

## 3. Technical Evidence & Artifact Triage
Analysis of the `conn.log` and `http.log` files yielded definitive evidence of an intensive **Nmap port scan (-sS -sV -O -p-)**:

1. **Volume Analysis (`conn.log`):** The adversary methodically scanned the entire TCP port spectrum. High-frequency connection metrics confirmed targeting on open infrastructure services:
   * Port 9200 (Elasticsearch Core)
   * Port 3000 (Grafana Dashboard)
   * Port 5601 (Kibana Instance)
   
2. **Application Layer Fingerprinting (`http.log`):** During version detection, the attacker triggered the Nmap Scripting Engine (NSE). The system intercepted clear text User-Agent strings and signature web-probing directories:
   * **Hardcoded String Detected:** `/nice ports,/Trinity.txt.bak` (Signature Nmap indicator)
   * **User-Agent Caught:** `Mozilla/5.0 (compatible; Nmap Scripting Engine; https://nmap.org/book/nse.html)`

## 4. Containment & Remediation Recommendations
* **Isolate Network Assets:** Ensure internal testing tools (like the GPD Win 1) are confined to an isolated testing VLAN rather than the production wireless subnet.
* **Firewall Access Control Lists (ACLs):** Restrict access to ports 3000, 5601, and 9200 exclusively to localhost loopback interfaces or explicit authorized administrative IPs to prevent external footprinting.
* **Implement Rate Limiting:** Configure iptables or local firewalls to drop traffic from hosts exceeding 100 connection attempts per minute.
