# -*- coding: utf-8 -*-

"""
Port scanner module.

Scans a small, predefined list of common ports.
"""

import asyncio
import socket
from .info import gather_info

# Подразумевани тајмаут за једну везу (у секундама)
DEFAULT_TIMEOUT = 0.5

# Листа најчешћих портова које скенирамо
COMMON_PORTS = {
    21:    "FTP",
    22:    "SSH",
    23:    "Telnet",
    25:    "SMTP",
    53:    "DNS",
    80:    "HTTP",
    110:   "POP3",
    143:   "IMAP",
    443:   "HTTPS",
    445:   "SMB",
    3306:  "MySQL",
    3389:  "RDP",
    5432:  "PostgreSQL",
    5900:  "VNC",
    6379:  "Redis",
    8080:  "HTTP-Alt",
    8443:  "HTTPS-Alt",
}


async def scan_port(host: str, port: int, timeout: float) -> bool:
    """
    Try to open a TCP connection to host:port.
    Returns True if the port is open, False otherwise.
    """
    try:
        # Отварамо везу ка асинхроном отвору
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port, family=socket.AF_INET),
            timeout=timeout,
        )
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return False

    # Ако смо стигли довде, веза је успела — затварамо је
    writer.close()
    try:
        await writer.wait_closed()
    except OSError:
        pass

    return True


async def scan_common(host: str, timeout: float) -> None:
    """
    Scan the predefined list of common ports on a single host.
    """
    total = len(COMMON_PORTS)
    print(f"\n[*] Scanning {host} ({total} common ports, timeout={timeout}s)")

    open_count = 0
    for port, service in COMMON_PORTS.items():
        is_open = await scan_port(host, port, timeout)
        if is_open:
            open_count += 1
            print(f"[+] {host}:{port:<5} open   ({service})")

    print(f"\n[*] Done. {open_count} open port(s) found.")


def run() -> None:
    """
    Interactive entry point called from the menu.
    """
    # Питамо корисника за циљ
    host = input("Target (IP or hostname): ").strip()
    if not host:
        print("[!] No target given.")
        return
    
    # Приказујемо основне информације о мети пре скенирања
    gather_info(host)

    try:
        asyncio.run(scan_common(host, DEFAULT_TIMEOUT))
    except KeyboardInterrupt:
        # Дозвољавамо прекид скенирања без изласка из програма
        print("\n[!] Scan interrupted.")