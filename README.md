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

## Roadmap

- [x] Day 1 — repo, venv, `.gitignore`, README, hello script
- [x] Day 2 — watchlist functions with validation
- [ ] Day 3 — JSON persistence
- [ ] Day 4 — `RepoSnapshot` dataclass, `app/` + `tests/` packages
- [ ] Day 5 — pytest suite (8+ tests)
- [ ] Day 6 — argparse CLI
