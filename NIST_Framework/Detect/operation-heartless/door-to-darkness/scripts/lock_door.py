#!/usr/bin/env python3
import os
import sys
import logging
from flask import Flask, request, jsonify
import subprocess

# Configure Logging
LOG_FILE = os.path.expanduser("~/Portfolios/operation-heartless/door-to-darkness/logs/block_events.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [DOOR-TO-DARKNESS] %(message)s"
)

app = Flask(__name__)

def block_ip(ip_address):
    """Executes iptables DROP command for the offending IP."""
    try:
        # Check if rule already exists to prevent duplicates
        check_cmd = f"sudo iptables -C INPUT -s {ip_address} -j DROP"
        res = subprocess.run(check_cmd, shell=True, stderr=subprocess.DEVNULL)
        
        if res.returncode == 0:
            msg = f"IP {ip_address} is already blocked in iptables. Skipping."
            print(f"[!] {msg}")
            logging.info(msg)
            return True

        # Apply iptables DROP rule
        block_cmd = f"sudo iptables -A INPUT -s {ip_address} -j DROP"
        subprocess.run(block_cmd, shell=True, check=True)
        
        msg = f"KEYBLADE LOCKED: Successfully dropped traffic from IP {ip_address}"
        print(f"[+] {msg}")
        logging.info(msg)
        return True

    except subprocess.CalledProcessError as e:
        err_msg = f"Failed to execute iptables rule for {ip_address}: {e}"
        print(f"[-] {err_msg}")
        logging.error(err_msg)
        return False

@app.route('/webhook', methods=['POST'])
def handle_alert():
    """Webhook endpoint for Grafana/Alertmanager payload."""
    data = request.get_json()
    if not data or 'alerts' not in data:
        return jsonify({"status": "ignored", "reason": "No alerts array found"}), 400

    for alert in data.get('alerts', []):
        labels = alert.get('labels', {})
        # Extract IP from id_orig_h (Zeek network alert) or target_ip / instance
        target_ip = labels.get('id_orig_h') or labels.get('instance') or labels.get('src_ip')
        alert_name = labels.get('alertname', 'UnknownAlert')

        if target_ip:
            logging.info(f"Triggered Alert '{alert_name}' for IP: {target_ip}")
            block_ip(target_ip)
        else:
            logging.warning(f"Alert '{alert_name}' received without target IP label.")

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    # Flask listener running on port 5001 to avoid collisions
    print("[*] Starting Door to Darkness SOAR Webhook Listener on port 5001...")
    app.run(host='0.0.0.0', port=5001)
