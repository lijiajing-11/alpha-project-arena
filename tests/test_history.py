"""Tests for `ara.history` — star history data generation."""

import pytest
from ara.history import cmd_history, _build_timeline_from_repo


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
