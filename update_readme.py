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
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/user/repos?per_page=100&page={page}&affiliation=owner"
        r = requests.get(url, headers=HEADERS)
        if r.status_code != 200:
            print(f"⚠️  Repos fetch failed: {r.status_code}")
            break
        data = r.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos


def get_repo_languages(repo_name: str) -> dict:
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/languages"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    return {}


def get_all_languages(all_repos: list) -> dict:
    total: Counter = Counter()
    for repo in all_repos:
        langs = get_repo_languages(repo["name"])
        total.update(langs)
    return dict(total.most_common())


def get_repo_info(repo_name: str, all_repos: list) -> dict:
    for repo in all_repos:
        if repo["name"] == repo_name:
            return {
                "stars":   repo.get("stargazers_count", 0),
                "forks":   repo.get("forks_count", 0),
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


def build_languages_section(lang_bytes: dict, top_n: int = 12) -> str:
    if not lang_bytes:
        return "_No language data found._"

    total_bytes = sum(lang_bytes.values())
    top = list(lang_bytes.items())[:top_n]

    lines = []
    for lang, count in top:
        pct = count / total_bytes * 100
        bar_len = int(pct / 2)
        bar = "█" * bar_len + "░" * (50 - bar_len)
        lines.append(f"`{lang:<20}` {bar} {pct:5.1f}%")

    return "\n".join(lines)


def update_readme():
    all_repos = get_all_repos()
    print(f"📦 Found {len(all_repos)} repos (public + private)")

    lang_bytes = get_all_languages(all_repos)
    print(f"🔤 Languages found: {', '.join(list(lang_bytes.keys()))}")

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # ── 1. Projects table ──────────────────────────────────────────────────────
    new_table = build_projects_table(all_repos)
    content = re.sub(
        r"(## 🚀 Projects\n\n).*?(\n\n---)",
        rf"\g<1>{new_table}\g<2>",
        content,
        flags=re.DOTALL,
    )

    # ── 2. Languages section ───────────────────────────────────────────────────
    new_langs = build_languages_section(lang_bytes)
    content = re.sub(
        r"(## 🔤 Languages\n\n).*?(\n\n---)",
        rf"\g<1>{new_langs}\g<2>",
        content,
        flags=re.DOTALL,
    )

    # ── 3. Total stars badge ───────────────────────────────────────────────────
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
