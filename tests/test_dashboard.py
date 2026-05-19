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


LICENSE_DICT_INFO = {
    "full_name": "test/license-dict",
    "name": "license-dict",
    "stars": 500,
    "forks": 50,
    "open_issues": 5,
    "language": "Python",
    "license": {"key": "mit", "name": "MIT License"},
    "description": "A repo with a dict license",
    "updated_at": "2026-05-18T14:30:00Z",
}

LICENSE_STRING_INFO = {
    "full_name": "test/license-str",
    "name": "license-str",
    "stars": 300,
    "forks": 30,
    "open_issues": 2,
    "language": "Rust",
    "license": "Apache-2.0",
    "description": "A repo with a string license",
    "updated_at": "2026-05-17T10:00:00Z",
}


@patch("ara.dashboard.GitHubClient")
def test_dashboard_license_dict(MockClient, capsys):
    """Dashboard should resolve dict license to 'MIT License'."""
    from ara.dashboard import cmd_dashboard

    mock_client = MockClient.return_value
    mock_client.get_repo_info.return_value = LICENSE_DICT_INFO
    args = type("Args", (), {"repos": ["test/license-dict"], "json": False})()
    cmd_dashboard(args, mock_client)
    captured = capsys.readouterr()
    assert "MIT License" in captured.out
    assert "None" not in captured.out  # dict should not fallback to literal string


@patch("ara.dashboard.GitHubClient")
def test_dashboard_license_string(MockClient, capsys):
    """Dashboard should pass through a plain string license value."""
    from ara.dashboard import cmd_dashboard

    mock_client = MockClient.return_value
    mock_client.get_repo_info.return_value = LICENSE_STRING_INFO
    args = type("Args", (), {"repos": ["test/license-str"], "json": False})()
    cmd_dashboard(args, mock_client)
    captured = capsys.readouterr()
    assert "Apache-2.0" in captured.out


@patch("ara.dashboard.GitHubClient")
def test_dashboard_json_output(MockClient):
    """Dashboard --json should print JSON payload with repo info."""
    from ara.dashboard import _dashboard_json

    mock_client = MockClient.return_value
    mock_client.get_repo_info.return_value = MOCK_REPO_INFO
    result = _dashboard_json(["facebook/react"], mock_client)
    import json
    data = json.loads(result)
    assert data["command"] == "dashboard"
    assert len(data["repos"]) == 1
    assert data["repos"][0]["full_name"] == "facebook/react"
    assert data["repos"][0]["stars"] == 226000
    assert data["errors"] is None


@patch("ara.dashboard.GitHubClient")
def test_dashboard_json_multi_repo(MockClient):
    """Dashboard --json with multiple repos returns all in the payload."""
    from ara.dashboard import _dashboard_json

    mock_client = MockClient.return_value

    mock_infos = {
        "vuejs/core": {
            "full_name": "vuejs/core",
            "name": "core",
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
            "name": "svelte",
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

    result = _dashboard_json(["vuejs/core", "sveltejs/svelte"], mock_client)
    import json
    data = json.loads(result)
    assert data["command"] == "dashboard"
    assert len(data["repos"]) == 2
    names = [r["full_name"] for r in data["repos"]]
    assert "vuejs/core" in names
    assert "sveltejs/svelte" in names


@patch("ara.dashboard.GitHubClient")
def test_dashboard_json_errors(MockClient):
    """Dashboard --json should capture errors in the payload."""
    from ara.dashboard import _dashboard_json

    mock_client = MockClient.return_value
    mock_client.get_repo_info.side_effect = ValueError("Not found")

    result = _dashboard_json(["bad/repo"], mock_client)
    import json
    data = json.loads(result)
    assert data["command"] == "dashboard"
    assert len(data["repos"]) == 0
    assert data["errors"] is not None
    assert data["errors"][0]["repo"] == "bad/repo"
    assert "Not found" in data["errors"][0]["error"]
