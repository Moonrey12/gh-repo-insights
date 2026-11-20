"""Tests for the in-memory watchlist operations."""

import pytest

from app.watchlist import add_repo, list_repos, remove_repo, validate_full_name


def test_add_repo_stores_full_name() -> None:
    repos: set[str] = set()
    add_repo(repos, "octocat/Hello-World")
    assert repos == {"octocat/Hello-World"}


def test_add_repo_ignores_duplicates(sample_repos: set[str]) -> None:
    repos = set(sample_repos)
    add_repo(repos, "octocat/Hello-World")
    assert len(repos) == 2


def test_remove_repo(sample_repos: set[str]) -> None:
    repos = set(sample_repos)
    remove_repo(repos, "python/cpython")
    assert repos == {"octocat/Hello-World"}


def test_remove_missing_repo_raises(sample_repos: set[str]) -> None:
    with pytest.raises(ValueError, match="not in the watchlist"):
        remove_repo(set(sample_repos), "missing/repo")


def test_list_repos_is_sorted(sample_repos: set[str]) -> None:
    assert list_repos(set(sample_repos)) == ["octocat/Hello-World", "python/cpython"]


@pytest.mark.parametrize(
    "bad_name",
    ["", "octocat", "a/b/c", "owner/", "/name", "own er/name", ".bad/name"],
)
def test_add_repo_rejects_bad_formats(bad_name: str) -> None:
    repos: set[str] = set()
    with pytest.raises(ValueError):
        add_repo(repos, bad_name)
    assert repos == set()


def test_validate_full_name_rejects_non_string() -> None:
    with pytest.raises(ValueError, match="must be a string"):
        validate_full_name(42)
