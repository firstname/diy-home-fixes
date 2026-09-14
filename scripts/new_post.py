#!/usr/bin/env python3
"""
Usage: ./.venv/bin/python scripts/new_post.py "How to Fix a Sagging Door"
Creates content/posts/<slug>.md with correct front matter, ready to edit.
"""
import sys
import re
from datetime import datetime
from pathlib import Path

TEMPLATE = """Title: {title}
Date: {date}
Category: Home Improvement
Tags: DIY, Repair
Slug: {slug}
Status: draft
Cover: images/{slug}-cover.jpg

Write your intro paragraph here.

### Step 1: ...

![Alt text describing the image]({{static}}/images/{slug}-step1.jpg)
"""

def slugify(title: str) -> str:
    slug = title.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")

def main():
    if len(sys.argv) < 2:
        print('Usage: new_post.py "Post Title"')
        sys.exit(1)

    title = sys.argv[1]
    slug = slugify(title)
    out_path = Path("content/posts") / f"{slug}.md"

    if out_path.exists():
        print(f"Refusing to overwrite existing file: {out_path}")
        sys.exit(1)

    out_path.write_text(
        TEMPLATE.format(title=title, slug=slug, date=datetime.now().strftime("%Y-%m-%d %H:%M")),
        encoding="utf-8",
    )
    print(f"Created {out_path}. Set Status to 'published' when ready.")

if __name__ == "__main__":
    main()
