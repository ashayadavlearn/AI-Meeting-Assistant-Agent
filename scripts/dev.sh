#!/usr/bin/env bash
set -e

ACTION="${1:-help}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

case "$ACTION" in
    backend)
        echo "Starting FastAPI Backend on http://localhost:8000..."
        cd "$DIR/backend"
        ./.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
        ;;
    frontend)
        echo "Starting Next.js Frontend on http://localhost:3000..."
        cd "$DIR/frontend"
        npm run dev
        ;;
    test)
        echo "Running Backend Pytest Suite..."
        cd "$DIR/backend"
        ./.venv/bin/pytest -v
        ;;
    lint)
        echo "Linting Backend with Ruff..."
        cd "$DIR/backend"
        ./.venv/bin/ruff check .
        echo "Linting Frontend with ESLint..."
        cd "$DIR/frontend"
        npm run lint
        ;;
    format)
        echo "Formatting Backend with Ruff..."
        cd "$DIR/backend"
        ./.venv/bin/ruff format .
        ./.venv/bin/ruff check --fix .
        ;;
    *)
        cat << EOF
AI Meeting Assistant Agent - Dev CLI

Usage:
  ./scripts/dev.sh backend   - Launch FastAPI backend (:8000)
  ./scripts/dev.sh frontend  - Launch Next.js frontend (:3000)
  ./scripts/dev.sh test      - Run Pytest test suite
  ./scripts/dev.sh lint      - Run Ruff and ESLint checks
  ./scripts/dev.sh format    - Auto-format backend code
EOF
        ;;
esac
