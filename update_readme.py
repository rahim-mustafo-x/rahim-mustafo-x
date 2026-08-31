"""
update_readme.py
Fetches public GitHub repositories and updates README.md.
"""

import os
import sys

import requests

GITHUB_USERNAME = "rahim-mustafo-x"
TELEGRAM_USERNAME = "rahim_mustafo_x"
YOUTUBE_URL = "https://www.youtube.com/@rahim.mustafo.x"

TOKEN = os.environ.get("GH_TOKEN")

# GitHub API headers

HEADERS = {
"Authorization": f"Bearer {TOKEN}",
"Accept": "application/vnd.github+json",
"X-GitHub-Api-Version": "2022-11-28",
}

# ============================================================

# REPOSITORIES TO IGNORE

# ============================================================

IGNORED_REPOS = {
"my_dinara",
"bruh",
}

IGNORED_KEYWORDS = {
"d2",
}

# ============================================================

# CUSTOM TECH STACKS

# ============================================================

CUSTOM_STACKS = {
"Muslim_Uz": "Kotlin, MVVM, StateFlow",
"Muslim_calendar": "Kotlin, Clean Architecture",
"eQarz": "Kotlin, JWT, REST API",
"DavomatBackend": "Java, PostgreSQL, JWT",
"Davomat_App": "Kotlin, Python, Telegram",
}

# ============================================================

# CUSTOM DISPLAY NAMES

# ============================================================

CUSTOM_DISPLAY_NAMES = {
"Muslim_Uz": "Muslim Uz",
"Muslim_calendar": "Muslim Calendar",
"DavomatBackend": "Davomat Backend",
"Davomat_App": "Davomat App",
"eQarz": "eQarz",
}

# ============================================================

# FETCH REPOSITORIES

# ============================================================

def get_all_repos():
repos = []
page = 1

```
while True:
    url = (
        "https://api.github.com/user/repos"
        f"?per_page=100"
        f"&page={page}"
        "&affiliation=owner"
        "&visibility=public"
        "&sort=updated"
        "&direction=desc"
    )

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15,
        )

        if response.status_code != 200:
            print(
                f"Repos fetch failed: "
                f"{response.status_code} "
                f"{response.text}",
                file=sys.stderr,
            )
            break

        data = response.json()

        if not isinstance(data, list):
            break

        if not data:
            break

        repos.extend(data)
        page += 1

    except requests.RequestException as error:
        print(
            f"Network error: {error}",
            file=sys.stderr,
        )
        break

return repos
```

# ============================================================

# FILTER REPOSITORIES

# ============================================================

def should_ignore_repo(repo):
name = repo.get("name", "")
name_lower = name.lower()

```
# Never display private repositories
if repo.get("private", False):
    return True

# Do not display profile repository
if name_lower == GITHUB_USERNAME.lower():
    return True

# Explicit ignored repositories
if name_lower in IGNORED_REPOS:
    return True

# Ignore repositories containing ignored keywords
for keyword in IGNORED_KEYWORDS:
    if keyword in name_lower:
        return True

return False
```

# ============================================================

# FORMAT REPOSITORY NAME

# ============================================================

def format_repo_name(name):
cleaned_name = name.replace("_", " ")
cleaned_name = cleaned_name.replace("-", " ")

```
return cleaned_name.title()
```

def get_display_name(repo_name):
if repo_name in CUSTOM_DISPLAY_NAMES:
return CUSTOM_DISPLAY_NAMES[repo_name]

```
return format_repo_name(repo_name)
```

# ============================================================

# GET TOTAL STARS

# ============================================================

def get_total_stars(repositories):
total_stars = 0

```
for repo in repositories:
    if should_ignore_repo(repo):
        continue

    total_stars += repo.get(
        "stargazers_count",
        0,
    )

return total_stars
```

# ============================================================

# BUILD PROJECTS TABLE

# ============================================================

def build_projects_table(repositories):
rows = [
"| Repository | Tech Stack / Main Language | Stars | Forks |",
"|---|---|:---:|:---:|",
]

```
visible_repositories = []

for repo in repositories:
    if should_ignore_repo(repo):
        continue

    visible_repositories.append(repo)

visible_repositories.sort(
    key=lambda repo: repo.get(
        "updated_at",
        "",
    ),
    reverse=True,
)

if not visible_repositories:
    return "_No public repositories found._"

for repo in visible_repositories:
    repo_name = repo.get("name", "")

    display_name = get_display_name(
        repo_name
    )

    repo_url = repo.get(
        "html_url",
        "",
    )

    stars_count = repo.get(
        "stargazers_count",
        0,
    )

    forks_count = repo.get(
        "forks_count",
        0,
    )

    tech_stack = CUSTOM_STACKS.get(
        repo_name,
        repo.get("language") or "General",
    )

    if stars_count > 0:
        stars = f"⭐ {stars_count}"
    else:
        stars = "—"

    if forks_count > 0:
        forks = f"🍴 {forks_count}"
    else:
        forks = "—"

    row = (
        f"| [**{display_name}**]({repo_url}) "
        f"| `{tech_stack}` "
        f"| {stars} "
        f"| {forks} |"
    )

    rows.append(row)

return "\n".join(rows)
```

# ============================================================

# BUILD README

# ============================================================

def build_readme(repositories):
total_stars = get_total_stars(
repositories
)

```
projects_table = build_projects_table(
    repositories
)

typing_header = (
    "https://readme-typing-svg.demolab.com"
    "?font=Fira+Code"
    "&weight=600"
    "&size=24"
    "&pause=1000"
    "&color=00FF2B"
    "&center=true"
    "&vCenter=true"
    "&width=600"
    "&lines="
    "Assalomu+Aleykum!+👋;"
    "Men+Mustafo+Rahim;"
    "Android+va+Backend+Dasturchiman"
)

typing_cmd = (
    "https://readme-typing-svg.demolab.com"
    "?font=Fira+Code"
    "&size=13"
    "&duration=3000"
    "&pause=500"
    "&color=00FF2B"
    "&center=true"
    "&vCenter=true"
    "&width=700"
    "&height=40"
    "&lines="
    "%24+sudo+apt+install+creativity;"
    "%24+git+clone+rahim-mustafo-x;"
    "%24+./run.sh+%5BSuccess%5D"
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
    '| **Frameworks** | ![Spring Boot](https://img.shields.io/badge/Spring_Boot-6DB33F?style=for-the-badge&logo=springboot&logoColor=white) ![Ktor](https://img.shields.io/badge/Ktor-0080FF?style=for-the-badge&logo=ktor&logoColor=white) |',
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
    '',
]

return "\n".join(lines)
```

# ============================================================

# UPDATE README

# ============================================================

def update_readme():
repositories = get_all_repos()

```
visible_repositories = []

for repo in repositories:
    if should_ignore_repo(repo):
        continue

    visible_repositories.append(repo)

print(
    f"Fetched {len(repositories)} repositories from GitHub."
)

print(
    f"Showing {len(visible_repositories)} repositories in README."
)

readme_content = build_readme(
    repositories
)

with open(
    "README.md",
    "w",
    encoding="utf-8",
) as file:
    file.write(readme_content)

total_stars = get_total_stars(
    repositories
)

print("README.md successfully updated!")
print(f"Total Stars: {total_stars}")
```

# ============================================================

# ENTRY POINT

# ============================================================

if **name** == "**main**":
update_readme()
