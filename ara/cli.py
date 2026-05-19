     1|"""CLI entry point for ARA - Arena Star Tracker.
     2|
     3|Supports:
     4|- ara watch <repo> [<repo> ...]
     5|- ara battle <repo1> <repo2> [<repo3> ...]
     6|- ara stars <repo>  (single fetch, from core)
     7|"""
     8|
     9|import argparse
    10|import sys
    11|import time
    12|
    13|from ara import __version__
    14|from ara.core import GitHubClient
    15|from ara.display import (
    16|    format_watch_summary,
    17|    format_multi_watch,
    18|    compute_delta,
    19|    BOLD,
    20|    CYAN,
    21|    GREEN,
    22|    RED,
    23|    RESET,
    24|)
    25|from ara.battle import format_battle
    26|
    27|
    28|def run_watch(repo: str, client: GitHubClient, previous: int | None = None) -> int:
    29|    """Fetch star count for a single repo and return it.
    30|
    31|    Args:
    32|        repo: Repository name (owner/repo).
    33|        client: GitHubClient instance.
    34|        previous: Previous star count (for delta computation), or None.
    35|
    36|    Returns:
    37|        Current star count.
    38|    """
    39|    stars = client.get_stars(repo)
    40|    return stars
    41|
    42|
    43|def run_battle(repos: list, client: GitHubClient) -> str:
    44|    """Fetch stars for multiple repos and generate battle display.
    45|
    46|    Args:
    47|        repos: List of repository names.
    48|        client: GitHubClient instance.
    49|
    50|    Returns:
    51|        Formatted battle string.
    52|    """
    53|    data = []
    54|    for repo in repos:
    55|        stars = client.get_stars(repo)
    56|        data.append((repo, stars))
    57|    return format_battle(data)
    58|
    59|
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
    82|
    83|
    84|def cmd_watch(args: argparse.Namespace, client: GitHubClient) -> None:
    85|    """Handle `ara watch <repo> [<repo> ...]` command."""
    86|    repos = args.repos
    87|    previous = {}
    88|
    89|    print(f"{BOLD}{CYAN}ARA Star Tracker v{__version__}{RESET}")
    90|    print(f"Watching {len(repos)} repo(s). Press Ctrl+C to stop.\n")
    91|
    92|    try:
    93|        while True:
    94|            snapshots = []
    95|            for repo in repos:
    96|                stars = client.get_stars(repo)
    97|                prev = previous.get(repo)
    98|                delta = compute_delta(stars, prev) if prev is not None else 0
    99|                previous[repo] = stars
   100|                snapshots.append((repo, stars, delta))
   101|
   102|            output = format_multi_watch(snapshots)
   103|            print(output, end="")
   104|
   105|            time.sleep(30)
   106|    except KeyboardInterrupt:
   107|        print(f"\n{BOLD}Watch ended.{RESET}")
   108|        for repo in repos:
   109|            snapshot_data = [
   110|                (0, previous.get(repo, 0)),
   111|                (1, previous.get(repo, 0)),
   112|            ]
   113|            print("")
   114|            print(format_watch_summary(repo, snapshot_data))
   115|
   116|
   117|def cmd_battle(args: argparse.Namespace, client: GitHubClient) -> None:
   118|    """Handle `ara battle <repo1> <repo2> [<repo3> ...]` command."""
   119|    repos = args.repos
   120|    data = []
   121|    for repo in repos:
   122|        stars = client.get_stars(repo)
   123|        data.append((repo, stars))
   124|
   125|    result = format_battle(data)
   126|    print(result)
   127|
   128|
   129|def build_parser() -> argparse.ArgumentParser:
   130|    """Build the argument parser for the CLI."""
   131|    parser = argparse.ArgumentParser(
   132|        prog="ara",
   133|        description="ARA - Arena Star Tracker: Monitor and compare GitHub Stars",
   134|        epilog="Battle your way to the top!",
   135|    )
   136|    parser.add_argument(
   137|        "--version", action="version", version=f"%(prog)s {__version__}"
   138|    )
   139|
   140|    subparsers = parser.add_subparsers(dest="command", help="Available commands")
   141|
   142|    # ara stars <repo> [<repo> ...]
   143|    stars_parser = subparsers.add_parser("stars", help="Fetch star count for repo(s)")
   144|    stars_parser.add_argument("repos", nargs="+", help="Repository in owner/name format")
   145|    stars_parser.set_defaults(func=cmd_stars)
   146|
   147|    # ara watch <repo> [<repo> ...]
   148|    watch_parser = subparsers.add_parser("watch", help="Watch repos in real-time")
   149|    watch_parser.add_argument("repos", nargs="+", help="Repos to watch (owner/name)")
   150|    watch_parser.set_defaults(func=cmd_watch)
   151|
   152|    # ara battle <repo1> <repo2> [<repo3> ...]
   153|    battle_parser = subparsers.add_parser("battle", help="Battle repos side-by-side")
   154|    battle_parser.add_argument(
   155|        "repos", nargs="+", help="Repos to battle (owner/name)"
   156|    )
   157|    battle_parser.set_defaults(func=cmd_battle)
   158|
   159|    return parser
   160|
   161|
   162|def main(argv: list | None = None) -> int:
   163|    """Main entry point for the ARA CLI."""
   164|    parser = build_parser()
   165|    args = parser.parse_args(argv)
   166|
   167|    if not args.command:
   168|        parser.print_help()
   169|        return 1
   170|
   171|    client = GitHubClient()
   172|
   173|    try:
   174|        args.func(args, client)
   175|    except ValueError as e:
   176|        print(f"Error: {e}", file=sys.stderr)
   177|        return 1
   178|    except RuntimeError as e:
   179|        print(f"Error: {e}", file=sys.stderr)
   180|        return 1
   181|
   182|    return 0
   183|
   184|
   185|if __name__ == "__main__":
   186|    sys.exit(main())
   187|