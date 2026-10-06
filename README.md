# secnet

A small, educational network security toolkit written in Python.

## Purpose

`secnet` is built from scratch as a learning project to understand how
network security tools work internally. It is not meant to replace tools
like Nmap — it is meant to teach the principles behind them.

Currently, it provides a simple TCP port scanner that checks a small,
predefined list of common ports on a single target.

## ⚠️ Ethical Use

This tool is intended **only** for:

- Scanning your own system (localhost, home lab)
- Authorized lab environments (TryHackMe, HackTheBox)
- Any network where you have **explicit written permission**

Scanning systems you do not own or have permission to test is illegal
in most jurisdictions. The author assumes no responsibility for misuse.

## Installation

Requires Python 3.10+ and `pipx`.

```bash
git clone https://github.com/<your-username>/secnet.git
cd secnet
pipx install -e .
