def evaluate_decision(case, threat_score):
    score = threat_score["score"]

    if case.compromise_confirmed:
        action = "CONTAIN"
        reason = "Confirmed compromise detected."

    elif score >= 80:
        action = "CONTAIN_PENDING_APPROVAL"
        reason = "Critical risk requires containment review."

    elif score >= 50:
        action = "INVESTIGATE"
        reason = "High-risk activity requires analyst investigation."

    elif score >= 25:
        action = "MONITOR"
        reason = "Suspicious activity warrants continued monitoring."

    else:
        action = "CLOSE"
        reason = "Insufficient evidence for further action."

    return {
        "action": action,
        "reason": reason,
        "requires_human_approval": action != "CLOSE",
    }
