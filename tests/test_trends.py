"""Tests for `ara trends` command (Task 004-B)."""

import json
import time
from unittest.mock import MagicMock, patch


# ===========================================================================
# Test helpers
# ===========================================================================


def _make_star_events(*timestamps: float, repo: str = "owner/repo"):
    """Create StarEvent list from timestamps."""
    from ara.trends import StarEvent
    return [StarEvent(timestamp=ts, repo=repo) for ts in timestamps]


# ===========================================================================
# StarEvent tests
# ===========================================================================


def test_star_event_dataclass():
    """StarEvent should store timestamp and repo."""
    from ara.trends import StarEvent

    e = StarEvent(timestamp=1000.0, repo="owner/repo")
    assert e.timestamp == 1000.0
    assert e.repo == "owner/repo"


def test_trend_bucket_dataclass():
    """TrendBucket should store label, count, delta."""
    from ara.trends import TrendBucket

    b = TrendBucket(label="09:00", count=5, delta=2)
    assert b.label == "09:00"
    assert b.count == 5
    assert b.delta == 2


# ===========================================================================
# get_star_history tests
# ===========================================================================


def test_get_star_history_returns_sorted_events():
    """get_star_history should return sorted StarEvents from paginated API."""
    from ara.trends import get_star_history

    mock_client = MagicMock()
    now = time.time()

    # Simulate two pages of stargazers
    page1 = [
        {"starred_at": "2026-05-18T10:00:00Z", "login": "user1"},
        {"starred_at": "2026-05-18T11:00:00Z", "login": "user2"},
    ]
    page2 = [
        {"starred_at": "2026-05-18T09:00:00Z", "login": "user0"},
        {"starred_at": "2026-05-18T12:00:00Z", "login": "user3"},
    ]

    # First call returns page1 with next link, second returns page2 with no link
    mock_client._fetch_page_with_headers.side_effect = [
        (page1, {"Link": '<https://api.github.com/repos/owner/repo/stargazers?per_page=100&page=2>; rel="next"'}),
        (page2, {}),
    ]

    events = get_star_history(mock_client, "owner/repo", pages=5)

    assert len(events) == 4
    # Should be sorted asc by timestamp
    timestamps = [e.timestamp for e in events]
    assert timestamps == sorted(timestamps)
    assert all(e.repo == "owner/repo" for e in events)


def test_get_star_history_respects_max_pages():
    """get_star_history should not fetch more than `pages` pages."""
    from ara.trends import get_star_history

    mock_client = MagicMock()
    page = [
        {"starred_at": "2026-05-18T10:00:00Z", "login": "user1"},
    ]
    mock_client._fetch_page_with_headers.return_value = (
        page,
        {"Link": '<https://api.github.com/next>; rel="next"'},
    )

    events = get_star_history(mock_client, "owner/repo", pages=2)
    assert len(events) == 2
    assert mock_client._fetch_page_with_headers.call_count == 2


def test_get_star_history_handles_empty():
    """get_star_history should return empty list for no stargazers."""
    from ara.trends import get_star_history

    mock_client = MagicMock()
    mock_client._fetch_page_with_headers.return_value = ([], {})

    events = get_star_history(mock_client, "owner/repo", pages=3)
    assert events == []


# ===========================================================================
# compute_trend_buckets tests
# ===========================================================================


def test_compute_trend_buckets_basic():
    """Given events, compute_trend_buckets should group them correctly."""
    from ara.trends import compute_trend_buckets

    now = time.time()
    # 3 events: 2 in one bucket, 1 in another
    events = _make_star_events(
        now - 3500,  # ~58 min ago
        now - 3400,  # ~57 min ago (same bucket as above)
        now - 1800,  # ~30 min ago (different bucket)
    )

    buckets = compute_trend_buckets(events, hours=2, interval_minutes=60)
    assert len(buckets) == 2  # 2 hours / 60 min = 2 buckets
    assert sum(b.count for b in buckets) == 3


def test_compute_trend_buckets_empty():
    """Empty events should produce buckets with zero counts."""
    from ara.trends import compute_trend_buckets

    buckets = compute_trend_buckets([], hours=72, interval_minutes=60)
    assert len(buckets) > 0
    assert all(b.count == 0 for b in buckets)


