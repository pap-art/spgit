"""Pytest configuration and fixtures"""

import pytest


@pytest.fixture(autouse=True)
def disable_colors():
    """Disable colors in tests."""
    import os
    os.environ["NO_COLOR"] = "1"
    yield
    if "NO_COLOR" in os.environ:
        del os.environ["NO_COLOR"]
