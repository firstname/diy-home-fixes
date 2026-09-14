# AI Agent Specification: Pelican DIY Static Site with Google AdSense & GitHub Pages Automation

## 1. System Objective
You are an expert AI software engineer. Your task is to initialize, configure, and build a Python-based static website using **Pelican** for a media-rich DIY / How-To blog. 
The site must be fully optimized for **Google AdSense** monetization, feature a **responsive image grid layout on the homepage**, integrate **Google Analytics (GA4)**, and deploy automatically via **GitHub Pages Actions**.

---

## 2. Directory Structure Blueprint
Initialize the repository with the exact file tree layout below:

```text
diy-home-fixes/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions deployment automation
├── content/
│   ├── images/
│   │   └── door-fix-step1.jpg  # Static asset storage
│   ├── posts/
│   │   └── door-wont-close.md  # Content source
│   └── pages/
├── themes/
│   └── flex/                   # Submodule or cloned copy of the Flex theme
├── output/                     # Generated static web files (git-ignored)
├── .gitignore
├── pelicanconf.py              # Local environment configuration
├── publishconf.py              # Production environment overrides
└── requirements.txt            # Python ecosystem dependencies
```

---

## 3. Dependency Environment (`requirements.txt`)
Write the following dependencies into the `requirements.txt` file to lock versions securely:

```text
pelican[markdown]==4.11.0
Jinja2==3.1.5
Markdown==3.7
ghp-import==2.1.4
```

---

## 4. Pelican Core Settings (`pelicanconf.py`)
Configure local parameters and inject global variables required by the **Flex** theme framework:

```python
import os

AUTHOR = 'DIY Expert'
SITENAME = 'The Ultimate DIY Hub'
SITEURL = 'http://localhost:8000'

PATH = 'content'
TIMEZONE = 'Pacific/Auckland'
DEFAULT_LANG = 'en'

# Theme Settings
THEME = 'themes/flex'
THEME_TEMPLATES_OVERRIDES = ['content/templates']

# Generate clean paths for SEO
ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'

# Content handling
DEFAULT_PAGINATION = 12
SUMMARY_MAX_LENGTH = 30

# Feed generation (Disabled for local dev)
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Custom CSS Injections to override the theme into an Image Grid
CUSTOM_CSS = 'static/custom.css'
STATIC_PATHS = ['images', 'extra/custom.css']
EXTRA_PATH_METADATA = {
    'extra/custom.css': {'path': 'static/custom.css'},
}

# Google Monetization & Measurement Strategy (Local placeholders)
GOOGLE_ADSENSE = {
    'ca_id': 'ca-pub-XXXXXXXXXXXXXXXX',  # Replace with actual AdSense Publisher ID
    'page_level_ads': True
}

GOOGLE_ANALYTICS = "G-XXXXXXXXXX"  # Replace with actual GA4 Measurement ID
```

---

## 5. Homepage Image Grid Layout (`content/extra/custom.css`)
To break away from the default vertical list view, inject this structural CSS rule to automatically tile articles on the homepage grid index:

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

## 6. Content Specification Template (`content/posts/door-wont-close.md`)
Enforce this formatting logic on all newly created content posts. It includes mixed markdown elements, optimized media attachments, and safe frame nesting configurations:

```markdown
Title: How to Fix a Sagging Door That Won't Close Comfortably
Date: 2026-09-14 10:18
Category: Home Improvement
Tags: DIY, Repair, Carpentry
Slug: door-wont-close
Status: published
Cover: images/door-fix-step1.jpg

Are your door hinges sagging under heavy use? Follow this dead-simple structural troubleshooting guide to pull your doors straight back into alignment.

### Step 1: Evaluate the Hinge Clearances
Examine where the door rubbing occurs against the frame container. Usually, tightening a loose structural hinge screw solves the problem.

![Inspecting door hinges structural check]({static}/images/door-fix-step1.jpg)

### Step 2: Swap Out Core Screws
Replace the short manufacturer screws with high-grade **3-inch wood screws** directly on the top frame block. This anchors the door straight to the foundational framing studs behind the casing.

### Video Walkthrough Tutorial
If you prefer a visual reference sequence, watch our full workshop breakdown directly in the frame module below:

<div class="video-container" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; margin: 20px 0;">
    <iframe 
        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;"
        src="https://www.youtube.com/embed/dQw4w9WgXcQ" 
        title="YouTube video player" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
        allowfullscreen>
    </iframe>
</div>
```

---

## 7. Production Overrides (`publishconf.py`)
Ensure your production build optimizes paths securely for web rendering:

```python
import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://firstname.github.io/diy-home-fixes' # Replace with production URL
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'

DELETE_OUTPUT_DIRECTORY = True
```

---

## 8. GitHub Actions CI/CD Deployment (`.github/workflows/deploy.yml`)
Configure this workflow execution engine to build, process, and automatically fast-forward compiled distribution artifacts directly onto your target `gh-pages` deployment branch:

```yaml
name: Deploy Pelican Site to GitHub Pages

on:
  push:
    branches:
      - main  # Trigger on updates to main codebase branch

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: write  # Crucial flag allowing automated updates to gh-pages branch
    steps:
      - name: Checkout Source Code Repository
        uses: actions/checkout@v4
        with:
          submodules: 'recursive' # Clones external layout themes like Flex safely

      - name: Initialize Python Runtime Environment
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install Architecture Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Compile Distribution Artifacts (Production)
        run: |
          pelican content -s publishconf.py

      - name: Distribute Static Deliverables to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./output
          publish_branch: gh-pages
```

---

## 9. Next Steps Execution Rules for AI Agent
1. **Initialize Workspace:** Read this whole spec sheet. Execute initialization script commands locally.
2. **Clone The Theme:** Execute `git submodule add https://github.com/alexandrevicenzi/flex.git themes/flex` or pull the repository cleanly.
3. **Build Target Check:** Verify processing output locally using `pelican content` or serve visually at local address space.