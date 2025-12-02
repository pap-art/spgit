"""
Color output utilities for spgit.
Provides git-like colored terminal output.
"""

import os
import sys
from typing import Optional


# ANSI color codes
class Colors:
    """ANSI color codes."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright foreground colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


def color_enabled() -> bool:
    """Check if color output is enabled."""
    # Check if stdout is a TTY
    if not sys.stdout.isatty():
        return False

    # Check if color is explicitly disabled
    if os.getenv("NO_COLOR"):
        return False

    # Check if running on Windows and enable ANSI support
    if sys.platform == "win32":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass

    return True


def colorize(text: str, color: str, bold: bool = False) -> str:
    """
    Colorize text if color is enabled.

    Args:
        text: Text to colorize
        color: Color code
        bold: Whether to make text bold

    Returns:
        Colorized text
    """
    if not color_enabled():
        return text

    prefix = f"{Colors.BOLD}{color}" if bold else color
    return f"{prefix}{text}{Colors.RESET}"


# Convenience functions for common colors
def red(text: str, bold: bool = False) -> str:
    """Red text."""
    return colorize(text, Colors.RED, bold)


def green(text: str, bold: bool = False) -> str:
    """Green text."""
    return colorize(text, Colors.GREEN, bold)


def yellow(text: str, bold: bool = False) -> str:
    """Yellow text."""
    return colorize(text, Colors.YELLOW, bold)


def blue(text: str, bold: bool = False) -> str:
    """Blue text."""
    return colorize(text, Colors.BLUE, bold)


def cyan(text: str, bold: bool = False) -> str:
    """Cyan text."""
    return colorize(text, Colors.CYAN, bold)


def magenta(text: str, bold: bool = False) -> str:
    """Magenta text."""
    return colorize(text, Colors.MAGENTA, bold)


def gray(text: str) -> str:
    """Gray text."""
    return colorize(text, Colors.BRIGHT_BLACK)


def bold(text: str) -> str:
    """Bold text."""
    if not color_enabled():
        return text
    return f"{Colors.BOLD}{text}{Colors.RESET}"


def dim(text: str) -> str:
    """Dim text."""
    if not color_enabled():
        return text
    return f"{Colors.DIM}{text}{Colors.RESET}"


# Git-like semantic colors
def added(text: str) -> str:
    """Color for added items (green)."""
    return green(text)


def removed(text: str) -> str:
    """Color for removed items (red)."""
    return red(text)


def modified(text: str) -> str:
    """Color for modified items (yellow)."""
    return yellow(text)


def untracked(text: str) -> str:
    """Color for untracked items (red)."""
    return red(text)


def branch(text: str) -> str:
    """Color for branch names (green)."""
    return green(text, bold=True)


def commit_hash(text: str) -> str:
    """Color for commit hashes (yellow)."""
    return yellow(text)


def header(text: str) -> str:
    """Color for headers (cyan, bold)."""
    return cyan(text, bold=True)


def error(text: str) -> str:
    """Color for errors (red, bold)."""
    return red(text, bold=True)


def warning(text: str) -> str:
    """Color for warnings (yellow, bold)."""
    return yellow(text, bold=True)


def info(text: str) -> str:
    """Color for info messages (blue)."""
    return blue(text)


def success(text: str) -> str:
    """Color for success messages (green, bold)."""
    return green(text, bold=True)
