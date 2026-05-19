"""ARA insight command — deep repository intelligence.

Provides `ara insight <repo>`:
  - Star velocity (stars/day with emoji label)
  - Repository topics (up to 5)
  - Human-relative timestamps
  - Language, license, description
"""

from datetime import datetime, timezone

from .colors import BOLD, CYAN, GOLD, GRAY, GREEN, RESET, YELLOW

from .core import GitHubClient


def compute_star_velocity(stars: int, created_at: str) -> tuple:
    """Return (stars_per_day, label) where label is emoji + text.

    >>> spd, label = compute_star_velocity(50000, "2025-01-01T00:00:00Z")
    >>> "Hypersonic" in label
    True
    """
    if not created_at:
        return (0.0, "\U0001f525 Unknown")

    try:
        raw = created_at.replace("Z", "+00:00")
        created = datetime.fromisoformat(raw)
        days = max(1, (datetime.now(timezone.utc) - created).days)
        spd = stars / days
    except (ValueError, TypeError):
        return (0.0, "\U0001f525 Unknown")

    if spd > 50:
        label = "\U0001f680 Hypersonic"
    elif spd > 10:
        label = "\U0001f525 Rapid"
    elif spd > 1:
        label = "\U0001f4ca Steady"
    else:
        label = "\U0001f422 Stale"

    return (round(spd, 1), label)


def compute_repo_age(created_at: str) -> tuple[float, str]:
    """Return (years, label) based on how many years since repo creation.

    >>> yrs, label = compute_repo_age(\"2013-05-29T21:12:00Z\")
    >>> yrs >= 12
    True
    """
    if not created_at:
        return (0, "\U0001f914 Unknown")

    try:
        raw = created_at.replace("Z", "+00:00")
        created = datetime.fromisoformat(raw)
        now = datetime.now(timezone.utc)
        years = max(0, (now - created).days / 365.0)
    except (ValueError, TypeError):
        return (0, "\U0001f914 Unknown")

    if years < 1:
        label = "\U0001f476 Newborn"
    elif years < 3:
        label = "\U0001f476 Teen"
    elif years < 7:
        label = "\U0001f451 Prime"
    else:
        label = "\U0001f3c6 Veteran"

    return (round(years, 1), label)


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
    age_years, age_label = compute_repo_age(created_at)
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
        "repo_age": {"years": age_years, "label": age_label},
        "created_at": created_at,
        "updated_at": updated_at,
        "updated_relative": updated_rel,
    }


def _render_insight_text(data: dict) -> None:
    """Render insight data as colored text output with speed tags, age tags, and enhanced topics."""
    print()
    print(f"  {BOLD}{CYAN}{data['full_name']}{RESET}  {GRAY}\u2014 Insight{RESET}")
    if data["description"]:
        print(f"  {GRAY}{data['description']}{RESET}")
        print()

    spd = data["star_velocity"]["per_day"]
    label = data["star_velocity"]["label"]

    # Speed label with color: 🚀 = gold, 🔥/📊 = yellow, 🐢 = gray
    speed_color = GOLD if "Hypersonic" in label else (YELLOW if "Rapid" in label or "Steady" in label else GRAY)
    print(f"  {YELLOW}\u2605{RESET} {BOLD}{data['stars']:,}{RESET} stars  \u00b7  +{spd}/day  {speed_color}{label}{RESET}")

    print(f"  {CYAN}\u2382{RESET} {data['forks']:,} forks  \u00b7  \u26a0 {data['open_issues']:,} open issues")

    lang_str = data["language"]
    lic_str = data["license"]

    # Age label with color — strip emoji prefix from label, add 📅
    age_label = data["repo_age"]["label"]
    age_years = data["repo_age"]["years"]
    # Strip emoji from label: "🏆 Veteran" -> "Veteran", "👶 Newborn" -> "Newborn"
    age_text = age_label.split(" ", 1)[-1] if " " in age_label else age_label
    age_color = GOLD if "Veteran" in age_text else (CYAN if "Prime" in age_text else GRAY)
    age_display = f"{int(age_years)}yo {age_text}"

    print(f"  {GRAY}\u2386{RESET} {lang_str}  \u00b7  {GRAY}\u00a9{RESET} {lic_str}  \u00b7  {age_color}\U0001f4c5 {age_display}{RESET}")

    # Enhanced topics display — comma-separated, no # prefix, capitalize
    topics_list = data["topics"]
    if topics_list:
        display_topics = [t.capitalize() if t[0].islower() else t for t in topics_list]
        topics_display = " \u00b7 ".join(display_topics)
    else:
        topics_display = "None"
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
