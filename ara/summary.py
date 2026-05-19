"""summary command — one-line repo overview.

Usage:
  ara summary facebook/react
  ara summary facebook/react --json
"""

import json

from ara.core import GitHubClient


def _format_number(n: int) -> str:
    """Format a number with commas (e.g. 226000 -> '226,000')."""
    return f"{n:,}"


def _resolve_license(info: dict) -> str:
    """Extract license name from repo info, handling dict or string value.

    GitHub API may return license as:
      - {"key": "mit", "name": "MIT License", ...}  (dict)
      - "MIT"  (string, unlikely but defensive)
      - None
    """
    license_ = info.get("license")
    if isinstance(license_, dict):
        return license_.get("name", license_.get("key", "Unknown"))
    if isinstance(license_, str):
        return license_
    return "None"


def format_summary_line(repo: str, info: dict) -> str:
    """Format a single-line summary string from repo info.

    Format: ★ facebook/react · 226,000 stars · 47,000 forks · 1,200 issues · JavaScript · MIT

    Args:
        repo: Repository name (owner/repo).
        info: Dict from client.get_repo_info().

    Returns:
        Formatted one-line summary string.
    """
    stars = _format_number(info.get("stars", 0))
    forks = _format_number(info.get("forks", 0))
    issues = _format_number(info.get("open_issues", 0))
    lang = info.get("language") or "N/A"
    license_ = _resolve_license(info)
    desc = (info.get("description") or "")[:60]
    desc_part = f"  —  {desc}" if desc else ""

    return (
        f"★ {repo} · {stars} stars · {forks} forks · "
        f"{issues} issues · {lang} · {license_}{desc_part}"
    )


def cmd_summary(args, client: GitHubClient) -> None:
    """Handle `ara summary <repo>` — one-line text summary.

    Args:
        args: argparse.Namespace with .repo attribute.
        client: GitHubClient instance.
    """
    repo = args.repo
    try:
        info = client.get_repo_info(repo)
        line = format_summary_line(repo, info)
        print(line)
    except (ValueError, RuntimeError) as e:
        print(f"★ {repo} · N/A stars · N/A forks · N/A issues · N/A · N/A  —  Error: {e}")


def cmd_summary_json(args, client: GitHubClient) -> None:
    """Handle `ara summary <repo> --json` — structured JSON output.

    Args:
        args: argparse.Namespace with .repo attribute.
        client: GitHubClient instance.
    """
    repo = args.repo
    try:
        info = client.get_repo_info(repo)
        result = {
            "stars": info.get("stars", 0),
            "forks": info.get("forks", 0),
            "open_issues": info.get("open_issues", 0),
            "language": info.get("language"),
            "license": _resolve_license(info),
            "description": info.get("description"),
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (ValueError, RuntimeError) as e:
        result = {
            "stars": None,
            "forks": None,
            "open_issues": None,
            "language": None,
            "license": None,
            "description": None,
            "error": str(e),
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
