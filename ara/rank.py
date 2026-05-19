"""ARA Rank command — show ranked GitHub repos by star count.

Provides:
- cmd_rank: Display a box-drawing ranking table of top repos
- cmd_rank_json: Return ranking data as JSON
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


def cmd_rank(args, client):
    """Handle `ara rank [--top N]` — show ranking table."""
    repos = args.repos if hasattr(args, "repos") and args.repos else DEFAULT_REPOS
    top_n = args.top

    # Fetch info for each repo
    results = []
    errors = []
    for repo in repos:
        try:
            info = client.get_repo_info(repo)
            results.append(info)
        except (ValueError, RuntimeError) as e:
            errors.append({"repo": repo, "error": str(e)})

    # Sort by stars descending
    results.sort(key=lambda x: x.get("stars", 0), reverse=True)

    # Limit to top N
    results = results[:top_n]

    # Print header
    print(f"\n{BOLD}{CYAN}🏆 ARA Rank — Top {len(results)} Hot Repos{RESET}\n")

    # Determine column widths
    rank_w = 3
    repo_w = max(len(r.get("full_name", "")) for r in results) if results else 30
    repo_w = max(repo_w, 28)
    stars_w = 10
    forks_w = 7
    lang_w = max(len(r.get("language", "") or "") for r in results) if results else 10
    lang_w = max(lang_w, 10)

    # Build table
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

    print(top_line)
    print(header_line)
    print(sep_line)

    for i, info in enumerate(results, 1):
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
        print(row)

    print(bot_line)
    print()

    if errors:
        print(f"{YELLOW}⚠ Errors fetching some repos:{RESET}")
        for err in errors:
            print(f"  {err['repo']}: {err['error']}")


def cmd_rank_json(args, client):
    """Handle `ara rank --json [--top N]` — return ranking as JSON."""
    repos = args.repos if hasattr(args, "repos") and args.repos else DEFAULT_REPOS
    top_n = args.top

    results = []
    errors = []
    for repo in repos:
        try:
            info = client.get_repo_info(repo)
            results.append(info)
        except (ValueError, RuntimeError) as e:
            errors.append({"repo": repo, "error": str(e)})

    # Sort by stars descending
    results.sort(key=lambda x: x.get("stars", 0), reverse=True)
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
