# **Technical Lab Report: Data Remanence, Forensic Carving, and Block-Level Sanitization**

**Prepared By:** Brandon Lawrence Gregg

**Project Category:** Digital Forensics & Defensive Security Engineering

---

## **1\. Executive Summary**

This laboratory exercise demonstrates the structural limitations of user-space file deletions and evaluates the efficacy of low-level anti-forensics sanitization techniques. The objective was to track a simulated sensitive data leak within unallocated disk space, diagnose system-level errors during the remediation process, and verify total data destruction at the physical storage layer. Final forensic auditing confirmed 100% compliance with a zero-residual data framework.

---

## **2\. Environment & Asset Mapping**

* **Host Operating System:** Linux (Kernel: Architecture-independent shell environment)  
* **Target Hardware Asset:** 4.0 GB (3.7 GiB effective) USB Mass Storage Block Device  
* **Dynamic Device Nodes:** Reassigned sequentially from `/dev/sdb` to `/dev/sdc` during hardware lifecycle phases.  
* **Target Partition Environment:** `/dev/sdc1` (Initially mapped to `/run/media/brandongregg/901B-E5F3`)

---

## **3\. Phase I: The Forensic Leak & Signature Discovery**

To simulate an active data leakage scenario, a configuration string containing target forensic markers was committed to the storage media:

Bash  
echo "Testing for Recover training for Cyber Security,,,Sorry NO CIA secrets HA\!" \> Sensitive\_Data.txt

### **The Mechanism of Data Remanence**

When a file is modified or an unclosed multiline shell string buffer gets aborted by the interpreter, data fragments are immediately orphaned into unallocated storage sectors. Standard operating systems merely delete the high-level pointer referencing the file in the file allocation table; the raw binary characters remain fully intact on the hardware platter or flash geometry.

### **Forensic Auditing Technique**

To mirror an adversary or forensic investigator carving an unallocated disk layout, a raw bitstream scrape was executed against the physical storage blocks using the `strings` utility to pipe printable sequences to a local audit file:

Bash  
sudo strings /dev/sdc1 \> /home/brandongregg/Desktop/Pre\_Wipe\_Audit.txt

Querying the text dump using strict regular expression matches revealed a critical security exposure:

Bash  
grep \-i "CIA secrets" /home/brandongregg/Desktop/Pre\_Wipe\_Audit.txt

**Output:** `tTesting for Recover training for Cyber Security,,,Sorry NO CIA secrets HA!`

The audit confirmed that signature-matching carving utilities (such as *Foremost* or *Scalpel*) could easily reconstruct files because the magic bytes and character streams remained entirely active in unallocated sectors.

---

## **4\. Phase II: The Fallacy of File-Path Shredding**

An initial attempt was made to sanitize the risk by executing a standard user-space overwrite tool directly against the apparent active file path:

Bash  
shred \-u \-v \-n 3 Sensitive\_Data.txt

### **The Root Cause of Failure**

While the utility reported a successful 3-pass overwrite sequence, subsequent forensic `strings` scrapes revealed the target markers **still survived** on the drive.

File-path utilities are inherently blind to orphaned blocks because they rely on active file-system indexes to find targets. Because previous runtime errors and text caches had already left duplicated fragments floating in unallocated disk space, the high-level application path tool could not reach or overwrite them.

---

## **5\. Phase III: Engineering System Obstacles & Troubleshooting**

### **Incident A: File-System Locking ("Target is Busy")**

When attempting to decouple the logical mount point using `sudo umount /dev/sdc1`, the Linux kernel rejected the command: `umount: /run/media/brandongregg/901B-E5F3: target is busy.`

* **Root Cause Analysis:** High-level applications (such as the *Thunar* graphical file manager) and environmental shell sessions held open file descriptors pointing inside the mount tree, creating a kernel lock to maintain data stability.  
* **Remediation Strategy:** A lazy unmount flag was executed to immediately isolate the directory tree from the operating system, severing application hooks:  
* Bash

sudo umount \-l /dev/sdc1

*   
* 

### **Incident B: Dynamic Kernel Device Node Reassignment**

Following block-level manipulation, the command `sudo mkfs.vfat /dev/sdb1` threw a terminal error: `mkfs.vfat: unable to open /dev/sdb1: No such file or directory`

* **Root Cause Analysis:** Low-level sanitization permanently scrambled the Master Boot Record (MBR) and Partition Tables. Upon processing this structural wipe, the Linux hotplug subsystem automatically dropped the stale `/dev/sdb` handle and dynamically remapped the physical USB interface to the hardware node tree as **`/dev/sdc`**.  
* **Remediation Strategy:** The storage architecture was evaluated using the block layer identification utility:  
* Bash

lsblk

*   
* The layout clearly exposed the shift to `/dev/sdc`, allowing subsequent management commands to target the correct device address without further incident.

---

## **6\. Phase IV: Raw Block Overwrite & Final Forensic Audit**

To force complete data destruction across all sectors regardless of file system status, a raw, low-level sequential write was broadcast directly across the master block architecture:

Bash  
sudo shred \-v \-n 1 /dev/sdc1

### **Verification Methodology**

The hardware partition was thoroughly rescanned, and a final forensic bitstream capture file was dumped onto the local desktop workspace:

Bash  
sudo strings /dev/sdc1 \> /home/brandongregg/Desktop/Post\_Block\_Wipe\_Strings.txt

Targeted search queries were run against the final binary scrape:

Bash  
grep \-i "CIA secrets" /home/brandongregg/Desktop/Post\_Block\_Wipe\_Strings.txt  
grep \-i "Sensitive\_Data" /home/brandongregg/Desktop/Post\_Block\_Wipe\_Strings.txt

### **Forensic Result**

Both queries returned **absolute radio silence** (exit status 0, zero lines printed). This conclusively proves that every raw sector from the first geometric address to the final cluster limit has been successfully sterilized. Automated signature carving tools are now completely neutralized.

---

## **7\. Operational Asset Restoration**

Because a block-level wipe strips a device of all partition architecture, the drive must be re-indexed before it can be redeployed into production. To make the physical USB device safe and functional for general storage deployment, a clean, cross-platform file allocation layout was laid down:

Bash  
sudo mkfs.vfat \-F 32 \-n "SECURE\_USB" /dev/sdc1

---

## **8\. Conclusion & Lab Takeaways**

1. **File Deletion vs. Block-Level Sanitization:** File-level paths only clear active pointers. To secure an enterprise asset against data recovery, the underlying raw partition geometries must be explicitly targeted.  
2. **Defensive Documentation Value:** Understanding the interaction between kernel file descriptors, dynamic device block lettering (`sda` \-\> `sdb` \-\> `sdc`), and data remanence provides a critical foundational skill set for building reliable corporate sanitization workflows.

