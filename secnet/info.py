# -*- coding: utf-8 -*-

"""
Target information module.

Gathers basic facts about a target host before scanning:
forward DNS, reverse DNS, and ICMP ping statistics.
"""

import socket

from icmplib import ping, ICMPLibError


def resolve_host(host: str) -> dict:
    """
    Resolve a hostname to IP and try reverse DNS.

    Returns a dict with keys: host, ip, reverse.
    Missing values are None.
    """
    result = {"host": host, "ip": None, "reverse": None}

    # Forward DNS: hostname -> IP
    try:
        result["ip"] = socket.gethostbyname(host)
    except socket.gaierror:
        return result

    # Reverse DNS: IP -> hostname
    try:
        reverse, _, _ = socket.gethostbyaddr(result["ip"])
        result["reverse"] = reverse
    except (socket.herror, socket.gaierror):
        pass

    return result


def ping_host(ip: str, count: int = 3, timeout: float = 1.0) -> dict | None:
    """
    Send ICMP echo requests and return precise statistics.

    Returns a dict with: min_rtt, avg_rtt, max_rtt, packet_loss, jitter.
    Returns None if the host is unreachable.
    """
    try:
        # privileged=False користи непривилеговане ICMP сокете
        host = ping(ip, count=count, timeout=timeout, privileged=False)
    except ICMPLibError:
        return None

    if not host.is_alive:
        return None

    return {
        "min_rtt": host.min_rtt,
        "avg_rtt": host.avg_rtt,
        "max_rtt": host.max_rtt,
        "packet_loss": host.packet_loss,
        "jitter": host.jitter,
    }


def gather_info(host: str) -> None:
    """
    Print basic information about the target host.
    """
    from .colors import info, success, warn, gray

    data = resolve_host(host)

    print(info("\n[*] Target information"))
    print(f"    {gray('Host:')}        {data['host']}")

    if not data["ip"]:
        print(warn("    [!] Could not resolve hostname."))
        return

    print(f"    {gray('Resolved IP:')} {data['ip']}")

    if data["reverse"]:
        print(f"    {gray('Reverse DNS:')} {data['reverse']}")
    else:
        print(f"    {gray('Reverse DNS:')} (none)")

    # Пингујемо само ако смо добили IP
    stats = ping_host(data["ip"])
    if not stats:
        print(f"    {gray('Ping:')}        (unreachable)")
        return

    print(
        f"    {gray('Ping:')}        "
        f"min {stats['min_rtt']:.2f} ms / "
        f"avg {stats['avg_rtt']:.2f} ms / "
        f"max {stats['max_rtt']:.2f} ms"
    )
    print(f"    {gray('Packet loss:')} {stats['packet_loss'] * 100:.0f}%")
    print(f"    {gray('Jitter:')}      {stats['jitter']:.2f} ms")