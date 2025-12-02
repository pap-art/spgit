"""Tests for utility functions"""

import pytest
from spgit.utils.helpers import (
    format_duration, truncate, pluralize, format_table
)
from spgit.utils.colors import colorize, Colors


class TestHelpers:
    """Test helper functions."""

    def test_format_duration(self):
        """Test duration formatting."""
        assert format_duration(0) == "0:00"
        assert format_duration(60000) == "1:00"
        assert format_duration(125000) == "2:05"
        assert format_duration(3661000) == "61:01"

    def test_truncate(self):
        """Test text truncation."""
        assert truncate("hello", 10) == "hello"
        assert truncate("hello world", 8) == "hello..."
        assert truncate("hello world", 8, "..") == "hello .."

    def test_pluralize(self):
        """Test pluralization."""
        assert pluralize(0, "track") == "0 tracks"
        assert pluralize(1, "track") == "1 track"
        assert pluralize(2, "track") == "2 tracks"
        assert pluralize(2, "commit", "commits") == "2 commits"

    def test_format_table(self):
        """Test table formatting."""
        rows = [
            ["John", "25", "Engineer"],
            ["Jane", "30", "Designer"],
        ]
        headers = ["Name", "Age", "Job"]

        table = format_table(rows, headers)
        assert "John" in table
        assert "Jane" in table
        assert "Engineer" in table


class TestColors:
    """Test color functions."""

    def test_colorize(self):
        """Test colorization."""
        # Color functions should work without errors
        text = colorize("test", Colors.RED)
        assert "test" in text

    def test_color_disabled(self):
        """Test color disabled mode."""
        import os
        os.environ["NO_COLOR"] = "1"

        from spgit.utils.colors import color_enabled
        assert not color_enabled()

        del os.environ["NO_COLOR"]
