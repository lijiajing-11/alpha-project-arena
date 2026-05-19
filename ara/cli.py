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
from ara.battle import format_battle
from ara.core import GitHubClient
from ara.dashboard import cmd_dashboard
from ara.display import (
    BOLD,
    CYAN,
    GREEN,
    RED,
    RESET,
    format_compare_table,
    format_multi_watch_dashboard,
    format_repo_info,
    format_watch_dashboard,
)
from ara.generate_stars import cmd_generate_stars
from ara.history import cmd_history, cmd_history_compare
from ara.insight import cmd_insight, cmd_insight_compare
from ara.rank import cmd_rank, cmd_rank_json
from ara.summary import cmd_summary, cmd_summary_json
from ara.trends import cmd_trends as trends_cmd


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


def _cmd_insight_wrapper(args: argparse.Namespace, client: GitHubClient) -> None:
    """Handle `ara insight <repo> [<repo> ...]` — dispatch to single or compare mode."""
    repos = getattr(args, "repos", []) or []
    as_json = getattr(args, "json", False)
    show_trend = getattr(args, "trend", False)
    if len(repos) == 1:
        cmd_insight(repos[0], client=client, as_json=as_json, show_trend=show_trend)
    else:
        cmd_insight_compare(repos, client=client, as_json=as_json)


def _cmd_history_wrapper(args: argparse.Namespace, client: GitHubClient) -> None:
    """Handle `ara history <repo> [<repo> ...]` — dispatch to cmd_history or cmd_history_compare."""
    repos = getattr(args, "repos", []) or []
    if len(repos) == 1:
        cmd_history(repos[0], client=client, as_json=getattr(args, "json", False))
    else:
        cmd_history_compare(
            repos,
            client=client,
            since=getattr(args, "since", None),
            as_json=getattr(args, "json", False),
        )


# ---------------------------------------------------------------------------
# Desktop notification support (via plyer, gracefully degraded)
# ---------------------------------------------------------------------------

_notify_engine: object | None = None  # cached notification backend, or False


def _send_notification(title: str, message: str) -> None:
    """Send a desktop notification via plyer; falls back to stderr.

    Uses the cross-platform ``plyer.notification`` module when available.
    On WSL/headless environments where plyer fails, prints a coloured banner
    to *stderr* so the user still sees the information.

    Args:
        title:   Notification title (e.g. 'ARA Star Tracker').
        message: Body text (e.g. 'owner/repo gained +5 stars!').
    """
    global _notify_engine  # noqa: PLW0603

    if _notify_engine is None:
        try:
            from plyer import notification as _plyer_notif  # type: ignore[import-untyped]
            _notify_engine = _plyer_notif
        except Exception:
            _notify_engine = False  # sentinel: plyer unavailable

    engine = _notify_engine
    if engine is not False:
        try:
            engine.notify(title=title, message=message, timeout=5)
            return
        except Exception:
            pass  # fall through to stderr fallback

    print(
        f"  {GREEN}\U0001f514 {BOLD}{title}{RESET}: {message}",
        file=sys.stderr,
    )


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
    """Handle `ara watch <repo> [<repo> ...]` command.

    Displays a box-drawing dashboard that refreshes every 30 seconds.
    Single repo → full dashboard; multiple repos → compact table.
    Shows stars, forks, open issues, language, license with delta coloring.
    When --notify is set, beeps and shows ✨ NEW! on star changes
    and sends a desktop notification.
    """
    repos = args.repos
    previous_infos: dict[str, dict] = {}
    notify = getattr(args, "notify", False)
    changed_repos: set[str] = set()
    total_new_stars = 0

    print(f"{BOLD}{CYAN}ARA Star Tracker v{__version__}{RESET}")
    print(f"Watching {len(repos)} repo(s). Press Ctrl+C to stop.")
    if notify:
        print(f"{BOLD}🔔 Notification mode: desktop notification + bell on star changes.{RESET}")
    print()

    try:
        while True:
            snapshots: list[tuple[str, dict, dict | None]] = []
            for repo in repos:
                try:
                    info = client.get_repo_info(repo)
                except (ConnectionError, RuntimeError, ValueError) as e:
                    print(f"  {RED}Error fetching {repo}: {e}{RESET}")
                    # Keep the previous info to continue monitoring
                    info = previous_infos.get(repo) or {}
                prev = previous_infos.get(repo)
                current_stars = info.get("stars", 0)

                if notify and prev is not None:
                    prev_stars = prev.get("stars", 0)
                    if current_stars > prev_stars:
                        delta = current_stars - prev_stars
                        total_new_stars += delta
                        changed_repos.add(repo)
                        # Terminal bell (ASCII \a = beep)
                        print("\a", end="", flush=True)
                        # Desktop notification (plyer, gracefully degraded)
                        _send_notification(
                            "ARA Star Tracker",
                            f"{repo} gained +{delta} star{'s' if delta > 1 else ''} "
                            f"({prev_stars:,} → {current_stars:,})",
                        )

                snapshots.append((repo, info, prev))
                previous_infos[repo] = info

            if len(repos) == 1:
                repo, info, prev = snapshots[0]
                output = format_watch_dashboard(repo, info, prev)
            else:
                output = format_multi_watch_dashboard(snapshots)

            print(output, end="")

            time.sleep(30)
    except KeyboardInterrupt:
        print(f"\n{BOLD}Watch ended.{RESET}")
        for repo in repos:
            info = previous_infos.get(repo, {})
            count = info.get("stars", 0)
            print(f"  {repo}: ★ {count:,}")
        if notify and total_new_stars > 0:
            print(f"\n  {GREEN}✨ {total_new_stars} new star(s) gained while watching!{RESET}")


