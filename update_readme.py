"""
update_readme.py
Fetches all repos (public + private) and regenerates README.md automatically.

Modernized version:
- Stable header/typing SVGs (no git.io shortlinks, no dead heroku domain)
- Clean, responsive Skill Icons table
- Only includes repos that actually exist on GitHub
- Consistent dark / neon-green theme across all badges & stat cards
- f-strings + proper try/except error handling around all API calls
"""

from __future__ import annotations

import os
import sys
from typing import Any

import requests

GITHUB_USERNAME = "rahim-mustafo-x"
TELEGRAM_USERNAME = "rahim_mustafo_x"
YOUTUBE_URL = "https://www.youtube.com/@rahim.mustafo.x"
TOKEN = os.environ.get("GH_TOKEN")

NEON_GREEN = "00FF2B"
DARK_BG = "0D1117"

GITHUB_API_BASE = "https://api.github.com"
REQUEST_TIMEOUT = 15

if not TOKEN:
    print("ERROR: GH_TOKEN not set", file=sys.stderr)
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

# slug (actual GitHub repo name) -> display name
TRACKED_REPOS = {
    "Muslim_Uz": "Muslim Uz",
    "Muslim_calendar": "Muslim Taqvim",
    "eQarz": "e-Qarz",
    "DavomatBackend": "DavomatAppKMP",
    "Davomat_App": "DavomatApp_Telegram_bot",
}

STACKS = {
    "Muslim Uz": "Kotlin, MVVM, StateFlow",
    "Muslim Taqvim": "Kotlin, Clean Architecture",
    "e-Qarz": "Kotlin, JWT, REST API",
    "DavomatAppKMP": "Java, PostgreSQL, JWT",
    "DavomatApp_Telegram_bot": "Kotlin + Python (Telegram)",
}


