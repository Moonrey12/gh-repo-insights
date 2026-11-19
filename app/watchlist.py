"""In-memory watchlist operations for GitHub repositories.

A repository is identified by its full name in ``owner/name`` form, for
example ``octocat/Hello-World``. All operations validate that format and
raise :class:`ValueError` with a helpful message when it is wrong.
"""

import re

_FULL_NAME_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def validate_full_name(full_name: str) -> str:
    """Return *full_name* if it is a valid ``owner/name`` string.

    Raises:
        ValueError: If the value is not a string, does not contain exactly
            one ``/``, has an empty owner or name, or contains invalid
            characters.
    """
    if not isinstance(full_name, str):
        raise ValueError(
            f"Repository must be a string in 'owner/name' format, got {type(full_name).__name__}."
        )

    if full_name.count("/") != 1:
        raise ValueError(
            f"Invalid repository {full_name!r}: expected 'owner/name' with exactly one '/'."
        )

    owner, name = full_name.split("/")
    for label, part in (("owner", owner), ("name", name)):
        if not part:
            raise ValueError(f"Invalid repository {full_name!r}: {label} cannot be empty.")
        if not _FULL_NAME_PATTERN.fullmatch(part):
            raise ValueError(
                f"Invalid repository {full_name!r}: {label} may only contain "
                "letters, digits, '.', '_' and '-' and cannot start with '.' or '-'."
            )

    return full_name


def add_repo(repos: set[str], full_name: str) -> None:
    """Add a validated repository to *repos* (adding twice is a no-op)."""
    repos.add(validate_full_name(full_name))


def remove_repo(repos: set[str], full_name: str) -> None:
    """Remove a repository from *repos*.

    Raises:
        ValueError: If the name is invalid or is not in the watchlist.
    """
    name = validate_full_name(full_name)
    if name not in repos:
        raise ValueError(f"Repository {name!r} is not in the watchlist.")
    repos.remove(name)


def list_repos(repos: set[str]) -> list[str]:
    """Return the watched repositories in alphabetical order."""
    return sorted([repo for repo in repos])


if __name__ == "__main__":
    watched: set[str] = set()
    add_repo(watched, "octocat/Hello-World")
    add_repo(watched, "python/cpython")
    add_repo(watched, "octocat/Hello-World")  # duplicate: still one entry
    print("Watching:", ", ".join(list_repos(watched)))
