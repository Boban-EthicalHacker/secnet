# -*- coding: utf-8 -*-

"""
Entry point for `python -m secnet`.
"""

import sys
from . import main


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        # Хватамо Ctrl+C и излазимо лепо
        print("\n[!] Interrupted by user. Goodbye.")
        sys.exit(130)