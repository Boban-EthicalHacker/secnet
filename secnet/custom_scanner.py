# -*- coding: utf-8 -*-

"""
Custom port scanner module.

Scans a user-defined port, list, or range on a single target.
Reuses scan_port and COMMON_PORTS from scanner.py.
"""

import asyncio

from .scanner import (
    COMMON_PORTS,
    PORT_SETS,
    DEFAULT_TIMEOUT,
    collect_target_info,
    scan_ports_parallel,
)
from .export import build_report, save_report, default_filename


def parse_ports(spec: str) -> list[int]:
    """
    Parse a port specification string into a list of ports.

    Accepts:
        Numbers:      "80"          -> [80]
        Lists:        "22,80,443"   -> [22, 80, 443]
        Ranges:       "1-1024"      -> [1, 2, ..., 1024]
        Named sets:   "web"         -> [80, 443, 8000, 8080, 8443, 8888]
        Combination:  "web,22,100-200"

    Raises ValueError on invalid input.
    """
    ports: set[int] = set()

    for chunk in spec.split(","):
        chunk = chunk.strip().lower()
        if not chunk:
            continue

        # Именовани сет, нпр. "web" или "db"
        if chunk in PORT_SETS:
            ports.update(PORT_SETS[chunk])
            continue

        # Опсег портова, нпр. 1-1024
        if "-" in chunk:
            start_s, end_s = chunk.split("-", 1)
            start, end = int(start_s), int(end_s)
            if not (0 < start <= 65535 and 0 < end <= 65535):
                raise ValueError(f"Port out of range: {chunk}")
            if start > end:
                start, end = end, start
            ports.update(range(start, end + 1))
        else:
            # Појединачна порт
            try:
                port = int(chunk)
            except ValueError:
                # Није број и није именовани сет — пријављујемо
                names = ", ".join(PORT_SETS.keys())
                raise ValueError(
                    f"Unknown port or set: '{chunk}'. "
                    f"Named sets: {names}"
                )
            if not (0 < port <= 65535):
                raise ValueError(f"Port out of range: {port}")
            ports.add(port)

    return sorted(ports)


async def scan_custom(
    host: str, ports: list[int], timeout: float
) -> list[tuple[int, str, str]]:
    """
    Scan a user-defined list of ports on a single host, in parallel.

    Returns a list of (port, service, banner) tuples for open ports.
    """
    from .colors import info, success

    total = len(ports)
    print(info(f"\n[*] Scanning {host} ({total} custom ports, timeout={timeout}s)"))

    # Покрећемо паралелно скенирање
    raw_results = await scan_ports_parallel(host, ports, timeout)

    # Додајемо име сервиса из COMMON_PORTS (ако постоји)
    results: list[tuple[int, str, str]] = []
    for port, banner in raw_results:
        service = COMMON_PORTS.get(port, "")
        results.append((port, service, banner))

    # Исписујемо резултате
    for port, service, banner in results:
        label = f"   ({service})" if service else ""
        if banner:
            print(success(f"[+] {host}:{port:<5} open{label}") + f" -> {banner}")
        else:
            print(success(f"[+] {host}:{port:<5} open{label}"))

    print(info(f"\n[*] Done. {len(results)} open port(s) found."))
    return results

def run_custom() -> None:
    """
    Interactive entry point for the custom port scanner.
    """
    from .colors import success, warn, error

    # Питамо корисника за циљ
    host = input("Target (IP or hostname): ").strip()
    if not host:
        print(warn("[!] No target given."))
        return

    # Питамо за порт, опсег или именовани сет
    ports_input = input(
        "Ports (e.g. 80, 1-1024, web, db, mail, windows): "
    ).strip()
    if not ports_input:
        print(warn("[!] No ports given."))
        return

    # Парсирамо унос, хватамо грешке и враћамо се у мени
    try:
        ports = parse_ports(ports_input)
    except ValueError as exc:
        print(error(f"[!] {exc}"))
        return

    try:
        results = asyncio.run(scan_custom(host, ports, DEFAULT_TIMEOUT))
    except KeyboardInterrupt:
        print(warn("\n[!] Scan interrupted."))
        return

    # Питамо да ли корисник жели да сачува резултате
    if not results:
        return

    answer = input("\nSave results to JSON? [y/N]: ").strip().lower()
    if answer != "y":
        return

    # Градимо извештај и чувамо га
    target_info = collect_target_info(host)
    report = build_report(host, target_info, "custom", results)
    filename = default_filename(host, "custom")
    try:
        save_report(report, filename)
        print(success(f"[+] Saved to {filename}"))
    except OSError as exc:
        print(error(f"[!] Could not save: {exc}"))