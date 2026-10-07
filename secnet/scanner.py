# -*- coding: utf-8 -*-

"""
Port scanner module.

Scans a small, predefined list of common ports.
"""

import asyncio
import socket
from .info import gather_info
from .banner import grab_banner
from .export import build_report, save_report, default_filename

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


async def scan_ports_parallel(
    host: str,
    ports: list[int],
    timeout: float,
    concurrency: int = 200,
) -> list[tuple[int, str]]:
    """
    Scan a list of ports in parallel.

    Returns a list of (port, banner) tuples for open ports,
    sorted by port number.
    """
    sem = asyncio.Semaphore(concurrency)
    results: list[tuple[int, str]] = []

    async def worker(port: int) -> None:
        # Ограничавамо број истовремених веза
        async with sem:
            is_open = await scan_port(host, port, timeout)
            if not is_open:
                return
            # Узимамо банер само за отворене портове
            banner = await grab_banner(host, port)
            results.append((port, banner))

    # Правимо задатке за све портове одједном
    tasks = [asyncio.create_task(worker(p)) for p in ports]
    await asyncio.gather(*tasks)

    return sorted(results)


async def scan_common(host: str, timeout: float) -> list[tuple[int, str, str]]:
    """
    Scan the predefined list of common ports on a single host.

    Returns a list of (port, service, banner) tuples for open ports.
    """
    total = len(COMMON_PORTS)
    print(f"\n[*] Scanning {host} ({total} common ports, timeout={timeout}s)")

    results: list[tuple[int, str, str]] = []
    for port, service in COMMON_PORTS.items():
        is_open = await scan_port(host, port, timeout)
        if is_open:
            banner = await grab_banner(host, port)
            results.append((port, service, banner))
            if banner:
                print(f"[+] {host}:{port:<5} open   ({service}) -> {banner}")
            else:
                print(f"[+] {host}:{port:<5} open   ({service})")

    print(f"\n[*] Done. {len(results)} open port(s) found.")
    return results

def collect_target_info(host: str) -> dict:
    """
    Collect target info in a dict form for the JSON report.
    """
    from .info import resolve_host, ping_host

    info = resolve_host(host)
    result = {
        "resolved_ip": info["ip"],
        "reverse_dns": info["reverse"],
    }
    if info["ip"]:
        stats = ping_host(info["ip"])
        if stats:
            result["ping"] = stats
    return result


def run() -> None:
    """
    Interactive entry point for scan-common.
    """
    # Питамо корисника за циљ
    host = input("Target (IP or hostname): ").strip()
    if not host:
        print("[!] No target given.")
        return

    # Приказујемо основне информације о мети пре скенирања
    gather_info(host)

    try:
        results = asyncio.run(scan_common(host, DEFAULT_TIMEOUT))
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted.")
        return

    # Питамо да ли корисник жели да сачува резултате
    if not results:
        return

    answer = input("\nSave results to JSON? [y/N]: ").strip().lower()
    if answer != "y":
        return

    # Градимо извештај и чувамо га
    target_info = collect_target_info(host)
    report = build_report(host, target_info, "common", results)
    filename = default_filename(host, "common")
    try:
        save_report(report, filename)
        print(f"[+] Saved to {filename}")
    except OSError as exc:
        print(f"[!] Could not save: {exc}")