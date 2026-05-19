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

from ara.colors import BOLD, CLEAR, CYAN, GREEN, RED, RESET, YELLOW


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
        f"{CLEAR}",
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
# Repo comparison display
# ---------------------------------------------------------------------------


def _compare_cell(
    label: str,
    val1: str | int | list | None,
    val2: str | int | list | None,
    width: int = 28,
    higher_is_better: bool = True,
) -> tuple[str, str]:
    """Format two cells for a comparison row, highlighting the better value.

    Returns:
        Tuple of (col1_str, col2_str) for the left and right columns.
    """
    if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
        color1 = GREEN if val1 > val2 else (RED if val1 < val2 else RESET)
        color2 = GREEN if val2 > val1 else (RED if val2 < val1 else RESET)
        if not higher_is_better:
            color1 = RED if color1 == GREEN else (GREEN if color1 == RED else RESET)
            color2 = RED if color2 == GREEN else (GREEN if color2 == RED else RESET)
        s1 = f"{color1}{val1:,}{RESET}" if isinstance(val1, int) else f"{color1}{val1}{RESET}"
        s2 = f"{color2}{val2:,}{RESET}" if isinstance(val2, int) else f"{color2}{val2}{RESET}"
    elif val1 and not val2:
        s1 = f"{GREEN}{val1}{RESET}"
        s2 = f"{RED}—{RESET}"
    elif val2 and not val1:
        s1 = f"{RED}—{RESET}"
        s2 = f"{GREEN}{val2}{RESET}"
    else:
        if val1 is not None and val2 is not None and val1 == val2:
            s1 = s2 = str(val1)
        else:
            s1 = str(val1 or "—")
            s2 = str(val2 or "—")

    if isinstance(val1, list):
        s1 = ", ".join(val1) if val1 else "—"
    if isinstance(val2, list):
        s2 = ", ".join(val2) if val2 else "—"

    return s1.ljust(width), s2.ljust(width)


def format_compare(repo1: dict, repo2: dict) -> str:
    """Format a side-by-side comparison of two repositories.

    Args:
        repo1: Dict from GitHubClient.get_repo_info().
        repo2: Dict from GitHubClient.get_repo_info().

    Returns:
        A formatted multi-line string.
    """
    # Determine column widths based on repo names
    name_w = max(len(repo1["full_name"]), len(repo2["full_name"]), 20)
    val_w = name_w + 4

    name1 = f"{BOLD}{CYAN}{repo1['full_name']}{RESET}"
    name2 = f"{BOLD}{CYAN}{repo2['full_name']}{RESET}"

    lines = [
        "",
        f"{BOLD}╔══ Repo Comparison ══╗{RESET}",
        f"║  {name1}  vs  {name2}",
        f"{BOLD}╚══════════════════════╝{RESET}",
        "",
        f"  {'Metric'.ljust(16)}  {repo1['full_name'].ljust(val_w)}  {repo2['full_name'].ljust(val_w)}",
        f"  {'─' * 16}  {'─' * val_w}  {'─' * val_w}",
    ]

    fields = [
        ("Stars", "stars", True),
        ("Forks", "forks", True),
        ("Open Issues", "open_issues", False),
        ("Language", "language", None),
        ("License", "license", None),
    ]

    for label, key, higher_better in fields:
        c1, c2 = _compare_cell(
            label,
            repo1.get(key),
            repo2.get(key),
            width=val_w,
            higher_is_better=higher_better if higher_better is not None else True,
        )
        lines.append(f"  {label.ljust(16)}  {c1}  {c2}")

    # Topics line
    t1 = ", ".join(repo1.get("topics", [])) or "—"
    t2 = ", ".join(repo2.get("topics", [])) or "—"
    lines.append(f"  {'Topics'.ljust(16)}  {t1.ljust(val_w)}  {t2.ljust(val_w)}")

    lines.append("")

    # Winner declaration
    s1 = repo1.get("stars", 0)
    s2 = repo2.get("stars", 0)
    if s1 > s2:
        lines.append(f"  {GREEN}★ {repo1['full_name']} wins by {s1 - s2:,} stars!{RESET}")
    elif s2 > s1:
        lines.append(f"  {GREEN}★ {repo2['full_name']} wins by {s2 - s1:,} stars!{RESET}")
    else:
        lines.append(f"  {YELLOW}★ It's a tie at {s1:,} stars each!{RESET}")

    lines.append("")
    return "\n".join(lines)
