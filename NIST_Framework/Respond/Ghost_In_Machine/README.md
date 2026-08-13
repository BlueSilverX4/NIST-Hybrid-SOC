# 👻 Operation: Ghost in the Machine

## Host-Based Digital Forensics & Anti-Forensics Threat Hunt

## 🎯 Objective

**Operation Ghost in the Machine** demonstrates an end-to-end host-based forensic investigation performed on physical storage media using **Kali Purple**.

The investigation simulates an insider-threat scenario in which an adversary deploys a malicious payload and attempts to conceal their activity through **timestomping**.

The objective was to:

* Preserve digital evidence
* Recover deleted artifacts
* Inspect filesystem metadata
* Identify timeline inconsistencies
* Detect evidence of anti-forensics activity
* Document the resulting indicators of compromise

---

# 🛠️ Toolset & Environment

| Component                | Purpose                            |
| ------------------------ | ---------------------------------- |
| **Kali Purple**          | Forensic investigation environment |
| **Physical USB Storage** | Target evidence media              |
| **`dd`**                 | Forensic disk imaging              |
| **Foremost**             | File carving and artifact recovery |
| **`stat`**               | Filesystem metadata inspection     |
| **`sha256sum`**          | Evidence integrity verification    |

Target media was mounted at:

```text id="j3b0af"
/media/usb
```

---

# 📑 Phase 1 — Storage Preservation & Data Carving

Before conducting the investigation, a bit-stream forensic image of the physical media was created.

The purpose of imaging the media first was to preserve the available evidence, including potentially recoverable data within unallocated space.

### Forensic Imaging

```bash id="3t3czz"
sudo dd \
  if=/dev/sdb1 \
  of=~/Desktop/Ghost_In_Machine/evidence/usb_hunt.img \
  bs=4M \
  status=progress
```

The resulting image provided a working forensic copy for subsequent analysis.

---

## File Carving

**Foremost** was used to perform binary signature-based recovery against the forensic image.

The investigation successfully recovered historical artifacts representing multiple file types, including:

```text id="b7h0qi"
.exe
.pdf
.png
.zip
.docx
```

The recovered artifacts demonstrated that historical file data remained recoverable from the storage media despite deletion from the active filesystem structure.

---

# 📑 Phase 2 — Threat Simulation

## Timestomp Attack

An adversary footprint was simulated by deploying a stealth execution script:

```text id="qqkhm8"
backdoor.sh
```

The file's modification timestamp was then manipulated to create a false historical timeline.

```bash id="0q0l9x"
sudo touch -d "2026-03-09 14:30:00" /media/usb/backdoor.sh
```

The objective was to make the file appear to have been modified months earlier than its actual creation timeframe.

---

# 📑 Phase 3 — Threat Hunt

## Timeline Anomaly Discovery

Filesystem metadata was examined using the Linux `stat` utility.

The investigation identified a significant chronological discrepancy:

| Metadata                        | Observed Value        |
| ------------------------------- | --------------------- |
| **Modification Time (`mtime`)** | `2026-03-09 14:30:00` |
| **Birth Time (`btime`)**        | `2026-06-14 07:29:35` |

---

## 🚨 The Forensic Catch

The modified timestamp predates the recorded filesystem birth timestamp.

This created a **timeline anomaly**:

```text id="4glcqc"
2026-03-09
     │
     │  Modified timestamp
     ▼
   mtime
     
     ...

2026-06-14
     │
     │  Recorded creation/birth time
     ▼
   btime
```

Because the modification timestamp had been deliberately altered, the discrepancy between `mtime` and `btime` provided a strong forensic indicator that the file's timeline had been manipulated.

This demonstrated how anti-forensics techniques can be exposed by correlating multiple filesystem metadata attributes rather than relying on a single timestamp.

---

# 🔎 Investigation Methodology

```text id="l6w7jy"
Physical Storage
      │
      ▼
Forensic Image
      │
      ▼
File Carving
      │
      ▼
Recovered Artifacts
      │
      ▼
Metadata Inspection
      │
      ▼
Timeline Correlation
      │
      ▼
Timestamp Anomaly
      │
      ▼
Anti-Forensics Indicator
```

---

# 📈 Key Takeaways for SOC Operations

## 1. Never Trust a Single Timestamp

Basic filesystem listings can present timestamps that have been intentionally manipulated.

Investigators should correlate multiple available metadata attributes when reconstructing an event timeline.

---

## 2. Correlate Filesystem Metadata

The investigation demonstrates the value of examining attributes such as:

* `mtime`
* `btime`
* Other available filesystem metadata
* Change-history sources where available

A discrepancy between independently maintained timestamps can provide an important indicator for further investigation.

---

## 3. Preserve Evidence Before Investigation

Creating a forensic image before performing structural analysis helps preserve the original evidence and reduces the risk of modifying recoverable artifacts.

The investigation therefore followed a preservation-first workflow:

```text id="b5d3dy"
Original Media
      │
      ▼
Forensic Image
      │
      ▼
Investigation Copy
      │
      ├── File Carving
      ├── Metadata Analysis
      └── Timeline Investigation
```

---

# 🛡️ NIST CSF Alignment

## Respond (RS)

The project supports the Respond function through:

* Forensic investigation
* Incident characterization
* Evidence preservation
* Artifact recovery
* Anti-forensics identification
* Timeline reconstruction

The investigation demonstrates how forensic evidence can be used to characterize suspicious activity after an incident has been identified.

---

# 🧪 Evidence & Validation

The investigation preserved:

* Forensic disk image
* Recovered file artifacts
* Filesystem metadata
* Timeline analysis
* Audit information
* Terminal evidence
* Investigation screenshots

All analytical evidence, audit logs, and system screenshots are preserved locally within the repository structure.

---

# 🧠 Skills Demonstrated

Operation Ghost in the Machine demonstrates practical experience with:

* Digital forensics
* Host-based investigation
* Evidence preservation
* Forensic imaging
* File carving
* Filesystem metadata analysis
* Timeline reconstruction
* Anti-forensics detection
* Timestomp analysis
* Linux command-line investigation
* Evidence integrity
* Incident response
