"""Display utilities for ARA watch command.

Provides formatting functions for:
- Delta display (+5, -3, 0)
- ANSI color coding
- Watch summary
- Multi-repo watch display
- Repo info details
- Repo comparison table
"""

from datetime import datetime

from ara.colors import BOLD, CYAN, GRAY, GREEN, RED, RESET, YELLOW


def format_delta(current: int, previous: int) -> str:
    """Format the delta between two star counts.

    Args:
        current: Current star count.
        previous: Previous star count.

    Returns:
        Formatted string like "+5" or "-3" or " 0".
    """
    diff = current - previous
    if diff > 0:
        return f"+{diff}"
    elif diff < 0:
        return f"{diff}"
    return " 0"


def color_for_delta(delta: int) -> str:
    """Return ANSI color code for a given delta value.

    Args:
        delta: The change in star count.

    Returns:
        ANSI escape code for coloring.
    """
    if delta > 0:
        return GREEN
    elif delta < 0:
        return RED
    return RESET


def compute_delta(current: int, previous: int) -> int:
    """Compute the delta between two star counts.

    Args:
        current: Current star count.
        previous: Previous star count.

    Returns:
        Integer difference (current - previous).
    """
    return current - previous


def format_watch_header() -> str:
    """Format the watch display header with timestamp.

    Returns:
        A formatted header string.
    """
    now = datetime.now().strftime("%H:%M:%S")
    return f"{BOLD}{CYAN}╔══ ARA Star Tracker ══╗{RESET}\n║ {now}{RESET}"


def format_watch_summary(repo: str, snapshots: list) -> str:
    """Format a watch session summary.

    Args:
        repo: Repository name (owner/repo).
        snapshots: List of (timestamp, stars) tuples.

    Returns:
        A formatted summary string.
    """
    if not snapshots:
        return f"{repo}: No data collected."

    first_stars = snapshots[0][1]
    last_stars = snapshots[-1][1]
    total_delta = last_stars - first_stars
    duration_secs = snapshots[-1][0] - snapshots[0][0]
    duration_mins = max(1, int(duration_secs / 60))

    color = color_for_delta(total_delta)
    sign = "+" if total_delta > 0 else ""

    return (
        f"{BOLD}╔══ Watch Summary ══╗{RESET}\n"
        f"║ {repo}\n"
        f"║ Duration: {duration_mins} min\n"
        f"║ Started:  ★ {first_stars:,}\n"
        f"║ Ended:    ★ {last_stars:,}\n"
        f"║ Change:   {color}{sign}{total_delta}{RESET}\n"
        f"{BOLD}╚══════════════════╝{RESET}"
    )


