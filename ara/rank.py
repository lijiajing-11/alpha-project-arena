"""ARA Rank command — show ranked GitHub repos by star count.

Provides:
- fetch_all_repos(): Fetch info for a list of repos, sorted by stars desc
- format_rank_table(): Render results as a box-drawing ASCII table
- cmd_rank: CLI handler for `ara rank`
- cmd_rank_json: CLI handler for `ara rank --json`
"""

import json as _json

from ara.colors import BOLD, CYAN, GREEN, RESET, YELLOW

DEFAULT_REPOS = [
    "facebook/react",
    "vuejs/core",
    "vercel/next.js",
    "twbs/bootstrap",
    "sveltejs/svelte",
    "angular/angular",
    "d3/d3",
    "nodejs/node",
    "lodash/lodash",
    "jquery/jquery",
]


def _format_stars(n: int) -> str:
    """Format star count: N,NNN or Nk for display."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n:,}"
    return str(n)


def _format_forks(n: int) -> str:
    """Format fork count compactly."""
    if n >= 1_000:
        return f"{n // 1000}k"
    return str(n)


def fetch_all_repos(client, repos: list[str]) -> tuple[list[dict], list[dict]]:
    """Fetch info for all repos, return (sorted_results, errors).

    Args:
        client: GitHubClient instance.
        repos: List of repo names (owner/name).

    Returns:
        Tuple of (results_sorted_by_stars_desc, error_dicts).
    """
    results = []
    errors = []
    for repo in repos:
        try:
            info = client.get_repo_info(repo)
            results.append(info)
        except (ValueError, RuntimeError) as e:
            errors.append({"repo": repo, "error": str(e)})

    results.sort(key=lambda x: x.get("stars", 0), reverse=True)
    return results, errors


def format_rank_table(results: list[dict], top_n: int = 10) -> str:
    """Format ranked repo results as an ASCII box-drawing table.

    Args:
        results: List of repo info dicts (sorted by stars descending).
        top_n: Max number of repos to display.

    Returns:
        Formatted table string with box-drawing characters.
    """
    displayed = results[:top_n]
    if not displayed:
        return "No repo data available."

    # Column widths
    rank_w = 3
    repo_w = max(len(r.get("full_name", "")) for r in displayed) if displayed else 28
    repo_w = max(repo_w, 28)
    stars_w = 10
    forks_w = 7
    lang_w = max(len(r.get("language", "") or "") for r in displayed) if displayed else 10
    lang_w = max(lang_w, 10)

    col_widths = [rank_w, repo_w, stars_w, forks_w, lang_w]

    def _sep(char_left="├", char_mid="┼", char_right="┤"):
        parts = [char_left]
        for i, w in enumerate(col_widths):
            parts.append("─" * (w + 2))
            parts.append(char_mid if i < len(col_widths) - 1 else char_right)
        return "".join(parts)

    top_line = "┌" + _sep("┬")[1:-1].replace("┼", "┬") + "┐"
    header_line = (
        f"│ {'#'.ljust(rank_w)} "
        f"│ {'Repo'.ljust(repo_w)} "
        f"│ {'Stars'.rjust(stars_w)} "
        f"│ {'Forks'.rjust(forks_w)} "
        f"│ {'Language'.ljust(lang_w)} │"
    )
    sep_line = _sep()
    bot_line = "└" + _sep("┴")[1:-1].replace("┼", "┴") + "┘"

    lines = [top_line, header_line, sep_line]

    for i, info in enumerate(displayed, 1):
        name = info.get("full_name", "")
        stars = info.get("stars", 0)
        forks = info.get("forks", 0)
        lang = info.get("language") or "—"

        stars_str = _format_stars(stars).rjust(stars_w)
        forks_str = _format_forks(forks).rjust(forks_w)

        rank_str = str(i).rjust(rank_w)
        if i == 1:
            rank_str = f"{GREEN}🥇{RESET} 1".rjust(rank_w + 6)
        elif i == 2:
            rank_str = f"🥈 2".rjust(rank_w + 4)
        elif i == 3:
            rank_str = f"🥉 3".rjust(rank_w + 4)

        row = (
            f"│ {rank_str:<{rank_w + 5 if i <= 3 else 0}} "
            f"│ {name:<{repo_w}} "
            f"│ {stars_str} "
            f"│ {forks_str} "
            f"│ {lang:<{lang_w}} │"
        )
        lines.append(row)

    lines.append(bot_line)

    return "\n".join(lines)


def cmd_rank(args, client):
    """Handle `ara rank [--top N]` — show ranking table."""
    repos = args.repos if args.repos else DEFAULT_REPOS
    top_n = args.top

    results, errors = fetch_all_repos(client, repos)
    table = format_rank_table(results, top_n)

    print(f"\n{BOLD}{CYAN}🏆 ARA Rank — Top {min(len(results), top_n)} Hot Repos{RESET}\n")
    print(table)
    print()

    if errors:
        print(f"{YELLOW}⚠ Errors fetching some repos:{RESET}")
        for err in errors:
            print(f"  {err['repo']}: {err['error']}")


def cmd_rank_json(args, client):
    """Handle `ara rank --json [--top N]` — return ranking as JSON."""
    repos = args.repos if args.repos else DEFAULT_REPOS
    top_n = args.top

    results, errors = fetch_all_repos(client, repos)
    results = results[:top_n]

    # Assign ranks
    ranked = []
    for i, info in enumerate(results, 1):
        info["rank"] = i
        ranked.append(info)

    output = {
        "command": "rank",
        "top": top_n,
        "repos": ranked,
        "errors": errors or None,
    }
    print(_json.dumps(output, indent=2, ensure_ascii=False))
