#!/usr/bin/env python3
"""
build.py — Saguaro Prole static site builder

Usage:
    python build.py

_posts/ structure mirrors the URL structure:

    _posts/
      desk/
        writing/   → built to desk/writing/<slug>.html
        notes/     → built to desk/notes/<slug>.html
      workshop/    → built to workshop/<slug>.html
      living-room/ → built to living-room/<slug>.html

_drafts/ mirrors _posts/ and is never read or built.
Move a file from _drafts/ to _posts/ when ready to publish.

Fragments must open with a frontmatter comment:
<!--
title: Your Post Title
date: 2026-03-01
category: writing
-->
"""

import re
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

# ── Config ────────────────────────────────────────────────────────────────────

POSTS_DIR   = Path("_posts")
TEMPLATE    = Path("templates/_base.html")
DONATION    = Path("templates/_donation.html")
OUTPUT_ROOT = Path(".")

SITE_URL    = "https://s4gu4r0.github.io"
SITE_TITLE  = "Saguaro Prole"
SITE_DESC   = "My online house."

# Categories that get a donation nudge (matched against the immediate parent dir)
DONATION_CATEGORIES = {"writing"}

# ── Helpers ───────────────────────────────────────────────────────────────────

def find_fragments(root: Path):
    """
    Yield (fragment_path, relative_out_path) for every .html file under root,
    walking up to two directory levels deep.

    _posts/desk/writing/my-post.html → out: desk/writing/my-post.html
    _posts/workshop/my-project.html  → out: workshop/my-project.html
    """
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        yield path, rel


def parse_fragment(path: Path) -> dict:
    """Extract frontmatter comment and body from a content fragment."""
    raw = path.read_text(encoding="utf-8")

    meta = {}
    match = re.match(r"^\s*<!--(.*?)-->", raw, re.DOTALL)
    if match:
        for line in match.group(1).strip().splitlines():
            if ":" in line:
                key, _, val = line.partition(":")
                meta[key.strip()] = val.strip()
        content = raw[match.end():].strip()
    else:
        content = raw.strip()

    # category = immediate parent dir name (e.g. "writing", "notes", "workshop")
    category = path.parent.name

    return {
        "title":    meta.get("title", path.stem.replace("-", " ").title()),
        "date":     meta.get("date", ""),
        "category": meta.get("category", category),
        "content":  content,
        "slug":     path.stem,
    }


def build_page(fragment: dict, rel_out: Path, base_template: str, donation_block: str) -> str:
    """Substitute template placeholders with fragment data."""
    category     = fragment["category"]
    extra        = donation_block if category in DONATION_CATEGORIES else ""

    # Compute root-relative path depth for nav hrefs (e.g. desk/writing → ../../)
    depth   = len(rel_out.parts) - 1
    root_prefix = "../" * depth if depth else ""

    page = base_template
    page = page.replace("{{title}}",       fragment["title"])
    page = page.replace("{{date}}",        fragment["date"])
    page = page.replace("{{category}}",    category)
    page = page.replace("{{content}}",     fragment["content"])
    page = page.replace("{{extra}}",       extra)
    page = page.replace("{{root}}",        root_prefix)
    return page


def parse_date(date_str: str):
    for fmt in ("%Y-%m-%d", "%b %Y", "%B %Y"):
        try:
            return datetime.strptime(date_str.strip(), fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def rfc822(dt: datetime) -> str:
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")


def build_rss(fragments: list) -> str:
    dated = [f for f in fragments if parse_date(f["date"])]
    dated.sort(key=lambda f: parse_date(f["date"]), reverse=True)
    now = rfc822(datetime.now(timezone.utc))

    items = []
    for f in dated:
        url  = f"{SITE_URL}/{f['rel_out'].as_posix()}"
        dt   = rfc822(parse_date(f["date"]))
        desc = re.sub(r"<[^>]+>", "", f["content"])[:280].strip()
        if len(desc) == 280:
            desc = desc[:desc.rfind(" ")] + "…"

        items.append(f"""    <item>
      <title>{escape(f["title"])}</title>
      <link>{url}</link>
      <guid isPermaLink="true">{url}</guid>
      <pubDate>{dt}</pubDate>
      <category>{escape(f["category"])}</category>
      <description>{escape(desc)}</description>
    </item>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{escape(SITE_TITLE)}</title>
    <link>{SITE_URL}</link>
    <description>{escape(SITE_DESC)}</description>
    <language>en-us</language>
    <lastBuildDate>{now}</lastBuildDate>
    <atom:link href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml"/>
{chr(10).join(items)}
  </channel>
</rss>
"""


# ── Main ──────────────────────────────────────────────────────────────────────

def build_all():
    base_template  = TEMPLATE.read_text(encoding="utf-8")
    donation_block = DONATION.read_text(encoding="utf-8")

    built     = 0
    errors    = []
    all_frags = []

    for frag_path, rel_out in find_fragments(POSTS_DIR):
        try:
            fragment           = parse_fragment(frag_path)
            fragment["rel_out"] = rel_out

            out_path = OUTPUT_ROOT / rel_out
            out_path.parent.mkdir(parents=True, exist_ok=True)

            page = build_page(fragment, rel_out, base_template, donation_block)
            out_path.write_text(page, encoding="utf-8")

            all_frags.append(fragment)
            print(f"  ✓  {rel_out}")
            built += 1
        except Exception as e:
            msg = f"  ✗  {frag_path} — {e}"
            print(msg)
            errors.append(msg)

    # RSS
    rss      = build_rss(all_frags)
    rss_path = OUTPUT_ROOT / "rss.xml"
    rss_path.write_text(rss, encoding="utf-8")
    rss_count = rss.count("<item>")
    print(f"  ✓  rss.xml ({rss_count} item(s))")

    print(f"\n{built} page(s) built.", end="")
    if errors:
        print(f" {len(errors)} error(s).")
    else:
        print(" All good.")


if __name__ == "__main__":
    build_all()
