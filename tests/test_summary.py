"""Tests for `ara summary` command (Task 008-A)."""

import json
from unittest.mock import MagicMock, patch

import pytest


MOCK_INFO = {
    "full_name": "facebook/react",
    "name": "react",
    "stars": 226000,
    "forks": 47000,
    "open_issues": 1200,
    "language": "JavaScript",
    "license": {
        "key": "mit",
        "name": "MIT License",
    },
    "description": "A declarative UI library",
    "updated_at": "2026-05-18T14:30:00Z",
}


# ===========================================================================
# format_summary_line tests
# ===========================================================================


def test_format_summary_line_basic():
    """format_summary_line should produce correct format string."""
    from ara.summary import format_summary_line

    result = format_summary_line("facebook/react", MOCK_INFO)
    assert "★ facebook/react" in result
    assert "226,000 stars" in result
    assert "47,000 forks" in result
    assert "1,200 issues" in result
    assert "JavaScript" in result
    assert "MIT License" in result
    assert "A declarative UI library" in result


def test_format_summary_line_no_description():
    """format_summary_line should handle missing description."""
    from ara.summary import format_summary_line

    info = {**MOCK_INFO, "description": ""}
    result = format_summary_line("no/desc", info)
    assert "★ no/desc" in result
    assert "226,000 stars" in result
    assert "—" not in result  # no desc part


def test_format_summary_line_no_language():
    """format_summary_line should show N/A for missing language."""
    from ara.summary import format_summary_line

    info = {**MOCK_INFO, "language": None}
    result = format_summary_line("no/lang", info)
    assert "N/A" in result


def test_format_summary_line_license_string():
    """format_summary_line should handle license as plain string."""
    from ara.summary import format_summary_line

    info = {**MOCK_INFO, "license": "MIT"}
    result = format_summary_line("test/repo", info)
    assert "MIT" in result


def test_format_summary_line_license_none():
    """format_summary_line should show 'None' for missing license."""
    from ara.summary import format_summary_line

    info = {**MOCK_INFO, "license": None}
    result = format_summary_line("no-license/repo", info)
    assert "None" in result


# ===========================================================================
# cmd_summary (text mode) tests
# ===========================================================================


@patch("ara.summary.GitHubClient")
def test_cmd_summary_basic(MockClient, capsys):
    """cmd_summary should print one-line summary."""
    from ara.summary import cmd_summary

    mock_client = MockClient.return_value
    mock_client.get_repo_info.return_value = MOCK_INFO

    args = type("Args", (), {"repo": "facebook/react", "json": False})()
    cmd_summary(args, mock_client)

    captured = capsys.readouterr()
    assert "★ facebook/react" in captured.out
    assert "226,000 stars" in captured.out
    assert "47,000 forks" in captured.out
    assert "1,200 issues" in captured.out
    assert "JavaScript" in captured.out
    assert "MIT License" in captured.out


@patch("ara.summary.GitHubClient")
def test_cmd_summary_error(MockClient, capsys):
    """cmd_summary should handle fetch errors gracefully."""
    from ara.summary import cmd_summary

    mock_client = MockClient.return_value
    mock_client.get_repo_info.side_effect = ValueError("Repository not found")

    args = type("Args", (), {"repo": "nonexistent/repo", "json": False})()
    cmd_summary(args, mock_client)

    captured = capsys.readouterr()
    assert "N/A stars" in captured.out
    assert "Error: Repository not found" in captured.out


# ===========================================================================
# cmd_summary_json tests
# ===========================================================================


@patch("ara.summary.GitHubClient")
def test_cmd_summary_json_output(MockClient, capsys):
    """cmd_summary_json should print valid JSON with all expected fields."""
    from ara.summary import cmd_summary_json

    mock_client = MockClient.return_value
    mock_client.get_repo_info.return_value = MOCK_INFO

    args = type("Args", (), {"repo": "facebook/react"})()
    cmd_summary_json(args, mock_client)

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["stars"] == 226000
    assert data["forks"] == 47000
    assert data["open_issues"] == 1200
    assert data["language"] == "JavaScript"
    assert data["license"] == "MIT License"
    assert data["description"] == "A declarative UI library"


@patch("ara.summary.GitHubClient")
def test_cmd_summary_json_error(MockClient, capsys):
    """cmd_summary_json should include error field on failure."""
    from ara.summary import cmd_summary_json

    mock_client = MockClient.return_value
    mock_client.get_repo_info.side_effect = RuntimeError("API rate limit")

    args = type("Args", (), {"repo": "bad/repo"})()
    cmd_summary_json(args, mock_client)

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["stars"] is None
    assert data["forks"] is None
    assert "API rate limit" in data["error"]


# ===========================================================================
# CLI integration tests
# ===========================================================================


def test_parser_summary_command():
    """Parser should parse 'summary' subcommand with single repo."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["summary", "facebook/react"])
    assert args.command == "summary"
    assert args.repo == "facebook/react"
    assert args.json is False


def test_parser_summary_json_flag():
    """Parser should accept --json with summary command."""
    from ara.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["summary", "--json", "facebook/react"])
    assert args.json is True
    assert args.repo == "facebook/react"


def test_parser_summary_rejects_no_repo():
    """Parser should reject 'summary' without a repo argument."""
    from ara.cli import build_parser

    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["summary"])


@patch("ara.cli.GitHubClient")
def test_main_summary_command(MockClient, capsys):
    """main() should dispatch summary command successfully."""
    from ara.cli import main

    mock_instance = MagicMock()
    MockClient.return_value = mock_instance
    mock_instance.get_repo_info.return_value = MOCK_INFO

    result = main(["summary", "facebook/react"])
    assert result == 0

    captured = capsys.readouterr()
    assert "★ facebook/react" in captured.out
    assert "226,000 stars" in captured.out


@patch("ara.cli.GitHubClient")
def test_main_summary_json(MockClient, capsys):
    """main() should dispatch summary --json via json_handlers."""
    from ara.cli import main

    mock_instance = MagicMock()
    MockClient.return_value = mock_instance
    mock_instance.get_repo_info.return_value = MOCK_INFO

    result = main(["summary", "--json", "facebook/react"])
    assert result == 0

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["stars"] == 226000
    assert data["language"] == "JavaScript"
