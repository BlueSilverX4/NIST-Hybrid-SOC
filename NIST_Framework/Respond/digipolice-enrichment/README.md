# Digipolice Enrichment Pipeline (NIST CSF: Respond)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![NIST CSF v2.0](https://img.shields.io/badge/NIST%20CSF%20v2.0-Respond%20%28RS.AN%29-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

An automated Security Operations Center (SOC) triage and enrichment tool designed to process raw security alerts, extract Indicators of Compromise (IoCs), and enrich them using OSINT threat intelligence feeds (VirusTotal, AbuseIPDB, and CISA Known Exploited Vulnerabilities).

This project automates the initial incident analysis workflow, transforming raw JSON alert payloads into structured, actionable Markdown triage reports for SOC analysts.

---

## 🎯 NIST Cybersecurity Framework Alignment

This repository maps directly to the **Respond (RS)** core function of the NIST CSF v2.0 framework:

* **Primary Category — Incident Analysis (RS.AN):** Automates IoC extraction, threat intelligence correlation, and context aggregation to determine alert severity and scope.
* **Secondary Category — Incident Reporting & Communication (RS.CO):** Generates standardized, human-readable markdown triage reports (`triage_report.md`) for immediate situational awareness and escalation.

---

## 🏗️ Project Architecture

The pipeline follows a modular structure to enforce clear separation of concerns across extraction, enrichment, vulnerability check, and report generation:

```text
digipolice-enrichment/
├── config/
│   └── cisa_kev.json          # Local cached fallback catalog for CISA KEV
├── input/
│   └── sample_alert.json      # Raw security alert payload
├── output/
│   └── reports/
│       └── triage_report.md   # Generated Markdown triage output
├── screenshots/               # Execution verification & proof of concept
│   ├── execution/
│   ├── api_queries/
│   └── osint_verification/
├── src/
│   ├── extractors.py          # Regex/parsing logic for IPs, hashes, domains
│   ├── enrichers.py           # VirusTotal & AbuseIPDB API client logic
│   ├── kev.py                 # CISA KEV lookup engine & synchronization
│   └── reporter.py            # Markdown report builder & main entrypoint
├── tests/
│   └── test_extractors.py     # Unit testing suite
├── .gitignore
├── requirements.txt
└── README.md
