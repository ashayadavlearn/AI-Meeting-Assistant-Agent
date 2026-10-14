# AI Meeting Assistant Agent

Production-ready AI Meeting Assistant combining Faster-Whisper speech-to-text, Google Gemini 2.5 Flash, LangGraph workflow pipelines, FAISS semantic search, and a Next.js 15 dashboard.

## Project Structure
```
├── backend/            # FastAPI ASGI backend (Clean Architecture)
│   ├── app/
│   │   ├── api/v1/     # API routes (health, etc.)
│   │   ├── core/       # Config, exceptions, handlers, logging, middleware
│   │   ├── schemas/    # Pydantic data envelopes and contracts
│   │   └── main.py     # FastAPI application factory
│   └── tests/          # Pytest async test suite
├── frontend/           # Next.js 15 (React 19, Tailwind CSS v4, Lucide)
├── shared/             # Shared TypeScript types and constants
├── docker/             # Docker compose and container definitions
├── scripts/            # Development helper scripts (dev.ps1, dev.sh)
└── Makefile            # Make command runner
```

## Quick Start

### PowerShell (Windows)
```powershell
# Run backend
.\scripts\dev.ps1 backend

# Run frontend
.\scripts\dev.ps1 frontend

# Run backend tests
.\scripts\dev.ps1 test

# Run linters
.\scripts\dev.ps1 lint
```

### Bash (macOS/Linux)
```bash
./scripts/dev.sh backend
./scripts/dev.sh frontend
./scripts/dev.sh test
./scripts/dev.sh lint
```

### Docker Compose
```bash
docker compose -f docker/docker-compose.yml up --build
```
