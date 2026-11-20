# gh-repo-insights

A small JSON-backed watchlist CLI for GitHub repositories, built as a
week-long learning project.

## Status

Week 1: a JSON-backed watchlist CLI, built one tested day at a time.

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python hello.py

python -m app.cli add octocat/Hello-World
python -m app.cli list
python -m app.cli remove octocat/Hello-World
```

## Day 2: watchlist functions

`app/watchlist.py` provides `add_repo`, `remove_repo`, and `list_repos` over
an in-memory `set[str]` of `owner/name` strings. Invalid names raise a
`ValueError` with a specific message.

```bash
python -m app.watchlist
```

## Day 3: JSON persistence

`app/storage.py` saves the watchlist to `data/watchlist.json` and loads it
back. A missing file means an empty watchlist; a corrupt file prints a
warning and also gives an empty watchlist instead of crashing.

```bash
python -m app.storage
```

## Day 4: models and packages

`app/models.py` defines `RepoSnapshot`, a dataclass holding a repository's
numbers at a moment in time. The `app/` and `tests/` folders are Python
packages, so modules can be run and imported with `python -m`.

```bash
python -m app.models
python -m pytest
```

## Project layout

```
hello.py                 demo script
app/__init__.py          marks app as a package
app/watchlist.py         in-memory operations + validation
app/storage.py           JSON load/save
app/models.py            RepoSnapshot dataclass
app/cli.py               argparse command-line interface
tests/__init__.py        marks tests as a package
tests/conftest.py        shared fixtures
tests/test_imports.py    import smoke tests
tests/test_watchlist.py  watchlist tests
tests/test_storage.py    JSON persistence tests
tests/test_models.py     dataclass tests
tests/test_cli.py        CLI tests
```

## Day 5: tests

The `tests/` package has 29 passing tests covering the watchlist, JSON
storage, and the `RepoSnapshot` model. Shared setup lives in
`tests/conftest.py`; file tests use pytest's `tmp_path` fixture so the real
`data/watchlist.json` is never touched.

```bash
python -m pytest -q       # 29 passed
python -m pytest -v       # one line per test
```

## Day 6: CLI

`app/cli.py` uses `argparse` to expose `add`, `list` and `remove`. Each
command loads the JSON watchlist, changes it in memory, and saves it back.
Invalid names print an error and exit with code 1.

```bash
python -m app.cli add owner/name
python -m app.cli list
python -m app.cli remove owner/name
```

## Roadmap

- [x] Day 1 — repo, venv, `.gitignore`, README, hello script
- [x] Day 2 — watchlist functions with validation
- [x] Day 3 — JSON persistence
- [x] Day 4 — `RepoSnapshot` dataclass, `app/` + `tests/` packages
- [x] Day 5 — pytest suite (8+ tests)
- [x] Day 6 — argparse CLI
