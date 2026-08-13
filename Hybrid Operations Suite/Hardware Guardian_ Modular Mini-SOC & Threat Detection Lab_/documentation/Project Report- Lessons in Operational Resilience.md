Project Report: Lessons in Operational Resilience
Project: Hardware Guardian Mini-SOC
Analyst: Brandon Lawrence Gregg
I. Strategic Overview
The primary lesson of this project was Resource Management. Building a SOC on an HP
Pavilion 23 required a shift from "default installation" to "bespoke configuration." In
cybersecurity, you rarely have unlimited resources; learning to optimize what is available is a
critical Blue Team skill.
II. Technical Transitions
From Personal Shopping to SOC Analyst: My previous career required managing complex
inventory and rapid problem-solving. I applied these "logistics" skills to data packets and system
logs. Ensuring a log moves from a file to a dashboard is identical to ensuring a high-value item
moves from a shelf to a client—integrity and timing are everything.
The Importance of "Green" Status: I learned that a service being "active" does not mean it is
"functional." The auditd module error taught me to look beyond the surface level of systemctl
status and dive into raw logs to find the "silent" failures.
III. Core Competencies Gained
System Optimization: Learned to balance JVM heap sizes against system swap space to
prevent kernel panics.
Data Persistence: Successfully managed Elasticsearch indices to ensure May 14th logs were
searchable and visualized.
Pipeline Troubleshooting: Mastered the relationship between a log harvester (Filebeat), a
database (Elasticsearch), and a visualizer (Grafana).
IV. Final Conclusion
The Hardware Guardian project is proof that security visibility is possible on any hardware if the
analyst understands the underlying architecture. This lab now stands as a verified "Proof of
Concept" for small-scale, high-efficiency threat detection.


