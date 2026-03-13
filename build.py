#!/usr/bin/env python3
"""
build.py — Saguaro Prole static site builder

Usage:
    python build.py

Reads content fragments from _posts/<category>/*.html,
wraps them in the base template, and writes built pages to
<category>/<slug>.html at the repo root.

Content fragments must start with an HTML comment block:
<!--
title: Your Post Title
date: 2026-03-01
category: writing
-->
"""

import os
import re
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

CONTENT_DIR  = Path("_posts")
TEMPLATE     = Path("templates/_base.html")
DONATION     = Path("templates/_donation.html")
OUTPUT_ROOT  = Path(".")  # repo root — GH Pages serves from here

# Categories that get a donation nudge
DONATION_CATEGORIES = {"writing"}

# ── Helpers ───────────────────────────────────────────────────────────────────

def parse_fragment(path: Path) -> dict:
    """Extract frontmatter comment and body from a content fragment."""
    raw = path.read_text(encoding="utf-8")

    # Pull the leading <!-- ... --> comment block
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


def build_all():
    base_template = TEMPLATE.read_text(encoding="utf-8")
    donation_block = DONATION.read_text(encoding="utf-8")

    built = 0
    errors = []

    for category_dir in sorted(CONTENT_DIR.iterdir()):
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
                print(f"  ✓  {category}/{fragment_path.name}")
                built += 1
            except Exception as e:
                msg = f"  ✗  {fragment_path} — {e}"
                print(msg)
                errors.append(msg)

    print(f"\n{built} page(s) built.", end="")
    if errors:
        print(f" {len(errors)} error(s).")
    else:
        print(" All good.")


if __name__ == "__main__":
    build_all()