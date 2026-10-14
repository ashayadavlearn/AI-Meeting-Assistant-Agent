# Windows PowerShell Development Helper Script
param (
    [Parameter(Position=0)]
    [ValidateSet("backend", "frontend", "test", "lint", "format", "help")]
    [string]$Action = "help"
)

$RootDir = Split-Path -Parent $PSScriptRoot

switch ($Action) {
    "backend" {
        Write-Host "Starting FastAPI Backend on http://localhost:8000..." -ForegroundColor Cyan
        Set-Location "$RootDir\backend"
        & ".\.venv\Scripts\uvicorn.exe" app.main:app --reload --host 127.0.0.1 --port 8000
    }
    "frontend" {
        Write-Host "Starting Next.js Frontend on http://localhost:3000..." -ForegroundColor Cyan
        Set-Location "$RootDir\frontend"
        npm run dev
    }
    "test" {
        Write-Host "Running Backend Pytest Suite..." -ForegroundColor Green
        Set-Location "$RootDir\backend"
        & ".\.venv\Scripts\pytest.exe" -v
    }
    "lint" {
        Write-Host "Linting Backend with Ruff..." -ForegroundColor Yellow
        Set-Location "$RootDir\backend"
        & ".\.venv\Scripts\ruff.exe" check .
        Write-Host "Linting Frontend with ESLint..." -ForegroundColor Yellow
        Set-Location "$RootDir\frontend"
        npm run lint
    }
    "format" {
        Write-Host "Formatting Backend with Ruff..." -ForegroundColor Green
        Set-Location "$RootDir\backend"
        & ".\.venv\Scripts\ruff.exe" format .
        & ".\.venv\Scripts\ruff.exe" check --fix .
    }
    Default {
        Write-Host @"
AI Meeting Assistant Agent - PowerShell Dev CLI

Usage:
  .\scripts\dev.ps1 backend   - Launch FastAPI backend (:8000)
  .\scripts\dev.ps1 frontend  - Launch Next.js frontend (:3000)
  .\scripts\dev.ps1 test      - Run Pytest test suite
  .\scripts\dev.ps1 lint      - Run Ruff and ESLint checks
  .\scripts\dev.ps1 format    - Auto-format code
"@ -ForegroundColor White
    }
}
