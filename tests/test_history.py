"""Tests for `ara.history` — star history ASCII chart."""

import pytest
from ara.history import _render_chart, cmd_history
from ara.history import _build_timeline_from_repo


class TestRenderChart:
    """Tests for the _render_chart function."""

    def test_empty_timeline(self):
        """Empty timeline should not crash and return a no-data message."""
        result = _render_chart([], "test/repo")
        assert "No history" in result or "test/repo" in result

    def test_single_point(self):
        """Single data point should render without crashing."""
        result = _render_chart([{"stars": 100, "date": "2025-01-01"}], "test/repo")
        assert "test/repo" in result
        assert "100" in result

    def test_multiple_points(self):
        """Multiple points should produce a chart with the bar character."""
        timeline = [
            {"stars": 0, "date": "2020-01-01"},
            {"stars": 50, "date": "2022-01-01"},
            {"stars": 100, "date": "2024-01-01"},
            {"stars": 200, "date": "2026-01-01"},
        ]
        result = _render_chart(timeline, "growing/repo")
        assert "growing/repo" in result
        assert "●" in result

    def test_upward_trend_label(self):
        """Chart should include 'Star History' label."""
        timeline = [
            {"stars": 10, "date": "2020-01-01"},
            {"stars": 500, "date": "2026-01-01"},
        ]
        result = _render_chart(timeline, "trend/repo")
        assert "Star History" in result

    def test_chart_contains_repo_name(self):
        """Repo name should appear in the chart header."""
        result = _render_chart(
            [{"stars": 42, "date": "2023-06-01"}],
            "my-org/my-repo",
        )
        assert "my-org/my-repo" in result

    def test_chart_has_dates(self):
        """First and last dates should appear in the chart."""
        timeline = [
            {"stars": 10, "date": "2020-01-01"},
            {"stars": 20, "date": "2023-06-01"},
            {"stars": 30, "date": "2026-12-31"},
        ]
        result = _render_chart(timeline, "dated/repo")
        assert "2020-01-01" in result
        assert "2026-12-31" in result

    def test_large_star_count_formatting(self):
        """Large star counts should be formatted with commas."""
        timeline = [
            {"stars": 0, "date": "2013-01-01"},
            {"stars": 226000, "date": "2026-01-01"},
        ]
        result = _render_chart(timeline, "big/repo")
        assert "226,000" in result


class TestBuildTimeline:
    """Tests for _build_timeline_from_repo."""

    def test_with_valid_repo_info(self, monkeypatch):
        """Should return non-empty timeline with valid mock data."""
        def mock_get_repo_info(_self, repo):
            return {
                "full_name": "facebook/react",
                "stars": 226000,
                "created_at": "2013-05-29T21:12:00Z",
                "description": "A UI library",
            }

        from ara.core import GitHubClient
        monkeypatch.setattr(
            "ara.core.GitHubClient.get_repo_info", mock_get_repo_info
        )
        client = GitHubClient()
        result = _build_timeline_from_repo(client, "facebook/react")
        assert len(result) == 21
        assert result[0]["stars"] == 0
        assert result[-1]["stars"] == 226000

    def test_no_created_at(self, monkeypatch):
        """Missing created_at should return empty list."""
        def mock_get_repo_info(_self, repo):
            return {"full_name": "new/repo", "stars": 5, "created_at": ""}

        from ara.core import GitHubClient
        monkeypatch.setattr(
            "ara.core.GitHubClient.get_repo_info", mock_get_repo_info
        )
        client = GitHubClient()
        result = _build_timeline_from_repo(client, "new/repo")
        assert result == []

    def test_zero_stars(self, monkeypatch):
        """Zero stars should return empty list."""
        def mock_get_repo_info(_self, repo):
            return {"full_name": "empty/repo", "stars": 0, "created_at": "2024-01-01T00:00:00Z"}

        from ara.core import GitHubClient
        monkeypatch.setattr(
            "ara.core.GitHubClient.get_repo_info", mock_get_repo_info
        )
        client = GitHubClient()
        result = _build_timeline_from_repo(client, "empty/repo")
        assert result == []

    def test_timeline_monotonic(self, monkeypatch):
        """Stars should be non-decreasing in the timeline."""
        def mock_get_repo_info(_self, repo):
            return {
                "full_name": "growing/repo",
                "stars": 1000,
                "created_at": "2020-01-01T00:00:00Z",
            }

        from ara.core import GitHubClient
        monkeypatch.setattr(
            "ara.core.GitHubClient.get_repo_info", mock_get_repo_info
        )
        client = GitHubClient()
        result = _build_timeline_from_repo(client, "growing/repo")
        stars = [p["stars"] for p in result]
        assert all(stars[i] <= stars[i + 1] for i in range(len(stars) - 1))


class TestCmdHistory:
    """Tests for the cmd_history entry point."""

    def test_cmd_history_callable(self):
        """cmd_history should be callable."""
        assert callable(cmd_history)

    def test_cmd_history_no_crash(self, monkeypatch):
        """cmd_history should not crash with mock data."""
        def mock_get_repo_info(_self, repo):
            return {
                "full_name": "facebook/react",
                "stars": 226000,
                "created_at": "2013-05-29T21:12:00Z",
                "description": "A UI library",
            }

        monkeypatch.setattr(
            "ara.core.GitHubClient.get_repo_info", mock_get_repo_info
        )
        cmd_history("facebook/react")

    def test_cmd_history_json_output(self, monkeypatch):
        """cmd_history with as_json=True should produce valid JSON."""
        import json

        def mock_get_repo_info(_self, repo):
            return {
                "full_name": "facebook/react",
                "stars": 226000,
                "created_at": "2013-05-29T21:12:00Z",
                "description": "A UI library",
            }

        monkeypatch.setattr(
            "ara.core.GitHubClient.get_repo_info", mock_get_repo_info
        )

        import io
        import sys
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            cmd_history("facebook/react", as_json=True)
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        parsed = json.loads(output)
        assert parsed["command"] == "history"
        assert parsed["repo"] == "facebook/react"
        assert "timeline" in parsed
        assert len(parsed["timeline"]) == 21

    def test_cmd_history_minimal_repo(self, monkeypatch):
        """Handle repos with minimal data (0 stars, no created_at)."""
        def mock_get_repo_info(_self, repo):
            return {"full_name": "empty/repo", "stars": 0, "created_at": ""}

        monkeypatch.setattr(
            "ara.core.GitHubClient.get_repo_info", mock_get_repo_info
        )
        cmd_history("empty/repo")
