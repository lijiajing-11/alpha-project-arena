"""CLI entry point for ARA - Arena Star Tracker.

Supports:
- ara watch <repo> [<repo> ...]
- ara battle <repo1> <repo2> [<repo3> ...]
- ara stars <repo>  (single fetch, from core)
"""

import argparse
import sys
import time

from ara import __version__
from ara.core import GitHubClient
from ara.display import (
    format_multi_watch,
    format_repo_info,
    format_compare,
    compute_delta,
    BOLD,
    CYAN,
    GREEN,
    RED,
    RESET,
)
from ara.battle import format_battle


def run_watch(repo: str, client: GitHubClient, previous: int | None = None) -> int:
    """Fetch star count for a single repo and return it.

    Args:
        repo: Repository name (owner/repo).
        client: GitHubClient instance.
        previous: Previous star count (for delta computation), or None.

    Returns:
        Current star count.
    """
    stars = client.get_stars(repo)
    return stars


def run_battle(repos: list, client: GitHubClient) -> str:
    """Fetch stars for multiple repos and generate battle display.

    Args:
        repos: List of repository names.
        client: GitHubClient instance.

    Returns:
        Formatted battle string.
    """
    data = []
    for repo in repos:
        stars = client.get_stars(repo)
        data.append((repo, stars))
    return format_battle(data)


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------


def json_result(data: dict) -> str:
    """Return a pretty-printed JSON string with indent 2."""
    import json as _json
    return _json.dumps(data, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------


def cmd_stars(args: argparse.Namespace, client: GitHubClient) -> None:
    """Handle `ara stars <repo> [<repo> ...]` command.

    Fetches each repo exactly once, prints individual results,
    and if multiple repos were given, shows a mini leaderboard.
    """
    results = []
    for repo in args.repos:
        stars = client.get_stars(repo)
        if stars is not None:
            print(f"  {GREEN}★{RESET} {repo}: {BOLD}{stars:,}{RESET} stars")
            results.append((repo, stars))
        else:
            print(f"  {RED}✗{RESET} {repo}: could not fetch")

    if len(results) > 1:
        print(f"\n  {BOLD}Mini Leaderboard{RESET}")
        print(f"  {'─' * 40}")
        results.sort(key=lambda x: x[1], reverse=True)
        for i, (repo, stars) in enumerate(results, 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"  {i}.")
            print(f"  {medal} {repo:<25} {stars:>6,} ★")


def cmd_stars_json(args: argparse.Namespace, client: GitHubClient) -> None:
    """Handle `ara stars --json <repo> ...`."""
    repos_data = []
    errors = []
    for repo in args.repos:
        try:
            stars = client.get_stars(repo)
            repos_data.append({"repo": repo, "stars": stars})
        except (ValueError, RuntimeError) as e:
            errors.append({"repo": repo, "error": str(e)})
    print(json_result({"command": "stars", "repos": repos_data, "errors": errors or None}))


def cmd_watch(args: argparse.Namespace, client: GitHubClient) -> None:
    """Handle `ara watch <repo> [<repo> ...]` command."""
    repos = args.repos
    previous = {}

    print(f"{BOLD}{CYAN}ARA Star Tracker v{__version__}{RESET}")
    print(f"Watching {len(repos)} repo(s). Press Ctrl+C to stop.\n")

    try:
        while True:
            snapshots = []
            for repo in repos:
                stars = client.get_stars(repo)
                prev = previous.get(repo)
                delta = compute_delta(stars, prev) if prev is not None else 0
                previous[repo] = stars
                snapshots.append((repo, stars, delta))

            output = format_multi_watch(snapshots)
            print(output, end="")

            time.sleep(30)
    except KeyboardInterrupt:
        print(f"\n{BOLD}Watch ended.{RESET}")
        for repo in repos:
            count = previous.get(repo, 0)
            print(f"  {repo}: ★ {count:,}")


def cmd_watch_json(args: argparse.Namespace, client: GitHubClient) -> None:
    """Handle `ara watch --json <repo> ...` — one JSON line per tick."""
    repos = args.repos
    print(json_result({"command": "watch", "repos": repos, "status": "started"}))
    try:
        while True:
            snapshots = []
            for repo in repos:
                stars = client.get_stars(repo)
                snapshots.append({"repo": repo, "stars": stars})
            print(json_result({"command": "watch", "tick": snapshots}))
            time.sleep(30)
    except KeyboardInterrupt:
        print(json_result({"command": "watch", "status": "ended"}))


def cmd_battle(args: argparse.Namespace, client: GitHubClient) -> None:
    """Handle `ara battle <repo1> <repo2> [<repo3> ...]` command."""
    repos = args.repos
    data = []
    for repo in repos:
        stars = client.get_stars(repo)
        data.append((repo, stars))

    result = format_battle(data)
    print(result)


def cmd_battle_json(args: argparse.Namespace, client: GitHubClient) -> None:
    """Handle `ara battle --json <repo1> <repo2> ...`."""
    repos = args.repos
    data = []
    errors = []
    for repo in repos:
        try:
            stars = client.get_stars(repo)
            data.append({"repo": repo, "stars": stars})
        except (ValueError, RuntimeError) as e:
            errors.append({"repo": repo, "error": str(e)})
    print(json_result({"command": "battle", "repos": data, "winner": _resolve_winner(data), "errors": errors or None}))


def _resolve_winner(repos_data: list[dict]) -> str | None:
    """Return the winner repo name from a list of {'repo', 'stars'} dicts."""
    if not repos_data:
        return None
    max_stars = max(r["stars"] for r in repos_data)
    winners = [r["repo"] for r in repos_data if r["stars"] == max_stars]
    return winners[0] if len(winners) == 1 else "Tie — Draw!"


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="ara",
        description="ARA - Arena Star Tracker: Monitor and compare GitHub Stars",
        epilog="Battle your way to the top!",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ara stars <repo> [<repo> ...]
    stars_parser = subparsers.add_parser("stars", help="Fetch star count for repo(s)")
    stars_parser.add_argument("repos", nargs="+", help="Repository in owner/name format")
    stars_parser.add_argument("--json", action="store_true", help="Output as JSON")
    stars_parser.set_defaults(func=cmd_stars)

    # ara watch <repo> [<repo> ...]
    watch_parser = subparsers.add_parser("watch", help="Watch repos in real-time")
    watch_parser.add_argument("repos", nargs="+", help="Repos to watch (owner/name)")
    watch_parser.add_argument("--json", action="store_true", help="Output as JSON")
    watch_parser.set_defaults(func=cmd_watch)

    # ara battle <repo1> <repo2> [<repo3> ...]
    battle_parser = subparsers.add_parser("battle", help="Battle repos side-by-side")
    battle_parser.add_argument(
        "repos", nargs="+", help="Repos to battle (owner/name)"
    )
    battle_parser.add_argument("--json", action="store_true", help="Output as JSON")
    battle_parser.set_defaults(func=cmd_battle)

    return parser


def main(argv: list | None = None) -> int:
    """Main entry point for the ARA CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    # Dispatch to JSON handler when --json is set
    json_handlers = {
        "stars": cmd_stars_json,
        "watch": cmd_watch_json,
        "battle": cmd_battle_json,
    }
    if getattr(args, "json", False) and args.command in json_handlers:
        args.func = json_handlers[args.command]

    client = GitHubClient()

    try:
        args.func(args, client)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