def test_compute_trend_buckets_delta():
    """Deltas should be computed between consecutive buckets."""
    from ara.trends import compute_trend_buckets

    now = time.time()
    # Place events so bucket 1 has 1, bucket 2 has 3
    events = _make_star_events(
        now - 5400,  # ~90 min ago
        now - 1800,  # ~30 min ago
        now - 1700,  # ~28 min ago
        now - 1600,  # ~27 min ago
    )

    buckets = compute_trend_buckets(events, hours=2, interval_minutes=60)
    assert len(buckets) == 2

    # First bucket delta: count - 0 = count
    assert buckets[0].delta == buckets[0].count

    # Second bucket delta: count - prev_count
    assert buckets[1].delta == buckets[1].count - buckets[0].count


# ===========================================================================
# render_trend_chart tests
# ===========================================================================


def test_render_trend_chart_format():
    """render_trend_chart should produce tabular output with box drawing."""
    from ara.trends import TrendBucket, render_trend_chart

    buckets = [
        TrendBucket(label="09:00", count=5, delta=3),
        TrendBucket(label="10:00", count=10, delta=5),
    ]

    result = render_trend_chart(buckets, "owner/repo")
    assert "📈" in result
    assert "owner/repo" in result
    assert "09:00" in result
    assert "10:00" in result
    assert "━" in result
    assert "Total new stars: 15" in result


def test_render_trend_chart_empty():
    """render_trend_chart should show friendly message for empty data."""
    from ara.trends import render_trend_chart

    result = render_trend_chart([], "owner/repo")
    assert "No trend data" in result
    assert "owner/repo" in result


def test_render_trend_chart_highlights_best_hour():
    """render_trend_chart should mention the best hour."""
    from ara.trends import TrendBucket, render_trend_chart

    buckets = [
        TrendBucket(label="09:00", count=2, delta=2),
        TrendBucket(label="10:00", count=10, delta=8),
        TrendBucket(label="11:00", count=3, delta=-7),
    ]

    result = render_trend_chart(buckets, "owner/repo")
    assert "Best hour: 10:00" in result


# ===========================================================================
# cmd_trends tests
# ===========================================================================


@patch("ara.trends.get_star_history")
def test_cmd_trends_happy_path(mock_get_history):
    """cmd_trends should fetch history and render chart."""
    from ara.trends import cmd_trends
    from ara.trends import StarEvent

    now = time.time()
    mock_get_history.return_value = [
        StarEvent(timestamp=now - 1800, repo="owner/repo"),
        StarEvent(timestamp=now - 900, repo="owner/repo"),
    ]

    class MockArgs:
        repo = "owner/repo"
        hours = 72
        interval = 60
        json = False

    result = cmd_trends(MockArgs(), None)
    assert isinstance(result, str)
    assert "owner/repo" in result


@patch("ara.trends.get_star_history")
def test_cmd_trends_json_output(mock_get_history):
    """cmd_trends --json should produce valid JSON."""
    from ara.trends import cmd_trends, StarEvent

    now = time.time()
    mock_get_history.return_value = [
        StarEvent(timestamp=now - 2000, repo="owner/repo"),
        StarEvent(timestamp=now - 1000, repo="owner/repo"),
    ]

    class MockArgs:
        repo = "owner/repo"
        hours = 72
        interval = 60
        json = True

    result = cmd_trends(MockArgs(), None)
    data = json.loads(result)
    assert data["repo"] == "owner/repo"
    assert isinstance(data["buckets"], list)
    assert data["total"] >= 0
    assert "best_hour" in data


# ===========================================================================
# CLI integration tests
# ===========================================================================


def test_trends_subcommand_registered():
    """The trends subcommand should be registered in the parser."""
    from ara.cli import build_parser

    parser = build_parser()
    # Parse a trends command
    args = parser.parse_args(["trends", "owner/repo"])
    assert args.command == "trends"
    assert args.repo == "owner/repo"
    assert args.hours == 72
    assert args.interval == 60
