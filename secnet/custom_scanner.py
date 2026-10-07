# -*- coding: utf-8 -*-

"""
Custom port scanner module.

Scans a user-defined port, list, or range on a single target.
Reuses scan_port and COMMON_PORTS from scanner.py.
"""

import asyncio

from .scanner import scan_port, COMMON_PORTS, DEFAULT_TIMEOUT


def parse_ports(spec: str) -> list[int]:
    """
    Parse a port specification string into a list of ports.

    Supported formats:
        "80"            -> [80]
        "22,80,443"     -> [22, 80, 443]
        "1-1024"        -> [1, 2, ..., 1024]
        "22,80,100-200" -> mixed

    Raises ValueError on invalid input.
    """
    ports: set[int] = set()

    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
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
            port = int(chunk)
            if not (0 < port <= 65535):
                raise ValueError(f"Port out of range: {port}")
            ports.add(port)

    return sorted(ports)


async def scan_custom(host: str, ports: list[int], timeout: float) -> None:
    """
    Scan a user-defined list of ports on a single host.
    """
    total = len(ports)
    print(f"\n[*] Scanning {host} ({total} custom ports, timeout={timeout}s)")

    open_count = 0
    for port in ports:
        is_open = await scan_port(host, port, timeout)
        if is_open:
            open_count += 1
            # Ако знамо име сервиса из COMMON_PORTS, приказујемо га
            service = COMMON_PORTS.get(port, "")
            label = f"   ({service})" if service else ""
            print(f"[+] {host}:{port:<5} open{label}")

    print(f"\n[*] Done. {open_count} open port(s) found.")


def run_custom() -> None:
    """
    Interactive entry point for the custom port scanner.
    """
    # Питамо корисника за циљ
    host = input("Target (IP or hostname): ").strip()
    if not host:
        print("[!] No target given.")
        return

    # Питамо за порт или опсег
    ports_input = input("Ports (e.g. 80, 22,80,443 or 1-1024): ").strip()
    if not ports_input:
        print("[!] No ports given.")
        return

    # Парсирамо унос, хватамо грешке и враћамо се у мени
    try:
        ports = parse_ports(ports_input)
    except ValueError as exc:
        print(f"[!] {exc}")
        return

    try:
        asyncio.run(scan_custom(host, ports, DEFAULT_TIMEOUT))
    except KeyboardInterrupt:
        # Дозвољавамо прекид скенирања без изласка из програма
        print("\n[!] Scan interrupted.")