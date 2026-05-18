"""Tests for `ara watch` command (Task 003)."""

import time
from unittest.mock import MagicMock, patch

# --- Unit tests for the watch display logic ---


def test_delta_shows_positive_growth():
    """Delta display should show +N for growth (current > previous)."""
    from ara.display import format_delta

    result = format_delta(105, 100)
    assert "+5" in result, f"Expected '+5' in delta, got: {result}"


def test_delta_shows_negative_growth():
    """Delta display should show -N for loss (current < previous)."""
    from ara.display import format_delta

    result = format_delta(100, 105)
    assert "-5" in result, f"Expected '-5' in delta, got: {result}"


def test_delta_shows_unchanged():
    """Delta display should be empty or '0' when unchanged."""
    from ara.display import format_delta

    result = format_delta(100, 100)
    assert "0" in result or result == "", f"Expected '0' or empty delta: {result}"


def test_color_green_for_growth():
    """Growth should use green ANSI code."""
    from ara.display import color_for_delta

    result = color_for_delta(5)
    assert "\033[92m" in result, f"Expected green ANSI for positive: {result}"


def test_color_red_for_loss():
    """Loss should use red ANSI code."""
    from ara.display import color_for_delta

    result = color_for_delta(-3)
    assert "\033[91m" in result, f"Expected red ANSI for negative: {result}"


def test_color_white_for_unchanged():
    """No change should use reset (white) ANSI code."""
    from ara.display import color_for_delta

    result = color_for_delta(0)
    assert "\033[0m" in result, f"Expected reset ANSI for zero: {result}"


def test_watch_summary_shows_total_growth():
    """Watch summary should display total growth over the session."""
    from ara.display import format_watch_summary

    snapshots = [(time.time() - 60, 100), (time.time(), 115)]
    result = format_watch_summary("owner/repo", snapshots)
    assert "owner/repo" in result
    assert "115" in result or "+15" in result, f"Expected total in summary: {result}"


def test_watch_creates_cache_entry():
    """Watch should cache star counts with timestamps."""
    from ara.core import star_cache

    # Simulate calling cache with repo data
    star_cache["owner/repo"] = {"count": 100, "timestamp": time.time()}
    entry = star_cache.get("owner/repo")
    assert entry is not None
    assert entry["count"] == 100
    assert "timestamp" in entry


def test_watch_updates_delta_on_new_fetch():
    """Watch should compute delta between consecutive fetches."""
    from ara.display import compute_delta

    # Simulate two consecutive fetches: current=105, previous=100
    delta = compute_delta(105, 100)
    assert delta == 5, f"Expected delta 5, got: {delta}"

    delta = compute_delta(90, 100)
    assert delta == -10, f"Expected delta -10, got: {delta}"


def test_watch_multiple_repos():
    """Watch should support monitoring multiple repos simultaneously."""
    from ara.display import format_multi_watch

    data = [
        ("repo/a", 1234, 5),
        ("repo/b", 567, -2),
        ("repo/c", 89, 0),
    ]
    result = format_multi_watch(data)
    assert "repo/a" in result
    assert "repo/b" in result
    assert "repo/c" in result
    # Each should have star count
    assert "1,234" in result or "1234" in result
    assert "567" in result
    assert "89" in result


def test_watch_timestamp_format():
    """Each watch update should include a timestamp."""
    from ara.display import format_watch_header

    result = format_watch_header()
    assert ":" in result, f"Expected time in header: {result}"
    assert "ARA" in result.upper() or "ara" in result.lower(), f"Expected ARA branding: {result}"


# --- Integration-style tests (mocked) ---


@patch("ara.core.GitHubClient")
def test_watch_command_integration(MockClient):
    """Watch CLI command should call GitHubClient and display results."""
    mock_instance = MockClient.return_value
    mock_instance.get_stars.return_value = 1234

    from ara.cli import run_watch

    # Run a single iteration (not the full loop)
    result = run_watch("owner/repo", mock_instance)
    mock_instance.get_stars.assert_called_once_with("owner/repo")
    assert result == 1234, f"Expected star count 1234, got: {result}"
