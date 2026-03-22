"""
update_readme.py
Fetches all repos (public + private), scans languages,
and updates README.md automatically.
"""

import os
import re
import requests
from collections import Counter

GITHUB_USERNAME = "rahim-mustafo-x"
TELEGRAM_USERNAME = "rahim_mustafo_x"
YOUTUBE_URL = "https://www.youtube.com/@rahim.mustafo.x"
TOKEN = os.environ.get("GH_TOKEN")
HEADERS = {"Authorization": "token " + TOKEN} if TOKEN else {}

TRACKED_REPOS = {
    "Muslim_Uz":       "Muslim Uz",
    "Muslim_calendar": "Muslim Taqvim",
    "eQarz":           "e-Qarz",
    "DavomatBackend":  "DavomatAppKMP",
    "Davomat_App":     "DavomatApp_Telegram_bot",
}

STACKS = {
    "Muslim Uz":               "Kotlin, MVVM, StateFlow",
    "Muslim Taqvim":           "Kotlin, Clean Architecture",
    "e-Qarz":                  "Kotlin, JWT, REST API",
    "DavomatAppKMP":           "Java, PostgreSQL, JWT",
    "DavomatApp_Telegram_bot": "Kotlin + Python (Telegram)",
}


def get_all_repos():
    repos = []
    page = 1
    while True:
        url = "https://api.github.com/user/repos?per_page=100&page=" + str(page) + "&affiliation=owner"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print("Repos fetch failed: " + str(r.status_code))
            break
        data = r.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos


def get_repo_languages(repo_name):
    url = "https://api.github.com/repos/" + GITHUB_USERNAME + "/" + repo_name + "/languages"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    return {}


def get_all_languages(all_repos):
    total = Counter()
    for repo in all_repos:
        langs = get_repo_languages(repo["name"])
        total.update(langs)
    return dict(total.most_common())


def get_repo_info(repo_name, all_repos):
    for repo in all_repos:
        if repo["name"] == repo_name:
            return {
                "stars":   repo.get("stargazers_count", 0),
                "forks":   repo.get("forks_count", 0),
                "private": repo.get("private", False),
            }
    return {"stars": 0, "forks": 0, "private": False}


def get_total_stars(all_repos):
    return sum(repo["stargazers_count"] for repo in all_repos)


def build_projects_table(all_repos):
    rows = [
        "| App | Stack | Stars | Status |",
        "|-----|-------|-------|--------|",
    ]
    for repo_slug, display_name in TRACKED_REPOS.items():
        info = get_repo_info(repo_slug, all_repos)
        stars = "⭐ " + str(info["stars"]) if info["stars"] > 0 else "—"
        stack = STACKS.get(display_name, "—")
        rows.append("| **" + display_name + "** | " + stack + " | " + stars + " | ✅ Production |")
    return "\n".join(rows)


def build_languages_section(lang_bytes, top_n=12):
    if not lang_bytes:
        return "_No language data found._"

    total_bytes = sum(lang_bytes.values())
    top = list(lang_bytes.items())[:top_n]

    lines = []
    for lang, count in top:
        pct = count / total_bytes * 100
        bar_len = int(pct / 2)
        bar = "█" * bar_len
        lang_padded = lang.ljust(20)
        pct_str = str(round(pct, 1)).rjust(5)
        lines.append("`" + lang_padded + "` " + bar + " " + pct_str + "%")

    return "\n".join(lines)


