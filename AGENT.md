# CLAUDE.md — Agent Behavior Rules: "DIY Home Fixes" Pelican Static Site

This file tells an AI coding agent **how to behave** while working in this repo — process,
discipline, and constraints. It intentionally does **not** contain file contents, directory
trees, or config schemas — those live in `SPEC.md`, which is the single source of truth for
"what the app looks like." Read both before making changes:

- **`CLAUDE.md`** (this file) — how the agent should work: environment discipline, coupling
  rules, token efficiency, engineering practices, execution checklist.
- **`SPEC.md`** — what the app is: directory structure, exact file contents (configs,
  scripts, CSS, CI workflow), dependency versions.
- **`README.md`** — for the human author: how to write, insert media into, and publish a
  blog post. Not agent-facing; keep build/agent internals out of it.
- **`TASKS.md`** — the sequential build plan. This is what you actually execute against;
  see §5 below.

If a rule here conflicts with something in `SPEC.md`, `SPEC.md` wins for "what a file should
contain"; this file wins for "how to go about changing it."

---

## 0. Prime Directives

1. **Everything runs inside a local virtualenv.** Never install Python packages globally.
   Never run `pelican`, `pip`, `ghp-import`, or any project tooling outside `.venv`.
2. **No secrets in source, commits, build output, or chat/logs.** Personal/financial/
   account-specific identifiers (GitHub username/repo, AdSense publisher ID, GA4 ID, any
   API key) live only in `.env` (git-ignored) locally, and in GitHub repo Secrets/Variables
   in CI — never hardcoded in `.py`, `.yml`, or `.md` files. See `SPEC.md` §5 for the exact
   schema.
3. **Low coupling.** Content, theme, configuration, and deployment are four independent
   layers; none should need to change because another one changed (see `SPEC.md` §2 for the
   layout this enforces).
4. **Minimize token/context burn.** See §3 below — a hard operating constraint, not a
   suggestion.
5. **Keep docs in their lane.** Agent-facing process → `CLAUDE.md`. Technical definition →
   `SPEC.md`. Human author workflow → `README.md`. Don't let these blur together again.

---

## 1. Environment & Tooling Discipline (venv-only)

1. Before running **any** Python/pelican/pip command, check whether `.venv` exists; if not,
   run `scripts/bootstrap.sh` first (see `SPEC.md` §4 for its contents).
2. Prefix every command with venv activation, or invoke the venv's binaries directly
   (`./.venv/bin/pelican`, `./.venv/bin/pip`) rather than relying on shell activation state
   persisting across tool calls.
3. Never suggest or perform a global `pip install`.
4. Always run a local build (`pelican content -s pelicanconf.py`) before pushing, to catch
   errors before burning a CI cycle.

---

## 2. Secret Handling Discipline

1. If you ever find a secret typed directly into a tracked file, stop, move it into `.env`,
   replace it with an environment-variable lookup, and flag it to the user — don't silently
   commit it.
2. Never print the *contents* of `.env` to chat/logs, even to "confirm" it worked. Confirm
   success by checking the build ran without error, or `os.environ.get(...) is not None` —
   not by echoing the value.
3. `publishconf.py` must fail loudly (`KeyError`) on missing required config rather than
   silently guessing a value — see `SPEC.md` §5.4 for why.

---

## 3. Token / Context Efficiency Rules

1. **Read before writing.** Never regenerate a whole file from memory if it already exists —
   `view` current content, then use targeted edits for small changes. Only recreate a file
   wholesale if the change touches most of it.
2. **Don't paste large file contents back into chat.** Summarize what changed instead of
   quoting the whole file.
3. **Don't re-run the same read-only command twice in a session** unless something in
   between could have changed its result.
4. **Batch related file operations** — e.g. scaffolding a post + copying its images + any
   front-matter edits in one pass, not one tool call per line changed.
5. **Never dump `.env` contents, API keys, or long build logs into the conversation.** Grep
   for the specific error line instead of pasting a full traceback unless asked.
6. **Prefer targeted `view` ranges or `grep`** over viewing entire large generated files
   (e.g. `output/` HTML) when only checking one detail.
7. **Don't restate CLAUDE.md's rules back to the user in full** — apply them silently; only
   surface a rule briefly when explaining *why* you did something a particular way.

---

## 4. Software Engineering Rules

1. **Idempotency.** Every script must be safe to re-run: check-before-create, never blind-
   overwrite (bootstrap and scaffolding scripts in `SPEC.md` §4/§7 already follow this —
   preserve it in any edits).
2. **Fail fast, fail loud** for anything determining the live site's canonical URL or
   monetization IDs — never fall back to a guessed value.
3. **Version pinning.** Bump dependencies deliberately, one at a time, and re-test a local
   build after each bump.
4. **Theme as a submodule, never edited in place.** Visual overrides go in
   `content/extra/custom.css` or `content/templates/` — never patch files inside
   `themes/flex/` directly, or the next `git submodule update` silently discards the change.
5. **One post = one file, self-contained.** A post's Markdown must not depend on another
   post's metadata or shared state beyond `config/site_vars.py`.
6. **`.gitignore` must always include** `.venv/`, `.env`, `output/`, `__pycache__/`, `*.pyc`.
7. **Commit hygiene.** Small, single-purpose commits, not bundled unrelated changes.
8. **Before any dependency or theme submodule bump:** run a local build and visually confirm
   the homepage grid and AdSense/GA snippets still render — theme updates can silently drop
   template hooks.
9. **Treat doc drift as a bug.** Update `SPEC.md` when the app's shape changes, `README.md`
   when the authoring workflow changes, and this file when the agent's process should
   change.

---

## 5. Sequential Execution — `TASKS.md`

The build is broken into ordered, checkable tasks in `TASKS.md` (repo skeleton → env →
config → theme → content tooling → local build verification → CI/CD → doc sync). Rules for
working against it:

1. **Always read `TASKS.md` before starting or resuming work.** Find the first unchecked
   task and continue from there — don't re-derive the plan from scratch, and don't
   re-verify tasks already checked off unless something you're doing now could invalidate
   them (this is also a token-efficiency rule, see §3).
2. **Process tasks in order.** Don't skip ahead into a later phase (e.g. CI/CD) before
   earlier phases (e.g. local build verification) pass their Definition of Done — later
   tasks assume earlier ones are actually done, not just started.
3. **Only check off a task once its Definition of Done is verified**, not merely attempted.
   If a DoD fails, fix the underlying issue before checking the box — don't check it and
   note the failure separately.
4. **New scope becomes a new phase appended at the end of `TASKS.md`**, never a renumbering
   of existing tasks — see the note at the bottom of that file.
5. If a task's DoD reveals that `SPEC.md` and reality have diverged, treat that as a bug per
   §4.9 and reconcile them before moving to the next task.
