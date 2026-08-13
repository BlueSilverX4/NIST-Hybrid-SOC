# Incident Response Playbook: Network Reconnaissance & Port Scanning

## 1. Preparation
- **Monitoring Sensor:** Zeek Network Security Monitor running on physical interface `wlan0`.
- **Log Source:** `/opt/zeek/spool/zeek/dns.log` and `conn.log`

## 2. Detection (The Trigger)
An incident is declared if an internal or external host initiates a rapid succession of connection requests across multiple closed ports, or exhibits mass anomalous DNS traffic.

## 3. Containment & Mitigation
- Identify the source IP address from the Zeek logs.
- Manually or via automated script deploy an firewall (`iptables` / `ufw`) rule to drop all traffic from the offending host.
