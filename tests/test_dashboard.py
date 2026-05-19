"""Tests for `ara dashboard` command (Task 007-A)."""

from unittest.mock import patch


MOCK_REPO_INFO = {
    "full_name": "facebook/react",
    "name": "react",
    "stars": 226000,
    "forks": 47000,
    "open_issues": 1200,
    "language": "JavaScript",
    "license": "MIT",
    "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.",
    "updated_at": "2026-05-18T14:30:00Z",
}


@patch("ara.dashboard.GitHubClient")
def test_dashboard_prints_repo_info(MockClient, capsys):
    """Dashboard output should contain repo name, stars, forks, issues."""
    from ara.dashboard import cmd_dashboard

    mock_client = MockClient.return_value
    mock_client.get_repo_info.return_value = MOCK_REPO_INFO

    args = type("Args", (), {"repos": ["facebook/react"]})()
    cmd_dashboard(args, mock_client)

    captured = capsys.readouterr()
    assert "facebook/react" in captured.out
    assert "226,000" in captured.out
    assert "47,000" in captured.out
    assert "1,200" in captured.out


@patch("ara.dashboard.GitHubClient")
def test_dashboard_multi_repo(MockClient, capsys):
    """Dashboard with two repos should print both."""
    from ara.dashboard import cmd_dashboard

    mock_client = MockClient.return_value

    mock_infos = {
        "vuejs/core": {
            "full_name": "vuejs/core",
            "stars": 48000,
            "forks": 8000,
            "open_issues": 300,
            "language": "TypeScript",
            "license": "MIT",
            "description": "Vue.js core",
            "updated_at": "2026-05-17T10:00:00Z",
        },
        "sveltejs/svelte": {
            "full_name": "sveltejs/svelte",
            "stars": 82000,
            "forks": 4000,
            "open_issues": 150,
            "language": "TypeScript",
            "license": "MIT",
            "description": "Svelte framework",
            "updated_at": "2026-05-16T08:00:00Z",
        },
    }

    def mock_get_repo_info(repo):
        return mock_infos[repo]

    mock_client.get_repo_info.side_effect = mock_get_repo_info

    args = type("Args", (), {"repos": ["vuejs/core", "sveltejs/svelte"]})()
    cmd_dashboard(args, mock_client)

    captured = capsys.readouterr()
    assert "vuejs/core" in captured.out
    assert "sveltejs/svelte" in captured.out


@patch("ara.dashboard.GitHubClient")
def test_dashboard_empty_fields(MockClient, capsys):
    """Dashboard should show 'N/A' for missing language and 'No description' for missing description."""
    from ara.dashboard import cmd_dashboard

    mock_client = MockClient.return_value

    empty_info = {
        "full_name": "some/empty",
        "name": "empty",
        "stars": 100,
        "forks": 10,
        "open_issues": 5,
        "language": None,
        "license": None,
        "description": None,
        "updated_at": "2026-05-18T14:30:00Z",
    }
    mock_client.get_repo_info.return_value = empty_info

    args = type("Args", (), {"repos": ["some/empty"]})()
    cmd_dashboard(args, mock_client)

    captured = capsys.readouterr()
    assert "some/empty" in captured.out
    assert "N/A" in captured.out
    assert "No description" in captured.out
