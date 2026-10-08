# ⚙️ Operation D-Brigade: Metal Empire SOC & Threat Defense Architecture

An enterprise-inspired **Security Operations Center (SOC) home lab** modeled after the **D-Brigade tactical unit from Digimon Metal Empire**.

Operation D-Brigade combines **endpoint telemetry, perimeter defense, centralized security logging, automated threat containment, and orchestration** into a unified Linux security architecture aligned with the **NIST Cybersecurity Framework (CSF)**.

The project focuses on three primary NIST functions:

- 🛡️ **PROTECT** — Harden endpoints and enforce perimeter controls.
- 🔎 **DETECT** — Centralize and monitor security telemetry.
- ⚔️ **RESPOND** — Automatically contain identified threats.

---

## 🧭 Architecture & NIST Framework Mapping

```text
                         ┌──────────────────────────────────────┐
                         │       BRIGADRAMON                    │
                         │       Command & Fleet                │
                         │                                      │
                         │  NIST: DETECT (DE.CM-01)             │
                         │  Rsyslog Central Telemetry Router    │
                         │  Dedicated C2 Log Stream             │
                         │  /var/log/brigadramon-c2.log        │
                         └──────────────────┬───────────────────┘
                                            │
             ┌──────────────────────────────┼──────────────────────────────┐
             │                              │                              │
             ▼                              ▼                              ▼
┌────────────────────────┐    ┌────────────────────────┐    ┌────────────────────────┐
│     COMMANDRAMON       │    │      GUARDROMON         │    │      MEGADRAMON        │
│     Host Endpoints     │───▶│    Perimeter Defense    │───▶│    SOAR Response       │
│                        │    │                        │    │                        │
│ NIST: PROTECT          │    │ NIST: PROTECT          │    │ NIST: RESPOND          │
│ Sysmon / Auditd        │    │ iptables / NIPS        │    │ Python SOAR Engine     │
│ Host Telemetry         │    │ Boundary Enforcement   │    │ Dynamic IP Blocking    │
└────────────────────────┘    └────────────────────────┘    └────────────────────────┘
```

---

## 🔄 Defensive Workflow

```text
Endpoint Activity
       │
       ▼
Commandramon
(Sysmon / Auditd)
       │
       ▼
Guardromon
(iptables Perimeter Defense)
       │
       ▼
Brigadramon
(Rsyslog Central Telemetry)
       │
       ▼
Megadramon
(Python SOAR Engine)
       │
       ▼
Dynamic Threat Containment
(iptables IP Drop)
```

---

## 🛡️ Component Roles

| Component | NIST Function | Tactical Role | Security Stack | Key Responsibilities |
|---|---|---|---|---|
| **Commandramon** | PROTECT | Lightweight Endpoint Sensor | Sysmon XML / Auditd Rules | Collects host telemetry, process activity, and socket connections. |
| **Guardromon** | PROTECT | Perimeter Fortification | iptables Baseline Script | Enforces host perimeter defense, establishes firewall policy, and identifies unauthorized probes. |
| **Brigadramon** | DETECT | Central Command / Telemetry Router | Rsyslog | Routes `[GUARDROMON-DROP]` events into a dedicated C2 log stream for centralized analysis. |
| **Megadramon** | RESPOND | Rapid Threat Containment | Python SOAR Engine | Parses telemetry and dynamically injects iptables DROP rules against identified offensive IPs. |

---

# 📁 Repository Structure

```text
operation-d-brigade/
├── start-d-brigade.sh
│   └── Master Pipeline Orchestrator
│
├── README.md
│   └── Documentation & Architecture
│
├── brigadramon-c2/
│   ├── 50-brigadramon.conf
│   │   └── Rsyslog rule filter
│   │
│   └── deploy-c2-logging.sh
│       └── C2 log isolation setup script
│
├── commandramon-endpoints/
│   ├── auditd-commandramon.rules
│   │   └── Linux security auditing baseline
│   │
│   └── sysmon-config.xml
│       └── Sysmon event configuration
│
├── guardromon-perimeter/
│   └── guardromon-firewall.sh
│       └── iptables perimeter-defense baseline
│
├── megadramon-soar/
│   └── megadramon_soar.py
│       └── Dynamic IP-blocking SOAR engine
│
└── docs/
    └── screenshots/
        ├── 01-folder_structure.png
        ├── 02-guardromon-and-megadramon-active.png
        ├── 03-start-operation-d-brigade-defense-grid.png
        └── 04-deploy-d-brigade-logs.png
```

