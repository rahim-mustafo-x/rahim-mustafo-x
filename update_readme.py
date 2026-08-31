"""
update_readme.py
Fetches all public repositories automatically and updates README.md
with a clean GitHub profile layout.
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
}

# ============================================================

# FETCH REPOSITORIES

# ============================================================

def get_all_repos():
"""
Fetch all PUBLIC repositories owned by the authenticated user.
"""

```
repos = []
page = 1

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
                f"{response.status_code} {response.text}",
                file=sys.stderr,
            )
            break

        data = response.json()

        if not data:
            break

        if not isinstance(data, list):
            print(
                "Unexpected GitHub API response.",
                file=sys.stderr,
            )
            break

        repos.extend(data)
        page += 1

    except requests.RequestException as error:
        print(
            f"Network error fetching repositories: {error}",
            file=sys.stderr,
        )
        break

return repos
```

# ============================================================

# FILTER REPOSITORIES

# ============================================================

def should_ignore_repo(repo):
"""
Returns True if the repository should not appear in README.
"""

```
name = repo.get("name", "")
name_lower = name.lower()

# Extra protection: private repositories never appear.
if repo.get("private", False):
    return True

# Ignore the GitHub profile repository itself.
if name_lower == GITHUB_USERNAME.lower():
    return True

# Ignore explicitly listed repositories.
if name_lower in IGNORED_REPOS:
    return True

# Ignore repositories containing forbidden keywords.
if any(keyword in name_lower for keyword in IGNORED_KEYWORDS):
    return True

return False
```

# ============================================================

# FORMAT REPOSITORY NAME

# ============================================================

def format_repo_name(name):
"""
Examples:

```
my_example
-> My Example

my-example
-> My Example

cool_backend_project
-> Cool Backend Project
"""

cleaned_name = name.replace("_", " ").replace("-", " ")

return cleaned_name.title()
```

def get_display_name(repo_name):
"""
Use custom display name if available.
Otherwise format automatically.
"""

```
return CUSTOM_DISPLAY_NAMES.get(
    repo_name,
    format_repo_name(repo_name),
)
```

# ============================================================

# STATISTICS

# ============================================================

def get_total_stars(all_repos):
"""
Calculate total stars from repositories.
"""

```
return sum(
    repo.get("stargazers_count", 0)
    for repo in all_repos
    if not should_ignore_repo(repo)
)
```

# ============================================================

# BUILD PROJECTS TABLE

# ============================================================

def build_projects_table(all_repos):

```
rows = [
    "| Repository | Tech Stack / Main Language | Stars | Forks |",
    "|---|---|:---:|:---:|",
]

filtered_repos = [
    repo
    for repo in all_repos
    if not should_ignore_repo(repo)
]

if not filtered_repos:
    return "_No public repositories found._"

filtered_repos.sort(
    key=lambda repo: repo.get("updated_at", ""),
    reverse=True,
)

for repo in filtered_repos:

    repo_name = repo.get("name", "")
    display_name = get_display_name(repo_name)

    repo_url = repo.get("html_url", "")
    stars_count = repo.get("stargazers_count", 0)
    forks_count = repo.get("forks_count", 0)

    stars = (
        f"⭐ {stars_count}"
        if stars_count > 0
        else "—"
    )

    forks = (
        f"🍴 {forks_count}"
        if forks_count > 0
        else "—"
    )

    tech_stack = CUSTOM_STACKS.get(
        repo_name,
        repo.get("language") or "General",
    )

    rows.append(
        f"| [**{display_name}**]({repo_url}) "
        f"| `{tech_stack}` "
        f"| {stars} "
        f"| {forks} |"
    )

return "\n".join(rows)
```

# ============================================================

# BUILD README

# ============================================================

def build_readme(all_repos):

