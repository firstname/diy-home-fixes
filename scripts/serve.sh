#!/usr/bin/env bash
set -euo pipefail

# Local preview server, run inside the venv. Reloads on file changes.
source "$(dirname "$0")/../.venv/bin/activate"

exec pelican -l -r content -s pelicanconf.py
