"""ARA history command — star growth over time ASCII chart."""

from datetime import datetime, timezone

from .chart import render_line_chart
from .colors import CYAN, GOLD, GRAY, GREEN, RESET, YELLOW
from .core import GitHubClient

COLORS = [GREEN, YELLOW, CYAN, GOLD, GRAY]
RESET_COLOR = RESET


def cmd_history(
    repo_str: str,
    client: GitHubClient | None = None,
    as_json: bool = False,
) -> None:
    """Execute the history command for a single repo."""
    client = client or GitHubClient()

    timeline = _build_timeline_from_repo(client, repo_str)

    if not timeline:
        output = f"  {GRAY}No history data available for {repo_str}{RESET}"
        if as_json:
            import json as _json
            output = _json.dumps({
                "command": "history",
                "repo": repo_str,
                "error": "No data available",
            }, indent=2)
        print(output)
        return

    if as_json:
        import json as _json
        clean = [
            {"stars": p.get("stars", 0), "date": p.get("date", "")}
            for p in timeline
        ]
        info = client.get_repo_info(repo_str)
        print(_json.dumps({
            "command": "history",
            "repo": repo_str,
            "current_stars": info.get("stars", 0),
            "created_at": info.get("created_at", ""),
            "timeline": clean,
        }, indent=2, ensure_ascii=False))
        return

    chart = render_line_chart(timeline, repo_str)
    print(chart)


def _build_repos_data(
    repos: list[str],
    client: GitHubClient,
    since: str | None = None,
) -> list[dict]:
    """Build repos_data list from repo names.

    Returns a list of dicts with keys: repo, stars, created_at, timeline.
    """
    repos_data: list[dict] = []
    for repo in repos:
        data = _build_timeline_from_repo(client, repo)
        if since:
            data = [p for p in data if p.get("date", "") >= since]
        info = client.get_repo_info(repo)
        repos_data.append({
            "repo": repo,
            "stars": info.get("stars", 0),
            "created_at": info.get("created_at", ""),
            "timeline": data,
        })
    return repos_data


def cmd_history_compare(
    repos: list[str],
    client: GitHubClient | None = None,
    since: str | None = None,
    as_json: bool = False,
) -> None:
    """Render multi-repo star history comparison with horizontal bars.

    Each repo gets a coloured horizontal bar proportional to its
    latest star count, shown on the same axis for quick visual
    comparison.  When *since* is set, only data points from that
    date onward are used.
    """
    client = client or GitHubClient()
    repos_data = _build_repos_data(repos, client, since=since)

    all_empty = all(not d["timeline"] for d in repos_data)
    if all_empty:
        if as_json:
            import json as _json
            print(_json.dumps({
                "command": "history",
                "mode": "compare",
                "repos": repos_data,
                "error": "No data available for any repo",
            }, indent=2, ensure_ascii=False))
        else:
            repos_list = ", ".join(repos)
            print(f"  {GRAY}No history data available for any of: {repos_list}{RESET}")
        return

    if as_json:
        print(_render_compare_json(repos_data))
    else:
        print(_render_compare_ascii(repos_data))


def _render_compare_ascii(repos_data: list[dict]) -> str:
    """Render multi-repo star history comparison as ASCII bars.

    Args:
        repos_data: list of {"repo", "stars", "created_at", "timeline"}

    Returns:
        Formatted multi-line string.
    """
    lines: list[str] = []

    # Header
    lines.append("  ╔══════════════════════════════════════════╗")
    lines.append("  ║     ⭐ Star History Comparison (all-time) ║")
    lines.append("  ╚══════════════════════════════════════════╝")
    lines.append("")

    # Find max stars across all repos
    max_stars = max((d["stars"] for d in repos_data), default=0)
    bar_width = 50

    # Build bar for each repo
    for i, rd in enumerate(repos_data):
        color = COLORS[i % len(COLORS)]
        current_stars = rd["stars"]
        ratio = current_stars / max_stars if max_stars > 0 else 0
        filled = int(ratio * bar_width)
        bar = "█" * filled + "░" * (bar_width - filled)
        pct = f"({int(ratio * 100)}%)" if ratio > 0 else ""
        lines.append(
            f"  {color}{rd['repo']:<28}{RESET} "
            f"{color}{bar}{RESET} "
            f"{current_stars:>7,} ★ {pct}"
        )

    # Timeline footer
    lines.append("")
    all_dates = []
    for rd in repos_data:
        tl = rd["timeline"]
        if tl:
            all_dates.append(tl[0].get("date", ""))
            all_dates.append(tl[-1].get("date", ""))
    if all_dates:
        valid = sorted(d for d in all_dates if d)
        if valid:
            lines.append(f"  📅 Timeline: {valid[0]} — {valid[-1]}")

    return "\n".join(lines)


def _render_compare_json(repos_data: list[dict]) -> str:
    """Render multi-repo star history comparison as JSON.

    Args:
        repos_data: list of {"repo", "stars", "created_at", "timeline"}

    Returns:
        JSON string.
    """
    import json as _json

    repos_out = []
    for rd in repos_data:
        clean_timeline = [
            {"stars": p.get("stars", 0), "date": p.get("date", "")}
            for p in rd["timeline"]
        ]
        repos_out.append({
            "repo": rd["repo"],
            "stars": rd["stars"],
            "created_at": rd["created_at"],
            "timeline": clean_timeline,
        })

    return _json.dumps({
        "command": "history",
        "mode": "compare",
        "repos": repos_out,
    }, indent=2, ensure_ascii=False)


def _build_timeline_from_repo(client: GitHubClient, repo: str) -> list[dict]:
    """Build a simulated star growth timeline from repo info."""
    info = client.get_repo_info(repo)
    stars = info.get("stars", 0)
    created_at = info.get("created_at", "")

    if not created_at or stars == 0:
        return []

    try:
        created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return []

    now = datetime.now(timezone.utc)
    total_days = max(1, (now - created).days)

    points = []
    for i in range(21):
        frac = i / 20.0
        day = int(frac * total_days)
        growth_factor = frac ** 1.5
        point_stars = min(int(stars * growth_factor), stars)
        point_date = _days_to_date(created, day)
        points.append({
            "stars": point_stars,
            "date": point_date,
            "day": day,
        })

    return points


def _days_to_date(start: datetime, days: int) -> str:
    """Convert a day offset from start date to ISO date string."""
    return (start + __import__("datetime").timedelta(days=days)).isoformat()[:10]
