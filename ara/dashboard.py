"""dashboard command — full repo overview at a glance."""

from ara.core import GitHubClient
from ara.colors import BOLD, RESET, GREEN


def _format_number(n: int) -> str:
    """Format number with commas."""
    return f"{n:,}"


def _resolve_license(lic) -> str:
    """Resolve license field — may be str, dict, or None."""
    if lic is None:
        return "None"
    if isinstance(lic, dict):
        return lic.get("name", lic.get("key", str(lic)))
    return str(lic)


def _print_dashboard(info: dict) -> None:
    """Print a compact dashboard for a single repo info dict."""
    name = info.get("full_name", info.get("name", "Unknown"))
    stars = info.get("stars", 0)
    forks = info.get("forks", 0)
    issues = info.get("open_issues", 0)
    lang = info.get("language") or "N/A"
    license_ = _resolve_license(info.get("license"))
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


def cmd_dashboard(args, client: GitHubClient) -> None:
    """Handle `ara dashboard <repo> [<repo> ...]`."""
    for i, repo in enumerate(args.repos):
        if i > 0:
            print()  # blank line between repos
        info = client.get_repo_info(repo)
        _print_dashboard(info)
