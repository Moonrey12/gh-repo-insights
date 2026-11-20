"""Save and load the watchlist as JSON.

The default file is ``data/watchlist.json`` next to the project root. Pass a
different path to the functions when you want to control where data lives
(handy for tests).
"""

import json
import sys
import tempfile
from pathlib import Path

from app.watchlist import validate_full_name

DEFAULT_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "watchlist.json"


def load_repos(path: Path | None = None) -> set[str]:
    """Load repositories from *path*, returning an empty set if unavailable.

    A missing file is normal on first run. A corrupt file is reported as a
    warning, but it never crashes the program.
    """
    target = path or DEFAULT_DATA_FILE
    if not target.exists():
        return set()

    try:
        with target.open(encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
        print(
            f"Warning: could not read {target} ({exc}); starting with an empty watchlist.",
            file=sys.stderr,
        )
        return set()

    if not isinstance(data, list):
        print(
            f"Warning: {target} does not contain a list; starting with an empty watchlist.",
            file=sys.stderr,
        )
        return set()

    repos: set[str] = set()
    for item in data:
        try:
            repos.add(validate_full_name(item))
        except ValueError as exc:
            print(f"Warning: skipping invalid entry {item!r}: {exc}", file=sys.stderr)
    return repos


def save_repos(repos: set[str], path: Path | None = None) -> None:
    """Write *repos* to *path* in a sorted, human-readable JSON format."""
    target = path or DEFAULT_DATA_FILE
    data = sorted({validate_full_name(repo) for repo in repos})
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
        file.write("\n")


if __name__ == "__main__":
    demo = Path(tempfile.gettempdir()) / "gh-repo-insights-demo.json"
    save_repos({"octocat/Hello-World", "python/cpython"}, demo)
    print("Loaded from JSON:", sorted(load_repos(demo)))
    demo.write_text("{ this is not valid JSON", encoding="utf-8")
    print("After corrupting the file:", sorted(load_repos(demo)))
    demo.unlink()
