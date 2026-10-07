# -*- coding: utf-8 -*-

"""
Help module.

Prints detailed documentation for every secnet command.
"""

from .colors import info, success, bold, gray


def show_help() -> None:
    # Детаљан опис сваке команде
    print(bold("\nsecnet — command reference"))
    print(bold("=========================="))

    print(f"\n{success('scan-common')}")
    print("    Scan a predefined list of common ports on a single target.")
    print("    Prompts for a host (IP or hostname) and checks the ports in")
    print("    COMMON_PORTS. Prints only the ports that are open.")

    print(f"\n{success('scan-custom')}")
    print("    Scan a custom port, list, or range on a single target.")
    print("    Prompts for a host and a port specification such as:")
    print(gray("        80                single port"))
    print(gray("        22,80,443         list of ports"))
    print(gray("        1-1024            range"))
    print(gray("        22,80,100-200     combination"))
    print("    Named port sets can also be used:")
    print(gray("        web      [80, 443, 8000, 8080, 8443, 8888]"))
    print(gray("        db       [1433, 1521, 3306, 5432, 6379, 27017]"))
    print(gray("        mail     [25, 110, 143, 465, 587, 993, 995]"))
    print(gray("        windows  [135, 139, 445, 3389, 5985]"))

    print(f"\n{success('help')}")
    print("    Show this help screen.")

    print(f"\n{success('exit')}")
    print("    Quit secnet.")

    print(f"\n{bold('General')}")
    print("-------")
    print("    Type 'exit', 'quit', or 'q' to leave the program.")
    print("    Press Ctrl+C or Ctrl+D at the prompt to exit immediately.")
    print("    Press Ctrl+C during a command to return to the menu.")

    print(f"\n    {info('[!]')} Use secnet only on systems you own or have written")
    print("        permission to test.")