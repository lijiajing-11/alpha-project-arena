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


def cmd_insight(repo: str, client: GitHubClient, as_json: bool = False) -> None:
    """Handle `ara insight <repo>` — deep repository insight.

    Args:
        repo: Repository name (owner/repo).
        client: GitHubClient instance.
        as_json: If True, print JSON instead of colored text.
    """
    data = _build_insight_data(repo, client)
    if as_json:
        import json as _json
        print(_json.dumps(data, indent=2, ensure_ascii=False))
    else:
        _render_insight_text(data)


# ===========================================================================
# Compare mode — side-by-side dual insight
# ===========================================================================


def _render_insight_compare_text(datas: list[dict]) -> None:
    """Render two insight data dicts side-by-side with ANSI colors.

    Each column is exactly COL_WIDTH display characters wide.
    ANSI escape codes are stripped for width calculation but kept for output.

    Args:
        datas: list of dicts from _build_insight_data(), max 2 repos.
    """
    if not datas:
        return

    COL_WIDTH = 44  # per-column display width (excluding the separator region)

    def _pick_speed_color(label: str) -> str:
        return GOLD if "Hypersonic" in label else (YELLOW if "Rapid" in label or "Steady" in label else GRAY)

    def _pick_age_color(age_text: str) -> str:
        return GOLD if "Veteran" in age_text else (CYAN if "Prime" in age_text else GRAY)

    def _visible_width(s: str) -> int:
        """Return display width of a string without ANSI codes."""
        import re as _re
        return len(_re.sub(r"\033\[[0-9;]*m", "", s))

    # Build per-column (plain_text, ansi_text) pairs for each line
    columns_plain: list[list[str]] = []
    columns_ansi: list[list[str]] = []

    for data in datas:
        plain_lines: list[str] = []
        ansi_lines: list[str] = []

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

        spd = data["star_velocity"]["per_day"]
        vel_label = data["star_velocity"]["label"]
        age_label = data["repo_age"]["label"]
        age_text = age_label.split(" ", 1)[-1] if " " in age_label else age_label
        age_years = data["repo_age"]["years"]

        speed_color = _pick_speed_color(vel_label)
        age_color = _pick_age_color(age_text)

        # Line 1: repo name — cyan + bold
        ansi_name = f"{BOLD}{CYAN}{name}{RESET}"
        plain_lines.append(name)
        ansi_lines.append(ansi_name)

        # Line 2: description — gray, truncated
        desc_short = (desc[:COL_WIDTH - 3] + "...") if len(desc) > COL_WIDTH else desc
        if desc_short:
            plain_lines.append(f"  {desc_short}")
            ansi_lines.append(f"  {GRAY}{desc_short}{RESET}")
        else:
            plain_lines.append("")
            ansi_lines.append("")

        # Line 3: blank
        plain_lines.append("")
        ansi_lines.append("")

        # Line 4: stars + velocity — with speed color on label
        plain_vel = f"\u2605 {stars:,} stars  \u00b7 +{spd}/day  {vel_label}"
        ansi_vel = f"\u2605 {BOLD}{stars:,}{RESET} stars  \u00b7 +{spd}/day  {speed_color}{vel_label}{RESET}"
        plain_lines.append(plain_vel)
        ansi_lines.append(ansi_vel)

        # Line 5: forks + issues — with cyan on fork/issue numbers
        plain_fork = f"\u2382 {forks:,} forks  \u00b7 \u26a0 {open_issues:,} open issues"
        ansi_fork = f"\u2382 {CYAN}{forks:,}{RESET} forks  \u00b7 \u26a0 {open_issues:,} open issues"
        plain_lines.append(plain_fork)
        ansi_lines.append(ansi_fork)

        # Line 6: language + license + age — with age color
        age_display = f"{int(age_years)}yo {age_text}"
        plain_age = f"\u2386 {lang}  \u00a9 {lic}  \U0001f4c5 {age_display}"
        ansi_age = f"\u2386 {lang}  \u00a9 {lic}  \U0001f4c5 {age_color}{age_display}{RESET}"
        plain_lines.append(plain_age)
        ansi_lines.append(ansi_age)

        # Line 7: topics — emoji only
        if topics:
            display_topics = [t.capitalize() if t[0].islower() else t for t in topics[:5]]
            topics_display = " \u00b7 ".join(display_topics)
        else:
            topics_display = "None"
        plain_topics = f"\U0001f3f7  {topics_display}"
        ansi_topics = f"\U0001f3f7  {GRAY}{topics_display}{RESET}"
        plain_lines.append(plain_topics)
        ansi_lines.append(ansi_topics)

        # Line 8: created + updated — gray
        plain_time = f"\U0001f4c5 Created {created}  \u00b7 Last updated {updated}"
        ansi_time = f"\U0001f4c5 Created {GRAY}{created}{RESET}  \u00b7 Last updated {GRAY}{updated}{RESET}"
        plain_lines.append(plain_time)
        ansi_lines.append(ansi_time)

        columns_plain.append(plain_lines)
        columns_ansi.append(ansi_lines)

    # Normalise line counts
    max_lines = max(max(len(c) for c in columns_plain), 1)
    for i in range(len(columns_plain)):
        while len(columns_plain[i]) < max_lines:
            columns_plain[i].append("")
            columns_ansi[i].append("")

    print()
    for i in range(max_lines):
        left_plain = columns_plain[0][i]
        right_plain = columns_plain[1][i] if len(columns_plain) > 1 else ""
        left_ansi = columns_ansi[0][i]
        right_ansi = columns_ansi[1][i] if len(columns_ansi) > 1 else ""

        # Pad each side to COL_WIDTH using plain-text width to keep alignment
        left_pad = COL_WIDTH - _visible_width(left_plain)
        right_pad = COL_WIDTH - _visible_width(right_plain)
        left_out = left_ansi + (" " * max(0, left_pad))
        right_out = right_ansi + (" " * max(0, right_pad))

        print(f"  {left_out}  \u2502  {right_out}")

    # Comparison summary footer
    print()
    print(f"  {'═' * 30}  COMPARISON  {'═' * 30}")
    print()

    d0 = datas[0]
    d1 = datas[1] if len(datas) > 1 else datas[0]

    # Star gap
    s0 = d0["stars"]
    s1 = d1["stars"]
    star_leader = d0["full_name"] if s0 >= s1 else d1["full_name"]
    star_gap = abs(s0 - s1)
    print(f"  \u2605 Star gap: {BOLD}{CYAN}{star_leader}{RESET} leads by {BOLD}{star_gap:,}{RESET} \u2605")

    # Velocity ratio
    v0 = d0["star_velocity"]["per_day"]
    v1 = d1["star_velocity"]["per_day"]
    v_leader = d0["full_name"] if v0 >= v1 else d1["full_name"]
    v_ratio = round(max(v0, v1) / max(0.1, min(v0, v1)), 1)
    print(f"  \U0001f525 Velocity: {BOLD}{CYAN}{v_leader}{RESET} is {BOLD}{v_ratio}\u00d7{RESET} faster ({v0:.1f} vs {v1:.1f}/day)")

    # Age gap
    a0 = d0["repo_age"]["years"]
    a1 = d1["repo_age"]["years"]
    age_gap = round(abs(a0 - a1), 1)
    younger = d0["full_name"] if a0 <= a1 else d1["full_name"]
    print(f"  \U0001f4c5 Age gap: {BOLD}{CYAN}{younger}{RESET} is {BOLD}{age_gap}{RESET} years younger")

    # Topic overlap
    t0 = set(t.lower() for t in d0.get("topics", []))
    t1 = set(t.lower() for t in d1.get("topics", []))
    overlap = t0 & t1
    if overlap:
        print(f"  \U0001f3f7 Topic overlap: {BOLD}{len(overlap)}{RESET} shared ({GRAY}{', '.join(sorted(overlap))}{RESET})")
    else:
        print(f"  \U0001f3f7 Topic overlap: {GRAY}0 shared topics{RESET}")

    print()


def _render_compare_json(datas: list[dict]) -> str:
    """Render insight compare data as JSON string.

    Args:
        datas: list of insight data dicts.

    Returns:
        Pretty-printed JSON string with comparison fields.
    """
    import json as _json

    if len(datas) == 2:
        d0, d1 = datas
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
    else:
        comparison = {}

    return _json.dumps({
        "command": "insight",
        "mode": "compare",
        "repos": datas,
        "comparison": comparison,
    }, indent=2, ensure_ascii=False)


def cmd_insight_compare(repos: list[str], client: GitHubClient, as_json: bool = False) -> None:
    """Handle `ara insight repo1 repo2 ...` (2 repos only) — side-by-side compare.

    Args:
        repos: List of repository names (only first 2 used).
        client: GitHubClient instance.
        as_json: If True, print JSON instead of colored text.
    """
    datas = [_build_insight_data(r, client) for r in repos[:2]]
    if as_json:
        print(_render_compare_json(datas))
    else:
        _render_insight_compare_text(datas)
