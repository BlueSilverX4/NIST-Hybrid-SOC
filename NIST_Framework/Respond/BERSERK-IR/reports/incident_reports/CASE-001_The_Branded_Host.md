# BERSERK-IR Incident Report

## Case 001 — The Branded Host

**Incident ID:** BERSERK-001

**Status:** Investigating / Contained Monitoring

**Severity:** HIGH

**Confidence:** HIGH

**Date of Investigation:** August 2026

**Primary Indicator:** `185.220.101.5`

---

# 1. Executive Summary

BERSERK-IR identified suspicious activity originating from
`185.220.101.5`.

The source generated multiple failed SSH authentication
attempts against the `admin` and `root` accounts.

The same source IP also appeared in web telemetry associated
with an attempted `/etc/passwd` request and a SQL-injection-style
request against a login endpoint.

The available evidence confirms malicious activity but does
not establish successful compromise.

The available timestamps also do not establish that the SSH
and web events were part of one continuous attack sequence.

The incident was therefore classified as HIGH severity with
successful compromise remaining unconfirmed.

---

# 2. Detection

The initial detection was based on authentication telemetry.

Observed SSH activity included four failed authentication
attempts from:

`185.220.101.5`

Targeted accounts:

- `admin`
- `root`

The attempts occurred within approximately nine seconds.

---

# 3. Investigation

## Authentication Evidence

The following behavior was observed:

- Failed password for invalid user `admin`
- Failed password for invalid user `admin`
- Failed password for `root`
- Failed password for `root`

No successful authentication from the suspicious source was
identified in the available authentication evidence.

---

## Web Evidence

The source IP was also observed in web telemetry.

Observed requests included:

`GET /etc/passwd`

Response:

`HTTP 403`

And:

`GET /login.php?user=admin' OR 1=1--`

Response:

`HTTP 500`

The second request contains a SQL-injection-style payload.

Successful exploitation was not established.

---

# 4. Timeline Analysis

The web access log records timestamps in UTC.

The Kali workstation uses:

`America/New_York`

`EDT (UTC-4)`

The web events therefore occurred approximately:

- 06:01:05 EDT
- 06:01:10 EDT

The SSH log entries do not contain an explicit timezone.

If interpreted as local system time, they occurred approximately:

- 08:14:22 EDT
- 08:14:25 EDT
- 08:14:28 EDT
- 08:14:31 EDT

Because the available evidence does not provide sufficient
timestamp normalization for all events, a single continuous
attack chain cannot be established.

---

# 5. MITRE ATT&CK Mapping

## T1110 — Brute Force

Potential sub-technique:

**T1110.001 — Password Guessing**

Confidence:

**HIGH**

Reason:

Repeated SSH authentication attempts targeted common and
privileged usernames.

---

## T1190 — Exploit Public-Facing Application

Confidence:

**MEDIUM**

Reason:

The web request contains a SQL-injection-style payload
targeting an application login endpoint.

Successful exploitation was not demonstrated.

---

# 6. Threat Judgment

## Severity

**HIGH**

## Confidence

**HIGH**

## Malicious Activity

**CONFIRMED**

## Successful Compromise

**NOT CONFIRMED**

## Unified Attack Chain

**NOT ESTABLISHED**

---

# 7. Response

The recommended response state is:

**MONITOR + INVESTIGATE + PREPARE CONTAINMENT**

Recommended actions include:

- Preserve relevant evidence
- Monitor the suspicious source
- Review authentication activity
- Review web activity
- Prepare network containment
- Escalate if successful authentication or additional
  compromise indicators appear

High-impact containment actions require human approval.

---

# 8. Evidence Preservation

Relevant evidence includes:

- `auth.log`
- `access.log`
- System time configuration
- Authentication telemetry
- Web telemetry
- Investigation screenshots
- MITRE analysis
- Threat judgment
- Response playbook

Original evidence should not be modified during investigation.

---

# 9. Lessons Learned

The investigation demonstrated several important SOC principles:

1. A suspicious IP appearing in multiple logs does not
   automatically establish one attack chain.

2. Timestamps must be normalized before establishing causality.

3. Malicious activity does not necessarily mean successful
   compromise.

4. Severity and confidence are separate decisions.

5. MITRE ATT&CK mappings require analyst validation.

6. AI-generated security recommendations should remain
   advisory until validated by a human analyst.

---

# 10. Final Assessment

BERSERK-IR identified and investigated suspicious activity
associated with `185.220.101.5`.

The strongest evidence supports SSH password-guessing
behavior.

Additional web activity indicates possible attempted
application exploitation.

No evidence currently confirms successful compromise.

The incident remains HIGH severity and should continue through
the appropriate monitoring, investigation, and containment
workflow.

---

# Analyst Principle

> **AI assists. Evidence decides. The analyst validates.**

**BERSERK-IR — Case 001 Complete Investigation Record**
