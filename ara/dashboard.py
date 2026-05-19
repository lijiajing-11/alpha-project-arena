"""dashboard command — full repo overview at a glance.

Usage:
    ara dashboard <repo> [<repo> ...]
    ara dashboard --json <repo> [<repo> ...]

Shows a compact terminal dashboard with stars, forks, issues, language,
license, last updated time, and description for each repo.
"""

import json

from ara.core import GitHubClient
from ara.colors import BOLD, RESET, GREEN


def _format_number(n: int) -> str:
    """Format number with commas."""
    return f"{n:,}"


def _extract_license(license_val) -> str:
    """Extract a human-readable license name from raw GitHub API value.

    The API returns either a string ('MIT') or a dict
    (``{'key': 'mit', 'name': 'MIT License', ...}``).
    """
    if isinstance(license_val, dict):
        return license_val.get("name", license_val.get("key", str(license_val)))
    return license_val or "None"


def _print_dashboard(info: dict) -> None:
    """Print a compact dashboard for a single repo info dict."""
    name = info.get("full_name", info.get("name", "Unknown"))
    stars = info.get("stars", 0)
    forks = info.get("forks", 0)
    issues = info.get("open_issues", 0)
    lang = info.get("language") or "N/A"
    license_ = _extract_license(info.get("license"))
    updated = (info.get("updated_at") or "Unknown")[:10]
    desc = info.get("description") or "No description"

    print(f"  {BOLD}{name}{RESET}")
    print(f"  {'─' * 50}")
    print(f"    {GREEN}★{RESET} Stars:      {BOLD}{_format_number(stars)}{RESET}")
    print(f"    🍴 Forks:      {_format_number(forks)}")
    print(f"    ⚠  Issues:     {_format_number(issues)}")
    print(f"    {'─' * 30}")
    print(f"    📦 Language:   {lang}")
    print(f"    📄 License:    {license_}")
    print(f"    🕐  Updated:    {updated}")
    print(f"    📝 {desc[:60]}{'...' if len(desc) > 60 else ''}")


def _dashboard_json(repos: list[str], client: GitHubClient) -> str:
    """Build a JSON payload for one or more repos.

    Returns a prettified JSON string matching the shape other ``--json``
    handlers in the project use.
    """
    results: list[dict] = []
    errors: list[dict] = []
    for repo in repos:
        try:
            info = client.get_repo_info(repo)
            # Normalise fields to match the terminal output shape
            license_ = _extract_license(info.get("license"))
            results.append({
                "full_name": info.get("full_name", info.get("name", "Unknown")),
                "stars": info.get("stars", 0),
                "forks": info.get("forks", 0),
                "open_issues": info.get("open_issues", 0),
                "language": info.get("language") or "N/A",
                "license": license_,
                "updated_at": (info.get("updated_at") or "Unknown")[:10],
                "description": info.get("description") or "No description",
            })
        except (ValueError, RuntimeError) as e:
            errors.append({"repo": repo, "error": str(e)})
    return json.dumps(
        {"command": "dashboard", "repos": results, "errors": errors or None},
        indent=2,
        ensure_ascii=False,
    )


def cmd_dashboard(args, client: GitHubClient) -> None:
    """Handle `ara dashboard <repo> [<repo> ...]`.

    When ``--json`` is set, prints JSON instead of the terminal dashboard.
    """
    if getattr(args, "json", False):
        print(_dashboard_json(args.repos, client))
        return

    for i, repo in enumerate(args.repos):
        if i > 0:
            print()  # blank line between repos
        info = client.get_repo_info(repo)
        _print_dashboard(info)
