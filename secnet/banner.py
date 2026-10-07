# -*- coding: utf-8 -*-

"""
Banner grabbing module.

Reads the greeting a service sends upon connection, or sends a
minimal HTTP/HTTPS request to obtain a Server header.

Uses only asyncio and ssl — no external libraries, no root.
"""

import asyncio
import ssl


# Празна листа портова који се понашају као HTTP
HTTP_PORTS = {80, 8000, 8080, 8888}

# Празна листа портова који се понашају као HTTPS
HTTPS_PORTS = {443, 8443}


def _clean(raw: bytes, limit: int = 200) -> str:
    """
    Decode raw bytes and return the first non-empty printable line.
    Returns empty string if the data is not text (e.g. binary protocols).
    """
    # Ако има пуно неисписивих бајтова, третирамо као бинарно
    printable = sum(1 for b in raw[:64] if 32 <= b < 127 or b in (9, 10, 13))
    if len(raw[:64]) > 0 and printable / min(len(raw), 64) < 0.8:
        return ""

    text = raw.decode(errors="ignore")
    for line in text.splitlines():
        line = line.strip()
        if line:
            # Узимамо само линије које су углавном читљив текст
            if sum(1 for c in line if c.isprintable()) / len(line) < 0.8:
                continue
            return line[:limit]
    return ""

async def _grab_passive(host: str, port: int, timeout: float) -> str:
    """
    Read whatever the service sends immediately after connecting.
    """
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout,
        )
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return ""

    banner = ""
    try:
        data = await asyncio.wait_for(reader.read(1024), timeout=timeout)
        banner = _clean(data)
    except (asyncio.TimeoutError, OSError):
        pass

    writer.close()
    try:
        await writer.wait_closed()
    except OSError:
        pass

    return banner


async def _grab_http(host: str, port: int, timeout: float) -> str:
    """
    Send a minimal HTTP request and extract the Server header.
    """
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout,
        )
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return ""

    # Минимални HTTP захтев — само заглавља
    request = f"HEAD / HTTP/1.0\r\nHost: {host}\r\n\r\n"
    try:
        writer.write(request.encode())
        await writer.drain()
    except OSError:
        writer.close()
        return ""

    response = b""
    try:
        # Читамо док не добијемо довољно или до тајмаута
        while True:
            chunk = await asyncio.wait_for(reader.read(1024), timeout=timeout)
            if not chunk:
                break
            response += chunk
            if b"\r\n\r\n" in response:
                break
    except (asyncio.TimeoutError, OSError):
        pass

    writer.close()
    try:
        await writer.wait_closed()
    except OSError:
        pass

    # Тражимо Server заглавље
    text = response.decode(errors="ignore")
    for line in text.splitlines():
        if line.lower().startswith("server:"):
            return line.split(":", 1)[1].strip()
    return ""


async def _grab_https(host: str, port: int, timeout: float) -> str:
    """
    Send a minimal HTTPS request and extract the Server header.
    """
    # Контекст који не верификује сертификат (лабораторијске мете)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port, ssl=ctx),
            timeout=timeout,
        )
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError, ssl.SSLError):
        return ""

    request = f"HEAD / HTTP/1.0\r\nHost: {host}\r\n\r\n"
    try:
        writer.write(request.encode())
        await writer.drain()
    except OSError:
        writer.close()
        return ""

    response = b""
    try:
        while True:
            chunk = await asyncio.wait_for(reader.read(1024), timeout=timeout)
            if not chunk:
                break
            response += chunk
            if b"\r\n\r\n" in response:
                break
    except (asyncio.TimeoutError, OSError):
        pass

    writer.close()
    try:
        await writer.wait_closed()
    except OSError:
        pass

    text = response.decode(errors="ignore")
    for line in text.splitlines():
        if line.lower().startswith("server:"):
            return line.split(":", 1)[1].strip()
    return ""


async def grab_banner(host: str, port: int, timeout: float = 1.5) -> str:
    """
    Return a banner for the given open port, or an empty string.

    Chooses the right strategy based on the port number:
    HTTP ports get an HTTP request, HTTPS ports get an HTTPS
    request, everything else gets a passive read.
    """
    if port in HTTP_PORTS:
        return await _grab_http(host, port, timeout)
    if port in HTTPS_PORTS:
        return await _grab_https(host, port, timeout)
    return await _grab_passive(host, port, timeout)