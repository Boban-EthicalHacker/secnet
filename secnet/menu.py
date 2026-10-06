# -*- coding: utf-8 -*-

"""
Module for the interactive menu and welcome screen.
"""

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
    print(BANNER)
    print(DESCRIPTION)


def show_menu() -> None:
    # Приказујемо главни мени са опцијама
    print("Main menu:")
    print("  [1] Port scanner")
    print("  [2] (coming soon)")
    print("  [3] (coming soon)")
    print("  [0] Exit")


def handle_choice(choice: str) -> None:
    # Обрађујемо избор корисника
    if choice == "1":
        # Увозимо локално да избегнемо циклус у увозу
        from .scanner import run as run_scanner
        run_scanner()
    elif choice in ("2", "3"):
        print("\n[!] This option is not implemented yet.")
    else:
        print("\n[!] Invalid choice. Try again.")