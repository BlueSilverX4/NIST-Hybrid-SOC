#!/usr/bin/env python3
"""
Playbook: TeamStyle Multi-Node Network Pivot Tracking
Framework: Style_Change_Framework
Description: Traces multi-host lateral movement, parses network connection graphs,
             and correlates multi-node pivoting during active incident response.
NIST Mapping: Incident Analysis & Lateral Movement Detection (SP 800-61 / SI-4 Monitoring)
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime

# Configure Structured Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [TeamStyle] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)


class PivotGraphTracker:
    """
    Constructs and analyzes directional pivot paths between network endpoints.
    """
    def __init__(self, initial_patient_zero: str):
        self.patient_zero = initial_patient_zero
        self.nodes = set([initial_patient_zero])
        self.edges = []  # List of tuples: (src_ip, dest_ip, protocol/port)

    def add_pivot_edge(self, src_ip: str, dest_ip: str, protocol: str = "SSH/3389"):
        """
        Records a directional pivot hop between two network nodes.
        """
        self.nodes.add(src_ip)
        self.nodes.add(dest_ip)
        self.edges.append({
            "source": src_ip,
            "destination": dest_ip,
            "protocol": protocol,
            "timestamp": datetime.now().isoformat()
        })
        logging.info(f"Pivot link mapped: {src_ip} ──[{protocol}]──► {dest_ip}")

    def generate_topology_summary(self) -> dict:
        """
        Summarizes the multi-node pivot map into structured telemetry format.
        """
        return {
            "patient_zero": self.patient_zero,
            "total_compromised_nodes": len(self.nodes),
            "node_list": list(self.nodes),
            "pivot_chain_length": len(self.edges),
            "hop_sequence": self.edges
        }


def export_team_telemetry(tracker_summary: dict, output_path: str = None) -> dict:
    """
    Exports TeamStyle multi-node tracking findings into a standardized SOAR artifact.
    """
    artifact = {
        "playbook": "TeamStyle_Pivot_Tracker",
        "domain": "Multi-Node Incident Correlation & Lateral Movement",
        "timestamp": datetime.now().isoformat(),
        "topology": tracker_summary,
        "status": "COMPLETED"
    }

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(artifact, f, indent=2)
        logging.info(f"TeamStyle telemetry exported to: {output_path}")

    return artifact


def main():
    parser = argparse.ArgumentParser(
        description="TeamStyle Playbook - Multi-Node Network Pivot Tracker"
    )
    parser.add_argument("-z", "--patient-zero", default="10.0.0.15", help="Initial weaponized IP node (Patient Zero)")
    parser.add_argument("-p", "--pivots", nargs="+", default=["10.0.0.15->192.168.1.50:SSH", "192.168.1.50->192.168.1.100:RDP"],
                        help="List of pivot hops in format 'SRC->DEST:PROTOCOL'")
    parser.add_argument("--dry-run", action="store_true", help="Simulate graph construction")
    parser.add_argument("-o", "--output", help="Path to export JSON telemetry artifact")

    args = parser.parse_args()

    logging.info(f"Initiating TeamStyle Pivot Tracker. Root Node: {args.patient_zero}")

    tracker = PivotGraphTracker(initial_patient_zero=args.patient_zero)

    # Parse and construct the pivot graph
    for hop in args.pivots:
        try:
            if "->" in hop:
                src_dest, proto = hop.split(":") if ":" in hop else (hop, "TCP")
                src, dest = src_dest.split("->")
                tracker.add_pivot_edge(src.strip(), dest.strip(), protocol=proto.strip())
        except Exception as e:
            logging.error(f"Failed to parse pivot hop pattern '{hop}': {e}")

    # Generate Topology Summary
    summary = tracker.generate_topology_summary()

    # Export Telemetry
    export_team_telemetry(summary, output_path=args.output)

    logging.info("TeamStyle Multi-Node Pivot Tracking Completed Successfully.")


if __name__ == "__main__":
    main()
