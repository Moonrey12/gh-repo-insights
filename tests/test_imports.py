"""Smoke test: every module can be imported and used."""

from datetime import datetime, timezone

from app.models import RepoSnapshot
from app.storage import load_repos, save_repos
from app.watchlist import add_repo, list_repos, remove_repo, validate_full_name


def test_imports_work() -> None:
    snapshot = RepoSnapshot(
        "octocat/Hello-World",
        1,
        2,
        3,
        datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    assert snapshot.full_name == "octocat/Hello-World"
    assert snapshot.stars == 1


def test_package_modules_are_callable() -> None:
    repos: set[str] = set()
    add_repo(repos, "python/cpython")
    assert list_repos(repos) == ["python/cpython"]
    remove_repo(repos, "python/cpython")
    assert validate_full_name("a/b") == "a/b"
    assert callable(load_repos) and callable(save_repos)
