"""summary command — one-line repo overview.

Usage:
  ara summary facebook/react
  ara summary facebook/react vercel/next.js
  ara summary facebook/react --json
"""

import json

from ara.core import GitHubClient
from ara.colors import BOLD, RESET


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


def _build_summary_line(info: dict) -> str:
    """Build a one-line summary string from repo info.

    Format: ⭐ 226,000 · 🍴 47,000 · ⚠ 1,200 · 📦 JavaScript · 📄 MIT
    """
    stars = _format_number(info.get("stars", 0))
    forks = _format_number(info.get("forks", 0))
    issues = _format_number(info.get("open_issues", 0))
    lang = info.get("language") or "N/A"
    license_ = _resolve_license(info)
    desc = (info.get("description") or "")[:40]

    line = f"⭐ {stars} · 🍴 {forks} · ⚠ {issues} · 📦 {lang} · 📄 {license_}"
    if desc:
        line += f"  —  {desc}"
    return line


def cmd_summary(args, client: GitHubClient) -> None:
    """Handle `ara summary <repo> [<repo> ...]`.

    Text mode: outputs lines prefixed with '# ' for easy copy-paste.
    JSON mode: outputs structured JSON with all fields.
    """
    if getattr(args, "json", False):
        results = []
        for repo in args.repos:
            info = client.get_repo_info(repo)
            results.append({
                "repo": repo,
                "stars": info.get("stars", 0),
                "forks": info.get("forks", 0),
                "open_issues": info.get("open_issues", 0),
                "language": info.get("language"),
                "license": _resolve_license(info),
                "description": info.get("description"),
            })
        print(json.dumps(
            {"command": "summary", "repos": results},
            indent=2, ensure_ascii=False,
        ))
    else:
        for i, repo in enumerate(args.repos):
            info = client.get_repo_info(repo)
            line = _build_summary_line(info)
            if len(args.repos) > 1:
                line += f"  —  {BOLD}{repo}{RESET}"
            print(f"# {line}")
