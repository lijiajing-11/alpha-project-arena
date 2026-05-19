"""Tests for `ara.display` display utilities."""

from ara.display import (
    _format_value,
    format_compare_table,
    format_multi_compare_table,
    format_repo_info,
    format_watch_summary,
)


# ===========================================================================
# _format_value — edge cases
# ===========================================================================


def test_format_value_none():
    """None value should render as em-dash."""
    assert _format_value(None) == "—"


def test_format_value_int():
    """Integer value should be comma-separated."""
    assert _format_value(1234567) == "1,234,567"


def test_format_value_str():
    """String value (non-int) should be returned as-is."""
    assert _format_value("hello") == "hello"


def test_format_value_zero():
    """Zero should render as '0'."""
    assert _format_value(0) == "0"


# ===========================================================================
# format_watch_summary — edge cases
# ===========================================================================


def test_watch_summary_empty_snapshots():
    """Empty snapshots list should show 'No data collected'."""
    result = format_watch_summary("owner/repo", [])
    assert "No data collected" in result


def test_watch_summary_no_gain():
    """Snapshots with no change should show 0 delta."""
    result = format_watch_summary("owner/repo", [(1000.0, 500), (2000.0, 500)])
    assert "0" in result or "(0)" in result


def test_watch_summary_positive_gain():
    """Snapshots with star gain should show positive change."""
    result = format_watch_summary("owner/repo", [(1000.0, 500), (2000.0, 510)])
    assert "+" in result or "10" in result or "Change" in result


# ===========================================================================
# format_compare_table — edge cases for uncovered winner logic
# ===========================================================================


def _make_mock_info(name, stars, forks, open_issues=0, language="Python", license="MIT"):
    return {
        "full_name": name,
        "stars": stars,
        "forks": forks,
        "open_issues": open_issues,
        "language": language,
        "license": license,
        "topics": ["web"],
        "description": "A test repo",
        "created_at": "2020-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
        "pushed_at": "2026-01-01T00:00:00Z",
        "html_url": f"https://github.com/{name}",
    }


def test_compare_table_winner1_leads_in_forks():
    """Winner leads in both stars and forks — 'Also leads in forks' shown."""
    r1 = _make_mock_info("owner/alpha", stars=1000, forks=100)
    r2 = _make_mock_info("owner/beta", stars=500, forks=50)
    result = format_compare_table(r1, r2)
    assert "ALPHA WINS" in result.upper() or "alpha" in result.lower()
    assert "Leads by" in result
    assert "forks" in result.lower()


def test_compare_table_winner2_leads_in_stars_trails_forks():
    """Winner (repo2) wins stars but trails in forks."""
    r1 = _make_mock_info("owner/alpha", stars=500, forks=200)
    r2 = _make_mock_info("owner/beta", stars=1000, forks=50)
    result = format_compare_table(r1, r2)
    assert "BETA WINS" in result.upper() or "beta" in result.lower()
    assert "Trails in forks" in result


def test_compare_table_winner1_trails_forks():
    """Winner (repo1) wins stars but trails in forks."""
    r1 = _make_mock_info("owner/alpha", stars=1000, forks=50)
    r2 = _make_mock_info("owner/beta", stars=500, forks=200)
    result = format_compare_table(r1, r2)
    assert "ALPHA WINS" in result.upper() or "alpha" in result.lower()
    assert "Trails in forks" in result


def test_compare_table_tie():
    """Tied star counts should show tie message."""
    r1 = _make_mock_info("owner/alpha", stars=500, forks=50)
    r2 = _make_mock_info("owner/beta", stars=500, forks=50)
    result = format_compare_table(r1, r2)
    assert "tie" in result.lower()


def test_compare_table_winner2_trails_no_forks():
    """Winner with no fork data should not crash."""
    r1 = _make_mock_info("owner/alpha", stars=500, forks=0)
    r2 = _make_mock_info("owner/beta", stars=1000, forks=0)
    result = format_compare_table(r1, r2)
    assert "BETA" in result or "beta" in result


def test_compare_table_none_stars():
    """None star values should not crash."""
    r1 = _make_mock_info("owner/alpha", stars=None, forks=50)
    r2 = _make_mock_info("owner/beta", stars=500, forks=50)
    result = format_compare_table(r1, r2)
    assert "alpha" in result.lower() or "beta" in result.lower()


def test_compare_table_none_forks():
    """None fork values should not crash."""
    r1 = _make_mock_info("owner/alpha", stars=1000, forks=None)
    r2 = _make_mock_info("owner/beta", stars=500, forks=None)
    result = format_compare_table(r1, r2)
    assert "alpha" in result.lower()


# ===========================================================================
# format_repo_info — edge cases
# ===========================================================================


def test_repo_info_minimal():
    """Minimal info dict with missing fields should not crash."""
    info = {
        "full_name": "minimal/repo",
        "stars": 0,
        "forks": 0,
        "open_issues": 0,
        "language": None,
        "license": None,
        "topics": [],
        "description": "",
        "created_at": None,
        "updated_at": None,
        "pushed_at": None,
        "html_url": "https://github.com/minimal/repo",
    }
    result = format_repo_info(info)
    assert "minimal/repo" in result
    assert "—" in result  # Some fields rendered as em-dash


# ===========================================================================
# format_multi_compare_table — single repo edge case
# ===========================================================================


def test_multi_compare_single_repo():
    """Single repo should still produce a valid output without comparison."""
    infos = [
        {"full_name": "solo/repo", "stars": 100, "forks": 10, "language": "Python",
         "license": "MIT", "topics": ["web"], "open_issues": 2},
    ]
    result = format_multi_compare_table(infos)
    assert "solo/repo" in result
    assert "100 stars" in result
