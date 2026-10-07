# -*- coding: utf-8 -*-

"""
Terminal color helpers.

Uses ANSI escape codes — no external libraries, no sudo.
"""

# ANSI кодери
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
GRAY = "\033[90m"


def info(text: str) -> str:
    """Cyan — informational messages like [*]."""
    return f"{CYAN}{text}{RESET}"


def success(text: str) -> str:
    """Green — successful results like [+]."""
    return f"{GREEN}{text}{RESET}"


def warn(text: str) -> str:
    """Yellow — warnings like [!]."""
    return f"{YELLOW}{text}{RESET}"


def error(text: str) -> str:
    """Red — errors."""
    return f"{RED}{text}{RESET}"


def bold(text: str) -> str:
    """Bold text, useful for headers."""
    return f"{BOLD}{text}{RESET}"


def gray(text: str) -> str:
    """Dim text, useful for secondary info."""
    return f"{GRAY}{text}{RESET}"