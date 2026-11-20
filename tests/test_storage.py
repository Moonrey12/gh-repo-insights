"""Tests for JSON persistence."""

import json
from pathlib import Path

from app.storage import load_repos, save_repos


def test_load_missing_file_returns_empty_set(data_file: Path) -> None:
    assert load_repos(data_file) == set()
    assert not data_file.exists()


def test_save_creates_file_and_parent(data_file: Path, sample_repos: set[str]) -> None:
    save_repos(sample_repos, data_file)
    assert data_file.exists()
    assert json.loads(data_file.read_text(encoding="utf-8")) == [
        "octocat/Hello-World",
        "python/cpython",
    ]


def test_save_then_load_roundtrip(data_file: Path, sample_repos: set[str]) -> None:
    save_repos(sample_repos, data_file)
    assert load_repos(data_file) == sample_repos


def test_corrupt_json_warns_and_returns_empty_set(data_file: Path, capsys) -> None:
    data_file.parent.mkdir(parents=True, exist_ok=True)
    data_file.write_text("{ broken json", encoding="utf-8")
    assert load_repos(data_file) == set()
    assert "Warning" in capsys.readouterr().err


def test_wrong_json_shape_returns_empty_set(data_file: Path) -> None:
    data_file.parent.mkdir(parents=True, exist_ok=True)
    data_file.write_text('{"not": "a list"}', encoding="utf-8")
    assert load_repos(data_file) == set()


def test_invalid_entries_are_skipped(data_file: Path) -> None:
    data_file.parent.mkdir(parents=True, exist_ok=True)
    data_file.write_text(
        '["octocat/Hello-World", "bad/name/extra"]', encoding="utf-8"
    )
    assert load_repos(data_file) == {"octocat/Hello-World"}