---

# 🚀 Deployment & Usage

## 1. Initialize Central Telemetry

```bash
cd brigadramon-c2
chmod +x deploy-c2-logging.sh
sudo ./deploy-c2-logging.sh
```

This establishes the dedicated Brigadramon telemetry path used to collect and monitor security events.

---

## 2. Launch the Defense Grid

```bash
cd ..
sudo ./start-d-brigade.sh
```

The master script initializes the D-Brigade defensive components.

---

## 3. Monitor Live C2 Telemetry

```bash
tail -f /var/log/brigadramon-c2.log
```

This provides a live view of events routed through the central telemetry layer.

---

# 🧠 NIST CSF Alignment

| NIST Function | D-Brigade Implementation |
|---|---|
| **PROTECT** | Commandramon endpoint telemetry and Guardromon perimeter controls |
| **DETECT** | Brigadramon centralized Rsyslog telemetry |
| **RESPOND** | Megadramon automated IP containment |

---

## ⚔️ 4. Respond (RS)

**Operation D-Brigade** serves as the **Respond (RS)** implementation within the broader NIST-aligned portfolio.

> **Operation D-Brigade — Automated SOAR & Incident Response Pipeline**

### Tactical Focus

The Respond layer focuses on:

- **Real-time log monitoring** using `rsyslog`
- **Custom SOAR automation** using Python
- **Dynamic IP containment** using `iptables`

### Response Components

| Component | Role |
|---|---|
| **Commandramon** | Endpoint Sensors |
| **Guardromon** | Perimeter Firewall |
| **Megadramon** | Automated SOAR Engine |
| **Brigadramon** | Central Telemetry Router |

### Respond Workflow

```text
Security Event
      │
      ▼
Commandramon
Endpoint Sensors
      │
      ▼
Guardromon
Perimeter Firewall
      │
      ▼
Brigadramon
Central Telemetry Router
      │
      ▼
Megadramon
Automated SOAR Engine
      │
      ▼
iptables
Dynamic IP Containment
```

The implementation demonstrates a closed defensive loop in which security telemetry can progress from **endpoint observation → centralized detection → automated response → network containment**.

---

# 📸 Execution Evidence

The repository includes screenshots documenting the deployment and verification process:

| Evidence | Purpose |
|---|---|
| `01-folder_structure.png` | Repository and module structure |
| `02-guardromon-and-megadramon-active.png` | Firewall and SOAR components running |
| `03-start-operation-d-brigade-defense-grid.png` | Master orchestration startup |
| `04-deploy-d-brigade-logs.png` | Centralized telemetry deployment and verification |

These artifacts provide visual evidence of the implementation rather than relying solely on configuration files.

---

# 🎯 Project Objectives

Operation D-Brigade was designed to demonstrate:

- Centralized Linux security telemetry
- Endpoint monitoring
- Host-based perimeter defense
- Automated threat containment
- Rsyslog-based event routing
- Python-based SOAR automation
- iptables enforcement
- NIST CSF-aligned defensive architecture
- Separation of **visibility, detection, and response**

---

# 🏁 Portfolio Takeaway

**Operation D-Brigade** demonstrates a complete defensive workflow built around a lightweight Linux SOC architecture:

```text
COLLECT
  ↓
Commandramon
  ↓
ENFORCE
  ↓
Guardromon
  ↓
DETECT
  ↓
Brigadramon
  ↓
RESPOND
  ↓
Megadramon
  ↓
CONTAIN
```

Rather than treating security tooling as isolated components, the project connects endpoint visibility, perimeter enforcement, centralized telemetry, and automated response into a single operational pipeline.

> **Detect the threat. Contain the threat. Preserve the telemetry.**
>
> — Operation D-Brigade

