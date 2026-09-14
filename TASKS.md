# TASKS.md — Sequential Build Plan

This is the execution driver. **Process tasks in order, top to bottom.** Each task has a
Definition of Done (DoD) — don't check it off until the DoD is verified, not just attempted.

**Resuming a session:** read this file first. Find the first unchecked `[ ]` task and
continue from there — don't re-derive the plan or re-verify already-checked tasks unless
something you're doing now could have invalidated them.

**Adding scope later:** append new tasks at the end under a new Phase rather than
renumbering existing ones — checked-off task IDs are a record of what happened, not just a
todo list.

Every task references the `SPEC.md` section that defines its exact contents — this file
doesn't duplicate file contents, only sequencing and verification.

---

## Phase 0 — Repo Skeleton

- [x] **T0.1** Create the directory tree from `SPEC.md` §2 (empty dirs are fine for now:
      `content/{images,videos,posts,pages,extra}`, `themes/`, `scripts/`, `config/`,
      `.github/workflows/`).
      **DoD:** `find . -maxdepth 2 -type d` matches `SPEC.md` §2.
- [x] **T0.2** Create `.gitignore` per `CLAUDE.md` §4.6 (`.venv/`, `.env`, `output/`,
      `__pycache__/`, `*.pyc`).
      **DoD:** each of those four patterns present; `git check-ignore .venv .env output` all
      return success once those paths exist.
- [x] **T0.3** `git init` (if not already a repo) and make an initial commit of the skeleton
      + docs (`CLAUDE.md`, `SPEC.md`, `README.md`, `TASKS.md`, `.gitignore`).
      **DoD:** `git log` shows one commit; `git status` is clean.

## Phase 1 — Environment

- [x] **T1.1** Write `requirements.txt` from `SPEC.md` §3.
      **DoD:** file matches spec exactly (versions pinned).
- [x] **T1.2** Write `scripts/bootstrap.sh` from `SPEC.md` §4; `chmod +x` it.
      **DoD:** script is executable and idempotent (safe to run twice).
- [x] **T1.3** Run `bash scripts/bootstrap.sh`.
      **DoD:** `.venv/` exists; `pip list` inside the venv shows all packages from
      `requirements.txt`; `themes/flex/` is populated as a submodule; `.env` was created from
      `.env.example`.

## Phase 2 — Configuration Layer

*(Do this before any content or theme work — everything else imports from here.)*

- [ ] **T2.1** Write `config/site_vars.py` from `SPEC.md` §5.1.
      **DoD:** `python -c "from config.site_vars import SITENAME; print(SITENAME)"` (run
      inside the venv) prints the expected value.
- [x] **T2.2** Write `.env.example` from `SPEC.md` §5.2.
      **DoD:** file committed; contains only placeholder values, no real IDs.
- [x] **T2.3** Confirm `.env` (git-ignored, created in T1.3) has been filled in by the human
      with real values, or flag to the user that it still contains placeholders.
      **DoD:** do NOT print `.env` contents to verify — check
      `os.environ.get("GOOGLE_ADSENSE_CLIENT_ID")` is truthy after `load_dotenv()`, without
      printing the value itself.
- [x] **T2.4** Write `pelicanconf.py` from `SPEC.md` §5.3.
      **DoD:** no literal AUTHOR/SITENAME/URL/ID values appear in this file — only imports
      and `os.environ` lookups.
- [ ] **T2.5** Write `publishconf.py` from `SPEC.md` §5.4.
      **DoD:** removing `GITHUB_USERNAME` from the environment causes an immediate
      `KeyError` when the file is imported (fail-fast check).

## Phase 3 — Theme & Styling

- [x] **T3.1** Confirm `themes/flex` submodule is present and pinned to a commit (from
      T1.3); commit the submodule reference (`.gitmodules` + gitlink) if not already
      committed.
      **DoD:** `git submodule status` shows a clean, non-dash-prefixed entry for `themes/flex`.
- [x] **T3.2** Write `content/extra/custom.css` from `SPEC.md` §6.
      **DoD:** file matches spec; not placed inside `themes/flex/` itself.
- [x] **T3.3** Verify `STATIC_PATHS` / `EXTRA_PATH_METADATA` in `pelicanconf.py` (T2.4)
      correctly map this CSS file into the build (see `SPEC.md` §5.3).
      **DoD:** after a local build (Phase 5), `output/static/custom.css` exists and its
      content matches `content/extra/custom.css`.

## Phase 4 — Content Tooling & First Post

- [x] **T4.1** Write `scripts/new_post.py` from `SPEC.md` §7; `chmod +x` it.
      **DoD:** idempotency check — running it twice with the same title refuses to
      overwrite the second time (per its own logic).
