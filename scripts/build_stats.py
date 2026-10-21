"""
Builds the black & white statistics cards for the profile README from GitHub's GraphQL API.

    GITHUB_TOKEN=<token> python scripts/build_stats.py [username]

Writes assets/stats/{stats,streak,graph}.svg. Runs daily in .github/workflows/stats.yml,
so the cards never depend on a third-party widget service. Only public activity is counted.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "stats"
USER = sys.argv[1] if len(sys.argv) > 1 else os.getenv("GITHUB_USER", "Abhxym")
TOKEN = os.environ["GITHUB_TOKEN"]

FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "'Courier New', Consolas, 'Liberation Mono', monospace"
BG, BORDER, FG, MUTED = "#050505", "#ffffff2e", "#ffffff", "#9a9a9a"


def gql(query: str, **variables) -> dict:
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"Bearer {TOKEN}", "User-Agent": "profile-stats"},
    )
    data = json.load(urllib.request.urlopen(req, timeout=60))
    if "errors" in data:
        raise SystemExit(f"GraphQL error: {data['errors']}")
    return data["data"]


def fetch() -> dict:
    base = gql(
        """query($login: String!) { user(login: $login) {
             createdAt
             followers { totalCount }
             pullRequests { totalCount }
             issues { totalCount }
             repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100) {
               totalCount nodes { stargazerCount } }
             repositoriesContributedTo(first: 1, privacy: PUBLIC,
               contributionTypes: [COMMIT, PULL_REQUEST, ISSUE, REPOSITORY]) { totalCount }
             contributionsCollection { totalCommitContributions contributionYears }
           } }""",
        login=USER,
    )["user"]

    # One calendar per contribution year (the API returns at most a year at a time)
    days: dict[str, int] = {}
    for year in sorted(base["contributionsCollection"]["contributionYears"]):
        cal = gql(
            """query($login: String!, $from: DateTime!, $to: DateTime!) { user(login: $login) {
                 contributionsCollection(from: $from, to: $to) { contributionCalendar {
                   weeks { contributionDays { date contributionCount } } } } } }""",
            login=USER, **{"from": f"{year}-01-01T00:00:00Z", "to": f"{year}-12-31T23:59:59Z"},
        )["user"]["contributionsCollection"]["contributionCalendar"]
        for week in cal["weeks"]:
            for d in week["contributionDays"]:
                days[d["date"]] = d["contributionCount"]
    base["days"] = dict(sorted(days.items()))
    return base


def streaks(days: dict[str, int]) -> dict:
    today = dt.date.today()
    dates = [dt.date.fromisoformat(d) for d in days if dt.date.fromisoformat(d) <= today]
    counts = {dt.date.fromisoformat(d): c for d, c in days.items()}
    first = min((d for d in dates if counts[d] > 0), default=today)

    longest = (0, None, None)
    run_start, run_len = None, 0
    for d in dates:
        if counts[d] > 0:
            run_start = run_start or d
            run_len += 1
            if run_len > longest[0]:
                longest = (run_len, run_start, d)
        else:
            run_start, run_len = None, 0

    # Current streak may end today or yesterday (today isn't over yet)
    end = today if counts.get(today, 0) > 0 else today - dt.timedelta(days=1)
    cur, d = 0, end
    while counts.get(d, 0) > 0:
        cur += 1
        d -= dt.timedelta(days=1)
    cur_start = d + dt.timedelta(days=1) if cur else None
    return {
        "total": sum(c for day, c in counts.items() if day <= today),
        "first": first,
        "current": cur, "current_range": (cur_start, end if cur else None),
        "longest": longest[0], "longest_range": (longest[1], longest[2]),
    }


def grade(commits: int, prs: int, issues: int, stars: int, followers: int) -> tuple[str, float]:
    """Rough level from activity, in the spirit of the familiar GitHub stats cards (not identical)."""
    score = commits + 3 * prs + 2 * issues + 4 * stars + 2 * followers
    levels = [(1500, "S"), (800, "A+"), (400, "A"), (200, "A-"), (100, "B+"), (50, "B"), (25, "B-"), (10, "C+"), (0, "C")]
    for i, (threshold, letter) in enumerate(levels):
        if score >= threshold:
            upper = levels[i - 1][0] if i else threshold * 2
            progress = min(1.0, (score - threshold) / max(1, upper - threshold))
            return letter, progress
    return "C", 0.0


def fmt(d: dt.date | None) -> str:
    return d.strftime("%b %-d, %Y") if d and os.name != "nt" else (d.strftime("%b %#d, %Y") if d else "")


def stats_svg(u: dict) -> str:
    year = dt.date.today().year
    stars = sum(n["stargazerCount"] for n in u["repositories"]["nodes"])
    commits = u["contributionsCollection"]["totalCommitContributions"]
    prs, issues = u["pullRequests"]["totalCount"], u["issues"]["totalCount"]
    letter, progress = grade(commits, prs, issues, stars, u["followers"]["totalCount"])
    rows = [
        ("star", "Total Stars Earned", stars),
        ("commit", f"Total Commits ({year})", commits),
        ("pr", "Total PRs", prs),
        ("issue", "Total Issues", issues),
        ("repo", "Public Repositories", u["repositories"]["totalCount"]),
        ("contrib", "Contributed to (last year)", u["repositoriesContributedTo"]["totalCount"]),
    ]
    icons = {
        "star": "M8 .8l2.2 4.5 5 .7-3.6 3.5.8 5L8 12.2 3.6 14.5l.8-5L.8 6l5-.7z",
        "commit": "M8 5a3 3 0 100 6 3 3 0 000-6zM0 7.2h4.6v1.6H0zm11.4 0H16v1.6h-4.6z",
        "pr": "M3 2.5a1.5 1.5 0 100 3 1.5 1.5 0 000-3zM3 10.5a1.5 1.5 0 100 3 1.5 1.5 0 000-3zm10 0a1.5 1.5 0 100 3 1.5 1.5 0 000-3zM2.3 5.5h1.4v5H2.3zm10 0V8.7h1.4V5.2a1.7 1.7 0 00-1.7-1.7H9V2L6.5 4.2 9 6.4V4.9h3a.3.3 0 01.3.3z",
        "issue": "M8 1a7 7 0 110 14A7 7 0 018 1zm0 1.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM8 6.5a1.5 1.5 0 110 3 1.5 1.5 0 010-3z",
        "repo": "M2 2.5A2.5 2.5 0 014.5 0h8.8a.7.7 0 01.7.7v12.6a.7.7 0 01-.7.7H11v-1.5h1.5v-2h-8a1 1 0 00-1 1v.5a1 1 0 001 1H6V15H4.5A2.5 2.5 0 012 12.5zm1.5 7.9a2.5 2.5 0 011-.2h8V1.5h-8a1 1 0 00-1 1z",
        "contrib": "M1 2.5h14v1.5H1zm0 4.75h14v1.5H1zm0 4.75h9v1.5H1z",
    }
    rows_svg = ""
    for i, (icon, label, value) in enumerate(rows):
        y = 70 + i * 27
        rows_svg += (
            f'<g transform="translate(25,{y - 12})" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{0.15 * i:.2f}s" dur=".5s" fill="freeze"/>'
            f'<path d="{icons[icon]}" fill="{MUTED}" transform="scale(.95)"/>'
            f'<text x="26" y="12.5" class="lbl">{label}:</text>'
            f'<text x="236" y="12.5" class="val">{value}</text></g>'
        )
    r, c = 40, 2 * math.pi * 40
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="495" height="230" viewBox="0 0 495 230" role="img" aria-label="{USER}'s GitHub stats">
  <style>
    .title{{font:700 17px {FONT};fill:{FG}}}
    .lbl{{font:600 13.5px {FONT};fill:#d4d4d4}}
    .val{{font:700 13.5px {FONT};fill:{FG}}}
    .rank{{font:800 26px {FONT};fill:{FG}}}
  </style>
  <rect x=".5" y=".5" width="494" height="229" rx="8" fill="{BG}" stroke="{BORDER}"/>
  <text x="25" y="36" class="title">{USER}'s GitHub Stats</text>
  {rows_svg}
  <g transform="translate(400,122)">
    <circle r="{r}" fill="none" stroke="#ffffff22" stroke-width="6"/>
    <circle r="{r}" fill="none" stroke="{FG}" stroke-width="6" stroke-linecap="round" transform="rotate(-90)"
      stroke-dasharray="{c:.1f}" stroke-dashoffset="{c:.1f}">
      <animate attributeName="stroke-dashoffset" from="{c:.1f}" to="{c * (1 - max(progress, .04)):.1f}" dur="1.2s" fill="freeze"/>
    </circle>
    <text y="9" text-anchor="middle" class="rank">{letter}</text>
  </g>
</svg>
'''


def streak_svg(s: dict) -> str:
    today = dt.date.today()

    def day(d):
        return "Today" if d == today else fmt(d)

    def rng(a, b):
        if not a:
            return "No active streak"
        return day(a) if a == b else f"{day(a)} - {day(b)}"

    cur_label = rng(*s["current_range"]) if s["current"] else "Start one today"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="495" height="230" viewBox="0 0 495 230" role="img" aria-label="Contribution streaks">
  <style>
    .big{{font:700 30px {FONT};fill:{FG}}}
    .lbl{{font:600 14px {FONT};fill:{FG}}}
    .sub{{font:400 11.5px {FONT};fill:{MUTED}}}
  </style>
  <rect x=".5" y=".5" width="494" height="229" rx="8" fill="{BG}" stroke="{BORDER}"/>
  <line x1="165" y1="30" x2="165" y2="200" stroke="#ffffff26"/>
  <line x1="330" y1="30" x2="330" y2="200" stroke="#ffffff26"/>

  <g text-anchor="middle">
    <text x="82.5" y="104" class="big">{s["total"]:,}</text>
    <text x="82.5" y="138" class="lbl">Total Contributions</text>
    <text x="82.5" y="164" class="sub">{fmt(s["first"])} - Present</text>

    <g transform="translate(247.5,82)">
      <circle r="40" fill="none" stroke="{FG}" stroke-width="5"/>
      <path d="M-9 -44 q9 -16 6 -24 q14 10 12 26" fill="{BG}" stroke="{FG}" stroke-width="3"/>
      <text y="11" class="big">{s["current"]}</text>
    </g>
    <text x="247.5" y="160" class="lbl" style="font-weight:700">Current Streak</text>
    <text x="247.5" y="184" class="sub">{cur_label}</text>

    <text x="412.5" y="104" class="big">{s["longest"]}</text>
    <text x="412.5" y="138" class="lbl">Longest Streak</text>
    <text x="412.5" y="164" class="sub">{rng(*s["longest_range"])}</text>
  </g>
</svg>
'''


def graph_svg(days: dict[str, int], n: int = 31) -> str:
    today = dt.date.today()
    series = [(dt.date.fromisoformat(d), c) for d, c in days.items() if dt.date.fromisoformat(d) <= today][-n:]
    w, h = 900, 320
    left, right, top, bottom = 70, 30, 60, 250
    peak = max([c for _, c in series] + [1])
    step = max(1, math.ceil(peak / 5))
    ymax = step * 5

    def xy(i, c):
        return left + i * (w - left - right) / (len(series) - 1), bottom - c / ymax * (bottom - top)

    pts = [xy(i, c) for i, (_, c) in enumerate(series)]
    # Smooth curve through the points (Catmull-Rom → cubic Bézier), clamped to the baseline
    path = f"M{pts[0][0]:.1f},{pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, min(bottom, p1[1] + (p2[1] - p0[1]) / 6))
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, min(bottom, p2[1] - (p3[1] - p1[1]) / 6))
        path += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    area = f"{path} L{pts[-1][0]:.1f},{bottom} L{pts[0][0]:.1f},{bottom} Z"

    grid = "".join(
        f'<line x1="{left}" y1="{bottom - k / 5 * (bottom - top):.1f}" x2="{w - right}" y2="{bottom - k / 5 * (bottom - top):.1f}" stroke="#ffffff14"/>'
        f'<text x="{left - 12}" y="{bottom - k / 5 * (bottom - top) + 4:.1f}" class="tick" text-anchor="end">{k * step}</text>'
        for k in range(6)
    )
    xt = "".join(
        f'<text x="{x:.1f}" y="{bottom + 20}" class="tick" text-anchor="middle">{d.day}</text>'
        for (x, _), (d, _) in zip(pts, series)
    )
    dots = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{FG}" opacity="0"><animate attributeName="opacity" to="1" begin="{1.2 + i * 0.02:.2f}s" dur=".3s" fill="freeze"/></circle>'
        for i, (x, y) in enumerate(pts)
    )
    first, last = series[0][0], series[-1][0]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{USER}'s contributions over the last {n} days">
  <style>
    .title{{font:700 17px {FONT};fill:{FG}}}
    .tick{{font:500 11px {FONT};fill:{MUTED}}}
    .axis{{font:600 12px {FONT};fill:#d4d4d4}}
  </style>
  <defs>
    <linearGradient id="fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".22"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>
    <clipPath id="reveal"><rect x="0" y="0" width="0" height="{h}"><animate attributeName="width" to="{w}" dur="1.4s" fill="freeze"/></rect></clipPath>
  </defs>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="8" fill="{BG}" stroke="{BORDER}"/>
  <text x="{w / 2}" y="34" class="title" text-anchor="middle">{USER}'s Contribution Graph</text>
  {grid}
  <g clip-path="url(#reveal)">
    <path d="{area}" fill="url(#fill)"/>
    <path d="{path}" fill="none" stroke="{FG}" stroke-width="2.5" stroke-linejoin="round"/>
  </g>
  {dots}
  {xt}
  <text x="{w / 2}" y="{h - 14}" class="axis" text-anchor="middle">Days ({fmt(first)} - {fmt(last)})</text>
  <text x="22" y="{(top + bottom) / 2}" class="axis" text-anchor="middle" transform="rotate(-90 22 {(top + bottom) / 2})">Contributions</text>
</svg>
'''


def main() -> None:
    u = fetch()
    s = streaks(u["days"])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "stats.svg").write_text(stats_svg(u), encoding="utf-8")
    (OUT / "streak.svg").write_text(streak_svg(s), encoding="utf-8")
    (OUT / "graph.svg").write_text(graph_svg(u["days"]), encoding="utf-8")
    print(f"{USER}: {s['total']} contributions, current streak {s['current']}, longest {s['longest']}")


if __name__ == "__main__":
    main()