def build_readme(all_repos, lang_bytes):
    total = get_total_stars(all_repos)
    projects_table = build_projects_table(all_repos)
    languages_section = build_languages_section(lang_bytes)
    badge = "![Stars](https://img.shields.io/badge/Total%20Stars-" + str(total) + "-yellow?style=flat-square)"

    lines = []
    lines.append('<div align="center">')
    lines.append('<img src="https://raw.githubusercontent.com/platane/snk/output/github-contribution-grid-snake-dark.svg" alt="Snake animation" />')
    lines.append('')
    lines.append('<a href="https://git.io/typing-svg">')
    lines.append('  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=28&duration=7000&pause=1000&color=00FF2B&center=true&vCenter=true&repeat=false&random=false&width=1000&lines=Men+haqimda+%3A" alt="Typing SVG"/>')
    lines.append('</a>')
    lines.append('')
    lines.append('<a href="https://git.io/typing-svg">')
    lines.append('  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=15&pause=1000&color=00FF2B&center=true&vCenter=true&multiline=true&repeat=false&random=false&width=950&height=75&lines=Ismim+Mustafo+Rahim,+Android+va+Backend+dasturchisiman" alt="Typing SVG" />')
    lines.append('</a>')
    lines.append('')
    lines.append(badge)
    lines.append('')
    lines.append('</div>')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## 🛠️ Skills & Technologies')
    lines.append('')
    lines.append('| Languages | Frameworks | IDEs | Tools | OS |')
    lines.append('| --------- | ---------- | ---- | ----- | -- |')
    lines.append('| <div align="center"><a href="https://skillicons.dev"><img src="https://skillicons.dev/icons?i=kotlin,java,python" title="Kotlin, Java, Python"/></a></div> | <div align="center"><a href="https://skillicons.dev"><img src="https://skillicons.dev/icons?i=spring,ktor" title="Spring Boot, Ktor"/></a></div> | <div align="center"><a href="https://skillicons.dev"><img src="https://skillicons.dev/icons?i=androidstudio,idea" title="Android Studio, IntelliJ IDEA"/></a></div> | <div align="center"><a href="https://skillicons.dev"><img src="https://skillicons.dev/icons?i=git,github,docker" title="Git, GitHub, Docker"/></a></div> | <div align="center"><a href="https://skillicons.dev"><img src="https://skillicons.dev/icons?i=linux,ubuntu" title="Linux, Ubuntu"/></a></div> |')
    lines.append('| <div align="center"><a href="https://skillicons.dev"><img src="https://skillicons.dev/icons?i=postgres,sqlite" title="PostgreSQL, SQLite"/></a></div> | <div align="center"><a href="https://skillicons.dev"><img src="https://skillicons.dev/icons?i=gradle" title="Gradle"/></a></div> | <div align="center"><a href="https://skillicons.dev"><img src="https://skillicons.dev/icons?i=vscode" title="VS Code"/></a></div> | <div align="center"><a href="https://skillicons.dev"><img src="https://skillicons.dev/icons?i=postman" title="Postman"/></a></div> | <div align="center"><a href="https://skillicons.dev"><img src="https://skillicons.dev/icons?i=windows" title="Windows"/></a></div> |')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('<a href="https://git.io/typing-svg">')
    lines.append('  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=12&duration=3000&pause=500&color=00FF2B&center=true&vCenter=true&multiline=true&repeat=true&random=false&width=800&height=100&lines=%24+sudo+apt+install+creativity;%24+git+clone+https%3A%2F%2Fgithub.com%2Frahim-mustafo-x;%24+cd+rahim-mustafo-x;%24+./run_awesome_code.sh;%5BSuccess%5D+Code+compiled+successfully!" alt="Terminal Animation" />')
    lines.append('</a>')
    lines.append('')
    lines.append('## 📊 GitHub Activity')
    lines.append('')
    lines.append('[![Mustafo GitHub activity graph](https://github-readme-activity-graph.vercel.app/graph?username=' + GITHUB_USERNAME + '&theme=github-compact&bg_color=000000&line=009A22&point=98FB98&color=00FF2B&title_color=00FF2B&area=true)](https://github.com/ashutosh00710/github-readme-activity-graph)')
    lines.append('')
    lines.append('<div align="center">')
    lines.append('  <img src="https://github-readme-stats.vercel.app/api/top-langs?username=' + GITHUB_USERNAME + '&show_icons=true&locale=en&layout=compact&langs_count=16&title_color=00FF2B&text_color=00FF2B&border_color=00FF2B&theme=chartreuse-dark" alt="Top Languages" width=300 />')
    lines.append('  <img src="https://github-readme-stats.vercel.app/api?username=' + GITHUB_USERNAME + '&show_icons=true&locale=en&title_color=00FF2B&text_color=00FF2B&icon_color=00FF2B&border_color=00FF2B&theme=chartreuse-dark&include_all_commits=true" alt="GitHub Stats" width=300 />')
    lines.append('  <img src="https://github-readme-streak-stats.herokuapp.com/?user=' + GITHUB_USERNAME + '&border=00FF2B&stroke=00FF2B&ring=00FF2B&fire=00FF2B&currStreakNum=00FF2B&sideNums=00FF2B&currStreakLabel=00FF2B&sideLabels=00FF2B&dates=00FF2B&theme=chartreuse-dark" alt="GitHub Streak" width=300 />')
    lines.append('</div>')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## 🚀 Projects')
    lines.append('')
    lines.append(projects_table)
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## 🔤 Languages')
    lines.append('')
    lines.append(languages_section)
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## 📞 Contact Me')
    lines.append('')
    lines.append('<div align="center">')
    lines.append('  <a href="https://t.me/' + TELEGRAM_USERNAME + '">')
    lines.append('    <img src="https://img.shields.io/badge/Telegram-1DA1F2?style=for-the-badge&logo=telegram&logoColor=white" />')
    lines.append('  </a>')
    lines.append('  <a href="' + YOUTUBE_URL + '">')
    lines.append('    <img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" />')
    lines.append('  </a>')
    lines.append('</div>')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('<div align="center">')
    lines.append('  <img src="https://komarev.com/ghpvc/?username=' + GITHUB_USERNAME + '&color=00FF2B&style=flat-square&label=Profile+Views" alt="Profile Views" />')
    lines.append('</div>')

    return "\n".join(lines)


def update_readme():
    all_repos = get_all_repos()
    print("Found " + str(len(all_repos)) + " repos (public + private)")

    lang_bytes = get_all_languages(all_repos)
    print("Languages found: " + ", ".join(list(lang_bytes.keys())))

    readme_content = build_readme(all_repos, lang_bytes)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("README updated — total stars: " + str(get_total_stars(all_repos)))


if __name__ == "__main__":
    update_readme()