def cmd_watch_json(args: argparse.Namespace, client: GitHubClient) -> None:
    """Handle `ara watch --json <repo> ...` — one JSON line per tick."""
    repos = args.repos
    notify = getattr(args, "notify", False)
    previous_stars: dict[str, int] = {}
    total_changes = 0
    print(json_result({"command": "watch", "repos": repos, "notify": notify, "status": "started"}))
    try:
        while True:
            snapshots = []
            for repo in repos:
                stars = client.get_stars(repo)
                changed = False
                if notify and repo in previous_stars:
                    if stars > previous_stars[repo]:
                        changed = True
                        total_changes += 1
                        _send_notification(
                            "ARA Star Tracker",
                            f"{repo} gained +{stars - previous_stars[repo]} star(s) "
                            f"({previous_stars[repo]:,} → {stars:,})",
                        )
                snapshots.append({"repo": repo, "stars": stars, "changed": changed})
                previous_stars[repo] = stars
            print(json_result({"command": "watch", "tick": snapshots, "total_changes": total_changes}))
            time.sleep(30)
    except KeyboardInterrupt:
        print(json_result({"command": "watch", "status": "ended", "total_changes": total_changes}))


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


# ---------------------------------------------------------------------------
# Info command
# ---------------------------------------------------------------------------


def cmd_info(args: argparse.Namespace, client: GitHubClient) -> None:
    """Handle `ara info <repo>` — show detailed repo information."""
    for repo in args.repos:
        info = client.get_repo_info(repo)
        print(format_repo_info(info))


def cmd_info_json(args: argparse.Namespace, client: GitHubClient) -> None:
    """Handle `ara info --json <repo>`."""
    results = []
    errors = []
    for repo in args.repos:
        try:
            info = client.get_repo_info(repo)
            results.append(info)
        except (ValueError, RuntimeError) as e:
            errors.append({"repo": repo, "error": str(e)})
    print(json_result({"command": "info", "repos": results, "errors": errors or None}))


# ---------------------------------------------------------------------------
# Compare command
# ---------------------------------------------------------------------------


