"""Tests for the ARA rank module.

Tests:
- fetch_all_repos: correct fetching, error handling, sorting
- format_rank_table: table structure, top_n limit, empty edge case
- _format_stars, _format_forks: formatting helpers
- cmd_rank_json: JSON output structure
"""

import json

from ara.rank import (
    DEFAULT_REPOS,
    _format_forks,
    _format_stars,
    cmd_rank_json,
    fetch_all_repos,
    format_rank_table,
)


class FakeClient:
    """Mock GitHubClient that returns predefined repo info."""

    def __init__(self, repos_data: dict | None = None):
        self.repos_data = repos_data or {}

    def get_repo_info(self, repo: str) -> dict:
        if repo in self.repos_data:
            return self.repos_data[repo]
        if repo == "error/repo":
            raise ValueError("Repository not found: error/repo")
        if repo == "timeout/repo":
            raise RuntimeError("GitHub API error 500: Internal Server Error")
        raise ValueError(f"Repository not found: {repo}")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_REPOS = [
    "facebook/react",
    "vuejs/core",
    "sveltejs/svelte",
]

SAMPLE_DATA = {
    "facebook/react": {
        "full_name": "facebook/react",
        "stars": 226000,
        "forks": 47000,
        "open_issues": 1200,
        "language": "JavaScript",
        "license": "MIT",
        "description": "A declarative UI library",
    },
    "vuejs/core": {
        "full_name": "vuejs/core",
        "stars": 47000,
        "forks": 7800,
        "open_issues": 800,
        "language": "TypeScript",
        "license": "MIT",
        "description": "Vue.js core",
    },
    "sveltejs/svelte": {
        "full_name": "sveltejs/svelte",
        "stars": 82000,
        "forks": 4500,
        "open_issues": 300,
        "language": "TypeScript",
        "license": "MIT",
        "description": "Svelte framework",
    },
}

SAMPLE_EMPTY_RESULTS: list[dict] = []


# ---------------------------------------------------------------------------
# Test _format_stars and _format_forks
# ---------------------------------------------------------------------------


class TestFormatHelpers:
    """Test the formatting helper functions."""

    def test_format_stars_under_1000(self):
        assert _format_stars(999) == "999"

    def test_format_stars_thousands(self):
        assert _format_stars(1000) == "1,000"
        assert _format_stars(226000) == "226,000"

    def test_format_stars_millions(self):
        assert _format_stars(1000000) == "1.0M"
        assert _format_stars(1500000) == "1.5M"

    def test_format_forks_under_1000(self):
        assert _format_forks(500) == "500"

    def test_format_forks_thousands(self):
        assert _format_forks(1000) == "1k"
        assert _format_forks(47000) == "47k"
        assert _format_forks(7800) == "7k"

    def test_format_forks_zero(self):
        assert _format_forks(0) == "0"


# ---------------------------------------------------------------------------
# Test fetch_all_repos
# ---------------------------------------------------------------------------


