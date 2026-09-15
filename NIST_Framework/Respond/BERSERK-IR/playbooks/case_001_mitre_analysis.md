# BERSERK-IR — Case 001 MITRE ATT&CK Analysis

## Case

**The Branded Host**

## Primary Indicator

`185.220.101.5`

## Evidence Reviewed

- `auth.log`
- `access.log`

---

## Behavior 1 — SSH Authentication Attempts

### Observed Behavior

The source IP `185.220.101.5` generated four failed SSH
authentication attempts within approximately nine seconds.

The attempts targeted:

- `admin`
- `root`

### Assessment

The behavior is consistent with password guessing / brute-force activity.

### MITRE ATT&CK

**T1110 — Brute Force**

Potential sub-technique:

**T1110.001 — Password Guessing**

### Confidence

HIGH

### Reasoning

Multiple authentication attempts were directed at common or
privileged usernames from the same external source.

No successful SSH authentication from this source was observed
in the available evidence.

---

## Behavior 2 — Web Application Request

### Observed Behavior

The source IP attempted:

`GET /login.php?user=admin' OR 1=1--`

The server returned:

`HTTP 500`

### Assessment

The request contains a SQL injection-style payload.

### MITRE ATT&CK

Potential technique:

**T1190 — Exploit Public-Facing Application**

### Confidence

MEDIUM

### Reasoning

The request appears designed to manipulate a web application's
authentication logic.

However, the available evidence does not demonstrate that the
application was successfully exploited.

---

## Analyst Conclusion

The evidence demonstrates suspicious activity originating from
`185.220.101.5`.

The SSH activity provides strong evidence of password-guessing
behavior.

The web request is consistent with an attempted web application
exploit, but successful exploitation is not established.

The available timestamps do not establish that the SSH and web
events were part of the same continuous attack sequence.

Therefore:

**Malicious activity: CONFIRMED**

**Successful compromise: NOT CONFIRMED**

**Unified attack chain: NOT ESTABLISHED**

---

## Human Validation

MITRE classifications must be reviewed and validated by a human
analyst before being treated as confirmed findings.
