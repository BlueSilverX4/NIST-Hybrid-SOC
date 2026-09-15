# BERSERK-IR — Case 001 Dragonslayer Response

## Case

**The Branded Host**

## Current Threat Assessment

**Severity:** HIGH

**Confidence:** HIGH

**Compromise:** NOT CONFIRMED

**Primary Indicator:** `185.220.101.5`

---

# 1. Response Objective

The objective is to reduce the immediate threat while
preserving evidence and avoiding unnecessary disruption.

Because successful compromise has not been established,
response actions should initially focus on:

- Evidence preservation
- Monitoring
- Threat containment
- Additional investigation
- Escalation

---

# 2. Response Decision

## Question 1

Has successful compromise been confirmed?

**NO**

Therefore, full endpoint isolation is not automatically
authorized at this stage.

---

# 3. Recommended Actions

## Action 1 — Preserve Evidence

Preserve relevant:

- Authentication logs
- Web access logs
- Security alerts
- Network telemetry
- System timestamps
- Relevant process information

Do not modify or delete the original evidence.

---

## Action 2 — Increase Monitoring

Monitor for additional activity from:

`185.220.101.5`

Look for:

- Additional SSH attempts
- Successful authentication
- New usernames
- Additional web exploitation attempts
- Privilege escalation
- Suspicious processes
- Lateral movement

---

## Action 3 — Network Containment

If organizational policy permits and the activity continues,
consider blocking the malicious source IP at the appropriate
network control.

Potential controls include:

- Firewall
- IDS/IPS
- Network ACL
- SIEM/SOAR response integration

The blocking action should be logged.

---

## Action 4 — Account Protection

Because `root` and `admin` were targeted:

- Review authentication activity
- Verify account status
- Confirm MFA where applicable
- Review recent successful logins
- Consider credential rotation if compromise is suspected

Do not disable legitimate accounts solely because they were
targeted.

---

# 4. Escalation Conditions

Escalate the incident if any of the following occur:

- Successful authentication from the suspicious source
- Evidence of privilege escalation
- Malware execution
- Persistence
- Lateral movement
- Data access or exfiltration
- Multiple systems become affected
- Continued activity after containment

---

# 5. Emergency Response

If compromise becomes confirmed:

1. Isolate the affected endpoint.
2. Preserve volatile and persistent evidence where possible.
3. Disable or protect compromised accounts.
4. Block confirmed malicious infrastructure.
5. Escalate to Incident Response / Tier 2.
6. Begin eradication and recovery procedures.

---

# 6. AI Safety Boundary

AI-generated recommendations are advisory.

The AI must not independently execute destructive or
high-impact containment actions.

Human approval is required for actions such as:

- Endpoint isolation
- Account disabling
- Firewall changes
- Credential rotation
- Process termination
- Evidence deletion or modification

---

# 7. Response Status

Current status:

**MONITOR + INVESTIGATE + PREPARE CONTAINMENT**

The incident remains HIGH severity.

Successful compromise remains unconfirmed.

---

# 8. Analyst Validation

The analyst must document:

- Decision made
- Evidence supporting the decision
- Action performed
- Time of action
- Person/system performing the action
- Result of the action

**Dragonslayer principle:**

> Strike the threat without destroying the evidence.
