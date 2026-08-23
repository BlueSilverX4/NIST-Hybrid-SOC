# Threat Model: Operation Heartless

## Asset Mapping & Definitions

| Lore Entity | SOC / Network Equivalent | Technical Function |
| :--- | :--- | :--- |
| **Kingdom Hearts** | Primary Domain Controller / Database | High-value target containing root authority data. |
| **Heartless** | Unauthenticated External Threat / Malware | Malicious activity attempting to consume system resources. |
| **Nobodies** | Phantom Processes / Persistence Mechanisms | Leftover background services executing without a valid user context. |
| **Corridor of Darkness** | Rogue Tunnel / Unencrypted Reverse Shell | Unauthorized ingress/egress channel bypassing perimeter firewalls. |
| **Keyblade** | Authentication Token / YubiKey | Cryptographic key used to lock/unlock systemic access. |

## Alert Severity Levels

* **Shadow Class (Low):** Repeated port scans or minor authentication failures.
* **Neoshadow Class (Medium):** Unauthorized service creation or suspicious script execution.
* **Darkside Class (Critical):** Domain-level privilege escalation or active credential dumping.
