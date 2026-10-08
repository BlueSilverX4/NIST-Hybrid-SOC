#!/usr/bin/env bash
# operation-d-brigade/guardromon-perimeter/guardromon-firewall.sh
# Guardromon Perimeter Defense - iptables Baseline Rules

echo "[+] Activating Guardromon Heavy Armor Rules..."

# 1. Flush existing rules and start clean
iptables -F
iptables -X
iptables -Z

# 2. Set default policies: Allow outgoing, drop unauthorized incoming
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# 3. Allow loopback interface (local communication)
iptables -A INPUT -i lo -j ACCEPT

# 4. Allow established and related connections (so outbound traffic works)
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# 5. Guardromon Anti-Scan & Rate-Limiting Rules (Drop port scans)
# Limit ICMP (ping) to prevent reconnaissance
iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 1/s -j ACCEPT

# Log dropped packets for telemetry collection (Tagged for Brigadramon/Syslog)
iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "[GUARDROMON-DROP]: " --log-level 7

echo "[+] Guardromon Rules Applied. Status:"
iptables -L INPUT -n -v --line-numbers
