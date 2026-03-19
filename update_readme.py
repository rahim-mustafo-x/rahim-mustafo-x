"""
update_readme.py
Fetches your real GitHub repo stats and updates README.md automatically.
"""

import os
import re
import requests

GITHUB_USERNAME = "rahim-mustafo-x"
TOKEN = os.environ.get("GH_TOKEN")

HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

TRACKED_REPOS = {
    "Muslim_Uz":          "Muslim Uz",
    "Muslim_calendar":    "Muslim Taqvim",
    "eQarz":              "e-Qarz",
    "DavomatBackend":     "DavomatAppKMP",
    "Davomat_App":        "DavomatApp_Telegram_bot",
}

STACKS = {
    "Muslim Uz":               "Kotlin, MVVM, StateFlow",
    "Muslim Taqvim":           "Kotlin, Clean Architecture",
    "e-Qarz":                  "Kotlin, JWT, REST API",
    "DavomatAppKMP":           "Java, PostgreSQL, JWT",
    "DavomatApp_Telegram_bot": "Kotlin + Python (Telegram)",
}

def get_all_repos() -> list:
    """Fetch all repos (public + private) using pagination."""
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/user/repos?per_page=100&page={page}&affiliation=owner"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            break
        data = r.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def get_repo_info(repo_name: str, all_repos: list) -> dict:
    for repo in all_repos:
        if repo["name"] == repo_name:
            return {
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
                "private": repo.get("private", False),
            }
    return {"stars": 0, "forks": 0, "private": False}

def get_total_stars(all_repos: list) -> int:
    return sum(repo["stargazers_count"] for repo in all_repos)

def build_projects_table(all_repos: list) -> str:
    rows = [
        "| App | Stack | Stars | Status |",
        "|-----|-------|-------|--------|",
    ]
    for repo_slug, display_name in TRACKED_REPOS.items():
        info = get_repo_info(repo_slug, all_repos)
        stars = f"⭐ {info['stars']}" if info["stars"] > 0 else "—"
        stack = STACKS.get(display_name, "—")
        rows.append(f"| **{display_name}** | {stack} | {stars} | ✅ Production |")
    return "\n".join(rows)

def update_readme():
    all_repos = get_all_repos()
    print(f"📦 Found {len(all_repos)} repos (public + private)")

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    new_table = build_projects_table(all_repos)
    content = re.sub(
        r"(## 🚀 Projects\n\n).*?(\n\n---)",
        rf"\g<1>{new_table}\g<2>",
        content,
        flags=re.DOTALL,
    )

    total = get_total_stars(all_repos)
    content = re.sub(
        r"!\[Stars\]\(.*?\)",
        f"

![Stars](https://img.shields.io/badge/Total%20Stars-{total}-yellow?style=flat-square)

",
        content,
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ README updated — total stars: {total}")

if __name__ == "__main__":
    update_readme()