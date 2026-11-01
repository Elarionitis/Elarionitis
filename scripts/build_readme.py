"""Refresh the auto-generated sections of README.md from the GitHub API."""

import json
import os
import pathlib
import re
import urllib.request
from datetime import datetime

USER = "Elarionitis"
# Profile repo, Pages placeholder and an empty team repo.
SKIP = {USER.lower(), f"{USER.lower()}.github.io", "innovx"}
LIMIT = 6
README = pathlib.Path(__file__).resolve().parent.parent / "README.md"


def fetch(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def shorten(text, limit=80):
    text = " ".join(text.split())
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(",.;:") + "…"


def recent_repos(repos):
    own = [
        r for r in repos
        if not r["fork"] and not r["archived"] and r["name"].lower() not in SKIP
    ]
    own.sort(key=lambda r: r["pushed_at"], reverse=True)
    lines = []
    for r in own[:LIMIT]:
        day = datetime.strptime(r["pushed_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%b %-d, %Y")
        line = f"[{r['name']}]({r['html_url']}) · {day}"
        if r.get("description"):
            line += f"<br><sub>{shorten(r['description'])}</sub>"
        lines.append(line)
    return "\n\n".join(lines)


def replace(text, marker, content):
    pattern = re.compile(rf"(<!-- {marker} starts -->).*?(<!-- {marker} ends -->)", re.DOTALL)
    return pattern.sub(lambda m: f"{m.group(1)}\n{content}\n{m.group(2)}", text)


def main(repos=None):
    if repos is None:
        repos = fetch(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&sort=pushed")
    text = README.read_text()
    README.write_text(replace(text, "recent_repos", recent_repos(repos)))


if __name__ == "__main__":
    main()
