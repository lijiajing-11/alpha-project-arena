"""Tests for `ara summary` command (Task 008-A)."""

from unittest.mock import patch

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


@patch("ara.summary.GitHubClient")
def test_summary_one_line(MockClient, capsys):
    """Single repo summary should output one line with key fields."""
    from ara.summary import cmd_summary

    mock_client = MockClient.return_value
    mock_client.get_repo_info.return_value = MOCK_INFO

    args = type("Args", (), {"repos": ["facebook/react"], "json": False})()
    cmd_summary(args, mock_client)

    captured = capsys.readouterr()
    assert "#" in captured.out
    assert "226,000" in captured.out
    assert "JavaScript" in captured.out
    assert "MIT License" in captured.out
    assert "A declarative" in captured.out


@patch("ara.summary.GitHubClient")
def test_summary_multi_repo(MockClient, capsys):
    """Multi-repo summary should show repo names as labels."""
    from ara.summary import cmd_summary

    mock_client = MockClient.return_value

    def mock_get_info(repo):
        return {**MOCK_INFO, "full_name": repo}

    mock_client.get_repo_info.side_effect = mock_get_info

    args = type("Args", (), {
        "repos": ["facebook/react", "vuejs/core"],
        "json": False,
    })()
    cmd_summary(args, mock_client)

    captured = capsys.readouterr()
    lines = [l for l in captured.out.split("\n") if l.strip()]
    assert len(lines) == 2
    assert "facebook/react" in captured.out
    assert "vuejs/core" in captured.out


@patch("ara.summary.GitHubClient")
def test_summary_json(MockClient, capsys):
    """JSON output should be parseable JSON with all fields."""
    import json
    from ara.summary import cmd_summary

    mock_client = MockClient.return_value
    mock_client.get_repo_info.return_value = MOCK_INFO

    args = type("Args", (), {"repos": ["facebook/react"], "json": True})()
    cmd_summary(args, mock_client)

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["command"] == "summary"
    assert len(data["repos"]) == 1
    assert data["repos"][0]["stars"] == 226000
    assert data["repos"][0]["license"] == "MIT License"


@patch("ara.summary.GitHubClient")
def test_summary_license_dict(MockClient, capsys):
    """License dict should be resolved to string name."""
    from ara.summary import cmd_summary

    mock_client = MockClient.return_value
    mock_client.get_repo_info.return_value = {
        **MOCK_INFO,
        "license": {"key": "apache-2.0", "name": "Apache License 2.0"},
    }

    args = type("Args", (), {"repos": ["apache/spark"], "json": False})()
    cmd_summary(args, mock_client)

    captured = capsys.readouterr()
    assert "Apache License 2.0" in captured.out


@patch("ara.summary.GitHubClient")
def test_summary_license_none(MockClient, capsys):
    """None license should be displayed as 'None'."""
    from ara.summary import cmd_summary

    mock_client = MockClient.return_value
    mock_client.get_repo_info.return_value = {
        **MOCK_INFO,
        "license": None,
    }

    args = type("Args", (), {"repos": ["no-license/repo"], "json": False})()
    cmd_summary(args, mock_client)

    captured = capsys.readouterr()
    assert "📄 None" in captured.out
