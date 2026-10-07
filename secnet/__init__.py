# -*- coding: utf-8 -*-

"""
secnet - a simple educational network security toolkit.
"""

import sys
from .menu import show_banner, show_menu, handle_choice


def main() -> int:
    from .colors import warn

    # Приказујемо поздравну поруку и банер
    show_banner()

    # Приказујемо мени одмах при покретању
    show_menu()

    # Главна петља програма
    while True:
        try:
            choice = input("\nsecnet > ").strip()
        except (EOFError, KeyboardInterrupt):
            # Ctrl+D или Ctrl+C на промпту — излазимо лепо
            print(warn("\n[!] Exiting secnet. Stay ethical."))
            return 0

        # Ако је корисник изабрао излаз, прекидамо петљу
        if choice in ("exit", "quit", "q"):
            print(warn("\n[!] Exiting secnet. Stay ethical."))
            return 0

        # Празна команда — радимо ништа
        if not choice:
            continue

        # Обрађујемо избор корисника.
        # KeyboardInterrupt унутар команде враћа нас у мени.
        try:
            handle_choice(choice)
        except KeyboardInterrupt:
            print(warn("\n[!] Interrupted."))

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        # Хватамо Ctrl+C и излазимо лепо
        print("\n[!] Interrupted by user. Goodbye.")
        sys.exit(130)