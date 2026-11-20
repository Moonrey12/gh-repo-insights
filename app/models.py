"""Data models for gh-repo-insights."""

from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.watchlist import validate_full_name


@dataclass
class RepoSnapshot:
    """A point-in-time snapshot of a GitHub repository's numbers.

    A dataclass writes the boring parts of a class for you: ``__init__``,
    ``__repr__`` (how it prints) and ``__eq__`` (how two snapshots compare).
    """

    full_name: str
    stars: int
    forks: int
    open_issues: int
    fetched_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        """Run after the generated ``__init__`` to check the values."""
        self.full_name = validate_full_name(self.full_name)
        for label in ("stars", "forks", "open_issues"):
            value = getattr(self, label)
            if not isinstance(value, int) or value < 0:
                raise ValueError(f"{label} must be a non-negative integer, got {value!r}")


if __name__ == "__main__":
    snapshot = RepoSnapshot("octocat/Hello-World", 100, 20, 3)
    print(snapshot)
