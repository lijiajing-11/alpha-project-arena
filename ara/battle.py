"""Battle display for ARA - Arena Star Tracker.

Provides formatting functions for:
- Side-by-side comparison of repos
- ASCII bar charts
- Box-drawing borders
- Winner declaration
"""

from typing import List, Tuple

from ara.colors import BOLD, CYAN, GREEN, RESET, YELLOW

MAX_BAR_WIDTH = 20


def make_bar(stars: int, max_stars: int, max_width: int = MAX_BAR_WIDTH) -> str:
    """Create an ASCII bar proportional to star count.

    Args:
        stars: This repo's star count.
        max_stars: Maximum star count across all repos (reference).
        max_width: Maximum width of the bar in characters.

    Returns:
        Formatted bar string like '▓▓▓▓▓▓▓▓▓▓░░ 1,234 ★'.
    """
    if max_stars <= 0:
        filled = 0
    else:
        filled = round((stars / max_stars) * max_width)

    empty = max_width - filled
    bar = "▓" * filled + "░" * empty
    return f"{bar} {stars:,} ★"


def declare_winner(repos: List[Tuple[str, int]]) -> str:
    """Declare the winner of a battle.

    Args:
        repos: List of (repo_name, star_count) tuples.

    Returns:
        Name of the winner, or "Tie!" / "Draw!" if tied.
    """
    if not repos:
        return "No repos in battle!"

    max_stars = max(r[1] for r in repos)
    winners = [r[0] for r in repos if r[1] == max_stars]

    if len(winners) == 1:
        return winners[0]
    else:
        return "Tie — Draw!"


def format_battle(repos: List[Tuple[str, int]]) -> str:
    """Format the full battle layout.

    Args:
        repos: List of (repo_name, star_count) tuples.

    Returns:
        A formatted string containing the complete battle display.
    """
    if not repos:
        return "No repos to battle!\nUsage: ara battle <repo1> <repo2> [<repo3> ...]"

    max_stars = max(r[1] for r in repos)
    winner = declare_winner(repos)

    lines = []
    lines.append(render_header())
    lines.append("")

    for repo_name, stars in repos:
        bar = make_bar(stars, max_stars)
        is_winner = (winner == repo_name or winner.startswith("Tie"))
        label = f"★ {repo_name}" if not is_winner else f"{YELLOW}★ {repo_name}  ← WINNER!{RESET}"
        lines.append(f"  {label}")
        lines.append(f"    {bar}")
        lines.append("")

    if winner and not winner.startswith("Tie"):
        lines.append(f"{BOLD}{GREEN}✦ {winner} dominates the arena! ✦{RESET}")
    elif winner.startswith("Tie"):
        lines.append(f"{BOLD}{YELLOW}✦ It's a draw! ✦{RESET}")

    raw = "\n".join(lines)
    return render_box(raw)


def render_box(content: str) -> str:
    """Wrap content in a unicode box.

    Args:
        content: The inner content string (may contain newlines).

    Returns:
        Content wrapped in box-drawing characters.
    """
    lines = content.strip("\n").split("\n")
    max_len = max(len(line) for line in lines)

    top = f"╔{'═' * (max_len + 2)}╗"
    bottom = f"╚{'═' * (max_len + 2)}╝"
    middle = "\n".join(f"║ {line}{' ' * (max_len - len(line))} ║" for line in lines)

    return f"{top}\n{middle}\n{bottom}"


def render_header() -> str:
    """Render the 'ARENA BATTLE' header.

    Returns:
        A formatted header string with star characters.
    """
    return f"{BOLD}{CYAN}★ ARENA BATTLE ★{RESET}"
