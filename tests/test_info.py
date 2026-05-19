"""Tests for repo info and compare functionality."""

import json
from unittest.mock import MagicMock, patch

import pytest


# ===========================================================================
# core.get_repo_info tests
# ===========================================================================


@patch("ara.core.urllib.request.urlopen")
def test_get_repo_info_returns_full_dict(mock_urlopen):
    """get_repo_info should return a dict with all expected keys."""
    from ara.core import GitHubClient

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({
        "name": "test-repo",
        "full_name": "owner/test-repo",
        "description": "A test repo",
        "stargazers_count": 500,
        "forks_count": 100,
        "open_issues_count": 10,
        "language": "Python",
        "topics": ["test", "demo"],
        "license": {"spdx_id": "MIT"},
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-06-01T00:00:00Z",
        "pushed_at": "2024-06-15T00:00:00Z",
        "html_url": "https://github.com/owner/test-repo",
    }).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp
    mock_urlopen.return_value = mock_resp

    client = GitHubClient()
    info = client.get_repo_info("owner/test-repo")
    assert info["name"] == "test-repo"
    assert info["full_name"] == "owner/test-repo"
    assert info["description"] == "A test repo"
    assert info["stars"] == 500
    assert info["forks"] == 100
    assert info["open_issues"] == 10
    assert info["language"] == "Python"
    assert info["topics"] == ["test", "demo"]
    assert info["license"] == "MIT"
    assert "2024-01-01" in info["created_at"]


@patch("ara.core.urllib.request.urlopen")
def test_get_repo_info_handles_missing_fields(mock_urlopen):
    """get_repo_info should handle missing optional fields gracefully."""
    from ara.core import GitHubClient

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({
        "name": "minimal-repo",
        "full_name": "owner/minimal-repo",
    }).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp
    mock_urlopen.return_value = mock_resp

    client = GitHubClient()
    info = client.get_repo_info("owner/minimal-repo")
    assert info["name"] == "minimal-repo"
    assert info["stars"] == 0
    assert info["description"] == ""
    assert info["language"] is None
    assert info["topics"] == []
    assert info["license"] is None


@patch("ara.core.urllib.request.urlopen")
def test_get_repo_info_404(mock_urlopen):
    """get_repo_info should raise ValueError on 404."""
    from ara.core import GitHubClient
    import urllib.error

    mock_urlopen.side_effect = urllib.error.HTTPError(
        url="https://api.github.com/repos/owner/nonexistent",
        code=404,
        msg="Not Found",
        hdrs={},
        fp=None,
    )

    client = GitHubClient()
    with pytest.raises(ValueError, match="Repository not found"):
        client.get_repo_info("owner/nonexistent")


# ===========================================================================
# cli info/compare command tests
# ===========================================================================


def test_parser_info_command():
    """Parser should parse 'info' subcommand."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["info", "owner/repo"])
    assert args.command == "info"
    assert args.repos == ["owner/repo"]


def test_parser_info_json_flag():
    """Parser should accept --json with info command."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["info", "--json", "owner/repo"])
    assert args.json is True


def test_parser_compare_command():
    """Parser should parse 'compare' subcommand with exactly 2 repos."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["compare", "owner/a", "owner/b"])
    assert args.command == "compare"
    assert args.repos == ["owner/a", "owner/b"]


def test_parser_compare_invalid_args():
    """Parser should reject 'compare' without exactly 2 repos."""
    from ara.cli import build_parser

    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["compare", "owner/a"])


def test_parser_compare_json_flag():
    """Parser should accept --json with compare command."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["compare", "--json", "owner/a", "owner/b"])
    assert args.json is True
    assert args.repos == ["owner/a", "owner/b"]


@patch("ara.cli.GitHubClient")
def test_main_info_command(MockClient):
    """main() should dispatch info command successfully."""
    from ara.cli import main

    mock_instance = MagicMock()
    MockClient.return_value = mock_instance
    mock_instance.get_repo_info.return_value = {
        "name": "test-repo", "full_name": "owner/test-repo",
        "stars": 500, "forks": 100, "open_issues": 10,
        "language": "Python", "topics": [], "license": "MIT",
        "html_url": "https://github.com/owner/test-repo",
        "description": "", "created_at": "", "updated_at": "", "pushed_at": "",
    }

    result = main(["info", "owner/test-repo"])
    assert result == 0


@patch("ara.cli.GitHubClient")
def test_main_compare_command(MockClient):
    """main() should dispatch compare command successfully."""
    from ara.cli import main

    mock_instance = MagicMock()
    MockClient.return_value = mock_instance
    info = {
        "name": "test-repo", "full_name": "owner/test-repo",
        "stars": 500, "forks": 100, "open_issues": 10,
        "language": "Python", "topics": [], "license": "MIT",
        "html_url": "", "description": "", "created_at": "",
        "updated_at": "", "pushed_at": "",
    }
    mock_instance.get_repo_info.return_value = info

    result = main(["compare", "owner/a", "owner/b"])
    assert result == 0