```
total_stars = get_total_stars(all_repos)

projects_table = build_projects_table(all_repos)

typing_header = (
    "https://readme-typing-svg.demolab.com?"
    "font=Fira+Code"
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
    "https://readme-typing-svg.demolab.com?"
    "font=Fira+Code"
    "&size=13"
    "&duration=3000"
    "&pause=500"
    "&color=00FF2B"
    "&center=true"
    "&vCenter=true"
    "&multiline=false"
    "&repeat=true"
    "&width=700"
    "&height=40"
    "&lines="
    "%24+sudo+apt+install+creativity;"
    "%24+git+clone+rahim-mustafo-x;"
    "%24+./run.sh+%5BSuccess%5D"
)

lines = [

    '<div align="center">',

    '  <img '
    'src="https://raw.githubusercontent.com/'
    'platane/snk/output/'
    'github-contribution-grid-snake-dark.svg" '
    'alt="Snake animation" '
    'width="100%" />',

    '  <br/><br/>',

    f'  <img src="{typing_header}" '
    'alt="Typing Header" />',

    '  <br/>',

    f'  <img '
    f'src="https://img.shields.io/badge/'
    f'Total%20Stars-{total_stars}-00FF2B'
    f'?style=for-the-badge'
    f'&logo=github'
    f'&logoColor=black'
    f'&labelColor=101010" '
    f'alt="Total Stars" />',

    '</div>',

    '',
    '---',
    '',

    '## 🛠️ Skills & Technologies',

    '',

    '| Category | Technologies |',
    '| --- | --- |',

    '| **Languages** | '
    '![Kotlin](https://img.shields.io/badge/'
    'Kotlin-7F52FF?style=for-the-badge'
    '&logo=kotlin&logoColor=white) '
    '![Java](https://img.shields.io/badge/'
    'Java-ED8B00?style=for-the-badge'
    '&logo=openjdk&logoColor=white) '
    '![Python](https://img.shields.io/badge/'
    'Python-3776AB?style=for-the-badge'
    '&logo=python&logoColor=white) |',

    '| **Frameworks** | '
    '![Spring Boot](https://img.shields.io/badge/'
    'Spring_Boot-6DB33F?style=for-the-badge'
    '&logo=springboot&logoColor=white) '
    '![Ktor](https://img.shields.io/badge/'
    'Ktor-0080FF?style=for-the-badge'
    '&logo=ktor&logoColor=white) |',

    '| **Databases** | '
    '![PostgreSQL](https://img.shields.io/badge/'
    'PostgreSQL-4169E1?style=for-the-badge'
    '&logo=postgresql&logoColor=white) '
    '![SQLite](https://img.shields.io/badge/'
    'SQLite-003B57?style=for-the-badge'
    '&logo=sqlite&logoColor=white) |',

    '| **Tools & OS** | '
    '![Docker](https://img.shields.io/badge/'
    'Docker-2496ED?style=for-the-badge'
    '&logo=docker&logoColor=white) '
    '![Git](https://img.shields.io/badge/'
    'Git-F05032?style=for-the-badge'
    '&logo=git&logoColor=white) '
    '![Linux](https://img.shields.io/badge/'
    'Linux-FCC624?style=for-the-badge'
    '&logo=linux&logoColor=black) |',

    '| **IDEs** | '
    '![Android Studio](https://img.shields.io/badge/'
    'Android_Studio-3DDC84?style=for-the-badge'
    '&logo=androidstudio&logoColor=white) '
    '![IntelliJ IDEA](https://img.shields.io/badge/'
    'IntelliJ_IDEA-000000?style=for-the-badge'
    '&logo=intellijidea&logoColor=white) |',

    '',
    '---',
    '',

    '<div align="center">',
    f'  <img src="{typing_cmd}" '
    'alt="Terminal Animation" />',
    '</div>',

    '',
    '## 📊 GitHub Statistics',
    '',

    f'![Activity Graph]('
    f'https://github-readme-activity-graph.vercel.app/'
    f'graph?username={GITHUB_USERNAME}'
    f'&theme=github-compact'
    f'&bg_color=0D1117'
    f'&hide_border=true'
    f'&line=00FF2B'
    f'&point=00FF2B'
    f'&color=00FF2B'
    f'&title_color=00FF2B'
    f'&area=true'
    f')',

    '',

    '<div align="center">',

    f'  <img '
    f'src="https://github-readme-stats.vercel.app/'
    f'api/top-langs?username={GITHUB_USERNAME}'
    f'&show_icons=true'
    f'&locale=en'
    f'&layout=compact'
    f'&langs_count=8'
    f'&title_color=00FF2B'
    f'&text_color=ffffff'
    f'&bg_color=0D1117'
    f'&hide_border=true" '
    f'alt="Top Languages" '
    f'height="165" />',

    f'  <img '
    f'src="https://github-readme-stats.vercel.app/'
    f'api?username={GITHUB_USERNAME}'
    f'&show_icons=true'
    f'&locale=en'
    f'&title_color=00FF2B'
    f'&text_color=ffffff'
    f'&bg_color=0D1117'
    f'&hide_border=true'
    f'&include_all_commits=true" '
    f'alt="GitHub Stats" '
    f'height="165" />',

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

    f'  <a href="https://t.me/{TELEGRAM_USERNAME}" '
    'target="_blank">',

    '    <img '
    'src="https://img.shields.io/badge/'
    'Telegram-26A5E4?style=for-the-badge'
    '&logo=telegram&logoColor=white" '
    'alt="Telegram" />',

    '  </a>',

    f'  <a href="{YOUTUBE_URL}" '
    'target="_blank">',

    '    <img '
    'src="https://img.shields.io/badge/'
    'YouTube-FF0000?style=for-the-badge'
    '&logo=youtube&logoColor=white" '
    'alt="YouTube" />',

    '  </a>',

    '</div>',

    '',
    '---',
    '',

    '<div align="center">',

    f'  <img '
    f'src="https://komarev.com/ghpvc/'
    f'?username={GITHUB_USERNAME}'
    f'&color=00FF2B'
    f'&style=flat-square'
    f'&label=Profile+Views" '
    f'alt="Profile Views" />',

    '</div>',

    '',
]

return "\n".join(lines)
```

# ============================================================

# UPDATE README

# ============================================================

def update_readme():

```
all_repos = get_all_repos()

visible_repos = [
    repo
    for repo in all_repos
    if not should_ignore_repo(repo)
]

print(
    f"Fetched {len(all_repos)} public repositories "
    f"from GitHub."
)

print(
    f"Showing {len(visible_repos)} repositories "
    f"in README."
)

readme_content = build_readme(all_repos)

with open(
    "README.md",
    "w",
    encoding="utf-8",
) as file:
    file.write(readme_content)

total_stars = get_total_stars(all_repos)

print(
    "README.md successfully updated!"
)

print(
    f"Total Stars: {total_stars}"
)
```

# ============================================================

# ENTRY POINT

# ============================================================

if **name** == "**main**":
update_readme()
