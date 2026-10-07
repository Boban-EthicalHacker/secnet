# secnet

A small, educational network security toolkit written in Python.

`secnet` is built from scratch as a learning project to understand how network security tools work internally. It is **not** a replacement for Nmap — it is a teaching tool.

---

## ⚠️ Ethical Use

This tool is intended **only** for:

- Scanning your own system (localhost, home lab)
- Authorized lab environments (TryHackMe, HackTheBox)
- Networks where you have **explicit written permission**

Scanning systems you do not own or have permission to test is illegal in most jurisdictions. The author assumes no responsibility for misuse.

---

## Features

- **`scan-common`** — scans a predefined list of 17 common ports
- **`scan-custom`** — scans a user-defined port, list, or range
- **Named port sets** — shortcut names like `web`, `db`, `mail`, `windows`
- **Parallel scanning** — up to 200 concurrent connections, thousands of ports in seconds
- **Target information** — forward DNS, reverse DNS, ping statistics (min/avg/max RTT, packet loss, jitter)
- **Banner grabbing** — reads service banners for open ports
  - Passive read (SSH, FTP, SMTP, ...)
  - HTTP request for web ports (`Server` header)
  - HTTPS request over TLS for secure web ports
- **JSON export** — save scan results as structured JSON (ready for databases or further processing)
- **Colored terminal output** — clean, readable results
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
```

The `-e` flag installs the project in editable mode, so code changes take effect immediately — no need to reinstall after editing.

### Optional dependency

`secnet` uses [icmplib](https://pypi.org/project/icmplib/) for precise ping statistics. Install it into the pipx environment:

```bash
pipx inject secnet icmplib
```

---

## Usage

Run the tool from anywhere:

```bash
secnet
```

You will see a banner, a short description, and an interactive prompt:

```
Available commands:
  scan-common   Scan a predefined list of common ports
  scan-custom   Scan a custom port, list, or range
  help          Show detailed help
  exit          Exit secnet

secnet > _
```

### Example — scan common ports

```
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

Save results to JSON? [y/N]: y
[+] Saved to secnet-common-127.0.0.1-20261007-231725.json
```

### Example — scan a custom range

```
secnet > scan-custom
Target (IP or hostname): 192.168.1.10
Ports (e.g. 80, 1-1024, web, db, mail, windows): 22,80,443,8000-8100
```

Supported port formats:

| Format             | Meaning                          |
| ------------------ | -------------------------------- |
| `80`               | single port                      |
| `22,80,443`        | list of ports                    |
| `1-1024`           | range                            |
| `22,80,100-200`    | combination of all of the above  |
| `web`              | named port set                   |
| `web,22,100-200`   | named set combined with numbers  |

### Named port sets

| Set       | Ports                                    |
| --------- | ---------------------------------------- |
| `web`     | 80, 443, 8000, 8080, 8443, 8888          |
| `db`      | 1433, 1521, 3306, 5432, 6379, 27017      |
| `mail`    | 25, 110, 143, 465, 587, 993, 995         |
| `windows` | 135, 139, 445, 3389, 5985                |

### JSON export

After every scan (`scan-common` or `scan-custom`), `secnet` offers to save the results as a JSON file. The report contains:

- Tool name and version
- Timestamp
- Scan type (`common` or `custom`)
- Target information (resolved IP, reverse DNS, ping statistics)
- List of open ports with service name and banner (if any)
- Summary with open port count

The JSON output is designed to be easy to import into a database or process with other tools.

---

## Common ports scanned by `scan-common`

| Port  | Service     |
| ----- | ----------- |
| 21    | FTP         |
| 22    | SSH         |
| 23    | Telnet      |
| 25    | SMTP        |
| 53    | DNS         |
| 80    | HTTP        |
| 110   | POP3        |
| 143   | IMAP        |
| 443   | HTTPS       |
| 445   | SMB         |
| 3306  | MySQL       |
| 3389  | RDP         |
| 5432  | PostgreSQL  |
| 5900  | VNC         |
| 6379  | Redis       |
| 8080  | HTTP-Alt    |
| 8443  | HTTPS-Alt   |

---

## Project structure

```
secnet/
├── pyproject.toml          # metadata + entry point for pipx
├── README.md               # this file
├── LICENSE                 # MIT
└── secnet/
    ├── __init__.py         # main() — application loop
    ├── __main__.py         # allows `python -m secnet`
    ├── menu.py             # banner, menu, command dispatch
    ├── help.py             # detailed help text
    ├── colors.py           # ANSI color helpers
    ├── scanner.py          # scan-common + shared scan_port
    ├── custom_scanner.py   # scan-custom command
    ├── info.py             # target info (DNS, ping stats)
    ├── banner.py           # banner grabbing (passive, HTTP, HTTPS)
    └── export.py           # JSON report builder
```

---

## Roadmap

- [x] Basic TCP port scanner (`scan-common`)
- [x] Interactive menu with named commands
- [x] Graceful exit (Ctrl+C, Ctrl+D, `exit`)
- [x] Target information (DNS + ping)
- [x] Banner grabbing (passive, HTTP, HTTPS)
- [x] Custom port scanner (`scan-custom`)
- [x] Parallel scanning with `asyncio`
- [x] Output to file (JSON)
- [x] Colored terminal output
- [x] Named port sets (`web`, `db`, `mail`, `windows`)
- [ ] Subnet / CIDR scanning (`192.168.1.0/24`)
- [ ] Tabular output for large scans
- [ ] Extended port sets (`top100`, `top1000`)
- [ ] Configurable default output directory

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## Disclaimer

`secnet` is an educational tool. The author is not responsible for any misuse or damage caused by this software. Always obtain proper authorization before scanning any network or system you do not own.