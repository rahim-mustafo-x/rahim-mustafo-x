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


# ============================================================
# FETCH USER PROFILE (for follower count)
# ============================================================

def get_user_profile():
    url = f"https://api.github.com/users/{GITHUB_USERNAME}"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15,
        )

        if response.status_code != 200:
            print(
                f"User profile fetch failed: "
                f"{response.status_code} "
                f"{response.text}",
                file=sys.stderr,
            )
            return {}

        return response.json()

    except requests.RequestException as error:
        print(
            f"Network error: {error}",
            file=sys.stderr,
        )
        return {}


# ============================================================
# FILTER REPOSITORIES
# ============================================================

def should_ignore_repo(repo):
    name = repo.get("name", "")
    name_lower = name.lower()

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


# ============================================================
# FORMAT REPOSITORY NAME
# ============================================================

def format_repo_name(name):
    cleaned_name = name.replace("_", " ")
    cleaned_name = cleaned_name.replace("-", " ")

    return cleaned_name.title()


def get_display_name(repo_name):
    if repo_name in CUSTOM_DISPLAY_NAMES:
        return CUSTOM_DISPLAY_NAMES[repo_name]

    return format_repo_name(repo_name)


# ============================================================
# GET TOTAL STARS
# ============================================================

def get_total_stars(repositories):
    total_stars = 0

    for repo in repositories:
        if should_ignore_repo(repo):
            continue

        total_stars += repo.get(
            "stargazers_count",
            0,
        )

    return total_stars


def get_total_forks(repositories):
    total_forks = 0

    for repo in repositories:
        if should_ignore_repo(repo):
            continue

        total_forks += repo.get(
            "forks_count",
            0,
        )

    return total_forks


# ============================================================
# LANGUAGE COLORS (for shields.io badges)
# ============================================================

LANGUAGE_COLORS = {
    "Kotlin": "7F52FF",
    "Java": "ED8B00",
    "Python": "3776AB",
    "JavaScript": "F7DF1E",
    "TypeScript": "3178C6",
    "Dart": "0175C2",
    "Swift": "FA7343",
    "C++": "00599C",
    "C": "A8B9CC",
    "C#": "239120",
    "Go": "00ADD8",
    "Rust": "000000",
    "PHP": "777BB4",
    "Ruby": "CC342D",
    "HTML": "E34F26",
    "CSS": "1572B6",
    "Shell": "89E051",
}

DEFAULT_LANGUAGE_COLOR = "6E7681"


def build_language_breakdown(repositories):
    counts = {}

    for repo in repositories:
        if should_ignore_repo(repo):
            continue

        language = repo.get("language")

        if not language:
            continue

        counts[language] = counts.get(language, 0) + 1

    if not counts:
        return "_No language data available._"

    total = sum(counts.values())

    sorted_languages = sorted(
        counts.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    badges = []

    for language, count in sorted_languages:
        percent = round((count / total) * 100)
        color = LANGUAGE_COLORS.get(
            language,
            DEFAULT_LANGUAGE_COLOR,
        )
        label = language.replace(" ", "_").replace("-", "--")

        badge = (
            f"![{language}](https://img.shields.io/badge/"
            f"{label}-{percent}%25-{color}?style=flat-square)"
        )

        badges.append(badge)

    return " ".join(badges)


# ============================================================
# RECENT ACTIVITY (self-computed, no external service)
# ============================================================

def build_recent_activity(repositories, limit=5):
    visible_repositories = []

    for repo in repositories:
        if should_ignore_repo(repo):
            continue

        visible_repositories.append(repo)

    visible_repositories.sort(
        key=lambda repo: repo.get("updated_at", ""),
        reverse=True,
    )

    if not visible_repositories:
        return "_No recent activity._"

    lines = []

    for repo in visible_repositories[:limit]:
        repo_name = repo.get("name", "")
        display_name = get_display_name(repo_name)
        repo_url = repo.get("html_url", "")
        updated_at = repo.get("updated_at", "")[:10]

        lines.append(
            f"- [**{display_name}**]({repo_url}) — updated `{updated_at}`"
        )

    return "\n".join(lines)


# ============================================================
# BUILD PROJECTS TABLE
# ============================================================

def build_projects_table(repositories):
    rows = [
        "| Repository | Tech Stack / Main Language | Stars | Forks |",
        "|---|---|:---:|:---:|",
    ]

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


# ============================================================
# BUILD README
# ============================================================

def build_readme(repositories, user_profile=None):
    if user_profile is None:
        user_profile = {}

    total_stars = get_total_stars(
        repositories
    )

    total_forks = get_total_forks(
        repositories
    )

    total_repos = user_profile.get(
        "public_repos",
        len([r for r in repositories if not should_ignore_repo(r)]),
    )

    projects_table = build_projects_table(
        repositories
    )

    language_breakdown = build_language_breakdown(
        repositories
    )

    recent_activity = build_recent_activity(
        repositories
    )

    lines = [
        '<div align="center">',
        '  <img src="https://raw.githubusercontent.com/platane/snk/output/github-contribution-grid-snake-dark.svg" alt="Snake animation" width="100%" />',
        '  <br/><br/>',
        '  <h2>👋 Assalomu Aleykum! Men Mustafo Rahim</h2>',
        '  <h3>💻 Android va Backend Dasturchiman</h3>',
        '  <br/>',
        f'  <img src="https://img.shields.io/badge/Total%20Stars-{total_stars}-00FF2B?style=for-the-badge&logo=github&logoColor=black&labelColor=101010" alt="Total Stars" />',
        f'  <img src="https://img.shields.io/badge/Public%20Repos-{total_repos}-00FF2B?style=for-the-badge&logo=github&logoColor=black&labelColor=101010" alt="Public Repos" />',
        f'  <img src="https://img.shields.io/badge/Total%20Forks-{total_forks}-00FF2B?style=for-the-badge&logo=github&logoColor=black&labelColor=101010" alt="Total Forks" />',
        f'  <img src="https://img.shields.io/github/followers/{GITHUB_USERNAME}?style=for-the-badge&logo=github&logoColor=black&labelColor=101010&color=00FF2B&label=Followers" alt="Followers" />',
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
        '| **Databases** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white) ![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white) |',
        '| **Tools & OS** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) |',
        '| **IDEs** | ![Android Studio](https://img.shields.io/badge/Android_Studio-3DDC84?style=for-the-badge&logo=android-studio&logoColor=white) ![IntelliJ IDEA](https://img.shields.io/badge/IntelliJ_IDEA-000000?style=for-the-badge&logo=intellij-idea&logoColor=white) |',
        '',
        '---',
        '',
        '## 📊 GitHub Statistics',
        '',
        '### Language Breakdown (by repositories)',
        '',
        language_breakdown,
        '',
        '### 🕒 Recently Active',
        '',
        recent_activity,
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


# ============================================================
# UPDATE README
# ============================================================

def update_readme():
    repositories = get_all_repos()
    user_profile = get_user_profile()

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
        repositories,
        user_profile,
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


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    update_readme()
