"""Tests for `ara.history` — star history data generation."""

import io
import json as _json
import sys

import pytest
from ara.history import cmd_history, cmd_history_compare, _build_timeline_from_repo


class TestBuildTimeline:
    """Tests for _build_timeline_from_repo."""

    def test_with_valid_repo_info(self, monkeypatch):
        def mock_get_repo_info(_self, repo):
            return {
                "full_name": "facebook/react",
                "stars": 226000,
                "created_at": "2013-05-29T21:12:00Z",
            }
        from ara.core import GitHubClient
        monkeypatch.setattr("ara.core.GitHubClient.get_repo_info", mock_get_repo_info)
        client = GitHubClient()
        result = _build_timeline_from_repo(client, "facebook/react")
        assert len(result) == 21
        assert result[0]["stars"] == 0
        assert result[-1]["stars"] == 226000

    def test_no_created_at(self, monkeypatch):
        def mock_get_repo_info(_self, repo):
            return {"full_name": "new/repo", "stars": 5, "created_at": ""}
        from ara.core import GitHubClient
        monkeypatch.setattr("ara.core.GitHubClient.get_repo_info", mock_get_repo_info)
        client = GitHubClient()
        assert _build_timeline_from_repo(client, "new/repo") == []

    def test_zero_stars(self, monkeypatch):
        def mock_get_repo_info(_self, repo):
            return {"full_name": "empty/repo", "stars": 0, "created_at": "2024-01-01T00:00:00Z"}
        from ara.core import GitHubClient
        monkeypatch.setattr("ara.core.GitHubClient.get_repo_info", mock_get_repo_info)
        client = GitHubClient()
        assert _build_timeline_from_repo(client, "empty/repo") == []

    def test_timeline_monotonic(self, monkeypatch):
        def mock_get_repo_info(_self, repo):
            return {"full_name": "growing/repo", "stars": 1000, "created_at": "2020-01-01T00:00:00Z"}
        from ara.core import GitHubClient
        monkeypatch.setattr("ara.core.GitHubClient.get_repo_info", mock_get_repo_info)
        client = GitHubClient()
        result = _build_timeline_from_repo(client, "growing/repo")
        stars = [p["stars"] for p in result]
        assert all(stars[i] <= stars[i + 1] for i in range(len(stars) - 1))


class TestCmdHistory:
    """Tests for cmd_history entry point."""

    def test_callable(self):
        assert callable(cmd_history)

    def test_no_crash(self, monkeypatch):
        def mock_get_repo_info(_self, repo):
            return {"full_name": "facebook/react", "stars": 226000, "created_at": "2013-05-29T21:12:00Z"}
        monkeypatch.setattr("ara.core.GitHubClient.get_repo_info", mock_get_repo_info)
        cmd_history("facebook/react")

    def test_json_output(self, monkeypatch):
        import json, io, sys
        def mock_get_repo_info(_self, repo):
            return {"full_name": "facebook/react", "stars": 226000, "created_at": "2013-05-29T21:12:00Z"}
        monkeypatch.setattr("ara.core.GitHubClient.get_repo_info", mock_get_repo_info)
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            cmd_history("facebook/react", as_json=True)
        finally:
            sys.stdout = old_stdout
        parsed = json.loads(captured.getvalue())
        assert parsed["command"] == "history"
        assert len(parsed["timeline"]) == 21

    def test_minimal_repo(self, monkeypatch):
        def mock_get_repo_info(_self, repo):
            return {"full_name": "empty/repo", "stars": 0, "created_at": ""}
        monkeypatch.setattr("ara.core.GitHubClient.get_repo_info", mock_get_repo_info)
        cmd_history("empty/repo")


class TestCmdHistoryCompare:
    """Tests for cmd_history_compare — multi-repo star history comparison."""

    def _mock_client(self, monkeypatch) -> "GitHubClient":
        """Patch GitHubClient.get_repo_info and return a client instance."""
        def mock_get_repo_info(_self, repo):
            mock_data = {
                "facebook/react": {
                    "full_name": "facebook/react",
                    "stars": 226000,
                    "created_at": "2013-05-29T21:12:00Z",
                },
                "vuejs/core": {
                    "full_name": "vuejs/core",
                    "stars": 48000,
                    "created_at": "2013-12-07T10:00:00Z",
                },
                "empty/repo": {
                    "full_name": "empty/repo",
                    "stars": 0,
                    "created_at": "",
                },
            }
            return mock_data.get(repo, {"full_name": repo, "stars": 0, "created_at": ""})
        monkeypatch.setattr("ara.core.GitHubClient.get_repo_info", mock_get_repo_info)
        from ara.core import GitHubClient
        return GitHubClient()

    def test_compare_basic(self, monkeypatch):
        """--compare should render multiple repos without crashing."""
        client = self._mock_client(monkeypatch)
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            cmd_history_compare(["facebook/react", "vuejs/core"], client=client)
        finally:
            sys.stdout = old_stdout
        output = captured.getvalue()
        # Should have a header
        assert "Star History Comparison" in output
        # Both repo names should appear
        assert "facebook/react" in output
        assert "vuejs/core" in output

    def test_compare_json(self, monkeypatch):
        """--compare --json should output valid JSON."""
        client = self._mock_client(monkeypatch)
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            cmd_history_compare(
                ["facebook/react", "vuejs/core"],
                client=client,
                as_json=True,
            )
        finally:
            sys.stdout = old_stdout
        parsed = _json.loads(captured.getvalue())
        assert parsed["command"] == "history"
        assert parsed["mode"] == "compare"
        assert len(parsed["repos"]) == 2
        repo_names = [r["repo"] for r in parsed["repos"]]
        assert "facebook/react" in repo_names
        assert "vuejs/core" in repo_names
        assert len(parsed["repos"][0]["timeline"]) == 21

    def test_compare_since_filter(self, monkeypatch):
        """--since should filter data points (only future dates remain)."""
        client = self._mock_client(monkeypatch)
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            cmd_history_compare(
                ["facebook/react"],
                client=client,
                since="2099-01-01",
                as_json=True,
            )
        finally:
            sys.stdout = old_stdout
        parsed = _json.loads(captured.getvalue())
        # With since far in the future, all data should be filtered out
        assert parsed["command"] == "history"
        assert parsed["mode"] == "compare"
        assert "error" in parsed
        assert len(parsed["repos"][0]["timeline"]) == 0

    def test_compare_empty_repo_skipped(self, monkeypatch):
        """A repo with no data should show 0 stars without crashing."""
        client = self._mock_client(monkeypatch)
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            cmd_history_compare(
                ["facebook/react", "empty/repo"],
                client=client,
            )
        finally:
            sys.stdout = old_stdout
        output = captured.getvalue()
        assert "facebook/react" in output
        assert "empty/repo" in output
        assert "0 ★" in output or "0," in output

    def test_compare_single_repo(self, monkeypatch):
        """--compare with a single repo should still work."""
        client = self._mock_client(monkeypatch)
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            cmd_history_compare(["facebook/react"], client=client)
        finally:
            sys.stdout = old_stdout
        output = captured.getvalue()
        assert "facebook/react" in output
