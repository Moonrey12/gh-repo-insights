"""Tests for the RepoSnapshot dataclass."""

from datetime import datetime, timezone

import pytest

from app.models import RepoSnapshot


def test_snapshot_stores_all_fields() -> None:
    fetched = datetime(2026, 1, 1, tzinfo=timezone.utc)
    snapshot = RepoSnapshot("octocat/Hello-World", 10, 2, 1, fetched)
    assert snapshot.full_name == "octocat/Hello-World"
    assert snapshot.stars == 10
    assert snapshot.forks == 2
    assert snapshot.open_issues == 1
    assert snapshot.fetched_at == fetched


def test_default_fetched_at_is_unique_per_snapshot() -> None:
    first = RepoSnapshot("a/b", 0, 0, 0)
    second = RepoSnapshot("a/b", 0, 0, 0)
    assert first.fetched_at != second.fetched_at
    assert first.fetched_at.tzinfo is not None


def test_equal_snapshots_compare_equal() -> None:
    fetched = datetime(2026, 1, 1, tzinfo=timezone.utc)
    first = RepoSnapshot("a/b", 1, 2, 3, fetched)
    second = RepoSnapshot("a/b", 1, 2, 3, fetched)
    assert first == second


def test_snapshot_rejects_bad_name() -> None:
    with pytest.raises(ValueError):
        RepoSnapshot("bad/name/extra", 0, 0, 0)


@pytest.mark.parametrize(
    "field,value",
    [("stars", -1), ("forks", -2), ("open_issues", -3), ("stars", "many")],
)
def test_snapshot_rejects_invalid_counts(field: str, value: object) -> None:
    values = {"full_name": "a/b", "stars": 0, "forks": 0, "open_issues": 0}
    values[field] = value
    with pytest.raises(ValueError):
        RepoSnapshot(**values)