def format_multi_watch(data: list) -> str:
    """Format display for multiple monitored repos.

    Args:
        data: List of (repo_name, star_count, delta) tuples.

    Returns:
        A formatted multi-line string for terminal display.
    """
    now = datetime.now().strftime("%H:%M:%S")
    lines = [
        f"{BOLD}{CYAN}╔══ ARA Multi-Watch @ {now} ══╗{RESET}",
    ]

    for repo, stars, delta in data:
        color = color_for_delta(delta)
        sign = "+" if delta > 0 else ""
        lines.append(
            f"║  {repo:30s} ★ {stars:>6,}  {color}({sign}{delta}){RESET}"
        )

    lines.append(f"{BOLD}╚══════════════════════════════╝{RESET}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Watch cursor-control helpers — local refresh instead of full CLEAR
# ---------------------------------------------------------------------------

_FIRST_WATCH_OUTPUT: dict[str, bool] = {}


def _cursor_up(n: int = 1) -> str:
    """Return ANSI escape to move cursor up N lines."""
    return f"\033[{n}A"


def _watch_refresh_prefix(lines: int, ctx_key: str = "default") -> str:
    """Return the appropriate prefix for watch refresh: first call → empty, then → cursor-up.

    Args:
        lines: Number of lines to move cursor up (i.e. number of output lines from previous tick).
        ctx_key: Context key to track first-call state (e.g. 'single' or 'multi').

    Returns:
        Empty string on first call, cursor-up + first-line-clear on subsequent calls.
    """
    first = _FIRST_WATCH_OUTPUT.get(ctx_key, True)
    if first:
        _FIRST_WATCH_OUTPUT[ctx_key] = False
        return ""
    return _cursor_up(lines) + "\033[J"


# ---------------------------------------------------------------------------
# Watch dashboard (Task 002-A)
# ---------------------------------------------------------------------------


def _format_value(val) -> str:
    """Format a single value for table cells — numbers get comma-separated."""
    if val is None:
        return "—"
    if isinstance(val, int):
        return f"{val:,}"
    return str(val)


def _delta_cell(delta: int | None) -> str:
    """Format a delta cell with color: green +N, red -N, reset 0."""
    if delta is None:
        return " —  "
    if delta > 0:
        return f" {GREEN}(+{delta}){RESET} "
    elif delta < 0:
        return f" {RED}({delta}){RESET} "
    return "  (0)  "


def format_watch_dashboard(
    repo_name: str,
    info: dict,
    previous_info: dict | None = None,
    timestamp: str = "",
) -> str:
    """Format a single-repo watch dashboard with box-drawing table.

    Args:
        repo_name: Repository name (owner/repo).
        info: Full repo info dict from GitHubClient.get_repo_info().
        previous_info: Previous tick's info dict (for delta), or None.
        timestamp: Current time string.

    Returns:
        A formatted string for terminal with local-refresh prefix instead of full CLEAR.
    """
    stars = info.get("stars", 0)
    forks = info.get("forks", 0)
    issues = info.get("open_issues", 0)
    lang = info.get("language") or "—"
    lic = info.get("license") or "—"
    updated = (info.get("updated_at") or "")[:19].replace("T", " ")
    created = (info.get("created_at") or "")[:10]

    prev_stars = previous_info.get("stars") if previous_info else None
    prev_forks = previous_info.get("forks") if previous_info else None
    prev_issues = previous_info.get("open_issues") if previous_info else None

    delta_stars = stars - prev_stars if prev_stars is not None else None
    delta_forks = forks - prev_forks if prev_forks is not None else None
    delta_issues = issues - prev_issues if prev_issues is not None else None

    stars_str = f"{stars:,}"
    forks_str = f"{forks:,}"
    issues_str = f"{issues:,}"

    now = timestamp or datetime.now().strftime("%H:%M:%S")

    lines = [
        f"{BOLD}{CYAN}╔════════════════════════════════════════════╗{RESET}",
        f"{BOLD}{CYAN}║        📡 ARA Star Tracker — WATCH         ║{RESET}",
        f"{BOLD}{CYAN}╚════════════════════════════════════════════╝{RESET}",
        "",
        "┌────────────────────┬────────────────────────┐",
        f"│ Repository         │ {repo_name:<22} │",
        "├────────────────────┼────────────────────────┤",
        f"│ ⭐ Stars           │ {stars_str:<12}{_delta_cell(delta_stars)} │",
        f"│ ⑂ Forks            │ {forks_str:<12}{_delta_cell(delta_forks)} │",
        f"│ ⚠ Issues           │ {issues_str:<12}{_delta_cell(delta_issues)} │",
        f"│ 🔤 Language        │ {lang:<22} │",
        f"│ 📜 License         │ {lic:<22} │",
        f"│ 🕐 Updated         │ {updated:<22} │",
        f"│ 📅 Created         │ {created:<22} │",
        "└────────────────────┴────────────────────────┘",
        "",
        f"Last updated: {now}  |  Press Ctrl+C to stop",
    ]
    content = "\n".join(lines)
    line_count = len(lines)  # number of lines the content occupies
    prefix = _watch_refresh_prefix(line_count, "single")
    return prefix + content


def format_multi_watch_dashboard(
    snapshots: list[tuple[str, dict, dict | None]],
    timestamp: str = "",
) -> str:
    """Format a compact multi-repo watch table.

    Args:
        snapshots: List of (repo_name, info_dict, previous_info_or_None) tuples.
        timestamp: Current time string.

    Returns:
        A formatted string for terminal with local-refresh prefix instead of full CLEAR.
    """
    now = timestamp or datetime.now().strftime("%H:%M:%S")
    n = len(snapshots)

    # Determine column widths
    repo_w = max(len(r) for r, _, _ in snapshots) + 2  # padding
    repo_w = max(repo_w, 8)

    col_defs = [
        ("Stars", 8),
        ("Forks", 6),
        ("Issues", 6),
        ("Lang", 6),
        ("Lic", 6),
    ]

    def _format_compact(val, delta=None):
        """Format a compact cell value, optionally with colored delta."""
        s = _format_value(val)
        if delta is not None:
            if delta > 0:
                s = f"{GREEN}{s}{RESET}"
            elif delta < 0:
                s = f"{RED}{s}{RESET}"
        return s

    # Build header row
    header_parts = [f"│ {'Repo'.ljust(repo_w)} "]
    for label, w in col_defs:
        header_parts.append(f"│ {label.ljust(w)} ")
    header_parts.append("│")
    header_str = "".join(header_parts)

    # Build separator
    sep_parts = ["├" + "─" * (repo_w + 2) + "┤"]
    for _, w in col_defs:
        sep_parts.append("─" * (w + 2) + "┤")
    sep_str = "".join(sep_parts)

    _top = "┌" + "─" * (len(header_str) - 2) + "┐"
    _bot = "└" + "─" * (len(header_str) - 2) + "┘"

    lines = [
        f"{BOLD}{CYAN}╔══════════════════════════════════════════════════════════════════╗{RESET}",
        f"{BOLD}{CYAN}║        📡 ARA Multi-Watch                                       ║{RESET}",
        f"{BOLD}{CYAN}╚══════════════════════════════════════════════════════════════════╝{RESET}",
        "",
        _top,
        header_str,
        sep_str,
    ]

    for repo, info, prev in snapshots:
        stars = info.get("stars", 0)
        forks = info.get("forks", 0)
        issues = info.get("open_issues", 0)
        lang = (info.get("language") or "—")[:6]
        lic = (info.get("license") or "—")[:6]

        p_stars = prev.get("stars") if prev else None
        p_forks = prev.get("forks") if prev else None
        p_issues = prev.get("open_issues") if prev else None

        d_stars = stars - p_stars if p_stars is not None else None
        d_forks = forks - p_forks if p_forks is not None else None
        d_issues = issues - p_issues if p_issues is not None else None

        row_parts = [f"│ {repo.ljust(repo_w)} "]
        row_parts.append(f"│ {_format_compact(stars, d_stars).ljust(8)} ")
        row_parts.append(f"│ {_format_compact(forks, d_forks).ljust(6)} ")
        row_parts.append(f"│ {_format_compact(issues, d_issues).ljust(6)} ")
        row_parts.append(f"│ {lang.ljust(6)} ")
        row_parts.append(f"│ {lic.ljust(6)} ")
        row_parts.append("│")
        lines.append("".join(row_parts))

    lines.append(_bot)
    lines.append("")
    lines.append(f"Watching {n} repo{'s' if n > 1 else ''}  ·  {now}  ·  Ctrl+C to stop")

    content = "\n".join(lines)
    line_count = len(lines)
    prefix = _watch_refresh_prefix(line_count, "multi")
    return prefix + content


# ---------------------------------------------------------------------------
# Repo info display
# ---------------------------------------------------------------------------


def format_raw_field(label: str, value: str | int | list | None) -> str:
    """Format a single field line for repo info display."""
    if isinstance(value, list):
        value = ", ".join(value) if value else "—"
    val_str = str(value) if value not in (None, "") else "—"
    return f"  {BOLD}{label}:{RESET} {val_str}"


def format_repo_info(info: dict) -> str:
    """Format full repository information for terminal display.

    Args:
        info: Dict returned by GitHubClient.get_repo_info().

    Returns:
        A formatted multi-line string.
    """
    lines = [
        "",
        f"{BOLD}{CYAN}╔══ Repository Info ══╗{RESET}",
        f"║  {BOLD}{info['full_name']}{RESET}",
        f"{BOLD}╚══════════════════════╝{RESET}",
        "",
        format_raw_field("Description", info["description"]),
        format_raw_field("Stars", f"{info['stars']:,} ★"),
        format_raw_field("Forks", f"{info['forks']:,}"),
        format_raw_field("Open Issues", f"{info['open_issues']:,}"),
        format_raw_field("Language", info["language"]),
        format_raw_field("License", info["license"]),
        format_raw_field("Topics", info["topics"]),
        "",
        format_raw_field("URL", info["html_url"]),
        format_raw_field("Created", info["created_at"][:10] if info["created_at"] else "—"),
        format_raw_field("Updated", info["updated_at"][:10] if info["updated_at"] else "—"),
        format_raw_field("Pushed", info["pushed_at"][:10] if info["pushed_at"] else "—"),
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Repo comparison display — table layout (Task 002-B)
# ---------------------------------------------------------------------------


def format_compare_table(repo1: dict, repo2: dict) -> str:
    """Format a side-by-side comparison using table layout with box-drawing chars.

    Args:
        repo1: Dict from GitHubClient.get_repo_info().
        repo2: Dict from GitHubClient.get_repo_info().

    Returns:
        A formatted string with borders, ANSI colors, and winner declaration.
    """
    name1 = repo1.get("full_name", "Repo A")
    name2 = repo2.get("full_name", "Repo B")

    # Column widths based on repo names, min 18
    col_w = max(len(name1), len(name2), 18) + 2

    def _fmt_num(val) -> str:
        if val is None:
            return "—"
        return f"{val:,}"

    fields = [
        ("⭐ Stars", "stars", True),
        ("⑂ Forks", "forks", True),
        ("⚠ Issues", "open_issues", False),
        ("🔤 Language", "language", None),
        ("📜 License", "license", None),
        ("📅 Created", "created_at", None),
        ("🕐 Updated", "updated_at", None),
    ]

    rows = []
    for label, key, higher_better in fields:
        v1 = repo1.get(key)
        v2 = repo2.get(key)
        is_numeric = isinstance(v1, (int, float)) and isinstance(v2, (int, float))

        if is_numeric:
            s1 = _fmt_num(v1)
            s2 = _fmt_num(v2)
            if higher_better or higher_better is None:
                c1 = GREEN if v1 > v2 else (RED if v1 < v2 else RESET)
                c2 = GREEN if v2 > v1 else (RED if v2 < v1 else RESET)
            else:
                c1 = GREEN if v1 < v2 else (RED if v1 > v2 else RESET)
                c2 = GREEN if v2 < v1 else (RED if v2 > v1 else RESET)
        else:
            s1 = str(v1) if v1 else "—"
            s2 = str(v2) if v2 else "—"
            c1 = c2 = RESET

        # Determine victor column
        if is_numeric and higher_better is not None:
            if v1 > v2:
                victor = f"🏆 {name1.split('/')[-1]}"
            elif v2 > v1:
                victor = f"🏆 {name2.split('/')[-1]}"
            else:
                victor = "—"
        else:
            victor = "—"

        rows.append(
            f"│ {label.ljust(14)} │ {c1}{s1.rjust(col_w)}{RESET} │ {c2}{s2.rjust(col_w)}{RESET} │ {victor.ljust(int(col_w * 0.6 + 4))} │"
        )

    label_w = 14
    victor_w = int(col_w * 0.6 + 4)

    header_line = f"│ {'Metric'.ljust(label_w)} │ {name1.ljust(col_w)} │ {name2.ljust(col_w)} │ {'Victor'.ljust(victor_w)} │"
    top_sep = "┌" + "─" * (len(header_line) - 2) + "┐"
    sep_line = "├" + "─" * (label_w + 2) + "┼" + "─" * (col_w + 2) + "┼" + "─" * (col_w + 2) + "┼" + "─" * (victor_w + 2) + "┤"
    bot_sep = "└" + "─" * (len(header_line) - 2) + "┘"

    lines = [
        "",
        f"{BOLD}{CYAN}╔══════════════════════════════════════════════════════════╗{RESET}",
        f"{BOLD}{CYAN}║             ⚖️  REPO COMPARISON                          ║{RESET}",
        f"{BOLD}{CYAN}╚══════════════════════════════════════════════════════════╝{RESET}",
        "",
        top_sep,
        header_line,
        sep_line,
    ]
    lines.extend(rows)
    lines.append(bot_sep)
    lines.append("")

    # Winner declaration
    s1 = repo1.get("stars", 0) or 0
    s2 = repo2.get("stars", 0) or 0
    f1 = repo1.get("forks", 0) or 0
    f2 = repo2.get("forks", 0) or 0

    if s1 > s2:
        lines.append(f"🏆 {BOLD}{GREEN}{name1}{RESET} WINS!")
        lines.append(f"   Leads by {s1 - s2:,} stars over {name2.split('/')[-1]}")
        if f1 > f2:
            lines.append(f"   Also leads in forks: {f1 - f2} more")
        elif f2 > f1:
            lines.append(f"   Trails in forks by {f2 - f1}")
    elif s2 > s1:
        lines.append(f"🏆 {BOLD}{GREEN}{name2}{RESET} WINS!")
        lines.append(f"   Leads by {s2 - s1:,} stars over {name1.split('/')[-1]}")
        if f2 > f1:
            lines.append(f"   Also leads in forks: {f2 - f1} more")
        elif f1 > f2:
            lines.append(f"   Trails in forks by {f1 - f2}")
    else:
        lines.append(f"  {YELLOW}★ It's a tie at {s1:,} stars each!{RESET}")

    lines.append("")
    return "\n".join(lines)


def format_multi_compare_table(infos: list[dict]) -> str:
    """Format 3+ repos into a compact multi-repo comparison table.

    Args:
        infos: List of repo info dicts from GitHubClient.get_repo_info().

    Returns:
        A formatted string with rankings, medals, and a winner declaration.
    """
    lines = []
    lines.append(f"  {BOLD}{CYAN}Multi-Repo Comparison{RESET}")
    lines.append(f"  {GRAY}{'─' * 61}{RESET}")

    # Sort by stars descending
    sorted_infos = sorted(infos, key=lambda x: x.get("stars", 0), reverse=True)

    for i, info in enumerate(sorted_infos):
        name = info.get("full_name", "unknown")
        stars = info.get("stars", 0)
        forks = info.get("forks", 0)
