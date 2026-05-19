"""generate-stars command — fetch stargazers and save to file."""

import json
from collections import defaultdict
from datetime import datetime, timezone

from ara.colors import BOLD, RESET
from ara.core import GitHubClient
from ara.trends import compute_trend_buckets, get_star_history


def _safe_filename(repo: str) -> str:
    """Convert owner/repo to a safe filename."""
    return f"stargazers_{repo.replace('/', '_')}.json"


def cmd_generate_stars(args, client: GitHubClient) -> str:
    """Handle `ara generate-stars <repo>`.

    Args:
        args.repo: str — repository name (owner/repo)
        args.pages: int (default 3) — max pages to fetch
        args.output: str (optional) — output file path
    """
    repo = args.repo
    max_pages = getattr(args, "pages", 3)

    print(f"Fetching stargazers for {BOLD}{repo}{RESET}...")

    events = get_star_history(client, repo, pages=max_pages)
    print(f"✔ Fetched {len(events)} stargazer events")

    # Save to file
    output_path = getattr(args, "output", None) or _safe_filename(repo)

    # Format for output: list of {timestamp, repo, iso_date}
    output_data = []
    for e in events:
        iso = datetime.fromtimestamp(e.timestamp, tz=timezone.utc).isoformat()
        output_data.append({
            "timestamp": e.timestamp,
            "iso_date": iso,
            "repo": e.repo,
        })

    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"✔ Saved to {BOLD}{output_path}{RESET} ({len(events)} entries)")

    # Show quick stats using trends bucket analysis
    buckets = compute_trend_buckets(events, hours=72, interval_minutes=60)
    if buckets:
        best = max(buckets, key=lambda b: b.count)

        print()
        print(f"Quick stats for {BOLD}{repo}{RESET} stargazers:")
        print("━" * 45)
        print(f"Total stargazers fetched:  {len(events)}")
        print(f"Time span:                 {buckets[0].label} - {buckets[-1].label}")
        print(f"Peak hour:                 {best.label} ({best.count} stars)")

        # Compute daily totals
        daily = defaultdict(int)
        for e in events:
            day = datetime.fromtimestamp(e.timestamp, tz=timezone.utc).strftime("%b %d")
            daily[day] += 1
        if daily:
            best_day = max(daily, key=daily.get)
            print(f"Highest single-day:        {best_day} ({daily[best_day]} stars)")

    return output_path