def cmd_compare(args: argparse.Namespace, client: GitHubClient) -> None:
    """Handle `ara compare <repo1> <repo2> [<repo3> ...]`."""
    repos = args.repos
    if len(repos) < 2:
        raise ValueError("compare requires at least 2 repositories")
    infos = [client.get_repo_info(r) for r in repos]

    if len(infos) == 2:
        # Keep existing 2-repo behavior
        print(format_compare_table(infos[0], infos[1]))
    else:
        # Multi-repo comparison
        from ara.display import format_multi_compare_table
        print(format_multi_compare_table(infos))


def cmd_compare_json(args: argparse.Namespace, client: GitHubClient) -> None:
    """Handle `ara compare --json <repo1> <repo2> [<repo3> ...]`."""
    repos = args.repos
    if len(repos) < 2:
        raise ValueError("compare requires at least 2 repositories")
    results = client.get_multiple_repos_info(repos)

    errors = [r for r in results if "error" in r]
    clean = [r for r in results if "error" not in r]

    # Determine winner/leader from clean results only
    winner = None
    lead_by = None
    fork_leader = None
    issue_leader = None

    if len(clean) >= 2:
        sorted_clean = sorted(clean, key=lambda x: x.get("stars", 0), reverse=True)
        winner = sorted_clean[0].get("full_name")
        if len(sorted_clean) > 1:
            lead_by = sorted_clean[0].get("stars", 0) - sorted_clean[1].get("stars", 0)

        fork_sorted = sorted(clean, key=lambda x: x.get("forks", 0), reverse=True)
        fork_leader = fork_sorted[0].get("full_name")

        issue_sorted = sorted(clean, key=lambda x: x.get("open_issues", 0))
        issue_leader = issue_sorted[0].get("full_name") if issue_sorted[0].get("open_issues", 0) < issue_sorted[-1].get("open_issues", 0) else "Tie"

    print(json_result({
        "command": "compare",
        "repos": clean if clean else results,
        "winner": winner,
        "lead_by": lead_by,
        "fork_leader": fork_leader,
        "issue_leader": issue_leader,
        "errors": errors or None,
    }))


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
    parser.add_argument(
        "--retries", type=int, default=3,
        help="Max retries per API request (default: 3)",
    )
    parser.add_argument(
        "--retry-delay", type=float, default=1.0,
        help="Base retry delay in seconds, doubles each attempt (default: 1.0)",
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
    watch_parser.add_argument(
        "--notify", action="store_true",
        help="Desktop notification + terminal bell on star changes"
    )
    watch_parser.set_defaults(func=cmd_watch)

    # ara battle <repo1> <repo2> [<repo3> ...]
    battle_parser = subparsers.add_parser("battle", help="Battle repos side-by-side")
    battle_parser.add_argument(
        "repos", nargs="+", help="Repos to battle (owner/name)"
    )
    battle_parser.add_argument("--json", action="store_true", help="Output as JSON")
    battle_parser.set_defaults(func=cmd_battle)

    # ara info <repo> [<repo> ...]
    info_parser = subparsers.add_parser("info", help="Show detailed repository info")
    info_parser.add_argument("repos", nargs="+", help="Repository in owner/name format")
    info_parser.add_argument("--json", action="store_true", help="Output as JSON")
    info_parser.set_defaults(func=cmd_info)

    # ara compare <repo1> <repo2> [<repo3> ...]
    compare_parser = subparsers.add_parser(
        "compare", help="Compare repositories side-by-side (2+)"
    )
    compare_parser.add_argument(
        "repos", nargs="+", help="Repos to compare (owner/name format, 2+)"
    )
    compare_parser.add_argument("--json", action="store_true", help="Output as JSON")
    compare_parser.set_defaults(func=cmd_compare)

    # ara trends <repo>
    trends_parser = subparsers.add_parser(
        "trends",
        help="Show star trend chart for a repo",
    )
    trends_parser.add_argument("repo", help="Repository (owner/repo)")
    trends_parser.add_argument(
        "--hours", type=int, default=72,
        help="Lookback window in hours (default: 72)",
    )
    trends_parser.add_argument(
        "--interval", type=int, default=60,
        help="Bucket interval in minutes (default: 60)",
    )
    trends_parser.add_argument(
        "--json", action="store_true", help="Output as JSON",
    )
    trends_parser.set_defaults(func=trends_cmd)

    # ara generate-stars <repo>
    gs_parser = subparsers.add_parser(
        "generate-stars",
        help="Fetch stargazers and save to JSON file (demo tool)",
    )
    gs_parser.add_argument("repo", help="Repository (owner/repo)")
    gs_parser.add_argument(
        "--pages", type=int, default=3,
        help="Max pages to fetch (default: 3, each page = 100 stargazers)",
    )
    gs_parser.add_argument(
        "--output", type=str, default=None,
        help="Output file path (default: stargazers_<repo>.json)",
    )
    gs_parser.set_defaults(func=cmd_generate_stars)

    # ara dashboard <repo> [<repo> ...]
    dash_parser = subparsers.add_parser(
        "dashboard",
        help="Show full repo overview dashboard",
    )
    dash_parser.add_argument("repos", nargs="+", help="Repository (owner/repo)")
    dash_parser.add_argument("--json", action="store_true", help="Output as JSON")
    dash_parser.set_defaults(func=cmd_dashboard)

    # ara summary <repo>
    summary_parser = subparsers.add_parser(
        "summary",
        help="One-line repo summary (copy-paste friendly)",
    )
    summary_parser.add_argument("repo", help="Repository (owner/repo)")
    summary_parser.add_argument(
        "--json", action="store_true", help="Output as JSON"
    )
    summary_parser.set_defaults(func=cmd_summary)

    # ara insight <repo> [<repo> ...]
    insight_parser = subparsers.add_parser(
        "insight",
        help="Deep repository insight -- star velocity, topics, age, and more",
    )
    insight_parser.add_argument(
        "repos", nargs="+", help="Repository(es) (owner/repo), 2+ for compare mode"
    )
    insight_parser.add_argument("--json", action="store_true", help="Output as JSON")
    insight_parser.add_argument(
        "--trend", action="store_true",
        help="Append star trend chart to insight output",
    )
    insight_parser.set_defaults(func=_cmd_insight_wrapper)

    # ara history <repo> [<repo> ...]
    history_parser = subparsers.add_parser(
        "history",
        help="Show star growth history as an ASCII chart",
    )
    history_parser.add_argument(
        "repos", nargs="+",
        help="Repository(owner/repo) — 1 for line chart, 2+ for compare mode",
    )
    history_parser.add_argument("--json", action="store_true", help="Output as JSON")
    history_parser.add_argument(
        "--since", type=str, default=None,
        help="Only show data since this date (YYYY-MM-DD)",
    )
    history_parser.set_defaults(func=_cmd_history_wrapper)

    # ara rank [--top N] [--json] [<repo> ...]
    rank_parser = subparsers.add_parser(
        "rank",
        help="Show ranked list of repos by star count",
    )
    rank_parser.add_argument("repos", nargs="*", help="Repos to rank (default: pre-defined hot repos)")
    rank_parser.add_argument(
        "--top", type=int, default=10,
        help="Number of repos to show (default: 10)"
    )
    rank_parser.add_argument("--json", action="store_true", help="Output as JSON")
    rank_parser.set_defaults(func=cmd_rank)

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
        "info": cmd_info_json,
        "compare": cmd_compare_json,
        "trends": trends_cmd,
        "dashboard": cmd_dashboard,
        "summary": cmd_summary_json,
        "insight": _cmd_insight_wrapper,
        "rank": cmd_rank_json,
    }
    if getattr(args, "json", False) and args.command in json_handlers:
        args.func = json_handlers[args.command]

    client = GitHubClient(
        max_retries=args.retries,
        retry_delay=args.retry_delay,
    )

    try:
        args.func(args, client)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted by user.", file=sys.stderr)
        return 130
    except (ConnectionError, TimeoutError) as e:
        print(f"Network error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected error: {type(e).__name__}: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
