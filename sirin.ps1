# Sirin's one-command launcher.
#
# 1. Updates to the latest `main` (best-effort — never blocks or overwrites
#    local work; falls back to whatever code is already on disk on any
#    failure: no network, no cached credentials, diverged history, etc.)
# 2. Installs/updates Python dependencies to match whatever code is now on disk
# 3. Starts the app
#
# Usage:  .\sirin.ps1   (or just double-click sirin.bat)

Set-Location $PSScriptRoot

# Prevents git from hanging on an interactive credential prompt (e.g. an
# expired cached token) -- without this, a stalled auth prompt would freeze
# the launch instead of failing fast.
$env:GIT_TERMINAL_PROMPT = "0"

$branch = git rev-parse --abbrev-ref HEAD 2>$null

if ($branch -ne "main") {
    Write-Host "Not on 'main' (currently on '$branch') -- skipping auto-update." -ForegroundColor Yellow
} else {
    Write-Host "Checking for updates on main..."
    # lowSpeedLimit/lowSpeedTime abort a stalled connection after ~10s instead of hanging.
    git -c http.lowSpeedLimit=1000 -c http.lowSpeedTime=10 pull --ff-only origin main
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Could not fast-forward (no network, or local changes conflict) -- continuing with the current code." -ForegroundColor Yellow
    } else {
        Write-Host "Up to date." -ForegroundColor Green
    }
}

Write-Host "Checking dependencies..."
& "$PSScriptRoot\.venv\Scripts\pip.exe" install -e ".[dev]" --quiet
if ($LASTEXITCODE -ne 0) {
    Write-Host "Dependency install failed -- continuing anyway with whatever is already installed." -ForegroundColor Yellow
} else {
    Write-Host "Dependencies OK." -ForegroundColor Green
}

Write-Host "Starting Streamlit..."
& "$PSScriptRoot\.venv\Scripts\streamlit.exe" run "$PSScriptRoot\app.py"
