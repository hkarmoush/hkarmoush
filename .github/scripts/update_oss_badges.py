"""Refresh the merged-PR badge row in README.md between the OSS-BADGES markers."""
import json
import re
import subprocess
import urllib.parse

USER = "hkarmoush"
README = "README.md"
START, END = "<!-- OSS-BADGES:START -->", "<!-- OSS-BADGES:END -->"

# (repo, label, simple-icons logo)
PROJECTS = [
    ("genkit-ai/genkit", "Genkit", "firebase"),
    ("mozilla-mobile/firefox-ios", "Firefox iOS", "firefoxbrowser"),
    ("dart-lang/tools", "dart-lang/tools", "dart"),
    ("flutter/devtools", "Flutter DevTools", "flutter"),
    ("CodeEditApp/CodeEdit", "CodeEdit", "swift"),
    ("iina/iina", "IINA", "apple"),
]


def merged_count(repo):
    out = subprocess.check_output(
        ["gh", "api", "-X", "GET", "search/issues",
         "-f", f"q=author:{USER} type:pr is:merged repo:{repo}"],
        text=True,
    )
    return json.loads(out)["total_count"]


def badge(repo, label, logo, count):
    img = (
        "https://img.shields.io/badge/"
        f"{urllib.parse.quote(label.replace('-', '--'), safe='')}-"
        f"{count}%20merged-58A6FF?style=for-the-badge&logo={logo}&logoColor=white&labelColor=333333"
    )
    query = urllib.parse.quote(f"author:{USER} is:pr is:merged repo:{repo}", safe="")
    link = f"https://github.com/search?q={query}&type=pullrequests"
    return f'  <a href="{link}"><img src="{img}" alt="{label}: {count} merged" /></a>'


def main():
    rows = []
    for repo, label, logo in PROJECTS:
        count = merged_count(repo)
        if count:
            rows.append((count, badge(repo, label, logo, count)))
    block = "<p align=\"center\">\n" + "\n".join(r[1] for r in rows) + "\n</p>"

    with open(README, encoding="utf-8") as f:
        text = f.read()
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    new = pattern.sub(lambda _: f"{START}\n{block}\n{END}", text)
    with open(README, "w", encoding="utf-8") as f:
        f.write(new)


if __name__ == "__main__":
    main()
