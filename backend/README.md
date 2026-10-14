# AI Meeting Assistant Agent - Backend

FastAPI backend providing speech-to-text processing, LangGraph MoM pipelines, vector semantic search, and task tracking.

## Tech Stack
- **FastAPI**: Modern, high-performance web framework
- **Pydantic v2 & Pydantic-Settings**: Environment and data validation
- **SQLAlchemy 2.0 & Alembic**: Asynchronous ORM and migrations
- **Google Gemini 2.5 Flash**: Agentic intelligence & extraction
- **Faster-Whisper**: Speech-to-text audio transcription
- **FAISS & Sentence-Transformers**: Vector store and embeddings
- **Uvicorn**: Lightning-fast ASGI server

## Getting Started

### 1. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 2. Run Tests
```bash
pytest -v
```

### 3. Run Dev Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
Interactive API documentation will be available at:
- Swagger UI: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`
