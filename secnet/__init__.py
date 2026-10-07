# -*- coding: utf-8 -*-

"""
secnet - a simple educational network security toolkit.
"""

import sys
from .menu import show_banner, show_menu, handle_choice


def main() -> int:
    # Приказујемо поздравну поруку и банер
    show_banner()

    # Приказујемо мени одмах при покретању
    show_menu()

    # Главна петља програма
    while True:
        try:
            choice = input("\nsecnet > ").strip()
        except (EOFError, KeyboardInterrupt):
            # Ctrl+D или Ctrl+C — излазимо лепо
            print("\n[!] Exiting secnet. Stay ethical.")
            return 0

        # Ако је корисник изабрао излаз, прекидамо петљу
        if choice in ("exit", "quit", "q"):
            print("\n[!] Exiting secnet. Stay ethical.")
            return 0

        # Празна команда — не радимо ништа
        if not choice:
            continue

        # Обрађујемо избор корисника
        handle_choice(choice)
    # Приказујемо поздравну поруку и банер
    show_banner()

    # Главна петља програма
    while True:
        try:
            choice = input("\nsecnet > ").strip()
        except (EOFError, KeyboardInterrupt):
            # Ctrl+D или Ctrl+C — излазимо лепо
            print("\n[!] Exiting secnet. Stay ethical.")
            return 0

        # Ако је корисник изабрао излаз, прекидамо петљу
        if choice in ("exit", "quit", "q"):
            print("\n[!] Exiting secnet. Stay ethical.")
            return 0

        # Празна команда — приказујемо мени поново
        if not choice:
            show_menu()
            continue

        # Обрађујемо избор корисника
        handle_choice(choice)
    # Приказујемо поздравну поруку и банер
    show_banner()

    # Главна петља програма
    while True:
        show_menu()
        try:
            choice = input("\nsecnet > ").strip()
        except (EOFError, KeyboardInterrupt):
            # Ctrl+D или Ctrl+C — излазимо лепо
            print("\n[!] Exiting secnet. Stay ethical.")
            return 0

        # Ако је корисник изабрао излаз, прекидамо петљу
        if choice in ("0", "q", "quit", "exit"):
            print("\n[!] Exiting secnet. Stay ethical.")
            return 0

        # Обрађујемо избор корисника
        handle_choice(choice)
    # Приказујемо поздравну поруку и банер
    show_banner()

    # Главна петља програма
    while True:
        show_menu()
        try:
            choice = input("\nsecnet > ").strip()
        except EOFError:
            print()
            return 0

        # Ако је корисник изабрао излаз, прекидамо петљу
        if choice in ("0", "q", "quit", "exit"):
            print("\n[!] Exiting secnet. Stay ethical.")
            return 0

        # Обрађујемо избор корисника
        handle_choice(choice)