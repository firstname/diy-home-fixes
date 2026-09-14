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
