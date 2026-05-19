"""Tests for `ara.insight` -- star velocity, relative time, full insight rendering."""

from datetime import datetime, timezone

from ara.insight import cmd_insight, compute_star_velocity, relative_time


# ===========================================================================
# compute_star_velocity
# ===========================================================================


def test_hypersonic():
    """50+ stars/day -> 🔥 Hypersonic"""
    spd, label = compute_star_velocity(50000, "2025-01-01T00:00:00Z")
    assert "Hypersonic" in label
    assert spd > 50


def test_rapid():
    """10-50 stars/day -> 📈 Rapid"""
    spd, label = compute_star_velocity(20000, "2025-01-01T00:00:00Z")
    assert "Rapid" in label
    assert 10 <= spd <= 50


def test_steady():
    """3-10 stars/day -> 📊 Steady"""
    spd, label = compute_star_velocity(3000, "2025-01-01T00:00:00Z")
    assert "Steady" in label
    assert 3 <= spd <= 10


def test_slow():
    """0.5-3 stars/day -> 💤 Slow"""
    spd, label = compute_star_velocity(2000, "2022-01-01T00:00:00Z")
    assert "Slow" in label
    assert 0.5 <= spd <= 3


def test_stale():
    """<0.5 stars/day -> 🪦 Stale"""
    spd, label = compute_star_velocity(10, "2015-01-01T00:00:00Z")
    assert "Stale" in label
    assert spd < 0.5


def test_no_date():
    """No creation date -> fallback"""
    spd, label = compute_star_velocity(100, "")
    assert spd == 0.0
    assert "Unknown" in label


def test_bad_date_format():
    """Invalid date string -> fallback"""
    spd, label = compute_star_velocity(100, "not-a-date")
    assert spd == 0.0
    assert "Unknown" in label


def test_zero_stars():
    """Zero stars with valid date -> stale"""
    spd, label = compute_star_velocity(0, "2020-01-01T00:00:00Z")
    assert "Stale" in label


def test_single_star():
    """1 star over many years -> stale"""
    spd, label = compute_star_velocity(1, "2010-01-01T00:00:00Z")
    assert "Stale" in label


# ===========================================================================
# relative_time
# ===========================================================================


def test_rt_today():
    result = relative_time(datetime.now(timezone.utc).isoformat())
    assert result == "Today"


def test_rt_yesterday():
    from datetime import timedelta
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    assert relative_time(yesterday) == "Yesterday"


def test_rt_days_ago():
    from datetime import timedelta
    d5 = (datetime.now(timezone.utc) - timedelta(days=5)).isoformat()
    assert relative_time(d5) == "5 days ago"


def test_rt_30_days_ago():
    from datetime import timedelta
    d30 = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    result = relative_time(d30)
    assert "month" in result or "days" in result


def test_rt_years_ago():
    from datetime import timedelta
    y2 = (datetime.now(timezone.utc) - timedelta(days=730)).isoformat()
    result = relative_time(y2)
    assert "year" in result or "years" in result


def test_rt_empty():
    assert relative_time("") == "Unknown"


def test_rt_bad_date():
    assert relative_time("garbage") == "Unknown"


def test_rt_future_date():
    from datetime import timedelta
    future = (datetime.now(timezone.utc) + timedelta(days=10)).isoformat()
    assert relative_time(future) == "Future?"


# ===========================================================================
# cmd_insight
# ===========================================================================


def test_cmd_insight_is_callable():
    """cmd_insight should exist and be callable."""
    assert callable(cmd_insight)


def test_cmd_insight_with_mock(monkeypatch):
    """Mock get_repo_info and verify insight doesn't crash."""

    def mock_get_repo_info(_self, repo):
        return {
            "full_name": "facebook/react",
            "stars": 226000,
            "forks": 47000,
            "open_issues": 1200,
            "language": "JavaScript",
            "license": "MIT",
            "topics": ["react", "ui", "javascript", "declarative", "frontend"],
            "description": "A declarative UI library",
            "created_at": "2013-05-29T21:12:00Z",
            "updated_at": "2026-05-19T00:00:00Z",
            "pushed_at": "2026-05-19T00:00:00Z",
            "html_url": "https://github.com/facebook/react",
        }

    monkeypatch.setattr("ara.core.GitHubClient.get_repo_info", mock_get_repo_info)
    cmd_insight("facebook/react")
    # Should not raise


def test_cmd_insight_minimal_data(monkeypatch):
    """Ensure insight handles repos with minimal data gracefully."""

    def mock_minimal(_self, repo):
        return {
            "full_name": "empty/repo",
            "stars": 100,
            "forks": 10,
            "open_issues": 5,
            "language": None,
            "license": None,
            "topics": [],
            "description": "",
            "created_at": "",
            "updated_at": "",
            "pushed_at": "",
            "html_url": "https://github.com/empty/repo",
        }

    monkeypatch.setattr("ara.core.GitHubClient.get_repo_info", mock_minimal)
    cmd_insight("empty/repo")
    # Should not raise
