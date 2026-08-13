# Forensic Data Remanence & Block-Level Sanitization Lab

An advanced defensive security and anti-forensics laboratory demonstrating the limitations of user-space file deletions and the implementation of raw hardware block sterilization.

---

## 🎯 Project Overview
This repository serves as a practical security engineering study on **data-at-rest sanitization**. In this lab, standard user-space file deletions were forensically evaluated via raw bitstream carving. When file fragments were discovered leaking within unallocated disk space due to environmental shell caching, a hardware-level defensive remediation strategy was executed to completely sterile the media device.

###  📊 Final Lab Audit Metric

| Phase | Operation | Forensic Target Signature Visibility | Asset Status |
| :--- | :--- | :--- | :--- |
| **Baseline** | File-Level Creation | **100% Exposed** (Plaintext visibility) | Active Deployment |
| **Phase I** | User-Space `shred` / Deletion | **100% Leaked** (Orphaned in unallocated blocks) | Vulnerable |
| **Phase II** | Raw Partition Block-Level Overwrite | **0% Remanence** (Absolute Radio Silence) | Forensically Sterile |

#### 🛠️ Core Skills Demonstrated
* **Low-Level Storage Forensics:** Direct bitstream parsing using binary scrapers to carve unallocated memory clusters.
* **Kernel & Storage Architecture Management:** Troubleshooting driver path locking states (`target is busy`) and managing dynamic device node reassignments (`/dev/sdb` -> `/dev/sdc`).
* **Anti-Forensics & Data Destruction:** Implementing sequential, pseudo-random block device writes via `shred` to eliminate file signature markers.
* **Security Automation:** Developing Bash utilities to handle automated, defensive sanitization and post-wipe validation auditing.

---

##### 📁 Repository Directory Map
* **`docs/`**: Contains the full, exhaustive [Technical Lab Report](docs/lab-report.md) detailing the complete remediation cycle, root-cause analysis, and step-by-step methodologies.
* **`scripts/`**: Holds custom administrative Bash automation tools:
  * `secure_wipe.sh`: Automatically isolates targeted devices, forces lazy unmounts on busy processes, and scrambles the block layer.
  * `backup_audit.sh`: Automatically extracts string patterns and checks device compliance against critical data leak regex signatures.
* **`assets/terminal-captures/`**: Stores physical image evidence verifying the 100% successful block wipe progress and the final sterile validation queries.

---

###### 🚀 Quick Start: Running the Automation Scripts

To execute the defensive tools developed in this lab, clone this repository, move into the workspace, and grant execution permissions:

```bash
git clone [https://github.com/YOUR_USERNAME/data-remanence-forensics-lab.git](https://github.com/YOUR_USERNAME/data-remanence-forensics-lab.git)
cd data-remanence-forensics-lab
chmod +x scripts/*.sh
