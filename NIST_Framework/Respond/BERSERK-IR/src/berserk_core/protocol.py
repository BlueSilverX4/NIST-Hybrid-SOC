PROTOCOL_PHASES = {
    "INVESTIGATE": {
        "phase": "Phase 4",
        "name": "Apostle Hunt",
        "objective": "Determine whether the activity represents malicious behavior.",
        "tasks": [
            "Identify indicators of compromise",
            "Search for related events",
            "Identify affected assets",
            "Identify affected accounts",
            "Search for repeated activity",
            "Determine attack pattern",
        ],
    },

    "CONTAIN_PENDING_APPROVAL": {
        "phase": "Phase 7",
        "name": "Dragonslayer Response",
        "objective": "Contain the threat while minimizing business impact.",
        "tasks": [
            "Validate malicious activity",
            "Review affected accounts",
            "Prepare containment action",
            "Obtain analyst approval",
            "Execute containment only after approval",
        ],
    },

    "CONTAIN": {
        "phase": "Phase 7",
        "name": "Dragonslayer Response",
        "objective": "Contain the confirmed threat.",
        "tasks": [
            "Block malicious network indicators",
            "Disable compromised accounts",
            "Isolate affected endpoints",
            "Preserve evidence",
            "Escalate to Incident Response",
        ],
    },

    "MONITOR": {
        "phase": "Phase 4",
        "name": "Apostle Hunt",
        "objective": "Continue investigating suspicious activity.",
        "tasks": [
            "Search for related events",
            "Search for repeated activity",
            "Identify attack patterns",
        ],
    },

    "CLOSE": {
        "phase": "Phase 8",
        "name": "Aftermath",
        "objective": "Document the incident and findings.",
        "tasks": [
            "Document the finding",
            "Record indicators",
            "Record investigation results",
            "Determine whether detection tuning is required",
        ],
    },
}


def get_protocol_phase(action):
    return PROTOCOL_PHASES.get(action)
