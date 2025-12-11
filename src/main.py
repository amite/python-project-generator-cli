#!/usr/bin/env python3
"""
Python Project Generator CLI
Entry point for the application.
"""
import sys
from .cli import run_cli


def main():
    """Main entry point"""
    try:
        run_cli()
    except KeyboardInterrupt:
        # Handle Ctrl-C gracefully (fallback if not caught in run_cli)
        sys.exit(0)


if __name__ == "__main__":
    main()
