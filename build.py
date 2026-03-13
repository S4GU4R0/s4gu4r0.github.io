#!/usr/bin/env python3
"""
build.py — Saguaro Prole static site builder

Usage:
    python build.py

Reads content fragments from _posts/<category>/*.html,
wraps them in the base template, and writes built pages to
<category>/<slug>.html at the repo root.

Also generates rss.xml at the repo root from all published posts.

_drafts/ is never read or built. Move a file from _drafts/ to
_posts/ when it's ready to publish.

Content fragments must start with an HTML comment block:
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
DRAFTS_DIR  = Path("_drafts")   # never touched by this script
TEMPLATE    = Path("templates/_base.html")
DONATION    = Path("templates/_donation.html")
OUTPUT_ROOT = Path(".")

SITE_URL    = "https://saguaroprole.github.io"  # update to your actual URL
SITE_TITLE  = "Saguaro Prole"
SITE_DESC   = "Writing, notes, and things I make."

# Categories that get a donation nudge
DONATION_CATEGORIES = {"writing"}

# ── Helpers ───────────────────────────────────────────────────────────────────

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

    return {
        "title":    meta.get("title", path.stem.replace("-", " ").title()),
        "date":     meta.get("date", ""),
        "category": meta.get("category", path.parent.name),
        "content":  content,
        "slug":     path.stem,
    }


def build_page(fragment: dict, base_template: str, donation_block: str) -> str:
    """Substitute template placeholders with fragment data."""
    extra = donation_block if fragment["category"] in DONATION_CATEGORIES else ""

    page = base_template
    page = page.replace("{{title}}",    fragment["title"])
    page = page.replace("{{date}}",     fragment["date"])
    page = page.replace("{{category}}", fragment["category"])
    page = page.replace("{{content}}",  fragment["content"])
    page = page.replace("{{extra}}",    extra)
    return page


def parse_date(date_str: str):
    """Try to parse a date string. Returns a datetime or None."""
    for fmt in ("%Y-%m-%d", "%b %Y", "%B %Y"):
        try:
            return datetime.strptime(date_str.strip(), fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def rfc822(dt: datetime) -> str:
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")


def build_rss(fragments: list) -> str:
    """Generate rss.xml content from a list of parsed fragments."""

    # Only include posts with a parseable date, sorted newest first
    dated = [f for f in fragments if parse_date(f["date"])]
    dated.sort(key=lambda f: parse_date(f["date"]), reverse=True)

    now = rfc822(datetime.now(timezone.utc))

    items = []
    for f in dated:
        url  = f"{SITE_URL}/{f['category']}/{f['slug']}.html"
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

    items_xml = "\n".join(items)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>{escape(SITE_TITLE)}</title>
    <link>{SITE_URL}</link>
    <description>{escape(SITE_DESC)}</description>
    <language>en-us</language>
    <lastBuildDate>{now}</lastBuildDate>
    <atom:link href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml"/>
{items_xml}
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

    for category_dir in sorted(POSTS_DIR.iterdir()):
        if not category_dir.is_dir():
            continue

        category = category_dir.name
        out_dir  = OUTPUT_ROOT / category
        out_dir.mkdir(exist_ok=True)

        for fragment_path in sorted(category_dir.glob("*.html")):
            try:
                fragment = parse_fragment(fragment_path)
                page     = build_page(fragment, base_template, donation_block)
                out_path = out_dir / fragment_path.name
                out_path.write_text(page, encoding="utf-8")
                all_frags.append(fragment)
                print(f"  ✓  {category}/{fragment_path.name}")
                built += 1
            except Exception as e:
                msg = f"  ✗  {fragment_path} — {e}"
                print(msg)
                errors.append(msg)

    # RSS
    rss = build_rss(all_frags)
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
