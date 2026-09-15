def calculate_threat_score(case):
    score = 0
    factors = []

    # Repeated authentication attempts
    if len(case.evidence) >= 3:
        score += 20
        factors.append("Repeated authentication failures")

    # Privileged account targeting
    usernames = {
        event.username.lower()
        for event in case.evidence
    }

    if "root" in usernames:
        score += 25
        factors.append("Root account targeted")

    if "admin" in usernames:
        score += 15
        factors.append("Admin account targeted")

    # Confirmed compromise
    if case.compromise_confirmed:
        score += 40
        factors.append("Successful compromise confirmed")

    # Determine severity
    if score >= 80:
        severity = "CRITICAL"
    elif score >= 50:
        severity = "HIGH"
    elif score >= 25:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "score": score,
        "severity": severity,
        "factors": factors,
    }
