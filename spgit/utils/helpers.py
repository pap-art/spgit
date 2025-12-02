"""
Helper utilities for spgit.
"""

import re
from pathlib import Path
from typing import List, Set
from datetime import datetime


def format_duration(milliseconds: int) -> str:
    """
    Format duration in milliseconds to MM:SS format.

    Args:
        milliseconds: Duration in milliseconds

    Returns:
        Formatted duration string
    """
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"


def format_timestamp(iso_timestamp: str) -> str:
    """
    Format ISO timestamp to human-readable format.

    Args:
        iso_timestamp: ISO format timestamp

    Returns:
        Formatted timestamp
    """
    try:
        dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return iso_timestamp


def format_relative_time(iso_timestamp: str) -> str:
    """
    Format ISO timestamp to relative time (e.g., "2 hours ago").

    Args:
        iso_timestamp: ISO format timestamp

    Returns:
        Relative time string
    """
    try:
        dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
        now = datetime.now(dt.tzinfo)
        delta = now - dt

        seconds = delta.total_seconds()
        if seconds < 60:
            return "just now"
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif seconds < 2592000:
            days = int(seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''} ago"
        elif seconds < 31536000:
            months = int(seconds / 2592000)
            return f"{months} month{'s' if months != 1 else ''} ago"
        else:
            years = int(seconds / 31536000)
            return f"{years} year{'s' if years != 1 else ''} ago"
    except Exception:
        return iso_timestamp


def truncate(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def load_ignore_patterns(repo) -> Set[str]:
    """
    Load ignore patterns from .spgitignore file.

    Args:
        repo: Repository instance

    Returns:
        Set of patterns to ignore
    """
    ignore_file = repo.work_dir / ".spgitignore"
    if not ignore_file.exists():
        return set()

    patterns = set()
    with open(ignore_file, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.add(line)

    return patterns


def should_ignore(uri: str, patterns: Set[str]) -> bool:
    """
    Check if a track URI should be ignored based on patterns.

    Args:
        uri: Track URI
        patterns: Set of ignore patterns

    Returns:
        True if should be ignored
    """
    for pattern in patterns:
        # Convert glob pattern to regex
        regex_pattern = pattern.replace("*", ".*").replace("?", ".")
        if re.match(f"^{regex_pattern}$", uri):
            return True
    return False


def get_terminal_width() -> int:
    """
    Get terminal width.

    Returns:
        Terminal width in characters
    """
    try:
        import shutil
        return shutil.get_terminal_size().columns
    except Exception:
        return 80


def format_table(rows: List[List[str]], headers: List[str] = None) -> str:
    """
    Format data as a table.

    Args:
        rows: List of rows (each row is a list of strings)
        headers: Optional list of header strings

    Returns:
        Formatted table string
    """
    if not rows:
        return ""

    # Calculate column widths
    all_rows = [headers] + rows if headers else rows
    col_widths = [max(len(str(row[i])) for row in all_rows) for i in range(len(all_rows[0]))]

    # Format rows
    lines = []
    if headers:
        header_line = "  ".join(str(headers[i]).ljust(col_widths[i]) for i in range(len(headers)))
        lines.append(header_line)
        lines.append("-" * len(header_line))

    for row in rows:
        line = "  ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row)))
        lines.append(line)

    return "\n".join(lines)


def pluralize(count: int, singular: str, plural: str = None) -> str:
    """
    Pluralize a word based on count.

    Args:
        count: Count
        singular: Singular form
        plural: Plural form (defaults to singular + 's')

    Returns:
        Pluralized string
    """
    if count == 1:
        return f"{count} {singular}"
    else:
        plural = plural or f"{singular}s"
        return f"{count} {plural}"


def confirm(message: str, default: bool = False) -> bool:
    """
    Ask user for confirmation.

    Args:
        message: Confirmation message
        default: Default response

    Returns:
        True if confirmed
    """
    suffix = " [Y/n] " if default else " [y/N] "
    response = input(message + suffix).strip().lower()

    if not response:
        return default

    return response in ("y", "yes")
