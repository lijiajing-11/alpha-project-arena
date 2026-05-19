"""Tests for `ara.insight` -- star velocity, relative time, full insight rendering."""

from datetime import datetime, timezone

from ara.insight import cmd_insight, cmd_insight_compare, compute_star_velocity, relative_time, compute_repo_age


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
    assert 1 <= spd <= 10


def test_slow_is_stale():
    """<0.5 stars/day merged into 🐢 Stale (previously 💤 Slow)"""
    spd, label = compute_star_velocity(10, "2020-01-01T00:00:00Z")
    assert "Stale" in label
    assert spd < 1


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
    mock_data = {
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
    monkeypatch.setattr("ara.core.GitHubClient.get_repo_info", lambda self, r: mock_data)

    class FakeClient:
        def get_repo_info(self, repo):
            return mock_data

    cmd_insight("facebook/react", FakeClient())
    # Should not raise


def test_cmd_insight_minimal_data(monkeypatch):
    """Ensure insight handles repos with minimal data gracefully."""
    mock_data = {
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
    monkeypatch.setattr("ara.core.GitHubClient.get_repo_info", lambda self, r: mock_data)

    class FakeClient:
        def get_repo_info(self, repo):
            return mock_data

    cmd_insight("empty/repo", FakeClient())
    # Should not raise


# ===========================================================================
# compute_repo_age
# ===========================================================================


def test_age_veteran():
    """7+ years -> Veteran"""
    _, label = compute_repo_age("2015-01-01T00:00:00Z")
    assert "Veteran" in label


def test_age_prime():
    """3-7 years -> Prime"""
    _, label = compute_repo_age("2021-01-01T00:00:00Z")
    assert "Prime" in label


def test_age_teen():
    """1-3 years -> Teen"""
    _, label = compute_repo_age("2024-01-01T00:00:00Z")
    assert "Teen" in label


def test_age_newborn():
    """<1 year -> Newborn"""
    _, label = compute_repo_age("2026-04-01T00:00:00Z")
    assert "Newborn" in label


def test_age_empty():
    """No creation date -> fallback"""
    _, label = compute_repo_age("")
    assert "Unknown" in label


def test_age_bad_date():
    """Invalid date -> fallback"""
    _, label = compute_repo_age("garbage-date")
    assert "Unknown" in label


# ===========================================================================
# cmd_insight_compare — side-by-side compare mode
# ===========================================================================


def _make_mock_react_data():
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


def _make_mock_vue_data():
    return {
        "full_name": "vuejs/core",
        "stars": 47000,
        "forks": 7000,
        "open_issues": 800,
        "language": "TypeScript",
        "license": "MIT",
        "topics": ["vue", "typescript", "frontend"],
        "description": "🖖 Vue.js is a progressive, incrementally-adoptable JavaScript framework for building UI on the web.",
        "created_at": "2019-12-14T00:00:00Z",
        "updated_at": "2026-05-19T00:00:00Z",
        "pushed_at": "2026-05-19T00:00:00Z",
        "html_url": "https://github.com/vuejs/core",
    }


class FakeCompareClient:
    """Fake client that returns mock data for react and vue."""

    def get_repo_info(self, repo):
        if "react" in repo:
            return _make_mock_react_data()
        return _make_mock_vue_data()


def test_cmd_insight_compare_text(monkeypatch):
    """Compare mode should not crash with 2 repos."""
    monkeypatch.setattr(
        "ara.core.GitHubClient.get_repo_info",
        lambda self, r: _make_mock_react_data() if "react" in r else _make_mock_vue_data(),
    )
    cmd_insight_compare(["facebook/react", "vuejs/core"], FakeCompareClient())
    # Should not raise


def test_cmd_insight_compare_json(monkeypatch):
    """Compare mode in JSON should produce valid output with comparison section."""
    monkeypatch.setattr(
        "ara.core.GitHubClient.get_repo_info",
        lambda self, r: _make_mock_react_data() if "react" in r else _make_mock_vue_data(),
    )
    import json

    # Capture stdout
    import io
    import sys
    captured = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = captured
    try:
        cmd_insight_compare(["facebook/react", "vuejs/core"], FakeCompareClient(), as_json=True)
    finally:
        sys.stdout = old_stdout

    output = captured.getvalue()
    result = json.loads(output)
    assert result["command"] == "insight"
    assert result["mode"] == "compare"
    assert len(result["repos"]) == 2
    assert "comparison" in result
    assert result["comparison"]["star_leader"] == "facebook/react"
    assert result["comparison"]["star_gap"] == 179000
    assert result["comparison"]["velocity_leader"] == "facebook/react"


def test_cmd_insight_single_repo_via_compare(monkeypatch):
    """Passing 1 repo to cmd_insight_compare (2 total) still works."""
    monkeypatch.setattr(
        "ara.core.GitHubClient.get_repo_info",
        lambda self, r: _make_mock_react_data(),
    )
    cmd_insight_compare(["facebook/react"], FakeCompareClient())
    # Should not raise — single repo, but uses compare path


def test_cmd_insight_compare_no_crash_minimal(monkeypatch):
    """Compare mode with minimal data should not crash."""
    mock_data = {
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
    monkeypatch.setattr("ara.core.GitHubClient.get_repo_info", lambda self, r: mock_data)

    class FakeClient:
        def get_repo_info(self, repo):
            return mock_data

    cmd_insight_compare(["empty/repo", "also/empty"], FakeClient())
    # Should not raise