class TestFetchAllRepos:
    """Test fetch_all_repos function."""

    def test_fetch_success(self):
        client = FakeClient(SAMPLE_DATA)
        results, errors = fetch_all_repos(client, SAMPLE_REPOS)

        assert len(errors) == 0
        # Should be sorted by stars descending: react (226k) > svelte (82k) > vue (47k)
        assert results[0]["full_name"] == "facebook/react"
        assert results[1]["full_name"] == "sveltejs/svelte"
        assert results[2]["full_name"] == "vuejs/core"

    def test_fetch_correct_count(self):
        client = FakeClient(SAMPLE_DATA)
        results, errors = fetch_all_repos(client, SAMPLE_REPOS)
        assert len(results) == 3
        assert results[0]["stars"] == 226000

    def test_fetch_with_errors(self):
        repos = ["facebook/react", "error/repo", "sveltejs/svelte", "timeout/repo"]
        client = FakeClient(SAMPLE_DATA)
        results, errors = fetch_all_repos(client, repos)

        assert len(results) == 2  # only successful ones
        assert len(errors) == 2
        assert errors[0]["repo"] == "error/repo"
        assert errors[1]["repo"] == "timeout/repo"

    def test_fetch_all_fail(self):
        repos = ["error/repo", "notfound/repo"]
        client = FakeClient({})
        results, errors = fetch_all_repos(client, repos)
        assert len(results) == 0
        assert len(errors) == 2

    def test_fetch_empty_list(self):
        client = FakeClient({})
        results, errors = fetch_all_repos(client, [])
        assert len(results) == 0
        assert len(errors) == 0

    def test_default_repos_is_not_empty(self):
        assert len(DEFAULT_REPOS) == 10
        assert "facebook/react" in DEFAULT_REPOS
        assert "jquery/jquery" in DEFAULT_REPOS

    def test_fetch_sorts_by_stars_descending(self):
        data = {
            "a/repo": {"full_name": "a/repo", "stars": 100},
            "b/repo": {"full_name": "b/repo", "stars": 500},
            "c/repo": {"full_name": "c/repo", "stars": 50},
        }
        client = FakeClient(data)
        results, _ = fetch_all_repos(client, ["a/repo", "b/repo", "c/repo"])
        assert results[0]["full_name"] == "b/repo"
        assert results[1]["full_name"] == "a/repo"
        assert results[2]["full_name"] == "c/repo"


# ---------------------------------------------------------------------------
# Test format_rank_table
# ---------------------------------------------------------------------------


class TestFormatRankTable:
    """Test format_rank_table formatting."""

    def _make_result(
        self, name: str, stars: int = 1000, forks: int = 100, lang: str = "Python"
    ) -> dict:
        return {
            "full_name": name,
            "stars": stars,
            "forks": forks,
            "language": lang,
            "license": "MIT",
            "description": "",
        }

    def test_empty_results(self):
        result = format_rank_table(SAMPLE_EMPTY_RESULTS, top_n=10)
        assert result == "No repo data available."

    def test_single_repo_table(self):
        results = [self._make_result("test/repo", stars=5000)]
        table = format_rank_table(results, top_n=10)
        assert "test/repo" in table
        assert "5,000" in table
        assert "┌" in table
        assert "└" in table

    def test_top_n_limit(self):
        results = [
            self._make_result(f"repo/{i}", stars=1000 - i * 10)
            for i in range(20)
        ]
        table = format_rank_table(results, top_n=5)
        # Count rows — each row line has "│" and repo name
        lines = table.split("\n")
        # 3 header lines (top, header, sep) + 5 data rows + 1 bottom
        assert len(lines) == 9, f"Expected 9 lines, got {len(lines)}"
        # First data row is repo/0 (highest stars)
        assert "repo/0" in table
        # Fifth data row is repo/4
        assert "repo/4" in table
        # repo/5 should NOT appear
        assert "repo/5" not in table

    def test_top_n_larger_than_results(self):
        results = [
            self._make_result("a/repo", stars=100),
            self._make_result("b/repo", stars=50),
        ]
        table = format_rank_table(results, top_n=10)
        lines = table.split("\n")
        # 3 header + 2 data + 1 bottom = 6
        assert len(lines) == 6
        assert "a/repo" in table
        assert "b/repo" in table

    def test_table_has_header_row(self):
        results = [self._make_result("test/repo")]
        table = format_rank_table(results, top_n=10)
        assert "Repo" in table
        assert "Stars" in table
        assert "Forks" in table
        assert "Language" in table

    def test_table_contains_rank_numbers(self):
        results = [
            self._make_result("a/repo", stars=300),
            self._make_result("b/repo", stars=200),
            self._make_result("c/repo", stars=100),
        ]
        table = format_rank_table(results, top_n=10)
        assert "1" in table
        assert "2" in table
        assert "3" in table

    def test_language_fallback(self):
        """Repo with no language should show — (em dash)."""
        results = [{"full_name": "no/lang", "stars": 100, "forks": 10, "language": None}]
        table = format_rank_table(results, top_n=10)
        assert "—" in table

    def test_box_drawing_borders(self):
        results = [self._make_result("test/repo", stars=500)]
        table = format_rank_table(results, top_n=10)
        assert table.startswith("┌")
        assert table.endswith("┘")

    def test_multi_repo_sorting_order_in_table(self):
        """Table should respect the sorted order passed in."""
        results = [
            self._make_result("top/repo", stars=999),
            self._make_result("mid/repo", stars=500),
            self._make_result("low/repo", stars=100),
        ]
        table = format_rank_table(results, top_n=10)
        # First data row after separator should be top/repo
        lines = [l for l in table.split("\n") if "repo/" in l]
        assert len(lines) == 3
        assert "top/repo" in lines[0]
        assert "mid/repo" in lines[1]
        assert "low/repo" in lines[2]


