Operation Heartless: Real-Time SSH Threat Detection & Observability Pipeline

Executive Summary
Engineered an end-to-end detection and log analytics pipeline on bare-metal architecture to detect rapid SSH brute-force authentication attempts in real time. The project integrates custom log generation, stream ingestion, LogQL detection logic, Loki Ruler automated evaluation, and dynamic Grafana telemetry dashboards.

Architecture & Telemetry Ingestion

Log Ingestion: Ingests authentication telemetry streams via Grafana Alloy / Filebeat directly into Grafana Loki.

Indexing & Metadata: Configured stream indexing with labels including job="operation-heartless", target_node, process, and realm for high-cardinality metadata queries.

Storage & Decoupled Architecture: Deployed single-tenant Loki storage backed by local directory structures with decoupled alerting services.

Detection Engineering & LogQL Logic
Developed real-time aggregation queries and Loki Ruler detection rules to identify threshold breaches:

Detection Rule Name: SSHBruteForceAttempt

Severity & Category: Critical | Security

Evaluation Window: 1-minute sliding window ([1m])

Detection Query:

Code snippet
sum by (job, filename) (
  count_over_time(
    {job="operation-heartless"} |= "Failed password" [1m]
  )
) > 3
Alert Logic: Triggers a firing alert whenever a single node experiences more than 3 failed SSH password attempts within 60 seconds.

Testing Strategy & Verification

Rule Endpoint Initialization: Configured /etc/loki/config.yml with native ruler execution and verified deployment via API endpoints (/loki/api/v1/rules).

Telemetry Simulation: Executed automated Bash injection loops appending mock SSH failure streams (sshd[1234]: Failed password for invalid user...) with live system timestamps to validate time-window alignment.

Alert Lifecycle Validation: Verified alert state progression from pending to firing via the Loki Prometheus API (/prometheus/api/v1/alerts).

Dashboard Integration: Created Grafana visualization panels to display threshold breach metrics, log volume spikes, and target account extraction.

Key Artifacts & Deliverables

Loki Ruler Config: /etc/loki/rules/fake/ssh_alerts.yaml

Grafana Dashboards: SSH Authentication Failure Rate (Threshold > 3) panel & real-time log viewer.

Log Evidence: Screen captures and exported raw log JSON archives capturing peak brute-force attempt bursts.
