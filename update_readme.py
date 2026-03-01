"""
update_readme.py
Fetches your real GitHub repo stats and updates README.md automatically.
Run locally or via GitHub Actions.
"""

import os
import re
import requests

GITHUB_USERNAME = "rahim-mustafo-x"
TOKEN = os.environ.get("GH_TOKEN")  # set in GitHub Actions secrets

HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

# ── Repos to track (name → display name) ──────────────────────────────────────
TRACKED_REPOS = {
    "Muslim_Uz":              "Muslim Uz",
    "Muslim_calendar":        "Muslim Taqvim",
    "eQarz":                  "e-Qarz",
    "DavomatBackend":         "Davomat Backend",
    "Davomat_App":            "Davomat App + Bot",
}

def get_repo_info(repo_name: str) -> dict:
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        data = r.json()
        return {
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
        }
    return {"stars": 0, "forks": 0}

def get_total_stars() -> int:
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?per_page=100"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return sum(repo["stargazers_count"] for repo in r.json())
    return 0

def build_projects_table() -> str:
    rows = []
    rows.append("| App | Stack | Stars | Status |")
    rows.append("|-----|-------|-------|--------|")

    stacks = {
        "Muslim Uz":          "Kotlin, MVVM, StateFlow",
        "Muslim Taqvim":      "Kotlin, Clean Architecture",
        "e-Qarz":             "Kotlin, JWT, REST API",
        "Davomat Backend":    "Java, PostgreSQL, JWT",
        "Davomat App + Bot":  "Kotlin + Python (Telegram)",
    }

    for repo_slug, display_name in TRACKED_REPOS.items():
        info = get_repo_info(repo_slug)
        stars = f"⭐ {info['stars']}" if info["stars"] > 0 else "—"
        stack = stacks.get(display_name, "—")
        rows.append(f"| **{display_name}** | {stack} | {stars} | ✅ Production |")

    return "\n".join(rows)

def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Replace projects table block
    new_table = build_projects_table()
    content = re.sub(
        r"(## 🚀 Projects\n\n).*?(\n\n---)",
        rf"\g<1>{new_table}\g<2>",
        content,
        flags=re.DOTALL,
    )

    # Update total stars badge (optional)
    total = get_total_stars()
    content = re.sub(
        r"!\[Stars\]\(.*?\)",
        f"![Stars](https://img.shields.io/badge/Total%20Stars-{total}-yellow?style=flat-square)",
        content,
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ README updated — total stars: {total}")

if __name__ == "__main__":
    update_readme()
