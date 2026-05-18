"""Display utilities for ARA watch command.

Provides formatting functions for:
- Delta display (+5, -3, 0)
- ANSI color coding
- Watch summary
- Multi-repo watch display
"""

from datetime import datetime

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"
CLEAR = "\033c"


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
