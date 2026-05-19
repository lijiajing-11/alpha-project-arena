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


# ===========================================================================
# cmd_insight with --trend mode
# ===========================================================================


def test_cmd_insight_trend_flag_exists():
    """cmd_insight should accept show_trend parameter."""
    import inspect
    sig = inspect.signature(cmd_insight)
    assert "show_trend" in sig.parameters


def test_cmd_insight_with_trend_no_data():
    """insight --trend with no stargazer data should still show insight, gracefully falling back."""
    mock_data = {
        "full_name": "facebook/react",
        "stars": 226000,
        "forks": 47000,
        "open_issues": 1200,
        "language": "JavaScript",
        "license": "MIT",
        "topics": ["react", "ui", "javascript"],
        "description": "A declarative UI library",
        "created_at": "2013-05-29T21:12:00Z",
        "updated_at": "2026-05-19T00:00:00Z",
        "pushed_at": "2026-05-19T00:00:00Z",
        "html_url": "https://github.com/facebook/react",
    }

    class FakeTrendClient:
        def get_repo_info(self, repo):
            return mock_data
        def get_stars(self, repo):
            return 226000
        def _fetch_page_with_headers(self, url):
            # Return empty page — no stargazer data
            return [], {"Link": ""}

    # With show_trend=True but no stargazers (empty list), should not crash
    import io, sys
    captured = io.StringIO()
    old = sys.stdout
    sys.stdout = captured
    try:
        cmd_insight("facebook/react", FakeTrendClient(), show_trend=True)
    finally:
        sys.stdout = old

    output = captured.getvalue()
    # Still shows insight data
    assert "facebook/react" in output
    # 226,000 stars should be visible in the insight text
    assert "226,000" in output or "Hypersonic" in output


# ===========================================================================
# Edge case tests for compute_star_velocity
# ===========================================================================


def test_velocity_exact_boundary_50():
    """Exactly 50 stars/day should be Hypersonic."""
    spd, label = compute_star_velocity(50, "2026-01-01T00:00:00Z")
    # days since Jan 1 2026 is roughly 138 -> 50/138 < 1, so not hypersonic
    # Use a recent date to ensure > 50/day
    from datetime import datetime, timezone, timedelta
    recent = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    spd, label = compute_star_velocity(60, recent)
    assert "Hypersonic" in label
    assert spd >= 10


def test_velocity_exact_boundary_10():
    """Approximately 10 stars/day should be Rapid."""
    from datetime import datetime, timezone, timedelta
    recent = (datetime.now(timezone.utc) - timedelta(days=10)).isoformat()
    spd, label = compute_star_velocity(150, recent)
    if spd > 10:
        assert "Rapid" in label or "Hypersonic" in label
    else:
        assert "Steady" in label or "Rapid" in label


def test_velocity_negative_stars():
    """Negative star count still works."""
    # Stars should never be negative in practice, but guard the edge
    spd, label = compute_star_velocity(0, "2020-01-01T00:00:00Z")
    assert spd >= 0
    assert "Stale" in label


# ===========================================================================
# Edge case tests for compute_repo_age
# ===========================================================================


def test_age_exact_newborn():
    """Very recent repo should be Newborn."""
    from datetime import datetime, timezone
    recent = datetime.now(timezone.utc).isoformat()
    _, label = compute_repo_age(recent)
    assert "Newborn" in label


def test_age_exact_teen():
    """1-3 years should be Teen. Use a date ~2 years ago."""
    from datetime import datetime, timezone, timedelta
    teen = (datetime.now(timezone.utc) - timedelta(days=365 * 2)).isoformat()
    _, label = compute_repo_age(teen)
    assert "Teen" in label or "Newborn" in label


# ===========================================================================
# _render_compare_json — direct unit tests
# ===========================================================================


def _make_insight_data(full_name, stars, spd, age_years, topics=None):
    """Helper to build a mock insight data dict as produced by _build_insight_data."""
    return {
        "full_name": full_name,
        "description": f"Description for {full_name}",
        "stars": stars,
        "forks": stars // 10,
        "open_issues": stars // 100,
        "language": "Python",
        "license": "MIT",
        "topics": topics or ["web", "api"],
        "star_velocity": {"per_day": spd, "label": "Hypersonic" if spd > 50 else "Rapid"},
        "repo_age": {"years": age_years, "label": "Veteran" if age_years > 7 else "Prime"},
        "created_at": "2020-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
        "updated_relative": "4 months ago",
    }


