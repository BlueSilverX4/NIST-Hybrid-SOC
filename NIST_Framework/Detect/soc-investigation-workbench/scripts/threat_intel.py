import os
import requests
import ipaddress
from flask import Flask, request, jsonify

app = Flask(__name__)

VT_API_KEY = os.getenv("VT_API_KEY", "INSERT VT_API_KEY_HERE")
VT_BASE_URL = "https://www.virustotal.com/api/v3"

def query_virustotal(ip_str):
    """Clean, validate, and query VirusTotal v3 API for a given IP."""
    # Catch unparsed Grafana variables
    if ip_str.startswith("${") or ip_str.startswith("%24%7B") or not ip_str:
        return jsonify({
            "error": "Invalid variable interpolation from Grafana",
            "hint": "Ensure the Grafana Data Link uses ${__value.raw} inside Panel Edit > Data Links."
        }), 400

    # Clean and validate IP address format and scope
    try:
        ip_obj = ipaddress.ip_address(ip_str.strip())
        
        # Filter out IPs that VirusTotal does not index
        if ip_obj.is_private or ip_obj.is_multicast or ip_obj.is_reserved or ip_obj.is_loopback:
            return jsonify({
                "ip": str(ip_obj),
                "status": "skipped",
                "reason": "Internal, loopback, or multicast IP addresses are not indexed by VirusTotal."
            }), 200
            
        if ip_obj.version == 6:
            return jsonify({
                "ip": str(ip_obj),
                "status": "skipped",
                "reason": "IPv6 addresses skipped for standard IPv4 lookup endpoint."
            }), 200

    except ValueError:
        return jsonify({"error": f"Invalid IP address format: {ip_str}"}), 400

    # Send request to VirusTotal API v3
    headers = {"x-apikey": VT_API_KEY}
    url = f"{VT_BASE_URL}/ip_addresses/{ip_str}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json().get('data', {}).get('attributes', {})
            stats = data.get('last_analysis_stats', {})
            return jsonify({
                "ip": ip_str,
                "reputation": data.get('reputation', 0),
                "malicious_count": stats.get('malicious', 0),
                "suspicious_count": stats.get('suspicious', 0),
                "harmless_count": stats.get('harmless', 0),
                "country": data.get('country', 'N/A'),
                "as_owner": data.get('as_owner', 'N/A')
            }), 200
        elif response.status_code == 404:
            return jsonify({
                "ip": ip_str,
                "status": "not_found",
                "reason": "No record found on VirusTotal for this address."
            }), 404
        else:
            return jsonify({
                "error": f"VirusTotal API returned HTTP {response.status_code}",
                "details": response.text
            }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/lookup/ip', methods=['GET'])
def lookup_ip_param():
    """Endpoint for query string parameters: /lookup/ip?address=8.8.8.8"""
    ip_addr = request.args.get('address', '')
    return query_virustotal(ip_addr)


@app.route('/lookup/ip/<path:ip_address>', methods=['GET'])
def lookup_ip_path(ip_address):
    """Endpoint for REST path parameters: /lookup/ip/8.8.8.8"""
    return query_virustotal(ip_address)


if __name__ == '__main__':
    print("[*] Starting Threat Intel Microservice on http://0.0.0.0:5000 ...")
    app.run(host='0.0.0.0', port=5000)