def test_cmd_info_json_output(capsys):
    """cmd_info_json should print valid JSON with repo info."""
    from ara.cli import cmd_info_json
    import argparse

    mock_client = MagicMock()
    mock_client.get_repo_info.return_value = {
        "name": "test-repo", "full_name": "owner/test-repo",
        "stars": 500, "forks": 100, "open_issues": 10,
        "language": "Python", "topics": ["demo"], "license": "MIT",
        "html_url": "https://github.com/owner/test-repo",
        "description": "A test repo", "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-06-01T00:00:00Z", "pushed_at": "2024-06-15T00:00:00Z",
    }

    args = argparse.Namespace(repos=["owner/test-repo"])
    cmd_info_json(args, mock_client)

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["command"] == "info"
    assert len(data["repos"]) == 1
    assert data["repos"][0]["full_name"] == "owner/test-repo"
    assert data["repos"][0]["stars"] == 500


def test_cmd_compare_json_output(capsys):
    """cmd_compare_json should print valid JSON with two repo infos."""
    from ara.cli import cmd_compare_json
    import argparse

    mock_client = MagicMock()
    info_a = {
        "name": "repo-a", "full_name": "owner/repo-a",
        "stars": 1000, "forks": 200, "open_issues": 5,
        "language": "Python", "topics": [], "license": "MIT",
        "html_url": "", "description": "", "created_at": "",
        "updated_at": "", "pushed_at": "",
    }
    info_b = {
        "name": "repo-b", "full_name": "owner/repo-b",
        "stars": 500, "forks": 50, "open_issues": 20,
        "language": "Rust", "topics": [], "license": "Apache-2.0",
        "html_url": "", "description": "", "created_at": "",
        "updated_at": "", "pushed_at": "",
    }

    def mock_get_info(repo):
        return {"owner/repo-a": info_a, "owner/repo-b": info_b}.get(repo, {})

    mock_client.get_repo_info.side_effect = mock_get_info

    args = argparse.Namespace(repos=["owner/repo-a", "owner/repo-b"])
    cmd_compare_json(args, mock_client)

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["command"] == "compare"
    assert len(data["repos"]) == 2
    assert data["repos"][0]["full_name"] == "owner/repo-a"
    assert data["repos"][1]["full_name"] == "owner/repo-b"


# ===========================================================================
# display formatter tests
# ===========================================================================


def test_format_repo_info_contains_fields():
    """format_repo_info should include key fields."""
    from ara.display import format_repo_info

    info = {
        "name": "test-repo", "full_name": "owner/test-repo",
        "stars": 1234, "forks": 100, "open_issues": 10,
        "language": "Python", "topics": ["ai", "cli"], "license": "MIT",
        "html_url": "https://github.com/owner/test-repo",
        "description": "A test repository",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-06-01T00:00:00Z",
        "pushed_at": "2024-06-15T00:00:00Z",
    }

    output = format_repo_info(info)
    assert "owner/test-repo" in output
    assert "1,234" in output  # star count formatted
    assert "100" in output   # forks
    assert "Python" in output
    assert "MIT" in output
    assert "ai, cli" in output
    assert "A test repository" in output


def test_format_compare_shows_winner():
    """format_compare should indicate the winning repo."""
    from ara.display import format_compare

    info_a = {
        "name": "repo-a", "full_name": "owner/repo-a",
        "stars": 1000, "forks": 200, "open_issues": 5,
        "language": "Python", "topics": [], "license": None,
        "html_url": "", "description": "", "created_at": "",
        "updated_at": "", "pushed_at": "",
    }
    info_b = {
        "name": "repo-b", "full_name": "owner/repo-b",
        "stars": 500, "forks": 50, "open_issues": 20,
        "language": "Rust", "topics": [], "license": None,
        "html_url": "", "description": "", "created_at": "",
        "updated_at": "", "pushed_at": "",
    }

    output = format_compare(info_a, info_b)
    assert "owner/repo-a" in output
    assert "owner/repo-b" in output
    assert "wins by 500" in output


def test_format_compare_tie():
    """format_compare should handle ties."""
    from ara.display import format_compare

    info = {
        "name": "repo", "full_name": "owner/repo",
        "stars": 100, "forks": 10, "open_issues": 0,
        "language": "Python", "topics": [], "license": None,
        "html_url": "", "description": "", "created_at": "",
        "updated_at": "", "pushed_at": "",
    }

    output = format_compare(info, info)
    assert "tie" in output.lower() or "draw" in output.lower()
