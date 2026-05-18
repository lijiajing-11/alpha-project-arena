#!/usr/bin/env python3
"""ARA — Arena Star Tracker CLI.

Usage:
    ara stars <repo>         Get current star count
    ara watch <repo> [...]   Watch repos in real-time
    ara battle <repo> [...]  Compare repos side-by-side
    ara leaderboard          Show cached repos sorted by stars
    ara info <repo>          Show detailed repo info
"""

import argparse
import sys
import time
import os

from ara import __version__
from ara.core import GitHubClient, Repo, StarSnapshot

# ─── Terminal Styling ─────────────────────────────────────────────────────

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"
CLEAR = "\033c"


def _color_stars(stars: int, delta: int = 0) -> str:
    """Color a star count based on growth."""
    if delta > 0:
        return f"{GREEN}★ {stars:,}{RESET}"
    elif delta < 0:
        return f"{RED}★ {stars:,}{RESET}"
    return f"★ {stars:,}"


def _format_delta(delta: int) -> str:
    """Format a delta value with color."""
    if delta > 0:
        return f"{GREEN}+{delta}{RESET}"
    elif delta < 0:
        return f"{RED}{delta}{RESET}"
    return "  0"


def _bar(value: int, max_value: int, width: int = 20) -> str:
    """Generate an ASCII progress bar."""
    if max_value <= 0:
        return "░" * width
    filled = min(int((value / max_value) * width), width)
    bar = "▓" * filled + "░" * (width - filled)
    if value > 0 and filled == 0:
        bar = "▏" + "░" * (width - 1)
    return bar


def _box_line(char: str = "═", width: int = 60) -> str:
    return char * width


# ─── Logo ──────────────────────────────────────────────────────────────────

LOGO = f"""{CYAN}
    ╔══════════════════════════════════════════════╗
    ║               ★  A R A  ★                   ║
    ║          Arena Star Tracker v{__version__}            ║
    ╚══════════════════════════════════════════════╝{RESET}
"""


# ─── Commands ──────────────────────────────────────────────────────────────

def cmd_stars(args: argparse.Namespace):
    """Show star count for one or more repos."""
    client = GitHubClient()
    print(LOGO)

    repos_info = []
    for repo_name in args.repos:
        info = client.get_repo_info(repo_name)
        if info:
            repos_info.append(info)

    if not repos_info:
        print(f"  {RED}No valid repos found.{RESET}")
        sys.exit(1)

    for info in repos_info:
        print(f"  {BOLD}{info['full_name']}{RESET}")
        print(f"    {_color_stars(info['stars'])} stars")
        if info["description"]:
            print(f"    {info['description']}")
        if info["language"]:
            print(f"    Language: {info['language']}")
        print()

    if client.rate_limit_remaining >= 0 and client.rate_limit_remaining < 100:
        print(f"  {YELLOW}⚠  Low rate limit: {client.rate_limit_remaining}{RESET}")


def cmd_watch(args: argparse.Namespace):
    """Watch repos in real-time, polling every N seconds."""
    interval = args.interval or 30
    client = GitHubClient()

    repos = [Repo(name) for name in args.repos]

    print(f"{CLEAR}{LOGO}")
    print(f"  Watching {', '.join(args.repos)}")
    print(f"  Refreshing every {interval}s | Press Ctrl+C to stop\n")

    first_run = True
    try:
        while True:
            if not first_run:
                time.sleep(interval)
                print(CLEAR, end="")
                print(LOGO)
                print(f"  Watching {', '.join(args.repos)}")
                print(f"  Refreshing every {interval}s | Press Ctrl+C to stop\n")
            first_run = False

            for repo in repos:
                stars = client.get_stars(repo.full_name)
                if stars is not None:
                    if repo.stars == 0 and repo.baseline_stars == 0:
                        repo.baseline_stars = stars
                    repo.update(stars)

            print(f"  {'NAME':25} {'STARS':>10} {'Δ':>6} {'GROWTH':>8}")
            print(f"  {'─'*25} {'─'*10} {'─'*6} {'─'*8}")
            for repo in repos:
                if repo.stars > 0:
                    growth_str = _format_delta(repo.total_growth)
                    delta_str = _format_delta(repo.delta)
                    star_str = _color_stars(repo.stars, repo.delta)
                    print(f"  {repo.display_name(25):25} {star_str:>18} {delta_str:>6} {growth_str:>10}")

            print(f"\n  {client.rate_limit_status()}")

    except KeyboardInterrupt:
        print(f"\n\n  {BOLD}Watch Summary:{RESET}")
        for repo in repos:
            growth = repo.total_growth
            gstr = _format_delta(growth)
            print(f"  {repo.full_name}: ★{repo.stars:,}  ({gstr} total growth)")
        print(f"  {YELLOW}See you in the arena!{RESET}")


