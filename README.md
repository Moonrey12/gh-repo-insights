# gh-repo-insights

A small JSON-backed watchlist CLI for GitHub repositories, built as a
week-long learning project.

## Status

Week 1, Day 1: project scaffold, virtual environment, and version control.

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python hello.py
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

## Roadmap

- [x] Day 1 — repo, venv, `.gitignore`, README, hello script
- [x] Day 2 — watchlist functions with validation
- [x] Day 3 — JSON persistence
- [ ] Day 4 — `RepoSnapshot` dataclass, `app/` + `tests/` packages
- [ ] Day 5 — pytest suite (8+ tests)
- [ ] Day 6 — argparse CLI
