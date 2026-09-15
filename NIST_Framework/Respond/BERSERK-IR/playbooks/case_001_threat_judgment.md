# BERSERK-IR — Case 001 Threat Judgment

## Case

**The Branded Host**

## Primary Indicator

`185.220.101.5`

---

## 1. Executive Judgment

**Severity:** HIGH

**Confidence:** HIGH

**Malicious Activity:** CONFIRMED

**Successful Compromise:** NOT CONFIRMED

**Unified Attack Chain:** NOT ESTABLISHED

---

## 2. Evidence Summary

The following activity was observed from `185.220.101.5`:

### Authentication Activity

Four failed SSH authentication attempts occurred within
approximately nine seconds.

Targeted usernames:

- `admin`
- `root`

No successful SSH authentication from this source was
observed in the available evidence.

### Web Activity

The same source IP appears in web telemetry with:

- Attempted access to `/etc/passwd`
- SQL-injection-style input against `/login.php`

The `/etc/passwd` request returned HTTP 403.

The SQL-injection-style request returned HTTP 500.

---

## 3. Severity Factors

### Factors Increasing Severity

- External source targeting the environment
- Repeated authentication attempts
- Targeting `root`
- Targeting `admin`
- Multiple suspicious behaviors
- Same source IP observed across authentication and web telemetry
- Evidence consistent with credential attack activity
- Evidence consistent with attempted web exploitation

### Factors Limiting Severity

- No successful authentication observed
- No confirmed privilege escalation
- No confirmed persistence
- No confirmed lateral movement
- No confirmed data exfiltration
- No confirmed malware execution
- Web and SSH timestamps do not establish a single attack chain

---

## 4. Threat Judgment

### LOW

Rejected.

The activity exceeds ordinary low-level suspicious behavior
because repeated authentication attacks and additional
suspicious web activity were observed.

### MEDIUM

Rejected.

The evidence demonstrates a stronger pattern of malicious
activity involving multiple attack behaviors and targeted
accounts.

### HIGH

**SELECTED**

The evidence supports escalation to HIGH because malicious
activity is strongly indicated and includes repeated attempts
against privileged/common accounts.

However, there is insufficient evidence to classify the host
as successfully compromised.

### CRITICAL

Rejected.

There is currently no evidence of successful compromise,
privilege escalation, persistence, lateral movement,
data exfiltration, or widespread impact.

---

## 5. Final Analyst Decision

**HIGH**

The incident should be escalated for additional investigation
and appropriate containment consideration.

The analyst must not describe the host as compromised unless
additional evidence confirms successful intrusion.

---

## 6. Recommended Next Action

Proceed to the BERSERK-IR **Dragonslayer Response** phase.

Potential response actions should be evaluated according to
confidence, asset criticality, and operational impact.

Automated containment should not occur solely because an alert
was classified as HIGH.

---

## 7. Human Validation

The final severity decision belongs to the human analyst.

AI-generated severity recommendations are advisory and must
be reviewed before response actions are executed.

**AI assists. The analyst decides.**
