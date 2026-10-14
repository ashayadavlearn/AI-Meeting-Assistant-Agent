.PHONY: help install dev-backend dev-frontend dev test lint format docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install       Install both backend and frontend dependencies"
	@echo "  make dev-backend   Run FastAPI backend with reload on :8000"
	@echo "  make dev-frontend  Run Next.js frontend on :3000"
	@echo "  make test          Run backend pytest suite"
	@echo "  make lint          Run backend and frontend linters (ruff, eslint)"
	@echo "  make format        Autoformat backend code with ruff"
	@echo "  make docker-up     Start Postgres, backend, frontend via Docker Compose"
	@echo "  make docker-down   Stop Docker Compose services"

install:
	cd backend && python -m venv .venv && .venv/bin/pip install -e ".[dev]"
	cd frontend && npm install

dev-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev

test:
	cd backend && pytest -v

lint:
	cd backend && ruff check .
	cd frontend && npm run lint

format:
	cd backend && ruff format . && ruff check --fix .

docker-up:
	docker compose -f docker/docker-compose.yml up --build

docker-down:
	docker compose -f docker/docker-compose.yml down
