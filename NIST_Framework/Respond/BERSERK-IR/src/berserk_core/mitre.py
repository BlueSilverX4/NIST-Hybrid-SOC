MITRE_RULES = {
    "SSH Brute Force": {
        "technique": "T1110",
        "subtechnique": "T1110.001",
        "name": "Password Guessing",
        "confidence": "HIGH",
    }
}


def recommend_mitre(detection):
    """
    Return a MITRE ATT&CK recommendation based on
    a deterministic detection.
    """

    rule = MITRE_RULES.get(detection)

    if not rule:
        return None

    return rule
