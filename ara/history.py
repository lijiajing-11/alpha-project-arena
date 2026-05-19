"""ARA history command — star growth over time ASCII chart."""

from datetime import datetime, timezone

from .chart import render_line_chart
from .core import GitHubClient


def cmd_history(
    repo_str: str,
    client: GitHubClient | None = None,
    as_json: bool = False,
) -> None:
    """Execute the history command for a single repo."""
    client = client or GitHubClient()

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

    chart = render_line_chart(timeline, repo_str)
    print(chart)


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
