"""Tests for `ara battle` command (Task 004)."""

from unittest.mock import patch

# --- Unit tests for battle display logic ---


def test_battle_side_by_side_two_repos():
    """Battle should show two repos side by side with star counts."""
    from ara.battle import format_battle

    repos = [
        ("owner/alpha", 1234),
        ("owner/beta", 567),
    ]
    result = format_battle(repos)
    assert "owner/alpha" in result
    assert "owner/beta" in result
    assert "1,234" in result or "1234" in result
    assert "567" in result


def test_battle_declares_winner():
    """Battle should declare the repo with more stars as winner."""
    from ara.battle import declare_winner

    repos = [
        ("owner/alpha", 1234),
        ("owner/beta", 567),
    ]
    winner = declare_winner(repos)
    assert winner == "owner/alpha", f"Expected alpha to win, got: {winner}"


def test_battle_winner_swaps_on_order():
    """Winner should change when star counts swap."""
    from ara.battle import declare_winner

    repos = [
        ("owner/beta", 999),
        ("owner/alpha", 1000),
    ]
    winner = declare_winner(repos)
    assert winner == "owner/alpha", f"Expected alpha to win, got: {winner}"


def test_battle_tie():
    """Tied repos should be declared a draw."""
    from ara.battle import declare_winner

    repos = [
        ("owner/alpha", 500),
        ("owner/beta", 500),
    ]
    winner = declare_winner(repos)
    assert "tie" in winner.lower() or "draw" in winner.lower(), \
        f"Expected tie/draw declaration, got: {winner}"


def test_battle_three_or_more():
    """Battle should support 3+ repos."""
    from ara.battle import format_battle

    repos = [
        ("repo/a", 1000),
        ("repo/b", 750),
        ("repo/c", 500),
        ("repo/d", 250),
    ]
    result = format_battle(repos)
    assert "repo/a" in result
    assert "repo/b" in result
    assert "repo/c" in result
    assert "repo/d" in result
    assert "WINNER" in result.upper() or "winner" in result.lower()


def test_battle_ascii_bar_proportional():
    """ASCII bars should be proportional to max star count."""
    from ara.battle import make_bar

    bar = make_bar(1000, 1000, max_width=20)
    # Full bar for max
    assert bar.count("▓") == 20, f"Expected 20 filled chars, got: {bar}"

    bar_half = make_bar(500, 1000, max_width=20)
    # Half bar for half the max
    assert bar_half.count("▓") == 10, f"Expected 10 filled chars, got: {bar_half}"

    bar_zero = make_bar(0, 1000, max_width=20)
    # Zero bar
    assert bar_zero.count("▓") == 0, f"Expected 0 filled chars, got: {bar_zero}"


def test_battle_ascii_bar_displays_star_count():
    """ASCII bar should show the star count number."""
    from ara.battle import make_bar

    bar = make_bar(1234, 2000, max_width=20)
    assert "1,234" in bar or "1234" in bar, f"Expected star count in bar: {bar}"


def test_battle_border_box():
    """Battle should be rendered inside a box with unicode borders."""
    from ara.battle import render_box

    content = "Test Content"
    result = render_box(content)
    assert "╔" in result, f"Expected top-left border: {result}"
    assert "╗" in result, f"Expected top-right border: {result}"
    assert "╚" in result, f"Expected bottom-left border: {result}"
    assert "╝" in result, f"Expected bottom-right border: {result}"
    assert "Test Content" in result


def test_battle_header():
    """Battle should have 'ARENA BATTLE' header."""
    from ara.battle import render_header

    result = render_header()
    assert "BATTLE" in result.upper(), f"Expected BATTLE in header: {result}"
    assert "★" in result or "*" in result, f"Expected star in header: {result}"


def test_battle_no_args_uses_leaderboard():
    """Battle with no args should use all repos from leaderboard cache."""
    from ara.battle import repos_from_leaderboard

    # Simulate cache with 3 repos
    cache_data = {
        "repo/a": {"count": 1000, "timestamp": 1},
        "repo/b": {"count": 750, "timestamp": 2},
        "repo/c": {"count": 500, "timestamp": 3},
    }
    repos = repos_from_leaderboard(cache_data)
    assert len(repos) == 3
    assert repos[0] == ("repo/c", 500), f"Expected sorted, got: {repos}"


# --- Integration tests ---


@patch("ara.core.GitHubClient")
def test_battle_command_integration(MockClient):
    """Battle CLI command should fetch stars and display comparison."""
    mock_instance = MockClient.return_value

    def mock_get_stars(repo):
        stars = {"owner/alpha": 1234, "owner/beta": 567}
        return stars.get(repo, 0)

    mock_instance.get_stars.side_effect = mock_get_stars

    from ara.cli import run_battle

    result = run_battle(["owner/alpha", "owner/beta"], mock_instance)
    assert mock_instance.get_stars.call_count == 2
    assert "owner/alpha" in result
    assert "owner/beta" in result
