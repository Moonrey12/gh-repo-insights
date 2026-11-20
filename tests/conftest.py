"""Shared test fixtures.

A fixture is a reusable setup function. pytest calls it automatically when a
test asks for it by name as an argument.
"""

import pytest


@pytest.fixture
def sample_repos() -> set[str]:
    """A small watchlist used by several tests."""
    return {"octocat/Hello-World", "python/cpython"}


@pytest.fixture
def data_file(tmp_path):
    """Path to a JSON file inside pytest's temporary folder.

    ``tmp_path`` is built into pytest: it gives each test its own empty
    folder, so tests never touch the real data/watchlist.json.
    """
    return tmp_path / "data" / "watchlist.json"
