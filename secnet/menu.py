# -*- coding: utf-8 -*-

"""
Module for the interactive menu and welcome screen.
"""

from .colors import info, success, warn, bold, gray, error

# ASCII банер алата
BANNER = r"""
  ___  ___ ___ _  _ ___ _____
 / __|/ __/ __| \| | __|_   _|
 \__ \ (_| (__| .` | _|  | |
 |___/\___\___|_|\_|___| |_|
        network toolkit v0.1
"""

# Опис алата и његова намена
DESCRIPTION = """
secnet is a small, educational network security toolkit.
It is intended for scanning your own systems, home lab,
and authorized lab environments (e.g. TryHackMe, HTB).

  [!] Use only on networks you own or have permission to test.
"""


def show_banner() -> None:
    # Исписујемо банер и опис
    print(info(BANNER))
    print(DESCRIPTION)


def show_menu() -> None:
    # Приказујемо доступне команде
    print(bold("Available commands:"))
    print(f"  {success('scan-common')}   Scan a predefined list of common ports")
    print(f"  {success('scan-custom')}   Scan a custom port, list, or range")
    print(f"  {success('help')}          Show detailed help")
    print(f"  {success('exit')}          Exit secnet")


def handle_choice(choice: str) -> None:
    # Обрађујемо избор корисника
    if choice == "scan-common":
        # Увозимо локално да избегнемо циклус у увозу
        from .scanner import run as run_scanner
        run_scanner()
    elif choice == "scan-custom":
        from .custom_scanner import run_custom
        run_custom()
    elif choice == "help":
        from .help import show_help
        show_help()
    else:
        print(error(f"[!] Unknown command: '{choice}'. Type 'help' for a list of commands."))