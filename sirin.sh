#!/usr/bin/env bash
# Sirin's one-command launcher (Git Bash / WSL / macOS / Linux).
#
# 1. Updates to the latest main (best-effort — never blocks or overwrites
#    local work; falls back to whatever code is already on disk on any
#    failure: no network, no cached credentials, diverged history, etc.)
# 2. Installs/updates Python dependencies to match whatever code is now on disk
# 3. Starts the app
#
# Usage: ./sirin.sh

cd "$(dirname "${BASH_SOURCE[0]}")"

# Prevents git from hanging on an interactive credential prompt (e.g. an
# expired cached token) -- without this, a stalled auth prompt would freeze
# the launch instead of failing fast.
export GIT_TERMINAL_PROMPT=0

branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)

if [ "$branch" != "main" ]; then
    echo "Not on 'main' (currently on '$branch') -- skipping auto-update."
else
    echo "Checking for updates on main..."
    # lowSpeedLimit/lowSpeedTime abort a stalled connection after ~10s instead of hanging.
    if git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=10 pull --ff-only origin main; then
        echo "Up to date."
    else
        echo "Could not fast-forward (no network, or local changes conflict) -- continuing with the current code."
    fi
fi

echo "Checking dependencies..."
if [ -f ".venv/Scripts/pip.exe" ]; then
    PIP=".venv/Scripts/pip.exe"
    STREAMLIT=".venv/Scripts/streamlit.exe"
else
    PIP=".venv/bin/pip"
    STREAMLIT=".venv/bin/streamlit"
fi

if "$PIP" install -e ".[dev]" --quiet; then
    echo "Dependencies OK."
else
    echo "Dependency install failed -- continuing anyway with whatever is already installed."
fi

echo "Starting Streamlit..."
"$STREAMLIT" run app.py
