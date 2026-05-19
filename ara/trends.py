"""Trends module — fetch star history and render ASCII trend charts."""

import json
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

from ara.colors import BOLD, GREEN, RED, RESET


@dataclass
class StarEvent:
    timestamp: float  # unix timestamp
    repo: str


@dataclass
class TrendBucket:
    label: str       # e.g. "09:00" or "May 18"
    count: int       # stars in this bucket
    delta: int       # change from previous bucket


def _parse_link_header(headers: dict) -> dict[str, str]:
    """Extract rel->url mapping from Link header.

    Parses something like:
        <https://api.github.com/...?page=2>; rel="next", <...>; rel="last"
    Returns a dict like {"next": "https://...", "last": "https://..."}
    """
    link = headers.get("Link", "")
    if not link:
        return {}
    result: dict[str, str] = {}
    for part in link.split(","):
        part = part.strip()
        m = re.match(r'<([^>]+)>\s*;\s*rel="([^"]+)"', part)
        if m:
            result[m.group(2)] = m.group(1)
    return result


def get_star_history(client, repo: str, pages: int = 3) -> List[StarEvent]:
    """Fetch star history by paginating stargazers.

    Uses /repos/{owner}/{repo}/stargazers with per_page=100.
    Returns list of StarEvent sorted by timestamp ascending.
    Each stargazer entry includes a `starred_at` field.
    """
    events: list[StarEvent] = []
    url = f"https://api.github.com/repos/{repo}/stargazers?per_page=100&page=1"
    fetched = 0

    while url and fetched < pages:
        data, headers = client._fetch_page_with_headers(url)
        if not isinstance(data, list):
            break

        for entry in data:
            starred_at = entry.get("starred_at")
            if starred_at:
                ts = _parse_iso8601(starred_at)
                events.append(StarEvent(timestamp=ts, repo=repo))

        fetched += 1

        # Follow next page via Link header
        links = _parse_link_header(headers)
        url = links.get("next", "")
        if not url:
            break

    # Sort ascending by timestamp
    events.sort(key=lambda e: e.timestamp)
    return events


