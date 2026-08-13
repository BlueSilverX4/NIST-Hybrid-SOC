#!/bin/bash
# =============================================================================
# Project Scilab Firewall - UnderNet Attack Simulator
# =============================================================================

# Array of simulated attacker IPs
IPS=("192.168.1.99" "10.0.0.15" "172.16.5.22" "192.168.1.157" "1.1.168.192")
# Array of protocols
PROTOCOLS=("TCP" "UDP" "ICMP")

echo "[-] Starting UnderNet Attack Simulator... Press [CTRL+C] to stop."

while true; do
    # Select random values
    SRC_IP=${IPS[$RANDOM % ${#IPS[@]}]}
    PROTO=${PROTOCOLS[$RANDOM % ${#PROTOCOLS[@]}]}
    
    # Randomly target high-risk port 4444 or a random port
    if [ $((RANDOM % 2)) -eq 0 ]; then
        DST_PORT="4444"
    else
        DST_PORT=$((RANDOM % 65535 + 1))
    fi

    # Format the log line based on protocol
    if [ "$PROTO" == "ICMP" ]; then
        LOG_LINE="<5>NETPOLICE_DROP: IN=wlan0 OUT= MAC=00:11:22:33:44:55 SRC=$SRC_IP DST=192.168.111.148 LEN=36 TOS=0x00 PREC=0x00 TTL=64 ID=36672 PROTO=ICMP TYPE=8 CODE=0"
    else
        LOG_LINE="<5>NETPOLICE_DROP: IN=wlan0 OUT= MAC=00:11:22:33:44:55 SRC=$SRC_IP DST=192.168.111.148 LEN=40 TOS=0x00 PREC=0x00 TTL=64 ID=54321 PROTO=$PROTO SPT=$((RANDOM % 65535 + 1)) DPT=$DST_PORT"
    fi

    # Inject into kernel log
    echo "$LOG_LINE" | sudo tee /dev/kmsg > /dev/null
    
    echo "[+] Injected Drop: SRC=$SRC_IP | PROTO=$PROTO | DST_PORT=$DST_PORT"
    
    # Wait a random time between 2 to 6 seconds before sending the next one
    sleep $((RANDOM % 5 + 2))
done
