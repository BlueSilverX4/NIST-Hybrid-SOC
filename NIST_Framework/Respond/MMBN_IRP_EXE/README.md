# MMBN_IRP_EXE (MegaMan Battle Network Incident Response Program)

> **Decoupled Autonomous Incident Response Engine Powered by Gemini AI**

`MMBN_IRP_EXE` is an automated, AI-driven Incident Response (IR) framework inspired by the tactical "Battle Chip" mechanics of *MegaMan Battle Network*. Built around a NetNavi core (`NetNaviCore`), the engine consumes real-time SIEM alert telemetry, leverage Gemini AI reasoning models to synthesize threat intelligence, dynamically selects tactical mitigation chips, and executes host-level remediation and forensic collection sequentially.

---

## 🏛️ System Architecture

[ SIEM Alert Telemetry ]
│
▼
[ NetNavi Core ] ──► (Gemini AI Tactical Reasoning)
│
├──► 1. MemoryDump.EXE  (Gcore / Volatile Memory Dump)
├──► 2. ProcessKill.EXE (Process Termination / SIGKILL)
└──► 3. AirGap.EXE      (Interface Teardown / Quarantine)


---

## 🗡️ Battle Chip Folder (Remediation Library)

| Chip Name | Code | Execution Type | Target Vector | Operation Description |
| :--- | :---: | :---: | :---: | :--- |
| **`MemoryDump.EXE`** | `M` | Forensic | Volatile RAM | Attaches `gcore` to target PID and generates ELF core dump to `./logs/dumps/`. |
| **`ProcessKill.EXE`** | `K` | Host Remediation | Process ID | Transmits `SIGKILL` (`kill -9`) to malicious PID to arrest payload execution. |
| **`AirGap.EXE`** | `A` | Containment | Network Interface | Drops target link (`ip link set <iface> down`) to halt C2 & exfiltration. |

---

## 📸 Incident Response Workflow & Tactical Screenshots

### Phase 01: SIEM Alert Ingestion

**Objective:** Parse raw JSON alert telemetry representing active threat activity on the target host.

![01_siem_alert_ingestion](./docs/screenshots/01_siem_alert_ingestion.png)

* **Ingested Payload:** High-severity Ransomware detection (`Ransomware.LockBit`) on target host `10.0.4.15` bound to PID `$TARGET_PID`.
* **Telemetry Normalization:** NetNavi engine parses threat type, host vector, network interface, and active process ID prior to reasoning.

---

### Phase 02: Gemini AI Tactical Reasoning

**Objective:** Pass normalized telemetry to the Gemini AI reasoning model to dynamically select the optimal Battle Chip combination.

![02_gemini_tactical_reasoning](./docs/screenshots/02_gemini_tactical_reasoning.png)

* **Tactical Synthesis:** AI evaluates threat severity and constructs a sequential mitigation strategy.
* **Chip Folder Queueing:** Queue sequence initialized as `[MemoryDump.EXE] -> [ProcessKill.EXE] -> [AirGap.EXE]`.

---

### Phase 03: Forensic Artifact Generation

**Objective:** Acquire volatile memory dumps of the target process before executing process termination.

![03_forensic_artifacts](./docs/screenshots/03_forensic_artifacts.png)

* **Memory Capture:** `gcore` attaches to PID `$TARGET_PID` and dumps state to `./logs/dumps/proc_mem_<PID>_<TIMESTAMP>.dmp.<PID>`.
* **Process Arrest:** Target process terminated immediately post-capture (`kill -9 $TARGET_PID`).

---

### Phase 04: Host Isolation & Network Containment

**Objective:** Immediately sever active Command & Control (C2) channels and neutralize exfiltration/lateral movement vectors while preserving volatile host state.

![04_airgap_containment](./docs/screenshots/04_airgap_containment.png)

* **Interface Teardown:** Physical/wireless interface (`wlan0` / `eth0`) status set to `DOWN` via `AirGap.EXE`.
* **Quarantine Verification:** Egress test (`ping -c 2 8.8.8.8`) returns `ping: connect: Network is unreachable`, confirming host isolation.

---

## 🚀 Quick Start & Usage

### 1. Prerequisites
* Kali Linux / Ubuntu
* Python 3.10+
* Root/Sudo privileges (required for `gcore` memory dumps and network interface manipulation)

### 2. Installation & Setup
```bash
# Clone repository
git clone [https://github.com/BlueSilverX4/MMBN_IRP_EXE.git](https://github.com/BlueSilverX4/MMBN_IRP_EXE.git)
cd MMBN_IRP_EXE

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
3. Execution
Execute a background target process and feed its PID directly into the NetNavi engine in a single command:

Bash
sleep 600 & sudo ./venv/bin/python main.py $!
🛡️ License
Distributed under the MIT License. See LICENSE for details.


***

