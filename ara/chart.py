"""ARA chart module — ASCII chart rendering utilities.

Provides generic ASCII bar/line chart rendering functions
that can be reused across commands (history, trends, etc.).
"""

from .colors import BOLD, CYAN, GRAY, GREEN, RESET, YELLOW


def render_line_chart(
    timeline: list[dict],
    repo_name: str,
    bar_char: str | None = None,
    chart_height: int = 10,
    chart_width: int = 40,
) -> str:
    """Render an ASCII line chart from timeline data.

    Args:
        timeline: List of dicts with 'stars' and 'date' keys,
                  in chronological order.
        repo_name: Repository name for chart title.
        bar_char: Character to use for the chart line (default: green ●).
        chart_height: Height of the chart in rows (default: 10).
        chart_width: Max width of the chart in columns (default: 40).

    Returns:
        A formatted ASCII chart string for terminal display.
    """
    if not timeline:
        return f"  {GRAY}No history data available for {repo_name}{RESET}"

    max_stars = max(p["stars"] for p in timeline) or 1
    min_stars = min(p["stars"] for p in timeline) or 0
    range_stars = max_stars - min_stars or 1

    # Sample to chart_width points if needed
    if len(timeline) > chart_width:
        step = len(timeline) / chart_width
        sampled = [timeline[int(i * step)] for i in range(chart_width)]
    else:
        sampled = timeline

    bar_char = bar_char or f"{GREEN}●{RESET}"
    axis_char = f"{GRAY}│{RESET}"

    lines: list[str] = []
    lines.append(f"  {BOLD}{YELLOW}★ {repo_name} — Star History{RESET}")
    lines.append(f"  {GRAY}{max_stars:,} stars total{RESET}")
    lines.append("")

    # Build chart rows from top to bottom
    for row in range(chart_height):
        threshold = max_stars - (row + 1) * (range_stars / chart_height)
        line = f"  {axis_char} "
        for point in sampled:
            line += bar_char if point["stars"] >= threshold else " "
        lines.append(line)

    # X-axis
    x_axis = f"  └{'─' * len(sampled)}"
    lines.append(x_axis)

    # Labels (first and last date)
    first_date = timeline[0].get("date", "")[:10]
    last_date = timeline[-1].get("date", "")[:10]
    label_pad = " " * (len(sampled) - len(first_date) - len(last_date) + 2)
    lines.append(f"   {GRAY}{first_date}{label_pad}{last_date}{RESET}")
    lines.append("")

    return "\n".join(lines)
