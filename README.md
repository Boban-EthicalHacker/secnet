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

The -e flag installs the project in editable mode, so code changes
take effect immediately — no need to reinstall after editing.

Optional dependency
secnet uses icmplib for precise
ping statistics. Install it into the pipx environment:

bash
pipx inject secnet icmplib
Usage
Run the tool from anywhere:

bash
secnet
You will see a banner, a short description, and an interactive prompt:

text
Available commands:
  scan-common   Scan a predefined list of common ports
  scan-custom   Scan a custom port, list, or range
  help          Show detailed help
  exit          Exit secnet

secnet > _
Example — scan common ports
text
secnet > scan-common
Target (IP or hostname): 127.0.0.1

[*] Target information
    Host:        127.0.0.1
    Resolved IP: 127.0.0.1
    Reverse DNS: localhost
    Ping:        min 0.06 ms / avg 0.13 ms / max 0.17 ms
    Packet loss: 0%
    Jitter:      0.06 ms

[*] Scanning 127.0.0.1 (17 common ports, timeout=0.5s)
[+] 127.0.0.1:3306  open   (MySQL)
[+] 127.0.0.1:8080  open   (HTTP-Alt) -> SimpleHTTP/0.6 Python/3.14.7

[*] Done. 2 open port(s) found.
Example — scan a custom range
text
secnet > scan-custom
Target (IP or hostname): 192.168.1.10
Ports (e.g. 80, 22,80,443 or 1-1024): 22,80,443,8000-8100
Supported port formats:

Format	Meaning
80	single port
22,80,443	list of ports
1-1024	range
22,80,100-200	combination of all of the above
Common ports scanned by scan-common
Port	Service
21	FTP
22	SSH
23	Telnet
25	SMTP
53	DNS
80	HTTP
110	POP3
143	IMAP
443	HTTPS
445	SMB
3306	MySQL
3389	RDP
5432	PostgreSQL
5900	VNC
6379	Redis
8080	HTTP-Alt
8443	HTTPS-Alt
Project structure
text
secnet/
├── pyproject.toml          # metadata + entry point for pipx
├── README.md               # this file
├── LICENSE                 # MIT
└── secnet/
    ├── __init__.py         # main() — application loop
    ├── __main__.py         # allows `python -m secnet`
    ├── menu.py             # banner, menu, command dispatch
    ├── help.py             # detailed help text
    ├── scanner.py          # scan-common + shared scan_port
    ├── custom_scanner.py   # scan-custom command
    ├── info.py             # target info (DNS, ping stats)
    └── banner.py           # banner grabbing (passive, HTTP, HTTPS)
Roadmap
☑ Basic TCP port scanner (scan-common)
☑ Interactive menu with named commands
☑ Graceful exit (Ctrl+C, Ctrl+D, exit)
☑ Target information (DNS + ping)
☑ Banner grabbing (passive, HTTP, HTTPS)
☑ Custom port scanner (scan-custom)
□ Parallel scanning with asyncio.gather
□ Output to file (JSON / TXT)
□ Colored terminal output
□ Named port sets (web, db, top100)
License
MIT — see LICENSE for details.

Disclaimer
secnet is an educational tool. The author is not responsible for
any misuse or damage caused by this software. Always obtain proper
authorization before scanning any network or system you do not own.