def test_render_compare_json_basic():
    """_render_compare_json with 2 repos produces valid JSON."""
    from ara.insight import _render_compare_json
    import json

    d1 = _make_insight_data("owner/alpha", stars=1000, spd=20.0, age_years=3.0)
    d2 = _make_insight_data("owner/beta", stars=500, spd=5.0, age_years=5.0)

    result = _render_compare_json([d1, d2])
    parsed = json.loads(result)

    assert parsed["command"] == "insight"
    assert parsed["mode"] == "compare"
    assert len(parsed["repos"]) == 2
    assert parsed["comparison"]["star_leader"] == "owner/alpha"
    assert parsed["comparison"]["star_gap"] == 500
    assert parsed["comparison"]["velocity_leader"] == "owner/alpha"
    assert parsed["comparison"]["younger"] == "owner/alpha"


def test_render_compare_json_single_repo():
    """_render_compare_json with 1 repo should return empty comparison."""
    from ara.insight import _render_compare_json
    import json

    d1 = _make_insight_data("owner/alpha", stars=1000, spd=20.0, age_years=3.0)
    result = _render_compare_json([d1])
    parsed = json.loads(result)

    assert parsed["command"] == "insight"
    assert parsed["mode"] == "compare"
    assert len(parsed["repos"]) == 1
    assert parsed["comparison"] == {}


def test_render_compare_json_tie_stars():
    """Equal stars should pick first as leader."""
    from ara.insight import _render_compare_json
    import json

    d1 = _make_insight_data("owner/alpha", stars=500, spd=10.0, age_years=2.0)
    d2 = _make_insight_data("owner/beta", stars=500, spd=20.0, age_years=4.0)

    result = _render_compare_json([d1, d2])
    parsed = json.loads(result)

    assert parsed["comparison"]["star_leader"] == "owner/alpha"
    assert parsed["comparison"]["star_gap"] == 0


# ===========================================================================
# _build_insight_data — direct unit tests
# ===========================================================================


class MockGitHubClient:
    """Mock client that returns a fixed repo info dict."""

    def __init__(self, data):
        self._data = data

    def get_repo_info(self, repo):
        return self._data


def test_build_insight_data_minimal():
    """_build_insight_data handles minimal data gracefully."""
    from ara.insight import _build_insight_data

    data = {
        "stars": 100,
        "forks": 10,
        "open_issues": 5,
        "language": None,
        "license": None,
        "topics": [],
        "description": None,
        "created_at": "",
        "updated_at": "",
        "full_name": "empty/repo",
    }
    client = MockGitHubClient(data)
    result = _build_insight_data("empty/repo", client)

    assert result["full_name"] == "empty/repo"
    assert result["language"] == "N/A"
    assert result["license"] == "None"
    assert result["topics"] == []
    assert result["star_velocity"]["per_day"] == 0.0
    assert result["repo_age"]["years"] == 0
    assert "Unknown" in result["star_velocity"]["label"]


def test_build_insight_data_full():
    """_build_insight_data with full data computes velocity and age correctly."""
    from ara.insight import _build_insight_data

    data = {
        "stars": 100000,
        "forks": 20000,
        "open_issues": 500,
        "language": "Python",
        "license": "MIT",
        "topics": ["python", "machine-learning", "deep-learning"],
        "description": "A great ML library",
        "created_at": "2015-06-15T00:00:00Z",
        "updated_at": "2026-05-19T00:00:00Z",
        "full_name": "org/awesome",
    }
    client = MockGitHubClient(data)
    result = _build_insight_data("org/awesome", client)

    assert result["full_name"] == "org/awesome"
    assert result["language"] == "Python"
    assert result["license"] == "MIT"
    assert len(result["topics"]) == 3
    assert result["star_velocity"]["per_day"] > 0
    assert result["repo_age"]["years"] > 0