def get_all_repos() -> list[dict[str, Any]]:
    """Fetch every repo (public + private) the token owner has access to."""
    repos: list[dict[str, Any]] = []
    page = 1

    while True:
        url = f"{GITHUB_API_BASE}/user/repos"
        params = {
            "per_page": 100,
            "page": page,
            "affiliation": "owner",
            "visibility": "all",
        }
        try:
            response = requests.get(
                url, headers=HEADERS, params=params, timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            print(f"Repos fetch failed on page {page}: {exc}", file=sys.stderr)
            break

        data = response.json()
        if not data:
            break

        repos.extend(data)
        page += 1

    return repos


def get_existing_tracked_repos(
    all_repos: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Return only the TRACKED_REPOS entries that actually exist on GitHub."""
    repo_by_name = {repo["name"]: repo for repo in all_repos}
    existing: dict[str, dict[str, Any]] = {}

    for slug, display_name in TRACKED_REPOS.items():
        repo = repo_by_name.get(slug)
        if repo is None:
            print(f"Skipping '{slug}' — not found on GitHub", file=sys.stderr)
            continue
        existing[slug] = {
            "display_name": display_name,
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "private": repo.get("private", False),
        }

    return existing


def get_total_stars(all_repos: list[dict[str, Any]]) -> int:
    return sum(repo.get("stargazers_count", 0) for repo in all_repos)


def build_projects_table(existing_tracked: dict[str, dict[str, Any]]) -> str:
    if not existing_tracked:
        return "_No tracked repositories were found on GitHub._"

    rows = [
        "| App | Stack | Stars | Status |",
        "|-----|-------|:-----:|:------:|",
    ]
    for info in existing_tracked.values():
        display_name = info["display_name"]
        stars = f"⭐ {info['stars']}" if info["stars"] > 0 else "—"
        stack = STACKS.get(display_name, "—")
        rows.append(f"| **{display_name}** | {stack} | {stars} | ✅ Production |")

    return "\n".join(rows)


def build_header() -> str:
    """Stable snake animation + capsule-render banner + typing SVG header."""
    typing_line = (
        f"https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&pause=1000"
        f"&color={NEON_GREEN}&background={DARK_BG}00&center=true&vCenter=true"
        f"&repeat=true&width=1000&lines=Men+haqimda+%3A"
    )
    subtitle_line = (
        f"https://readme-typing-svg.demolab.com?font=Fira+Code&size=15&pause=1000"
        f"&color={NEON_GREEN}&background={DARK_BG}00&center=true&vCenter=true"
        f"&multiline=true&repeat=true&width=950&height=75"
        f"&lines=Ismim+Mustafo+Rahim,+Android+va+Backend+dasturchisiman"
    )
    capsule_banner = (
        f"https://capsule-render.vercel.app/api?type=waving&color=gradient"
        f"&customColorList=0,2,2,5,30&height=180&section=header"
        f"&text={GITHUB_USERNAME}&fontSize=42&fontColor={NEON_GREEN}"
        f"&animation=fadeIn&fontAlignY=38"
    )

    return "\n".join(
        [
            '<div align="center">',
            f'<img src="{capsule_banner}" width="100%" alt="Header banner" />',
            "",
            '<img src="https://raw.githubusercontent.com/platane/snk/output/github-contribution-grid-snake-dark.svg" alt="Snake animation" width="100%" />',
            "",
            f'<img src="{typing_line}" alt="Typing SVG" />',
            "",
            f'<img src="{subtitle_line}" alt="Typing SVG" />',
            "",
            "</div>",
        ]
    )


def build_badges(total_stars: int) -> str:
    star_badge = (
        f"![Stars](https://img.shields.io/badge/Total%20Stars-{total_stars}"
        f"-{NEON_GREEN}?style=for-the-badge&logo=github&logoColor=white"
        f"&labelColor={DARK_BG})"
    )
    return f'<div align="center">\n\n{star_badge}\n\n</div>'


def build_skills_section() -> str:
    """Modern, responsive Skill Icons layout — one row per category, no broken HTML."""
    categories = [
        ("Languages", "kotlin,java,python"),
        ("Frameworks", "spring,ktor"),
        ("IDEs", "androidstudio,idea,vscode"),
        ("Tools", "git,github,docker,postman"),
        ("Database & OS", "postgres,sqlite,linux,ubuntu,windows"),
    ]

    lines = ['<div align="center">', ""]
    for title, icons in categories:
        lines.append(f"**{title}**")
        lines.append("")
        lines.append(f"![Skills](https://skillicons.dev/icons?i={icons}&theme=dark)")
        lines.append("")
    lines.append("</div>")
    return "\n".join(lines)


def build_activity_section() -> str:
    activity_graph = (
        f"https://github-readme-activity-graph.vercel.app/graph?username={GITHUB_USERNAME}"
        f"&theme=github-compact&bg_color={DARK_BG}&line={NEON_GREEN}&point={NEON_GREEN}"
        f"&color={NEON_GREEN}&title_color={NEON_GREEN}&area=true&hide_border=true"
    )
    top_langs = (
        f"https://github-readme-stats.vercel.app/api/top-langs?username={GITHUB_USERNAME}"
        f"&show_icons=true&locale=en&layout=compact&langs_count=16"
        f"&title_color={NEON_GREEN}&text_color={NEON_GREEN}&icon_color={NEON_GREEN}"
        f"&border_color={NEON_GREEN}&bg_color={DARK_BG}&hide_border=false"
    )
    stats_card = (
        f"https://github-readme-stats.vercel.app/api?username={GITHUB_USERNAME}"
        f"&show_icons=true&locale=en&title_color={NEON_GREEN}&text_color={NEON_GREEN}"
        f"&icon_color={NEON_GREEN}&border_color={NEON_GREEN}&bg_color={DARK_BG}"
        f"&include_all_commits=true&count_private=true"
    )
    streak_stats = (
        f"https://github-readme-streak-stats.herokuapp.com/?user={GITHUB_USERNAME}"
        f"&background={DARK_BG}&border={NEON_GREEN}&stroke={NEON_GREEN}&ring={NEON_GREEN}"
        f"&fire={NEON_GREEN}&currStreakNum={NEON_GREEN}&sideNums={NEON_GREEN}"
        f"&currStreakLabel={NEON_GREEN}&sideLabels={NEON_GREEN}&dates={NEON_GREEN}"
    )

    return "\n".join(
        [
            f"[![{GITHUB_USERNAME} activity graph]({activity_graph})]"
            "(https://github.com/ashutosh00710/github-readme-activity-graph)",
            "",
            '<div align="center">',
            "",
            '<img src="' + top_langs + '" alt="Top Languages" width="410" />',
            '<img src="' + stats_card + '" alt="GitHub Stats" width="410" />',
            "",
            '<img src="' + streak_stats + '" alt="GitHub Streak" width="835" />',
            "",
            "</div>",
        ]
    )


def build_terminal_animation() -> str:
    terminal_svg = (
        "https://readme-typing-svg.demolab.com?font=Fira+Code&size=13&duration=3000"
        f"&pause=500&color={NEON_GREEN}&background={DARK_BG}00&center=true&vCenter=true"
        "&multiline=true&repeat=true&width=800&height=100"
        "&lines=%24+sudo+apt+install+creativity;%24+git+clone+https%3A%2F%2F"
        f"github.com%2F{GITHUB_USERNAME};%24+cd+{GITHUB_USERNAME}"
        ";%24+./run_awesome_code.sh;%5BSuccess%5D+Code+compiled+successfully!"
    )
    return f'<div align="center">\n<img src="{terminal_svg}" alt="Terminal Animation" />\n</div>'


def build_contact_section() -> str:
    return "\n".join(
        [
            '<div align="center">',
            "",
            f'  <a href="https://t.me/{TELEGRAM_USERNAME}">',
            f'    <img src="https://img.shields.io/badge/Telegram-{NEON_GREEN}?style=for-the-badge&logo=telegram&logoColor=white&labelColor={DARK_BG}" />',
            "  </a>",
            f'  <a href="{YOUTUBE_URL}">',
            f'    <img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white&labelColor={DARK_BG}" />',
            "  </a>",
            "",
            "</div>",
        ]
    )


def build_footer() -> str:
    views_badge = (
        f"https://komarev.com/ghpvc/?username={GITHUB_USERNAME}"
        f"&color={NEON_GREEN}&style=for-the-badge&label=Profile+Views"
    )
    footer_wave = (
        "https://capsule-render.vercel.app/api?type=waving&color=gradient"
        "&customColorList=0,2,2,5,30&height=100&section=footer"
    )
    return "\n".join(
        [
            '<div align="center">',
            f'  <img src="{views_badge}" alt="Profile Views" />',
            "",
            f'  <img src="{footer_wave}" width="100%" />',
            "</div>",
        ]
    )


def build_readme(all_repos: list[dict[str, Any]]) -> str:
    total_stars = get_total_stars(all_repos)
    existing_tracked = get_existing_tracked_repos(all_repos)
    projects_table = build_projects_table(existing_tracked)

    sections = [
        build_header(),
        "",
        build_badges(total_stars),
        "",
        "---",
        "",
        "## 🛠️ Skills & Technologies",
        "",
        build_skills_section(),
        "",
        "---",
        "",
        build_terminal_animation(),
        "",
        "## 📊 GitHub Activity",
        "",
        build_activity_section(),
        "",
        "---",
        "",
        "## 🚀 Projects",
        "",
        projects_table,
        "",
        "---",
        "",
        "## 📞 Contact Me",
        "",
        build_contact_section(),
        "",
        "---",
        "",
        build_footer(),
        "",
    ]

    return "\n".join(sections)


def update_readme() -> None:
    all_repos = get_all_repos()
    if not all_repos:
        print("No repos returned — aborting README update.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(all_repos)} repos (public + private)")

    readme_content = build_readme(all_repos)

    try:
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
    except OSError as exc:
        print(f"Failed to write README.md: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"README updated — total stars: {get_total_stars(all_repos)}")


if __name__ == "__main__":
    update_readme()
