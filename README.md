# secnet

A small, educational network security toolkit written in Python.

`secnet` is built from scratch as a learning project to understand how
network security tools work internally. It is **not** a replacement for
Nmap — it is a teaching tool.

---

## ⚠️ Ethical Use

This tool is intended **only** for:

- Scanning your own system (localhost, home lab)
- Authorized lab environments (TryHackMe, HackTheBox)
- Networks where you have **explicit written permission**

Scanning systems you do not own or have permission to test is illegal
in most jurisdictions. The author assumes no responsibility for misuse.

---

## Features

- **`scan-common`** — scans a predefined list of 17 common ports
- **`scan-custom`** — scans a user-defined port, list, or range
- **Target information** — forward DNS, reverse DNS, ping statistics
  (min/avg/max RTT, packet loss, jitter)
- **Banner grabbing** — reads service banners for open ports
  - Passive read (SSH, FTP, SMTP, ...)
  - HTTP request for web ports (`Server` header)
  - HTTPS request over TLS for secure web ports
- **Interactive menu** with named commands
- **No `sudo` required** — runs entirely as an ordinary user
- **Graceful exit** via `exit`, `quit`, `q`, **Ctrl+C**, or **Ctrl+D**

---

## Installation

Requirements: **Python 3.10+** and **pipx**.

```bash
git clone https://github.com/Boban-EthicalHacker/secnet.git
cd secnet
pipx install -e .