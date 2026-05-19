"""ARA insight command — deep repository intelligence.

Provides `ara insight <repo>`:
  - Star velocity (stars/day with emoji label)
  - Repository topics (up to 5)
  - Human-relative timestamps
  - Language, license, description
"""

from datetime import datetime, timezone

from .colors import BOLD, CYAN, GRAY, RESET, YELLOW

from .core import GitHubClient


def compute_star_velocity(stars: int, created_at: str) -> tuple:
    """Return (stars_per_day, label) where label is emoji + text.

    >>> spd, label = compute_star_velocity(50000, "2025-01-01T00:00:00Z")
    >>> "Hypersonic" in label
    True
    """
    if not created_at:
        return (0.0, "\U0001f4a4 Unknown")

    try:
        raw = created_at.replace("Z", "+00:00")
        created = datetime.fromisoformat(raw)
        days = max(1, (datetime.now(timezone.utc) - created).days)
        spd = stars / days
    except (ValueError, TypeError):
        return (0.0, "\U0001f4a4 Unknown")

    if spd > 50:
        label = "\U0001f525 Hypersonic"
    elif spd > 10:
        label = "\U0001f4c8 Rapid"
    elif spd > 3:
        label = "\U0001f4ca Steady"
    elif spd > 0.5:
        label = "\U0001f4a4 Slow"
    else:
        label = "\U0001faa6 Stale"

    return (round(spd, 1), label)


def relative_time(iso_date: str) -> str:
    """Convert ISO date string to human-readable relative time.

    >>> relative_time(datetime.now(timezone.utc).isoformat())
    'Today'
    """
    if not iso_date:
        return "Unknown"
    try:
        dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        diff = now - dt
        days = diff.days
        if days < 0:
            return "Future?"
        if days == 0:
            return "Today"
        if days == 1:
            return "Yesterday"
        if days < 30:
            return f"{days} days ago"
        if days < 365:
            mo = days // 30
            return f"{mo} month{'s' if mo > 1 else ''} ago"
        yr = days // 365
        return f"{yr} year{'s' if yr > 1 else ''} ago"
    except (ValueError, TypeError):
        return "Unknown"


def _build_insight_data(repo_str: str, client: GitHubClient) -> dict:
    """Build insight data dict from a repo string."""
    repo = client.get_repo_info(repo_str)

    stars = repo.get("stars", 0)
    forks = repo.get("forks", 0)
    open_issues = repo.get("open_issues", 0)
    language = repo.get("language")
    license_name = repo.get("license")
    topics = repo.get("topics", [])
    description = repo.get("description", "")
    created_at = repo.get("created_at", "")
    updated_at = repo.get("updated_at", "")
    full_name = repo.get("full_name", repo_str)

    spd, speed_label = compute_star_velocity(stars, created_at)
    updated_rel = relative_time(updated_at)

    return {
        "full_name": full_name,
        "description": description,
        "stars": stars,
        "forks": forks,
        "open_issues": open_issues,
        "language": language or "N/A",
        "license": license_name or "None",
        "topics": topics[:5],
        "star_velocity": {"per_day": spd, "label": speed_label},
        "created_at": created_at,
        "updated_at": updated_at,
        "updated_relative": updated_rel,
    }


def _render_insight_text(data: dict) -> None:
    """Render insight data as colored text output."""
    print()
    print(f"  {BOLD}{CYAN}{data['full_name']}{RESET}  {GRAY}\u2014 Insight{RESET}")
    if data["description"]:
        print(f"  {GRAY}{data['description']}{RESET}")
        print()

    spd = data["star_velocity"]["per_day"]
    label = data["star_velocity"]["label"]
    print(f"  {YELLOW}\u2605{RESET} {BOLD}{data['stars']:,}{RESET} stars  \u00b7  {spd}/day  {label}")
    print(f"  {CYAN}\u2382{RESET} {data['forks']:,} forks  \u00b7  \u26a0 {data['open_issues']:,} open issues")
    lang_str = data["language"]
    lic_str = data["license"]
    print(f"  {GRAY}\u2386{RESET} {lang_str}  \u00b7  {GRAY}\u00a9{RESET} {lic_str}")

    topics_display = ", ".join(data["topics"]) if data["topics"] else "None"
    print(f"  \U0001f3f7  {topics_display}")

    created_short = data["created_at"][:10] if data["created_at"] else "N/A"
    print(f"  {GRAY}\U0001f4c5{RESET} Created {created_short}  \u00b7  Last updated {data['updated_relative']}")
    print()


def cmd_insight(args, client: GitHubClient):
    """Handle `ara insight <repo>` — deep repository insight."""
    data = _build_insight_data(args.repo, client)
    _render_insight_text(data)


def cmd_insight_json(args, client: GitHubClient):
    """Handle `ara insight --json <repo>`."""
    repo = args.repo
    data = _build_insight_data(repo, client)
    import json as _json
    print(_json.dumps(data, indent=2, ensure_ascii=False))
