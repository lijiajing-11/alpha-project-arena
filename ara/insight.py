"""ARA insight command — deep repository intelligence.

Provides `ara insight <repo>`:
  - Star velocity (stars/day with emoji label)
  - Repository topics (up to 5)
  - Human-relative timestamps
  - Language, license, description
"""

from datetime import datetime, timezone

from .colors import BOLD, CYAN, GOLD, GRAY, RESET, YELLOW
from .core import GitHubClient

# Reuse trend logic when --trend flag is active
from .trends import compute_trend_buckets, get_star_history, render_trend_chart


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


def compute_influence_score(stars: int, forks: int, open_issues: int) -> float:
    """Compute community influence score.

    Formula: (Stars × 0.5 + Forks × 0.3 + Open Issues × 0.2) / 1000

    >>> round(compute_influence_score(230000, 47000, 1200), 2)
    129.1
    """
    return round((stars * 0.5 + forks * 0.3 + open_issues * 0.2) / 1000, 2)


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
    influence = compute_influence_score(stars, forks, open_issues)

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
        "influence_score": influence,
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


def _render_insight_with_trend(data: dict, events, hours: int, interval: int) -> None:
    """Render insight data followed by a star trend chart.

    Handles the case where trend data is unavailable (e.g. no stargazers)
    gracefully — still shows insight, trend section says "no data".
    """
    _render_insight_text(data)

    if events:
        buckets = compute_trend_buckets(events, hours=hours, interval_minutes=interval)
        chart = render_trend_chart(buckets, data["full_name"])
    else:
        chart = f"  {GRAY}No trend data available for {data['full_name']}{RESET}"

    print()
    print(chart)


def cmd_insight(repo: str, client: GitHubClient, as_json: bool = False, show_trend: bool = False) -> None:
    """Handle `ara insight <repo>` — deep repository insight.

    Args:
        repo: Repository name (owner/repo).
        client: GitHubClient instance.
        as_json: If True, print JSON instead of colored text.
        show_trend: If True, append a star trend chart after the insight.
    """
    data = _build_insight_data(repo, client)
    if as_json:
        import json as _json
        output = _json.dumps(data, indent=2, ensure_ascii=False)
        if show_trend:
            events = get_star_history(client, repo, pages=3)
            buckets = compute_trend_buckets(events)
            trend_data = {
                "buckets": [
                    {"label": b.label, "count": b.count, "delta": b.delta}
                    for b in buckets
                ],
                "total": sum(b.count for b in buckets),
            }
            import json as _json2
            output = _json2.dumps({"insight": data, "trend": trend_data}, indent=2, ensure_ascii=False)
        print(output)
    elif show_trend:
        events = get_star_history(client, repo, pages=3)
        _render_insight_with_trend(data, events, hours=72, interval=60)
    else:
        _render_insight_text(data)


# ===========================================================================
# Compare mode — N-repo comparison with influence ranking
# ===========================================================================


_MEDAL_MAP = {0: "\\U0001f947", 1: "\\U0001f948", 2: "\\U0001f949"}
    """Add influence score if missing and sort descending.

    _build_insight_data already includes influence_score. This ensures
    backward compatibility and sorts.

    Args:
        datas: list of insight data dicts.

    Returns:
        Same list, sorted by influence_score descending.
    """
    for d in datas:
        if "influence_score" not in d:
            d["influence_score"] = compute_influence_score(
                d.get("stars", 0),
                d.get("forks", 0),
                d.get("open_issues", 0),
            )
    datas.sort(key=lambda d: d.get("influence_score", 0), reverse=True)
    return datas


_MEDAL_MAP = {0: "\U0001f947", 1: "\U0001f948", 2: "\U0001f949"}


def _medal(index: int) -> str:
    """Return medal emoji for rank index (0=gold, 1=silver, 2=bronze)."""
    return _MEDAL_MAP.get(index, f"  {index + 1}.")


def _visible_width(s: str) -> int:
    """Return display width of a string without ANSI codes."""
    import re as _re
    return len(_re.sub(r"\033\[[0-9;]*m", "", s))


def _pick_speed_color(label: str) -> str:
    return GOLD if "Hypersonic" in label else (YELLOW if "Rapid" in label or "Steady" in label else GRAY)


def _pick_age_color(age_text: str) -> str:
    return GOLD if "Veteran" in age_text else (CYAN if "Prime" in age_text else GRAY)


