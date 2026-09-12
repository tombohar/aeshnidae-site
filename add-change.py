#!/usr/bin/env python3
"""Add a world-change entry to changes.html from its .patchnote.md.

    python add-change.py C:\\ACEPublic\\Mods\\Content\\sql\\changes\\2026-09-11_001_tusk.patchnote.md
    python add-change.py <note.md> --push      also commit and push the site

One file drives three records - the Discord post, the git history and this page - so
they cannot drift. The note is the source; this script is the translation.

The note's shape (see any existing one):

    **Title line**                      -> <h3>
    blank-line-separated paragraphs     -> <p>, with **bold** and `code` kept
    ``` fenced blocks ```               -> <pre class="values"> (the value tables)

The date comes from the filename's leading YYYY-MM-DD. The entry goes at the TOP of
<div class="rules changes"> - newest first. Adding the same title twice is refused, so
re-running after a partial failure is safe.
"""
import argparse, html, io, os, re, subprocess, sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "changes.html")
MARK = '<div class="rules changes">'


def inline(text):
    """Escape, then re-introduce the two inline forms the notes use."""
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def convert(md):
    lines = md.strip().splitlines()

    # Title: the first non-empty line, bold markers stripped.
    while lines and not lines[0].strip():
        lines.pop(0)
    if not lines:
        sys.exit("empty note")
    title = re.sub(r"^\*\*(.+?)\*\*$", r"\1", lines.pop(0).strip())

    blocks, para, fence = [], [], None
    for line in lines:
        if line.strip().startswith("```"):
            if fence is None:
                if para:
                    blocks.append(("p", " ".join(para))); para = []
                fence = []
            else:
                blocks.append(("pre", "\n".join(fence))); fence = None
            continue
        if fence is not None:
            fence.append(line.rstrip())
        elif line.strip():
            para.append(line.strip())
        elif para:
            blocks.append(("p", " ".join(para))); para = []
    if para:
        blocks.append(("p", " ".join(para)))

    out = []
    for kind, body in blocks:
        if kind == "p":
            out.append(f"        <p>{inline(body)}</p>")
        else:
            out.append(f'        <pre class="values">{html.escape(body, quote=False)}</pre>')
    return title, "\n".join(out)


def entry_html(title, body, when):
    return (
        '      <div class="rule">\n'
        f'        <p class="eyebrow">{when}</p>\n'
        f"        <h3>{inline(title)}</h3>\n"
        f"{body}\n"
        "      </div>\n"
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("note")
    ap.add_argument("--push", action="store_true", help="commit and push the site afterwards")
    ap.add_argument("--date", help="override the date taken from the filename, e.g. 2026-09-11")
    args = ap.parse_args()

    md = io.open(args.note, encoding="utf-8").read()
    title, body = convert(md)

    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", os.path.basename(args.note))
    iso = args.date or (m.group(0) if m else date.today().isoformat())
    y, mo, d = (int(x) for x in iso.split("-"))
    when = f"{d} {date(y, mo, d).strftime('%B %Y')}"

    page = io.open(PAGE, encoding="utf-8").read()
    if f"<h3>{inline(title)}</h3>" in page:
        print(f"already on the page: {title}")
        return 0

    i = page.find(MARK)
    if i < 0:
        sys.exit(f"could not find {MARK} in changes.html")
    i += len(MARK)
    page = page[:i] + "\n" + entry_html(title, body, when) + page[i:].lstrip("\n")
    io.open(PAGE, "w", encoding="utf-8").write(page)
    print(f"added: {when} - {title}")

    if args.push:
        subprocess.run(["git", "-C", HERE, "add", "changes.html"], check=True)
        subprocess.run(["git", "-C", HERE, "commit", "-q", "-m",
                        f"Changes: {title}\n\nFrom {os.path.basename(args.note)}.\n\n"
                        "Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"], check=True)
        subprocess.run(["git", "-C", HERE, "push", "-q", "origin", "main"], check=True)
        print("site pushed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
