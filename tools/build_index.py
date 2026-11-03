#!/usr/bin/env python3
"""Rebuild README.md from notes/*.md: newest first, one line each (date, title, one-line summary)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEAD = """# Notes

Short write-ups of things I tested in AI tooling. Each says where its evidence is, with a rerun command where
the fixture is public. They say plainly what held and what did not.

"""


def meta(path):
    text = path.read_text()
    if text.startswith("---\n"):
        text = text.split("\n---\n", 1)[-1]
    title = next((l[2:].strip() for l in text.splitlines() if l.startswith("# ")), path.stem)
    body = [l.strip() for l in text.splitlines() if l.strip() and not l.startswith(("#", "```", "- "))]
    summary = re.sub(r"\s+", " ", body[0]) if body else ""
    if len(summary) > 140:
        summary = summary[:137].rsplit(" ", 1)[0] + "..."
    date = path.stem[:10]
    return date, title, summary


def main():
    rows = sorted((meta(p) + (p,) for p in (ROOT / "notes").glob("*.md")), reverse=True)
    lines = [HEAD]
    if not rows:
        lines.append("Nothing here yet.\n")
    for date, title, summary, p in rows:
        lines.append(f"- {date} · [{title}](notes/{p.name}): {summary}\n")
    (ROOT / "README.md").write_text("".join(lines))
    print(f"{len(rows)} notes indexed")


if __name__ == "__main__":
    main()
