# SPEC.md — Technical Definition: "DIY Home Fixes" Pelican Static Site

This file is the **reference definition** of the application: directory layout, exact file
contents, configuration schema, and the deployment pipeline. It answers "what does this
system look like." For *how the agent should behave while working on it* (venv discipline,
low coupling, token efficiency, engineering rules), see `CLAUDE.md`. For *how to write and
publish a blog post*, see `README.md`.

Treat this file as the source of truth: if a generated file in the repo drifts from what's
defined here, the drift is a bug — fix the file to match this spec, or update this spec
deliberately and note why.

---

## 1. Project Objective

A Python/Pelican static site for a media-rich DIY / How-To blog, optimized for Google
AdSense monetization, with a responsive image-grid homepage, GA4 analytics, and automatic
deployment to GitHub Pages via GitHub Actions.

---

## 2. Directory Structure

```text
diy-home-fixes/
├── .venv/                        # Local virtualenv (git-ignored, created once, reused always)
├── .env                          # Real secrets/config, git-ignored, NEVER committed
├── .env.example                  # Placeholder template, committed, safe to share
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Actions deployment automation
├── content/
│   ├── images/                   # Post images
│   ├── videos/                   # (optional) local video files if not embedding YouTube
│   ├── posts/                    # One .md file per blog post
│   ├── pages/                    # Static pages (About, Contact, Privacy Policy for AdSense)
│   └── extra/
│       └── custom.css            # Homepage image-grid override (see §5)
├── themes/
│   └── flex/                     # Theme, added as a git submodule (never edited in place)
├── output/                       # Generated site (git-ignored, build artifact only)
├── scripts/
│   ├── bootstrap.sh               # One-shot: create venv, install deps, init submodule
│   ├── new_post.py                # Scaffolds a new content/posts/<slug>.md from template
│   ├── serve.sh                   # Local preview server (inside venv)
│   └── deploy.sh                  # Manual/local production build + optional publish
├── config/
│   └── site_vars.py               # Single source of truth for NON-secret shared constants
├── .gitignore
├── pelicanconf.py                 # Local/dev settings — imports from config + .env
├── publishconf.py                 # Production overrides — imports pelicanconf + .env
├── requirements.txt
├── CLAUDE.md                      # Agent behavior rules
├── SPEC.md                        # This file — technical definition
└── README.md                      # Human-facing guide: how to write/publish a post
```

**Design rationale:** `config/site_vars.py` holds constants that are shared but not secret
(URL structure, pagination size, timezone). `.env` holds secret or per-deployment values
(GitHub identity, AdSense ID, GA4 ID). `pelicanconf.py` / `publishconf.py` never contain
literal values — they only import and assemble, so changing an account or renaming the repo
is a one-line `.env` edit, never a code change.

---

## 3. Dependencies — `requirements.txt` (pinned)

```text
pelican[markdown]==4.11.0
Jinja2==3.1.5
Markdown==3.7
ghp-import==2.1.4
python-dotenv==1.0.1
```

`python-dotenv` lets `pelicanconf.py` load `.env` locally the same way GitHub Actions loads
secrets in CI — one code path for both environments.

---

## 4. Bootstrap Script — `scripts/bootstrap.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

# Create the venv only if it doesn't already exist (idempotent)
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

# Theme as a submodule, not a vendored copy, so upstream fixes are pullable
if [ ! -d "themes/flex/.git" ] && [ ! -f "themes/flex/.git" ]; then
  git submodule add https://github.com/alexandrevicenzi/flex.git themes/flex || true
fi
git submodule update --init --recursive

# Seed .env from the template if missing — never overwrite an existing .env
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "Created .env from .env.example — fill in real values before publishing."
fi

echo "Bootstrap complete. Activate with: source .venv/bin/activate"
```

---

## 5. Configuration Schema

### 5.1 Non-secret shared constants — `config/site_vars.py`

```python
"""
Single source of truth for constants shared across pelicanconf.py and publishconf.py.
Nothing secret goes here — this file IS committed to git.
"""

AUTHOR = "DIY Expert"
SITENAME = "The Ultimate DIY Hub"
TIMEZONE = "Pacific/Auckland"
DEFAULT_LANG = "en"

DEFAULT_PAGINATION = 12
SUMMARY_MAX_LENGTH = 30

ARTICLE_URL = "posts/{slug}/"
ARTICLE_SAVE_AS = "posts/{slug}/index.html"
PAGE_URL = "pages/{slug}/"
PAGE_SAVE_AS = "pages/{slug}/index.html"
```

### 5.2 Secrets / per-deployment values — `.env.example` (committed) → `.env` (git-ignored)

```dotenv
# Copy this file to .env and fill in real values. .env is git-ignored.