def cmd_battle(args: argparse.Namespace):
    """Compare repos side-by-side and declare a winner."""
    client = GitHubClient()
    width = 80  # total box width

    if not args.repos:
        print(f"  {RED}Usage: ara battle <repo1> <repo2> [...]{RESET}")
        sys.exit(1)

    # Fetch star counts
    repo_objects = []
    for name in args.repos:
        stars = client.get_stars(name)
        if stars is not None:
            repo_objects.append(Repo(name, stars))

    if not repo_objects:
        print(f"  {RED}Could not fetch data for any repos.{RESET}")
        sys.exit(1)

    snapshot = StarSnapshot(repo_objects)
    sorted_repos = snapshot.sorted_by_stars()
    max_stars = max(r.stars for r in sorted_repos) or 1

    # Determine column widths
    name_width = max(len(r.full_name) for r in sorted_repos) + 2
    bar_width = 24

    # ── Render ──
    print(LOGO)

    # Top border
    inner = _box_line("═", width - 2)
    print(f"  ╔{inner}╗")
    title = "★  A R E N A   B A T T L E  ★"
    padding = width - 2 - len(title) - 2
    left_pad = padding // 2
    right_pad = padding - left_pad
    print(f"  ║{' ' * left_pad}{BOLD}{title}{RESET}{' ' * right_pad}║")
    print(f"  ╠{inner}╣")

    # Rows
    for i, repo in enumerate(sorted_repos):
        is_winner = (i == 0)
        bar = _bar(repo.stars, max_stars, bar_width)
        stars_str = f"★ {repo.stars:,}"
        bar_line = f"  ║  {repo.full_name:{name_width}} {bar} {stars_str:>10}"
        if is_winner and len(sorted_repos) > 1:
            bar_line += f"  {GREEN}← WINNER! 🏆{RESET}"
        bar_line += f"{' ' * max(0, width - len(bar_line) + 2)}║"
        print(bar_line)

    # Battle result when 2+ repos
    if len(sorted_repos) >= 2:
        winner = sorted_repos[0]
        runner_up = sorted_repos[1]
        diff = winner.stars - runner_up.stars
        print(f"  ╠{inner}╣")
        result = f"  ║  {BOLD}{GREEN}{winner.full_name}{RESET} wins by {diff:,} ★{'s' if diff != 1 else ''}!{' ' * 10}║"

    # Bottom border
    print(f"  ╚{inner}╝")
    print(f"\n  {client.rate_limit_status()}")


def cmd_leaderboard(args: argparse.Namespace):
    """Show leaderboard-style ranking."""
    # Leaderboard relies on cached repos from this session
    # For now, guide users to use `ara battle` instead
    print(f"{LOGO}")
    print(f"  {YELLOW}Leaderboard tracks repos you've recently watched.{RESET}")
    print(f"  Use {BOLD}ara battle{RESET} to compare repos directly.\n")
    print(f"  Quick comparison:")
    print(f"    {CYAN}ara battle li1050109098/alpha-project{RESET}")
    print(f"    {CYAN}ara watch li1050109098/alpha-project{RESET}")
    print()


def cmd_info(args: argparse.Namespace):
    """Show detailed info for a repo."""
    client = GitHubClient()
    info = client.get_repo_info(args.repo)
    if not info:
        print(f"  {RED}Could not fetch info for '{args.repo}'{RESET}")
        sys.exit(1)

    print(LOGO)
    print(f"  {BOLD}{info['full_name']}{RESET}")
    print(f"  {'─' * 40}")
    print(f"    Stars:      {_color_stars(info['stars'])}")
    print(f"    Forks:      ★ {info['forks']:,}")
    print(f"    Language:   {info['language'] or 'N/A'}")
    print(f"    Issues:     {info['open_issues']:,}")
    if info["description"]:
        print(f"    About:      {info['description']}")
    print(f"\n  {client.rate_limit_status()}")

    # Suggest battle
    print(f"\n  {YELLOW}💡 Want to compare?{RESET}")
    print(f"    {CYAN}ara battle {info['full_name']} <other-repo>{RESET}")


# ─── Argument Parser ──────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ara",
        description="Arena Star Tracker — track and compare GitHub Stars",
        epilog="Battle your way to the top! https://github.com/li1050109098/alpha-project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version", action="version", version=f"ARA v{__version__}"
    )

    sub = parser.add_subparsers(dest="command", help="Available commands")

    # stars
    p_stars = sub.add_parser("stars", help="Get current star count for repo(s)")
    p_stars.add_argument("repos", nargs="+", help="Repo(s) as owner/name")

    # watch
    p_watch = sub.add_parser("watch", help="Watch repos in real-time")
    p_watch.add_argument("repos", nargs="+", help="Repo(s) to watch")
    p_watch.add_argument(
        "-i", "--interval", type=int, default=30,
        help="Polling interval in seconds (default: 30)"
    )

    # battle
    p_battle = sub.add_parser("battle", help="Compare repos side-by-side")
    p_battle.add_argument(
        "repos", nargs="+",
        help="Repo(s) to battle (e.g., owner/repo1 owner/repo2)"
    )

    # leaderboard
    sub.add_parser("leaderboard", help="Show ranked leaderboard")

    # info
    p_info = sub.add_parser("info", help="Show detailed repo info")
    p_info.add_argument("repo", help="Repo as owner/name")

    return parser


# ─── Main ─────────────────────────────────────────────────────────────────

def main():
    """Main entry point for the ARA CLI."""
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        print(f"\n{LOGO}")
        print(f"  {BOLD}Quick start:{RESET}")
        print(f"    {CYAN}ara stars li1050109098/alpha-project{RESET}")
        print(f"    {CYAN}ara battle owner/repo1 owner/repo2{RESET}")
        print(f"    {CYAN}ara watch owner/repo{RESET}")
        print(f"    {CYAN}ara info owner/repo{RESET}")
        return

    command_map = {
        "stars": cmd_stars,
        "watch": cmd_watch,
        "battle": cmd_battle,
        "leaderboard": cmd_leaderboard,
        "info": cmd_info,
    }

    command_map[args.command](args)


if __name__ == "__main__":
    main()
