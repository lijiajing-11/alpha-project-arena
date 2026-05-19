"""Tests for `ara watch` command (Task 003)."""

import time
from unittest.mock import Mock, patch

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


# ===========================================================================
# Dashboard format tests (Task 002-A)
# ===========================================================================


def _make_info(
    full_name="owner/repo",
    stars=12345,
    forks=234,
    open_issues=12,
    language="Python",
    license="MIT",
    created_at="2020-01-15T00:00:00Z",
    updated_at="2026-05-19T14:30:22Z",
) -> dict:
    return {
        "full_name": full_name,
        "stars": stars,
        "forks": forks,
        "open_issues": open_issues,
        "language": language,
        "license": license,
        "created_at": created_at,
        "updated_at": updated_at,
        "description": "A test repo",
        "topics": ["test"],
        "html_url": f"https://github.com/{full_name}",
    }


def test_format_watch_dashboard_has_box_chars():
    """Single-repo dashboard should use box-drawing characters."""
    from ara.display import format_watch_dashboard

    info = _make_info()
    result = format_watch_dashboard("owner/repo", info)
    assert "╔" in result
    assert "╗" in result
    assert "┌" in result
    assert "┐" in result
    assert "│" in result
    assert "└" in result


def test_format_watch_dashboard_shows_repo_name():
    """Dashboard should display the repository name."""
    from ara.display import format_watch_dashboard

    info = _make_info(full_name="owner/awesome")
    result = format_watch_dashboard("owner/awesome", info)
    assert "owner/awesome" in result


def test_format_watch_dashboard_shows_all_fields():
    """Dashboard should include Stars, Forks, Issues, Language, License, Created, Updated."""
    from ara.display import format_watch_dashboard

    info = _make_info(stars=5000, forks=100, open_issues=5, language="Rust", license="Apache-2.0")
    result = format_watch_dashboard("owner/repo", info)
    assert "Stars" in result
    assert "Forks" in result
    assert "Issues" in result
    assert "Language" in result
    assert "License" in result
    assert "Updated" in result
    assert "Created" in result
    assert "5,000" in result
    assert "100" in result
    assert "Rust" in result
    assert "Apache" in result or "Apache-2.0" in result


def test_format_watch_dashboard_delta_green():
    """Positive delta should show green ANSI (+N)."""
    from ara.display import format_watch_dashboard

    info = _make_info(stars=100)
    prev = _make_info(stars=95)
    result = format_watch_dashboard("owner/repo", info, prev)
    # Green ANSI code around (+5)
    assert "\u001b[92m" in result
    assert "(+5)" in result


def test_format_watch_dashboard_delta_red():
    """Negative delta should show red ANSI (-N)."""
    from ara.display import format_watch_dashboard

    info = _make_info(stars=90)
    prev = _make_info(stars=100)
    result = format_watch_dashboard("owner/repo", info, prev)
    # Red ANSI code around (-10)
    assert "\u001b[91m" in result
    assert "(-10)" in result


def test_format_watch_dashboard_no_prev_no_delta():
    """First tick (no previous_info) should not show delta sign."""
    from ara.display import format_watch_dashboard

    info = _make_info(stars=100)
    result = format_watch_dashboard("owner/repo", info)
    assert "(+0)" not in result or "(0)" in result


def test_format_watch_dashboard_with_timestamp():
    """Dashboard should accept a custom timestamp string."""
    from ara.display import format_watch_dashboard

    info = _make_info()
    result = format_watch_dashboard("owner/repo", info, timestamp="12:34:56")
    assert "12:34:56" in result


def test_format_multi_watch_dashboard_has_box_chars():
    """Multi-repo dashboard should use box-drawing characters."""
    from ara.display import format_multi_watch_dashboard

    snapshots = [
        ("owner/a", _make_info(full_name="owner/a", stars=100), None),
        ("owner/b", _make_info(full_name="owner/b", stars=50), None),
    ]
    result = format_multi_watch_dashboard(snapshots)
    assert "╔" in result
    assert "┌" in result
    assert "│" in result
    assert "└" in result


def test_format_multi_watch_dashboard_shows_both_repos():
    """Multi-repo table should include all repo names."""
    from ara.display import format_multi_watch_dashboard

    snapshots = [
        ("owner/alpha", _make_info(full_name="owner/alpha", stars=1000), None),
        ("owner/beta", _make_info(full_name="owner/beta", stars=500), None),
    ]
    result = format_multi_watch_dashboard(snapshots)
    assert "owner/alpha" in result
    assert "owner/beta" in result


