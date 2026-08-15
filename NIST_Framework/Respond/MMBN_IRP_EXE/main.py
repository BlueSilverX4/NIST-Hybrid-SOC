import sys
import logging

from navi.navi_core import NetNaviCore

def main():
    # Initialize NetNavi AI Engine
    navi = NetNaviCore(navi_name="MegaMan.EXE")
    
    # Dynamic PID from command line, fallback to 152719 if no argument is passed
    target_pid = int(sys.argv[1]) if len(sys.argv) > 1 else 152719

    # Simulated SIEM Alert Payload
    incoming_alert = {
        "alert_id": "ALT-9021",
        "threat_type": "Ransomware.LockBit",
        "severity": "CRITICAL",
        "target_host": "10.0.4.15",
        "pid": target_pid,
        "interface": "wlan0",
        "description": "Unauthorized encryption activity detected on local disk. C2 beaconing active."
    }

    # Jack In and execute IR sequence
    navi.jack_in_and_respond(incoming_alert)

if __name__ == "__main__":
    main()
