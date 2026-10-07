# -*- coding: utf-8 -*-

"""
Help module.

Prints detailed documentation for every secnet command.
"""


def show_help() -> None:
    # Детаљан опис сваке команде
    print("""
secnet — command reference
==========================

scan-common
    Scan a predefined list of common ports on a single target.
    Prompts for a host (IP or hostname) and checks the ports in
    COMMON_PORTS. Prints only the ports that are open.

scan-custom
    Scan a custom port, list, or range on a single target.
    Prompts for a host and a port specification such as:
        80                single port
        22,80,443         list of ports
        1-1024            range
        22,80,100-200     combination

help
    Show this help screen.

exit
    Quit secnet.

General
-------
    Type 'exit', 'quit', or 'q' to leave the program.
    Press Ctrl+C or Ctrl+D at the prompt to exit immediately.

    [!] Use secnet only on systems you own or have written
        permission to test.
""")