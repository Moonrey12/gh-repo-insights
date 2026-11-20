"""Tests for the argparse command-line interface."""

from pathlib import Path

import pytest

from app.cli import main


def test_add_then_list(tmp_path: Path, capsys) -> None:
    data_file = tmp_path / "watchlist.json"
    assert main(["add", "octocat/Hello-World"], data_file) == 0
    assert main(["add", "python/cpython"], data_file) == 0
    assert main(["list"], data_file) == 0
    out = capsys.readouterr().out
    assert "octocat/Hello-World" in out
    assert "python/cpython" in out
    assert data_file.exists()


def test_remove_updates_the_file(tmp_path: Path, capsys) -> None:
    data_file = tmp_path / "watchlist.json"
    main(["add", "octocat/Hello-World"], data_file)
    capsys.readouterr()
    assert main(["remove", "octocat/Hello-World"], data_file) == 0
    assert main(["list"], data_file) == 0
    assert "Watchlist is empty." in capsys.readouterr().out


def test_list_on_missing_file_is_empty(tmp_path: Path, capsys) -> None:
    assert main(["list"], tmp_path / "nothing.json") == 0
    assert "Watchlist is empty." in capsys.readouterr().out


def test_invalid_name_returns_error(tmp_path: Path, capsys) -> None:
    data_file = tmp_path / "watchlist.json"
    assert main(["add", "bad/name/extra"], data_file) == 1
    assert "Error:" in capsys.readouterr().err
    assert not data_file.exists()


def test_remove_missing_repo_returns_error(tmp_path: Path, capsys) -> None:
    assert main(["remove", "missing/repo"], tmp_path / "watchlist.json") == 1
    assert "not in the watchlist" in capsys.readouterr().err


def test_no_command_shows_usage() -> None:
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 2