def test_format_multi_watch_dashboard_shows_count():
    """Multi-repo footer should show watching N repos."""
    from ara.display import format_multi_watch_dashboard

    snapshots = [
        ("owner/a", _make_info(full_name="owner/a"), None),
        ("owner/b", _make_info(full_name="owner/b"), None),
    ]
    result = format_multi_watch_dashboard(snapshots)
    assert "2 repos" in result or "2 repo" in result


def test_format_multi_watch_dashboard_single_repo_footer():
    """Single-repo in multi-watch should say '1 repo' not '1 repos'."""
    from ara.display import format_multi_watch_dashboard

    snapshots = [
        ("owner/solo", _make_info(full_name="owner/solo"), None),
    ]
    result = format_multi_watch_dashboard(snapshots)
    assert "1 repo" in result


# ===========================================================================
# --notify tests (Task 008-C)
# ===========================================================================


@patch("ara.cli.GitHubClient")
def test_watch_notify_flag_parsed(MockClient):
    """--notify flag should be parsed and available as args.notify."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["watch", "owner/repo", "--notify"])
    assert args.notify is True
    assert args.repos == ["owner/repo"]


@patch("ara.cli.GitHubClient")
def test_watch_notify_shows_message(MockClient, capsys):
    """Notify mode should print notification banner."""
    from ara.cli import cmd_watch
    from unittest.mock import patch as _patch

    mock_client = MockClient.return_value
    mock_client.get_repo_info.return_value = _make_info(stars=1000)

    args = type("Args", (), {"repos": ["owner/repo"], "notify": True, "json": False})()

    with _patch("ara.cli.time.sleep", side_effect=KeyboardInterrupt):
        cmd_watch(args, mock_client)

    captured = capsys.readouterr()
    assert "Notification mode" in captured.out
    assert "bell" in captured.out or "desktop" in captured.out


@patch("ara.cli.GitHubClient")
def test_watch_notify_no_notify_no_message(MockClient, capsys):
    """Without --notify, no notification banner should appear."""
    from ara.cli import cmd_watch
    from unittest.mock import patch as _patch

    mock_client = MockClient.return_value
    mock_client.get_repo_info.return_value = _make_info(stars=1000)

    args = type("Args", (), {"repos": ["owner/repo"], "notify": False, "json": False})()

    with _patch("ara.cli.time.sleep", side_effect=KeyboardInterrupt):
        cmd_watch(args, mock_client)

    captured = capsys.readouterr()
    assert "Notification mode" not in captured.out
    assert "bell" not in captured.out


@patch("ara.cli.GitHubClient")
def test_watch_notify_star_increase(MockClient, capsys):
    """When stars increase in notify mode, bell should ring."""
    from ara.cli import cmd_watch
    from unittest.mock import patch as _patch

    mock_client = MockClient.return_value
    # First call returns 1000, second call returns 1005 (increase of 5)
    mock_client.get_repo_info.side_effect = [
        _make_info(stars=1000),
        _make_info(stars=1005),
    ]

    args = type("Args", (), {"repos": ["owner/repo"], "notify": True, "json": False})()

    with _patch("ara.cli.time.sleep", side_effect=[None, KeyboardInterrupt]):
        cmd_watch(args, mock_client)

    captured = capsys.readouterr()
    # Bell character should be in output
    assert "\a" in captured.out
    # Summary should show stars gained
    assert "new star" in captured.out


@patch("ara.cli.GitHubClient")
def test_watch_notify_no_change_no_bell(MockClient, capsys):
    """When stars do NOT change, no bell should ring."""
    from ara.cli import cmd_watch
    from unittest.mock import patch as _patch

    mock_client = MockClient.return_value
    # Both calls return identical star count (no change)
    mock_client.get_repo_info.side_effect = [
        _make_info(stars=1000),
        _make_info(stars=1000),
    ]

    args = type("Args", (), {"repos": ["owner/repo"], "notify": True, "json": False})()

    with _patch("ara.cli.time.sleep", side_effect=[None, KeyboardInterrupt]):
        cmd_watch(args, mock_client)

    captured = capsys.readouterr()
    # Bell character should NOT be in output
    assert "\a" not in captured.out


@patch("ara.cli.GitHubClient")
def test_watch_notify_star_decrease_no_bell(MockClient, capsys):
    """When stars decrease in notify mode, NO bell should ring (only increases trigger)."""
    from ara.cli import cmd_watch
    from unittest.mock import patch as _patch

    mock_client = MockClient.return_value
    # First call 1000, second call 995 (decrease of 5 — should NOT trigger)
    mock_client.get_repo_info.side_effect = [
        _make_info(stars=1000),
        _make_info(stars=995),
    ]

    args = type("Args", (), {"repos": ["owner/repo"], "notify": True, "json": False})()

    with _patch("ara.cli.time.sleep", side_effect=[None, KeyboardInterrupt]):
        cmd_watch(args, mock_client)

    captured = capsys.readouterr()
    # Bell character should NOT be in output
    assert "\a" not in captured.out


@patch("ara.cli.GitHubClient")
def test_watch_network_error_handled_gracefully(MockClient, capsys):
    """Watch should handle ConnectionError gracefully — show error and continue.

    Simulating an API failure: the mock raises ConnectionError on first call,
    then succeeds on second call, then KeyboardInterrupt stops the loop.
    """
    from ara.cli import cmd_watch
    from unittest.mock import patch as _patch

    mock_client = MockClient.return_value
    # First call: network error; second call: succeeds with stars
    mock_client.get_repo_info.side_effect = [
        ConnectionError("API temporarily unavailable"),
        _make_info(stars=1000),
    ]

    args = type("Args", (), {"repos": ["owner/repo"], "notify": False, "json": False})()

    with _patch("ara.cli.time.sleep", side_effect=[None, KeyboardInterrupt]):
        cmd_watch(args, mock_client)

    captured = capsys.readouterr()
    # Should show some error/retry message
    assert "Error" in captured.out or "error" in captured.out
    # Should still show the repo info on the successful second tick
    assert "owner/repo" in captured.out


# ===========================================================================
# _send_notification unit tests (Task 015-C)
# ===========================================================================


def test_send_notification_fallback_stderr(capsys):
    """When plyer is unavailable, _send_notification should fall back to stderr."""
    from ara.cli import _send_notification

    _send_notification("Test Title", "Test Message")
    captured = capsys.readouterr()
    # Nothing on stdout
    assert captured.out == ""
    # Fallback message should go to stderr
    assert "Test Title" in captured.err
    assert "Test Message" in captured.err


@patch("ara.cli._notify_engine", False)
def test_send_notification_engine_false(capsys):
    """When _notify_engine is False (plyer failed), should use stderr fallback."""
    from ara.cli import _send_notification

    _send_notification("Engine Off", "Fallback check")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "Engine Off" in captured.err


@patch("ara.cli._send_notification")
def test_cmd_watch_notify_calls_send_notification(mock_notify):
    """Notify mode should call _send_notification when stars increase."""
    from ara.cli import cmd_watch
    from unittest.mock import patch as _patch

    mock_client = Mock()
    mock_client.get_repo_info.side_effect = [
        _make_info(stars=1000),
        _make_info(stars=1005),
    ]

    args = type("Args", (), {"repos": ["owner/repo"], "notify": True, "json": False})()

    with _patch("ara.cli.time.sleep", side_effect=[None, KeyboardInterrupt]):
        cmd_watch(args, mock_client)

    # _send_notification should have been called exactly once (on the increase)
    mock_notify.assert_called_once()
    call_title, call_message = mock_notify.call_args[0]
    assert "ARA Star Tracker" in call_title
    assert "owner/repo" in call_message
    assert "+5" in call_message


@patch("ara.cli._send_notification")
def test_cmd_watch_notify_no_call_without_change(mock_notify):
    """Notify mode should NOT call _send_notification when stars are unchanged."""
    from ara.cli import cmd_watch
    from unittest.mock import patch as _patch

    mock_client = Mock()
    mock_client.get_repo_info.side_effect = [
        _make_info(stars=1000),
        _make_info(stars=1000),
    ]

    args = type("Args", (), {"repos": ["owner/repo"], "notify": True, "json": False})()

    with _patch("ara.cli.time.sleep", side_effect=[None, KeyboardInterrupt]):
        cmd_watch(args, mock_client)

    mock_notify.assert_not_called()


@patch("ara.cli._send_notification")
def test_cmd_watch_notify_no_call_on_decrease(mock_notify):
    """Notify mode should NOT call _send_notification when stars decrease."""
    from ara.cli import cmd_watch
    from unittest.mock import patch as _patch

    mock_client = Mock()
    mock_client.get_repo_info.side_effect = [
        _make_info(stars=1000),
        _make_info(stars=995),
    ]

    args = type("Args", (), {"repos": ["owner/repo"], "notify": True, "json": False})()

    with _patch("ara.cli.time.sleep", side_effect=[None, KeyboardInterrupt]):
        cmd_watch(args, mock_client)

    mock_notify.assert_not_called()


@patch("ara.cli._send_notification")
def test_cmd_watch_notify_two_repos_one_change(mock_notify):
    """Multi-repo notify: only the repo that gained stars should trigger notification."""
    from ara.cli import cmd_watch
    from unittest.mock import patch as _patch

    mock_client = Mock()
    # Two repos: one changes, one stays
    mock_client.get_repo_info.side_effect = [
        _make_info(full_name="owner/alpha", stars=1000),
        _make_info(full_name="owner/beta", stars=500),
        # Second tick
        _make_info(full_name="owner/alpha", stars=1005),
        _make_info(full_name="owner/beta", stars=500),
    ]

    args = type("Args", (), {"repos": ["owner/alpha", "owner/beta"], "notify": True, "json": False})()

    with _patch("ara.cli.time.sleep", side_effect=[None, KeyboardInterrupt]):
        cmd_watch(args, mock_client)

    # Should be called exactly once (only alpha changed)
    assert mock_notify.call_count == 1
    call_message = mock_notify.call_args[0][1]
    assert "owner/alpha" in call_message
    assert "+5" in call_message


@patch("ara.cli._send_notification")
def test_cmd_watch_notify_two_repos_both_change(mock_notify):
    """Multi-repo notify: both repos gain stars, both trigger notifications."""
    from ara.cli import cmd_watch
    from unittest.mock import patch as _patch

    mock_client = Mock()
    mock_client.get_repo_info.side_effect = [
        _make_info(full_name="owner/alpha", stars=1000),
        _make_info(full_name="owner/beta", stars=500),
        # Second tick: both gained
        _make_info(full_name="owner/alpha", stars=1010),
        _make_info(full_name="owner/beta", stars=510),
    ]

    args = type("Args", (), {"repos": ["owner/alpha", "owner/beta"], "notify": True, "json": False})()

    with _patch("ara.cli.time.sleep", side_effect=[None, KeyboardInterrupt]):
        cmd_watch(args, mock_client)

    # Should be called twice (alpha: +10, beta: +10)
    assert mock_notify.call_count == 2


def _parse_json_blocks(text: str) -> list[dict]:
    """Split multi-line JSON output into individual JSON objects.

    ``cmd_watch_json`` prints *indented* JSON objects (2-space indent),
    separated by newlines.  This helper splits them back into individual
    dicts using a simple bracket-matching parser.
    """
    import json

    blocks = []
    depth = 0
    start = None
    for i, ch in enumerate(text):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                blocks.append(json.loads(text[start : i + 1]))
                start = None
    return blocks


@patch("ara.cli.GitHubClient")
def test_cmd_watch_json_notify_increase(MockClient, capsys):
    """cmd_watch_json should send notification when notify=True and stars increase."""
    from ara.cli import cmd_watch_json
    from unittest.mock import patch as _patch

    mock_client = MockClient.return_value
    mock_client.get_stars.side_effect = [1000, 1005]

    args = type("Args", (), {"repos": ["owner/repo"], "notify": True, "json": True})()

    with _patch("ara.cli.time.sleep", side_effect=[None, KeyboardInterrupt]):
        cmd_watch_json(args, mock_client)

    captured = capsys.readouterr()
    blocks = _parse_json_blocks(captured.out)

    # 4 blocks: start + tick-1000 + tick-1005 + end
    assert len(blocks) == 4
    assert blocks[0]["status"] == "started"
    # First tick: 1000 stars, no previous so no notification
    assert blocks[1]["tick"][0]["repo"] == "owner/repo"
    assert blocks[1]["tick"][0]["stars"] == 1000
    assert blocks[1]["tick"][0]["changed"] is False
    # Second tick: 1005 stars, increase triggers notification
    assert blocks[2]["tick"][0]["repo"] == "owner/repo"
    assert blocks[2]["tick"][0]["stars"] == 1005
    assert blocks[2]["tick"][0]["changed"] is True
    # End block
    assert blocks[3]["status"] == "ended"
    assert blocks[3]["total_changes"] == 1


@patch("ara.cli.GitHubClient")
def test_cmd_watch_json_notify_no_change(MockClient, capsys):
    """cmd_watch_json should NOT set changed=True when stars don't change."""
    from ara.cli import cmd_watch_json
    from unittest.mock import patch as _patch

    mock_client = MockClient.return_value
    mock_client.get_stars.side_effect = [1000, 1000]

    args = type("Args", (), {"repos": ["owner/repo"], "notify": True, "json": True})()

    with _patch("ara.cli.time.sleep", side_effect=[None, KeyboardInterrupt]):
        cmd_watch_json(args, mock_client)

    captured = capsys.readouterr()
    blocks = _parse_json_blocks(captured.out)

    assert len(blocks) == 4
    # First tick: 1000 stars, no change
    assert blocks[1]["tick"][0]["changed"] is False
    # Second tick: 1000 stars, still no change
    assert blocks[2]["tick"][0]["changed"] is False
    assert blocks[2]["total_changes"] == 0
