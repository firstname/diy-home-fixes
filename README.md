# The Ultimate DIY Hub — Author Guide

A Pelican static site for a media-rich DIY / How-To blog.

This guide is for writing and publishing posts. For the technical definition of the
project (directory layout, config schema, CI workflow), see `SPEC.md`.

---

## 1. First-time setup

```bash
bash scripts/bootstrap.sh
source .venv/bin/activate
```

`bootstrap.sh` creates the virtualenv, installs pinned dependencies from
`requirements.txt`, adds the `flex` theme as a git submodule, and seeds `.env` from
`.env.example`.

**Every** Python / Pelican / pip command must run inside that virtualenv.

---

## 2. Fill in `.env`

`.env` is git-ignored and holds the secret / per-deployment values:

| Variable | What it is |
| --- | --- |
| `GITHUB_USERNAME` | Your GitHub username — determines the live site URL |
| `GITHUB_REPO` | Repository name |
| `SITE_DOMAIN` | Optional custom domain; leave blank for `*.github.io` |
| `GOOGLE_ADSENSE_CLIENT_ID` | AdSense publisher ID (`ca-pub-...`) |
| `GOOGLE_ANALYTICS_ID` | GA4 measurement ID (`G-...`) |
| `LOCAL_SITEURL` | Local preview URL, usually `http://localhost:8000` |

`publishconf.py` **fails loudly** if `GITHUB_USERNAME` / `GITHUB_REPO` are missing —
it will never guess your live URL.

---

## 3. Writing a post

```bash
./.venv/bin/python scripts/new_post.py "How to Fix a Sagging Door"
```

This creates `content/posts/<slug>.md` with the correct front matter. Running it twice
with the same title refuses to overwrite the existing file.

Front matter:

```text
Title: How to Fix a Sagging Door
Date: 2026-01-01 09:00
Category: Home Improvement
Tags: DIY, Repair
Slug: how-to-fix-a-sagging-door
Status: draft
Cover: images/how-to-fix-a-sagging-door-cover.jpg
```

Leave `Status: draft` while writing. Flip it to `published` when ready.

---

## 4. Images and video

Put image files in `content/images/`. Reference them from a post with Pelican's
`{static}` tag — never a relative path, or the link breaks on the live site:

```markdown
![Tightening the hinge screws]({static}/images/how-to-fix-a-sagging-door-step1.jpg)
```

The `Cover:` field in the front matter is the thumbnail shown on the homepage grid.

For video, prefer embedding YouTube (paste the embed `<iframe>` into the post). To host
locally instead, put the file in `content/videos/` and add `videos` to `STATIC_PATHS`
in `pelicanconf.py`.

---

## 5. Preview locally

```bash
bash scripts/serve.sh
```

Then open <http://localhost:8000>. The server auto-reloads when you save a file.

To produce a build without serving it:

```bash
./.venv/bin/pelican content -s pelicanconf.py
```

Output lands in `output/` (git-ignored).

---

## 6. Publish

Commit and push to `main`:

```bash
git add content/posts/your-post.md
git commit -m "Post: your post title"
git push origin main
```

The GitHub Actions workflow in `.github/workflows/deploy.yml` builds the production
site with `publishconf.py` and publishes `output/` to the `gh-pages` branch. The site
goes live at `https://<username>.github.io/<repo>/` (or your custom domain).

Always run a local build before pushing — it catches broken image paths and front-matter
typos without burning a CI cycle.

---

## 7. Styling

The homepage image grid lives in `content/extra/custom.css`, which is copied to
`output/static/custom.css` at build time. Edit that file — **never** edit anything
inside `themes/flex/`, since the theme is a git submodule and local edits there are
discarded on the next `git submodule update`.
