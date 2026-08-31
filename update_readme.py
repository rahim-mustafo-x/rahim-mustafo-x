"""
update_readme.py
Fetches all public repos automatically and updates README.md with clean layout.
"""

import os
import sys
import requests

GITHUB_USERNAME = "rahim-mustafo-x"
TELEGRAM_USERNAME = "rahim_mustafo_x"
YOUTUBE_URL = "https://www.youtube.com/@rahim.mustafo.x"
TOKEN = os.environ.get("GH_TOKEN")

if not TOKEN:
    print("ERROR: GH_TOKEN not set", file=sys.stderr)
    sys.exit(1)

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json",
}

# Maxsus loyihalar uchun custom tech-stack (agar xohlasangiz). 
# Agar repo bu yerda bo'lmasa, GitHub'dagi asosiy dasturlash tili ko'rsatiladi.
CUSTOM_STACKS = {
    "Muslim_Uz":       "Kotlin, MVVM, StateFlow",
    "Muslim_calendar": "Kotlin, Clean Architecture",
    "eQarz":           "Kotlin, JWT, REST API",
    "DavomatBackend":  "Java, PostgreSQL, JWT",
    "Davomat_App":     "Kotlin, Python (Telegram)",
}


def get_all_repos():
    repos = []
    page = 1
    while True:
        url = (
            "https://api.github.com/user/repos"
            f"?per_page=100&page={page}"
            "&affiliation=owner&visibility=all"
        )
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                print(f"Repos fetch failed: {r.status_code} {r.text}", file=sys.stderr)
                break
            data = r.json()
            if not data or not isinstance(data, list):
                break
            repos.extend(data)
            page += 1
        except requests.RequestException as e:
            print(f"Network error fetching repos: {e}", file=sys.stderr)
            break
    return repos


def get_total_stars(all_repos):
    return sum(repo.get("stargazers_count", 0) for repo in all_repos)


def build_projects_table(all_repos):
    rows = [
        "| Repository | Tech Stack / Main Lang | Stars | Forks | Status |",
        "|---|---|:---:|:---:|:---:|",
    ]
    
    # Profile repozitoriyasining o'zini (rahim-mustafo-x) loyihalar jadvaliga qo'shmaymiz
    filtered_repos = [r for r in all_repos if r["name"].lower() != GITHUB_USERNAME.lower()]

    if not filtered_repos:
        return "_No public repositories found._"

    for repo in filtered_repos:
        name = repo["name"]
        repo_url = repo["html_url"]
        stars_cnt = repo.get("stargazers_count", 0)
        forks_cnt = repo.get("forks_count", 0)
        is_private = repo.get("private", False)
        
        stars = f"⭐ {stars_cnt}" if stars_cnt > 0 else "—"
        forks = f"🍴 {forks_cnt}" if forks_cnt > 0 else "—"
        
        # Custom stack bor bo'lsa uni oladi, bo'lmasa GitHub primary language'ni oladi
        stack = CUSTOM_STACKS.get(name, repo.get("language") or "General")
        status = "🔒 Private" if is_private else "⚡ Public"

        rows.append(
            f"| [**{name}**]({repo_url}) | `{stack}` | {stars} | {forks} | {status} |"
        )
    
    return "\n".join(rows)