def _render_insight_compare_text(datas: list[dict]) -> None:
    """Render N insight data dicts in a single-column ranked list.

    Each repo shows full insight data plus influence score and medal.
    Repos are sorted by influence score descending.

    Args:
        datas: list of dicts from _build_insight_data().
    """
    if not datas:
        return

    datas = _add_influence_to_datas(datas)

    print()
    print(f"  {BOLD}{CYAN}\U0001f3c6 Insight Influence Ranking{RESET}")
    print(f"  {GRAY}{'─' * 50}{RESET}")
    print()

    for idx, data in enumerate(datas):
        medal = _medal(idx)
        name = data["full_name"]
        desc = data.get("description", "")
        stars = data["stars"]
        forks = data["forks"]
        open_issues = data["open_issues"]
        lang = data.get("language", "N/A")
        lic = data.get("license", "None")
        topics = data.get("topics", [])
        created = data.get("created_at", "")[:10] if data.get("created_at") else "N/A"
        updated = data.get("updated_relative", "Unknown")
        influence = data.get("influence_score", 0)

        spd = data["star_velocity"]["per_day"]
        vel_label = data["star_velocity"]["label"]
        age_label = data["repo_age"]["label"]
        age_text = age_label.split(" ", 1)[-1] if " " in age_label else age_label
        age_years = data["repo_age"]["years"]

        speed_color = _pick_speed_color(vel_label)
        age_color = _pick_age_color(age_text)

        # Medal + name
        print(f"  {medal} {BOLD}{CYAN}{name}{RESET}")

        # Description
        if desc:
            print(f"     {GRAY}{desc[:70]}{'...' if len(desc) > 70 else ''}{RESET}")

        # Influence score — gold highlight
        print(f"     {YELLOW}\U0001f4a1 Influence{RESET}: {BOLD}{GOLD}{influence:.2f}{RESET}  "
              f"{YELLOW}\u2605{RESET} {BOLD}{stars:,}{RESET} stars  "
              f"\u2382 {forks:,} forks  \u26a0 {open_issues:,} issues")

        # Velocity + age
        print(f"     +{spd}/day  {speed_color}{vel_label}{RESET}  \u00b7  "
              f"{age_color}\U0001f4c5 {int(age_years)}yo {age_text}{RESET}")

        # Language + license
        print(f"     \u2386 {lang}  \u00a9 {lic}")

        # Topics
        if topics:
            display_topics = [t.capitalize() if t[0].islower() else t for t in topics[:5]]
            print(f"     \U0001f3f7  {' · '.join(display_topics)}")

        # Created + updated
        print(f"     \U0001f4c5 Created {created}  \u00b7 Last updated {updated}")
        print()


def _render_compare_json(datas: list[dict]) -> str:
    """Render insight compare data as JSON string with influence ranking.

    Args:
        datas: list of insight data dicts (2+ repos).

    Returns:
        Pretty-printed JSON string with influence ranking and comparison fields.
    """
    import json as _json

    # Sort by influence_score descending
    sorted_datas = sorted(datas, key=lambda d: d.get("influence_score", 0), reverse=True)

    # Build ranking list
    ranking = [
        {
            "rank": i + 1,
            "full_name": d["full_name"],
            "influence_score": d.get("influence_score", 0),
            "stars": d["stars"],
            "forks": d["forks"],
        }
        for i, d in enumerate(sorted_datas)
    ]

    # Pairwise comparison for exactly 2 repos
    comparison = {}
    if len(sorted_datas) == 2:
        d0, d1 = sorted_datas
        s0, s1 = d0["stars"], d1["stars"]
        v0 = d0["star_velocity"]["per_day"]
        v1 = d1["star_velocity"]["per_day"]
        comparison = {
            "star_leader": d0["full_name"] if s0 >= s1 else d1["full_name"],
            "star_gap": abs(s0 - s1),
            "velocity_leader": d0["full_name"] if v0 >= v1 else d1["full_name"],
            "velocity_ratio": round(max(v0, v1) / max(0.1, min(v0, v1)), 1),
            "younger": d0["full_name"] if d0["repo_age"]["years"] <= d1["repo_age"]["years"] else d1["full_name"],
            "age_gap_years": round(abs(d0["repo_age"]["years"] - d1["repo_age"]["years"]), 1),
        }

    return _json.dumps({
        "command": "insight",
        "mode": "compare",
        "count": len(sorted_datas),
        "repos": sorted_datas,
        "ranking": ranking,
        "comparison": comparison,
    }, indent=2, ensure_ascii=False)


def cmd_insight_compare(repos: list[str], client: GitHubClient, as_json: bool = False) -> None:
    """Handle `ara insight repo1 repo2 ...` — N-repo comparison with influence ranking.

    Args:
        repos: List of repository names (2+ repos for comparison).
        client: GitHubClient instance.
        as_json: If True, print JSON instead of colored text.
    """
    if not repos:
        print("  No repositories specified for comparison.")
        return
    datas = [_build_insight_data(r, client) for r in repos]
    if as_json:
        print(_render_compare_json(datas))
    else:
        _render_insight_compare_text(datas)
