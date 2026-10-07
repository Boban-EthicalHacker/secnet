# -*- coding: utf-8 -*-

"""
Export module.

Serializes scan results to JSON.
"""

import json
from datetime import datetime


def build_report(
    host: str,
    target_info: dict | None,
    scan_type: str,
    results: list[tuple[int, str, str]],
) -> dict:
    """
    Build a report dictionary from a scan.

    results: list of (port, service, banner) tuples.
    """
    return {
        "tool": "secnet",
        "version": "0.1.0",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "scan_type": scan_type,
        "target": {
            "host": host,
            "info": target_info or {},
        },
        "results": [
            {
                "port": port,
                "state": "open",
                "service": service or None,
                "banner": banner or None,
            }
            for port, service, banner in results
        ],
        "summary": {
            "open_ports": len(results),
        },
    }


def default_filename(host: str, scan_type: str) -> str:
    """
    Return a default filename for the report.
    """
    safe_host = host.replace("/", "_").replace(":", "_")
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"secnet-{scan_type}-{safe_host}-{ts}.json"


def save_report(report: dict, path: str) -> None:
    """
    Write the report to a JSON file.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)