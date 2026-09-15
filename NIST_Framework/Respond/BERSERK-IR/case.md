# BERSERK-001 — The Branded Host

## 1. Case Overview

| Field | Value |
|---|---|
| Case ID | BERSERK-001 |
| Title | The Branded Host |
| Detection | SSH Brute Force |
| Primary Indicator | 185.220.101.5 |
| Attempts | 4 |
| Severity | HIGH |
| Confidence | HIGH |
| Compromise Confirmed | False |
| Status | READY_FOR_CLOSURE |
| Human Approval | Required |

---

## 2. Executive Summary

BERSERK-IR detected repeated SSH authentication failures originating
from 185.220.101.5.

The activity targeted both the `admin` and `root` accounts.

The evidence supports a password-guessing attack. No successful attacker
authentication was observed, therefore compromise was not confirmed.

The case was classified as HIGH risk and routed to INVESTIGATE through
the BERSERK decision gate.

No automated containment or system changes were performed.

---

## 3. Evidence

| Timestamp | Username | Source IP | Port | Event |
|---|---|---|---|---|
| Aug 3 08:14:22 | admin | 185.220.101.5 | 42110 | SSH authentication failure |
| Aug 3 08:14:25 | admin | 185.220.101.5 | 42112 | SSH authentication failure |
| Aug 3 08:14:28 | root | 185.220.101.5 | 42115 | SSH authentication failure |
| Aug 3 08:14:31 | root | 185.220.101.5 | 42118 | SSH authentication failure |

---

## 4. Investigation Findings

### Observed

- Repeated authentication failures
- Admin account targeted
- Root account targeted
- Same source IP used across events
- Activity occurred within a short time period

### Not Observed

- Successful authentication
- Confirmed account compromise
- Confirmed privilege escalation
- Confirmed lateral movement
- Confirmed persistence
- Confirmed data exposure

---

## 5. MITRE ATT&CK Mapping

**Technique:** T1110
**Sub-technique:** T1110.001
**Name:** Password Guessing
**Confidence:** HIGH

**Validation:** Requires human validation.

---

## 6. BERSERK Threat Judgment

**Risk Score:** 60
**Recommended Severity:** HIGH

### Risk Factors

- Repeated authentication failures
- Root account targeted
- Admin account targeted

**Status:** Requires human validation.

---

## 7. Decision Gate

**Recommended Action:** INVESTIGATE

**Reason:** High-risk activity requires analyst investigation.

**Human Approval:** TRUE

---

## 8. Response

**Action:** INVESTIGATE
**Mode:** SIMULATION
**Playbook:** Black Swordsman Incident Response Protocol
**Protocol Phase:** Phase 4 — Apostle Hunt
**Human Approval:** TRUE

### Recommended Response

1. Review SSH authentication failures
2. Review targeted accounts
3. Check for successful authentication
4. Review related network and web activity
5. Determine whether containment is necessary

**System changes:** None performed.

---

## 9. Response Artifact

**Artifact:**
`BERSERK-001-response.json`

**Integrity file:**
`BERSERK-001-response.json.sha256`

**SHA-256:**

`a8f4a32d474d6be90f5904ceb890a1d69c797ba82fd281c373ae5d679d2bb3e6`

Integrity was independently verified using `sha256sum`.

---

## 10. Recovery Assessment

**Status:** NO_COMPROMISE_OBSERVED

**Compromise Confirmed:** False
**Containment Required:** False
**Recovery Required:** False

### Recovery Findings

1. Malicious authentication activity was detected.
2. No successful attacker authentication was observed.
3. No recovery action is currently required.

---

## 11. Closure Assessment

**Status:** READY_FOR_CLOSURE

**Closure Eligible:** True

**Human Approval:** Required

**Reason:**

> No compromise, containment, or recovery activity remains.

---

## 12. Lessons Learned

_To be completed during Phase 9 — Campfire._

---

## 13. Final Analyst Determination

_To be completed after lessons learned and final human review._
