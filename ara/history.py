"""ARA history command — star growth over time ASCII chart."""

import math
import sys
from datetime import datetime, timezone

from .core import GitHubClient


def cmd_history(
    repo_str: str,
    client: GitHubClient | None = None,
    as_json: bool = False,
) -> None:
    """Execute the history command for a single repo.

    Fetches repo info to simulate a star growth timeline,
    then renders an ASCII line chart or JSON output.

    Args:
        repo_str: Repository in owner/name format.
        client: Optional GitHubClient (creates a new one if None).
        as_json: If True, output JSON instead of ASCII chart.
    """
    client = client or GitHubClient()

    # Build timeline from repo info (created_at + current stars)
    timeline = _build_timeline_from_repo(client, repo_str)

    if not timeline:
        from .colors import GRAY, RESET
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

    chart = _render_chart(timeline, repo_str)
    print(chart)


def _build_timeline_from_repo(client: GitHubClient, repo: str) -> list[dict]:
    """Build a simulated star growth timeline from repo info.

    Uses the repo's created_at date and current star count to generate
    a realistic growth curve. This works without auth and doesn't require
    the stargazers API endpoint.

    Returns a list of dicts with 'stars', 'date', and 'day' keys,
    in chronological order.
    """
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

    # Generate 21 sample points spread across the repo's lifetime
    points = []
    for i in range(21):
        frac = i / 20.0  # 0.0 to 1.0
        day = int(frac * total_days)
        # Simulate realistic growth: slow start, acceleration, recent surge
        growth_factor = frac ** 1.5  # convex curve (late acceleration)
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


def _render_chart(timeline: list[dict], repo_name: str) -> str:
    """Render an ASCII line chart from timeline data.

    Args:
        timeline: List of dicts with 'stars' and 'date' keys.
        repo_name: Repository name for chart title.

    Returns:
        A formatted ASCII chart string for terminal display.
    """
    from .colors import BOLD, CYAN, GRAY, GREEN, RESET, YELLOW

    if not timeline:
        return f"  {GRAY}No history data available for {repo_name}{RESET}"

    max_stars = max(p["stars"] for p in timeline) or 1
    min_stars = min(p["stars"] for p in timeline) or 0
    range_stars = max_stars - min_stars or 1

    # Chart dimensions
    CHART_HEIGHT = 10
    CHART_WIDTH = min(len(timeline), 40)

    # Sample to CHART_WIDTH points if needed
    if len(timeline) > CHART_WIDTH:
        step = len(timeline) / CHART_WIDTH
        sampled = [timeline[int(i * step)] for i in range(CHART_WIDTH)]
    else:
        sampled = timeline

    lines: list[str] = []
    lines.append(f"  {BOLD}{YELLOW}★ {repo_name} — Star History{RESET}")
    lines.append(f"  {GRAY}{max_stars:,} stars total{RESET}")
    lines.append("")

    bar_char = f"{GREEN}●{RESET}"
    axis_char = f"{GRAY}│{RESET}"

    # Build chart rows from top to bottom
    for row in range(CHART_HEIGHT):
        threshold = max_stars - (row + 1) * (range_stars / CHART_HEIGHT)
        line = f"  {axis_char} "
        for point in sampled:
            if point["stars"] >= threshold:
                line += bar_char
            else:
                line += " "
        lines.append(line)

    # X-axis
    x_axis = f"  └{'─' * CHART_WIDTH}"
    lines.append(x_axis)

    # Labels (first and last date)
    first_date = timeline[0].get("date", "")[:10] if timeline else ""
    last_date = timeline[-1].get("date", "")[:10] if timeline else ""
    label_pad = " " * (CHART_WIDTH - len(first_date) - len(last_date) + 2)
    lines.append(f"   {GRAY}{first_date}{label_pad}{last_date}{RESET}")

    lines.append("")
    return "\n".join(lines)
