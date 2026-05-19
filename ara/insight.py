"""ARA insight command — deep repository intelligence.

Provides `ara insight <repo>`:
  - Star velocity (stars/day with emoji label)
  - Repository topics (up to 5)
  - Human-relative timestamps
  - Language, license, description
"""

from datetime import datetime, timezone

from .colors import BOLD, CYAN, RESET, YELLOW

GRAY = "\033[90m"
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


def cmd_insight(repo_str: str):
    """Execute the insight command for a single repo."""
    client = GitHubClient()
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
    topics_display = ", ".join(topics[:5]) if topics else "None"

    # ── Render ──
    print()

    # Header
    print(f"  {BOLD}{CYAN}{full_name}{RESET}  {GRAY}\u2014 Insight{RESET}")
    if description:
        print(f"  {GRAY}{description}{RESET}")
        print()

    # Stars + velocity
    print(f"  {YELLOW}\u2605{RESET} {BOLD}{stars:,}{RESET} stars  \u00b7  {spd}/day  {speed_label}")
    print(f"  {CYAN}\u2382{RESET} {forks:,} forks  \u00b7  \u26a0 {open_issues:,} open issues")

    lang_str = language or "N/A"
    lic_str = license_name or "None"
    print(f"  {GRAY}\u2386{RESET} {lang_str}  \u00b7  {GRAY}\u00a9{RESET} {lic_str}")

    print(f"  \U0001f3f7  {topics_display}")

    created_short = created_at[:10] if created_at else "N/A"
    print(f"  {GRAY}\U0001f4c5{RESET} Created {created_short}  \u00b7  Last updated {updated_rel}")
    print()
