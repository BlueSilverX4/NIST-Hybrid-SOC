# Incident Report: Operation Ghost in the Machine
**Investigator:** Brandon Lawrence Gregg
**Date of Investigation:** June 14, 2026
**Target Media:** Physical USB Drive (`/dev/sdb1` mounted at `/media/usb`)

---

## 1. Executive Summary
During a routine forensic sweep of a legacy storage device, an anomalous file named `backdoor.sh` was discovered. Initial inspection revealed deliberate metadata tampering (timestomping) intended to deceive investigators into believing the file was historical system data.

## 2. Evidence Artifact Analysis
The file system metadata was extracted using the `stat` utility. The analysis revealed a critical physical conflict in the timeline:

* **File Birth Time:** June 14, 2026 (Today)
* **File Modification Time:** March 9, 2026 (Forged)

**Conclusion:** The file content claims to have been modified *before* the file was physically created on the disk clusters. This confirms malicious anti-forensics activity (Timestomping).

## 3. Toolset & Methodology Used
* **Foremost:** Successfully carved unallocated space on the raw disk image, recovering older deleted directories (`png`, `zip`, `docx`).
* **Linux Stat Utility:** Utilized to expose kernel-level file system timestamps.
* **dd:** Used to create bit-stream physical media backup images for secure offline analysis.

---
*Screenshots archived in `~/Desktop/Ghost_In_Machine/screenshots/`*