def _parse_iso8601(iso_str: str) -> float:
    """Parse ISO 8601 timestamp string to unix timestamp (float).

    Handles formats like '2026-05-18T09:00:00Z' and '2026-05-18T09:00:00+00:00'.
    """
    # Python 3.7+ datetime.fromisoformat can't handle trailing Z in 3.10-
    if iso_str.endswith("Z"):
        iso_str = iso_str[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(iso_str)
    except ValueError:
        # Fallback: try strptime
        dt = datetime.strptime(iso_str[:19], "%Y-%m-%dT%H:%M:%S")
    return dt.timestamp()


def compute_trend_buckets(
    events: List[StarEvent],
    hours: int = 72,
    interval_minutes: int = 60,
) -> List[TrendBucket]:
    """Group star events into time buckets.

    Args:
        events: Sorted star events (ascending by timestamp).
        hours: Lookback window in hours.
        interval_minutes: Bucket size in minutes.

    Returns:
        List of TrendBucket with label, count, delta.
    """
    now = time.time()
    cutoff = now - (hours * 3600)
    interval_seconds = interval_minutes * 60

    # Filter events within window
    filtered = [e for e in events if e.timestamp >= cutoff]

    # Build buckets from now going back
    buckets: list[TrendBucket] = []
    bucket_end = now
    bucket_start = now - interval_seconds

    while bucket_end > cutoff:
        label = _format_bucket_label(bucket_start, bucket_end, hours)
        count = sum(
            1 for e in filtered
            if bucket_start <= e.timestamp < bucket_end
        )
        buckets.append(TrendBucket(label=label, count=count, delta=0))
        bucket_end = bucket_start
        bucket_start = bucket_end - interval_seconds

    # Reverse so oldest comes first
    buckets.reverse()

    # Compute deltas
    prev = 0
    for b in buckets:
        b.delta = b.count - prev
        prev = b.count

    return buckets


def _format_bucket_label(start: float, end: float, total_hours: int) -> str:
    """Format a bucket label based on time range.

    For <= 24h windows: show "HH:MM"
    For > 24h windows: show "MMM DD HH:MM"
    """
    dt = datetime.fromtimestamp(start)
    if total_hours <= 24:
        return dt.strftime("%H:%M")
    return dt.strftime("%b %d %H:%M")


def render_trend_chart(buckets: List[TrendBucket], repo: str) -> str:
    """Render ASCII trend table.

    Uses ━━━ box-drawing borders, ▲/▼ delta indicators.
    Colors: GREEN for positive delta, RED for negative.
    """
    if not buckets:
        return f"No trend data available for {repo}."

    # Compute window info
    total_stars = sum(b.count for b in buckets)
    best_bucket = max(buckets, key=lambda b: b.count)
    worst_bucket = min(buckets, key=lambda b: b.count)

    # Determine column widths
    label_w = max(len(b.label) for b in buckets) + 2
    count_w = max(len(str(b.count)) for b in buckets) + 2

    # Header
    lines = [
        f"{BOLD}📈 Trends for {repo} (last {_compute_window_label(buckets)}){RESET}",
        "━" * (label_w + count_w + 14),
        f"{'Time'.ljust(label_w)}  {'Stars'.rjust(count_w - 1)}  {'▲/▼'.rjust(5)}",
        "─" * (label_w + count_w + 14),
    ]

    for b in buckets:
        delta_str = _format_delta(b.delta, padded=True)
        count_str = f"{b.count:,}"
        lines.append(
            f"{b.label.ljust(label_w)}  {count_str.rjust(count_w - 1)}  {delta_str}"
        )

    lines.append("━" * (label_w + count_w + 14))

    # Best and worst hour info
    best_delta = best_bucket.delta if buckets else 0
    worst_delta = worst_bucket.delta if buckets else 0
    best_label = best_bucket.label if buckets else "N/A"
    worst_label = worst_bucket.label if buckets else "N/A"
    best_count = best_bucket.count if buckets else 0
    worst_count = worst_bucket.count if buckets else 0

    lines.append(
        f"Total new stars: {total_stars:,}"
        f"   Best hour: {best_label} ({best_count}, {_format_delta(best_delta).strip()})"
        f"   Worst hour: {worst_label} ({worst_count}, {_format_delta(worst_delta).strip()})"
    )

    return "\n".join(lines)


def _compute_window_label(buckets: list[TrendBucket]) -> str:
    """Compute human-readable window label from buckets."""
    if len(buckets) < 2:
        return "N/A"
    first = buckets[0].label
    last = buckets[-1].label
    return f"{first} – {last}"


def _format_delta(delta: int, padded: bool = False) -> str:
    """Format delta with ▲/▼ indicator and color.

    Args:
        delta: The delta value.
        padded: If True, right-pad to 5 chars for table alignment.

    Returns:
        Colored delta string like "▲ +5", "▼ -3", or "  0".
    """
    if delta > 0:
        s = f"{GREEN}▲ +{delta}{RESET}"
    elif delta < 0:
        s = f"{RED}▼ {delta}{RESET}"
    else:
        s = "  0"
    if padded:
        plain = _strip_ansi(s)
        pad = " " * (5 - len(plain))
        return f"{pad}{s}"
    return s


def _strip_ansi(text: str) -> str:
    """Strip ANSI escape sequences from a string."""
    import re as _re
    return _re.sub(r"\033\[[0-9;]*m", "", text)


def cmd_trends(args, client) -> str:
    """Command handler for `ara trends`.

    Args from argparse namespace:
    - args.repo: str
    - args.hours: int (default 72)
    - args.interval: int (default 60, in minutes)
    - args.json: bool (default False)
    """
    events = get_star_history(client, args.repo, pages=3)
    buckets = compute_trend_buckets(events, hours=args.hours, interval_minutes=args.interval)

    if getattr(args, "json", False):
        result = _json_output(buckets, args.repo)
    else:
        result = render_trend_chart(buckets, args.repo)
    print(result)
    return result


def _json_output(buckets: list[TrendBucket], repo: str) -> str:
    """Produce JSON output for trends command."""
    total = sum(b.count for b in buckets)
    best = max(buckets, key=lambda b: b.count) if buckets else None
    worst = min(buckets, key=lambda b: b.count) if buckets else None

    data = {
        "repo": repo,
        "buckets": [
            {"label": b.label, "count": b.count, "delta": b.delta}
            for b in buckets
        ],
        "total": total,
        "best_hour": {"label": best.label, "count": best.count} if best else None,
        "worst_hour": {"label": worst.label, "count": worst.count} if worst else None,
    }
    return json.dumps(data, indent=2, ensure_ascii=False)