- [x] **T4.2** Write `scripts/serve.sh` (local preview launcher, wraps
      `pelican -l -r content -s pelicanconf.py`, run through the venv).
      **DoD:** running it starts a local server reachable at `http://localhost:8000`.
- [x] **T4.3** Generate one real sample post with `scripts/new_post.py` (e.g. the
      "door won't close" example) to prove the pipeline end-to-end. Add a real or
      placeholder cover image to `content/images/`.
      **DoD:** post file exists with correct front matter; referenced image file exists at
      the path the post points to.
- [x] **T4.4** Set the sample post's `Status: published`.
      **DoD:** ready for Phase 5 build to pick it up.

## Phase 5 — Local Build Verification

*(Do not proceed to Phase 6 until every DoD below passes — this is the checkpoint that
catches config/content bugs before they cost a CI cycle.)*

- [x] **T5.1** Run a local dev build: `pelican content -s pelicanconf.py` (via the venv).
      **DoD:** build exits 0, no warnings about missing files.
- [x] **T5.2** Visually check `output/index.html` (or via `serve.sh`): homepage renders as a
      responsive image grid (Phase 3), the sample post's cover image shows, and the post
      page itself renders with any embedded image/video correctly (see `README.md` §3–4 for
      what "correct" means).
      **DoD:** grid CSS is applied at ≥768px width; images/video load without broken links.
- [x] **T5.3** Confirm AdSense/GA snippets are present in the rendered HTML `<head>` (even
      if the IDs are still placeholders at this stage).
      **DoD:** `grep -r "google" output/*.html` shows the expected script tags.

## Phase 6 — CI/CD Deployment

- [x] **T6.1** Write `.github/workflows/deploy.yml` from `SPEC.md` §8.
      **DoD:** yaml lints cleanly (`actionlint` or GitHub's own workflow validation on push).
- [x] **T6.2** Confirm with the user that the following are set as real values in the GitHub
      repo (Settings → Secrets and variables → Actions) — the agent does not set these
      itself since they're entered through the GitHub UI/CLI by the repo owner:
      Secrets: `GOOGLE_ADSENSE_CLIENT_ID`, `GOOGLE_ANALYTICS_ID`;
      Variables: `GITHUB_USERNAME`, `GITHUB_REPO`, `SITE_DOMAIN` (optional).
      **DoD:** user confirms these are set; agent does not ask to see the values.
- [x] **T6.3** Push `main` and watch the Actions run.
      **DoD:** workflow run is green; `gh-pages` branch is updated; live URL
      (`https://<user>.github.io/<repo>/` or custom domain) serves the homepage grid with
      the sample post visible.
- [x] **T6.4** Spot-check the live site's `<head>` for the real (non-placeholder) AdSense/GA
      IDs.
      **DoD:** IDs present and match what's configured in GitHub Secrets (agent checks
      presence/shape, not by echoing the secret value back).

## Phase 7 — Documentation Sync

- [x] **T7.1** Confirm `README.md` instructions (`new_post.py` usage, image/video
      insertion, `.env` setup, publish flow) match what was actually built in Phases 1–6.
      **DoD:** a fresh read-through of `README.md` produces the same commands that were just
      run in this file.
- [x] **T7.2** If anything in Phases 0–6 deviated from `SPEC.md` (e.g. a different theme
      version, an extra config key), update `SPEC.md` to match reality in the same commit.
      **DoD:** no drift between `SPEC.md` and the actual repo contents.

---

## Phase 8 — Privacy Page & Additional Posts

*(Appended 2026-09-14 at the author's request: a Privacy Policy page — needed for AdSense —
and a few more sample posts so the homepage grid can be judged with real volume.)*

- [x] **T8.1** Write `content/pages/privacy-policy.md` (Status: published) covering AdSense /
      cookie / GA4 disclosure, per `SPEC.md` §2 (`content/pages/`).
      **DoD:** builds to `output/pages/privacy-policy/index.html`; the page appears in the
      rendered site navigation (`DISPLAY_PAGES_ON_MENU`); no broken links introduced.
- [x] **T8.2** Add three more posts with `scripts/new_post.py`, each with a real cover image
      and at least one in-body image, `Status: published`.
      **DoD:** each slug is new (script refuses duplicates); front matter complete; every
      image referenced by `Cover:` or `{static}` exists in `content/images/`.
- [x] **T8.3** Local build with `pelicanconf.py`.
      **DoD:** build exits 0 with no warnings; all four posts render on the homepage grid
      with cover images; local link check reports zero broken links.
- [x] **T8.4** Push `main` to both remotes and watch the Actions run.
      **DoD:** workflow green; the privacy page and all new post URLs return 200 on the
      live site.

---

## Adding a new future task (e.g. a second post, a new page type, a design tweak)

Append a new `## Phase N — <name>` section below this line, following the same format
(task ID, action, DoD). Don't insert it between existing phases.