# --- GitHub / deployment identity ---
GITHUB_USERNAME=your-github-username
GITHUB_REPO=diy-home-fixes
SITE_DOMAIN=            # leave blank if using default github.io URL

# --- Google monetization & analytics ---
GOOGLE_ADSENSE_CLIENT_ID=ca-pub-0000000000000000
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX

# --- Local dev server ---
LOCAL_SITEURL=http://localhost:8000
```

### 5.3 `pelicanconf.py` (imports only, no literals)

```python
import os
from dotenv import load_dotenv
from config.site_vars import *  # noqa: F401,F403  (AUTHOR, SITENAME, TIMEZONE, ...)

load_dotenv()  # loads .env in local/dev; in CI, real env vars are already set by Actions

SITEURL = os.environ.get("LOCAL_SITEURL", "http://localhost:8000")
PATH = "content"

THEME = "themes/flex"
THEME_TEMPLATES_OVERRIDES = ["content/templates"]

STATIC_PATHS = ["images", "extra/custom.css"]
EXTRA_PATH_METADATA = {
    "extra/custom.css": {"path": "static/custom.css"},
}
CUSTOM_CSS = "static/custom.css"

# Feeds disabled for local/dev speed
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

GOOGLE_ADSENSE = {
    "ca_id": os.environ.get("GOOGLE_ADSENSE_CLIENT_ID", ""),
    "page_level_ads": True,
}
GOOGLE_ANALYTICS = os.environ.get("GOOGLE_ANALYTICS_ID", "")
```

### 5.4 `publishconf.py` (production overrides only)

```python
import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *  # noqa: F401,F403
from dotenv import load_dotenv

load_dotenv()

_user = os.environ["GITHUB_USERNAME"]      # hard fail if missing — never guess/hardcode
_repo = os.environ["GITHUB_REPO"]
_custom_domain = os.environ.get("SITE_DOMAIN", "").strip()

SITEURL = f"https://{_custom_domain}" if _custom_domain else f"https://{_user}.github.io/{_repo}"
RELATIVE_URLS = False

FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"

DELETE_OUTPUT_DIRECTORY = True
```

`publishconf.py` fails loudly (`KeyError`) if `GITHUB_USERNAME`/`GITHUB_REPO` are unset,
rather than silently building a broken URL. Fail fast > fail silently for anything that
determines the live site's canonical URL.

---

## 6. Homepage Image Grid — `content/extra/custom.css`

Standalone stylesheet so theme upgrades never clobber it:

```css
@media (min-width: 768px) {
    .main-content .articles-list {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 24px;
        padding: 20px 0;
    }

    .main-content .articles-list article {
        border: 1px solid #eee;
        border-radius: 8px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background: #fff;
    }

    .main-content .articles-list article img {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 4px;
        margin-bottom: 12px;
    }
}
```

---

## 7. Post Scaffolding — `scripts/new_post.py`

```python
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
```

---

## 8. GitHub Actions Deployment — `.github/workflows/deploy.yml`

Configure once in **Settings → Secrets and variables → Actions** on the repo:

- Repository **Secrets**: `GOOGLE_ADSENSE_CLIENT_ID`, `GOOGLE_ANALYTICS_ID`
- Repository **Variables**: `GITHUB_USERNAME`, `GITHUB_REPO`, `SITE_DOMAIN` (optional)

```yaml
name: Deploy Pelican Site to GitHub Pages

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    env:
      GOOGLE_ADSENSE_CLIENT_ID: ${{ secrets.GOOGLE_ADSENSE_CLIENT_ID }}
      GOOGLE_ANALYTICS_ID: ${{ secrets.GOOGLE_ANALYTICS_ID }}
      GITHUB_USERNAME: ${{ vars.GITHUB_USERNAME }}
      GITHUB_REPO: ${{ vars.GITHUB_REPO }}
      SITE_DOMAIN: ${{ vars.SITE_DOMAIN }}
    steps:
      - name: Checkout Source Code
        uses: actions/checkout@v4
        with:
          submodules: 'recursive'

      - name: Set Up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Build Production Site
        run: |
          python -m pelican content -s publishconf.py

      - name: Publish to gh-pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./output
          publish_branch: gh-pages
```

Note this workflow does **not** use a local `.venv` (CI runners are already isolated
per-job), but it mirrors the exact same `pelicanconf.py` / `publishconf.py` / `.env`-driven
config path used locally — one configuration system, two execution environments.

---

## 9. Non-Goals

- No comment system, search, or CMS — keep the stack minimal.
- No JavaScript frameworks in the theme; the grid layout (§6) is pure CSS by design, to
  keep AdSense page weight/CLS low.

---

## 10. Change Log Discipline

Any change to directory structure, config schema, CSS, scripts, or the CI workflow must be
reflected here first (or in the same commit), since `CLAUDE.md` and `README.md` both refer
to this file rather than duplicating its contents.
