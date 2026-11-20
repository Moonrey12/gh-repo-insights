"""Command-line interface: python -m app.cli {add,list,remove}."""

import argparse
import sys
from pathlib import Path

from app.storage import load_repos, save_repos
from app.watchlist import add_repo, list_repos, remove_repo


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser with its three commands."""
    parser = argparse.ArgumentParser(
        prog="python -m app.cli",
        description="Manage a JSON-backed watchlist of GitHub repositories.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="Add a repository")
    add.add_argument("full_name", help="Repository in owner/name format")

    commands.add_parser("list", help="List watched repositories")

    remove = commands.add_parser("remove", help="Remove a repository")
    remove.add_argument("full_name", help="Repository in owner/name format")

    return parser


def main(argv: list[str] | None = None, data_file: Path | None = None) -> int:
    """Run the CLI. Return 0 on success, 1 on a handled error."""
    args = build_parser().parse_args(argv)
    repos = load_repos(data_file)

    if args.command == "list":
        names = list_repos(repos)
        if names:
            for name in names:
                print(name)
        else:
            print("Watchlist is empty.")
        return 0

    try:
        if args.command == "add":
            add_repo(repos, args.full_name)
            action = "Added"
        else:
            remove_repo(repos, args.full_name)
            action = "Removed"
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    save_repos(repos, data_file)
    print(f"{action} {args.full_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