# ---------------------------------------------------------------------------
# Test cmd_rank_json
# ---------------------------------------------------------------------------


class TestCmdRankJson:
    """Test the JSON output of rank."""

    def test_json_structure(self, capsys):
        client = FakeClient(SAMPLE_DATA)
        repos = ["facebook/react", "vuejs/core"]
        args = type("Args", (), {"repos": repos, "top": 10, "json": True})()

        cmd_rank_json(args, client)

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["command"] == "rank"
        assert data["top"] == 10
        assert len(data["repos"]) == 2
        assert data["errors"] is None

    def test_json_sorted_by_stars(self, capsys):
        client = FakeClient(SAMPLE_DATA)
        repos = ["vuejs/core", "facebook/react"]  # intentionally unsorted
        args = type("Args", (), {"repos": repos, "top": 10, "json": True})()

        cmd_rank_json(args, client)

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["repos"][0]["full_name"] == "facebook/react"

    def test_json_has_rank_field(self, capsys):
        client = FakeClient(SAMPLE_DATA)
        repos = ["facebook/react", "vuejs/core"]
        args = type("Args", (), {"repos": repos, "top": 10, "json": True})()

        cmd_rank_json(args, client)

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["repos"][0]["rank"] == 1
        assert data["repos"][1]["rank"] == 2

    def test_json_errors_included(self, capsys):
        repos = ["facebook/react", "error/repo"]
        client = FakeClient(SAMPLE_DATA)
        args = type("Args", (), {"repos": repos, "top": 10, "json": True})()

        cmd_rank_json(args, client)

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert len(data["repos"]) == 1  # only successful
        assert data["errors"] is not None
        assert len(data["errors"]) == 1
        assert data["errors"][0]["repo"] == "error/repo"

    def test_json_all_fail(self, capsys):
        repos = ["error/repo", "timeout/repo"]
        client = FakeClient({})
        args = type("Args", (), {"repos": repos, "top": 10, "json": True})()

        cmd_rank_json(args, client)

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert len(data["repos"]) == 0
        assert len(data["errors"]) == 2

    def test_json_top_n_limit(self, capsys):
        client = FakeClient(SAMPLE_DATA)
        repos = ["facebook/react", "vuejs/core", "sveltejs/svelte"]
        args = type("Args", (), {"repos": repos, "top": 2, "json": True})()

        cmd_rank_json(args, client)

        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert len(data["repos"]) == 2
        assert data["top"] == 2


# ---------------------------------------------------------------------------
# Test CLI integration
# ---------------------------------------------------------------------------


class TestCliIntegration:
    """Test that rank can be invoked via CLI entry points."""

    def test_invoke_via_build_parser(self):
        """Smoke test: rank parser builds and parses correctly."""
        from ara.cli import build_parser

        parser = build_parser()
        args = parser.parse_args(["rank"])
        assert args.command == "rank"
        assert args.top == 10  # default
        assert args.repos == []  # defaults to empty list for nargs="*"
        assert not args.json

    def test_parse_custom_top(self):
        from ara.cli import build_parser

        parser = build_parser()
        args = parser.parse_args(["rank", "--top", "5"])
        assert args.top == 5

    def test_parse_with_repos(self):
        from ara.cli import build_parser

        parser = build_parser()
        args = parser.parse_args(["rank", "facebook/react", "vuejs/core"])
        assert args.repos == ["facebook/react", "vuejs/core"]

    def test_parse_json_flag(self):
        from ara.cli import build_parser

        parser = build_parser()
        args = parser.parse_args(["rank", "--json"])
        assert args.json