def build_readme(all_repos):
    total_stars = get_total_stars(all_repos)
    projects_table = build_projects_table(all_repos)
    
    typing_header = (
        "https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24"
        "&pause=1000&color=00FF2B&center=true&vCenter=true&width=600&lines="
        "Assalomu+Aleykum!+👋;Men+Mustafo+Rahim;Android+va+Backend+Dasturchiman"
    )
    
    typing_cmd = (
        "https://readme-typing-svg.demolab.com?font=Fira+Code&size=13"
        "&duration=3000&pause=500&color=00FF2B&center=true&vCenter=true"
        "&multiline=false&repeat=true&width=700&height=40"
        "&lines=%24+sudo+apt+install+creativity;%24+git+clone+rahim-mustafo-x;%24+./run.sh+%5BSuccess%5D"
    )

    lines = [
        '<div align="center">',
        '  <img src="https://raw.githubusercontent.com/platane/snk/output/github-contribution-grid-snake-dark.svg" alt="Snake animation" width="100%" />',
        '  <br/><br/>',
        f'  <img src="{typing_header}" alt="Typing Header" />',
        '  <br/>',
        f'  <img src="https://img.shields.io/badge/Total%20Stars-{total_stars}-00FF2B?style=for-the-badge&logo=github&logoColor=black&labelColor=101010" alt="Total Stars" />',
        '</div>',
        '',
        '---',
        '',
        '## 🛠️ Skills & Technologies',
        '',
        '| Category | Technologies |',
        '| --- | --- |',
        '| **Languages** | ![Kotlin](https://img.shields.io/badge/Kotlin-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white) ![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) |',
        '| **Frameworks** | ![Spring](https://img.shields.io/badge/Spring_Boot-6DB33F?style=for-the-badge&logo=springboot&logoColor=white) ![Ktor](https://img.shields.io/badge/Ktor-0080FF?style=for-the-badge&logo=ktor&logoColor=white) |',
        '| **Databases** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white) |',
        '| **Tools & OS** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) |',
        '| **IDEs** | ![Android Studio](https://img.shields.io/badge/Android_Studio-3DDC84?style=for-the-badge&logo=androidstudio&logoColor=white) ![IntelliJ IDEA](https://img.shields.io/badge/IntelliJ_IDEA-000000?style=for-the-badge&logo=intellijidea&logoColor=white) |',
        '',
        '---',
        '',
        '<div align="center">',
        f'  <img src="{typing_cmd}" alt="Terminal Animation" />',
        '</div>',
        '',
        '## 📊 GitHub Statistics',
        '',
        f'![Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username={GITHUB_USERNAME}&theme=github-compact&bg_color=0D1117&hide_border=true&line=00FF2B&point=00FF2B&color=00FF2B&title_color=00FF2B&area=true)',
        '',
        '<div align="center">',
        f'  <img src="https://github-readme-stats.vercel.app/api/top-langs?username={GITHUB_USERNAME}&show_icons=true&locale=en&layout=compact&langs_count=8&title_color=00FF2B&text_color=ffffff&bg_color=0D1117&hide_border=true" alt="Top Languages" height="165" />',
        f'  <img src="https://github-readme-stats.vercel.app/api?username={GITHUB_USERNAME}&show_icons=true&locale=en&title_color=00FF2B&text_color=ffffff&bg_color=0D1117&hide_border=true&include_all_commits=true" alt="GitHub Stats" height="165" />',
        '</div>',
        '',
        '---',
        '',
        '## 🚀 Public Projects',
        '',
        projects_table,
        '',
        '---',
        '',
        '## 📞 Connect With Me',
        '',
        '<div align="center">',
        f'  <a href="https://t.me/{TELEGRAM_USERNAME}" target="_blank">',
        '    <img src="https://img.shields.io/badge/Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram" />',
        '  </a>',
        f'  <a href="{YOUTUBE_URL}" target="_blank">',
        '    <img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube" />',
        '  </a>',
        '</div>',
        '',
        '---',
        '',
        '<div align="center">',
        f'  <img src="https://komarev.com/ghpvc/?username={GITHUB_USERNAME}&color=00FF2B&style=flat-square&label=Profile+Views" alt="Profile Views" />',
        '</div>',
        ''
    ]

    return "\n".join(lines)


def update_readme():
    all_repos = get_all_repos()
    print(f"Fetched {len(all_repos)} repositories from GitHub.")

    readme_content = build_readme(all_repos)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print(f"README.md successfully updated! Total Stars: {get_total_stars(all_repos)}")


if __name__ == "__main__":
    update_readme()
