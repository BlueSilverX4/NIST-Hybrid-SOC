from src.berserk_core.detector import detect_ssh_bruteforce


def test_ssh_bruteforce_detection():

    logs = [
        "Aug  3 08:14:22 sshd[1001]: Failed password for admin from 185.220.101.5 port 42110 ssh2",
        "Aug  3 08:14:25 sshd[1002]: Failed password for admin from 185.220.101.5 port 42112 ssh2",
        "Aug  3 08:14:28 sshd[1003]: Failed password for root from 185.220.101.5 port 42115 ssh2",
        "Aug  3 08:14:31 sshd[1004]: Failed password for root from 185.220.101.5 port 42118 ssh2",
    ]

    findings = detect_ssh_bruteforce(logs)

    assert findings
    assert findings[0]["indicator"] == "185.220.101.5"
    assert findings[0]["event"] == "SSH Brute Force"
    assert findings[0]["failed_attempts"] == 4
    assert findings[0]["severity"] == "HIGH"
    assert findings[0]["confidence"] == "HIGH"
    assert len(findings[0]["evidence"]) == 4

def test_benign_ssh_activity():

    logs = [
        "Aug  3 09:10:22 sshd[2001]: Accepted password for brandon from 192.168.1.20 port 50100 ssh2",
        "Aug  3 09:15:42 sshd[2002]: Accepted password for brandon from 192.168.1.20 port 50101 ssh2",
    ]

    findings = detect_ssh_bruteforce(logs)

    assert findings == []
