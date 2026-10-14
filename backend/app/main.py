"""FastAPI application factory and lifecycle entry point."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api.v1.router import api_v1_router
from app.core.config import Settings, get_settings
from app.core.handlers import register_exception_handlers
from app.core.logging import get_logger, setup_logging
from app.core.middleware import RequestContextMiddleware

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan context manager for startup and shutdown hooks."""
    settings: Settings = getattr(app.state, "settings", None) or get_settings()
    setup_logging(settings.LOG_LEVEL)
    logger.info(
        "Starting %s v%s in [%s] mode...",
        settings.PROJECT_NAME,
        settings.VERSION,
        settings.ENVIRONMENT,
    )

    yield

    logger.info("Shutting down %s...", settings.PROJECT_NAME)


def create_app(settings: Settings | None = None) -> FastAPI:
    """Factory creating and configuring the FastAPI application instance."""
    current_settings = settings or get_settings()

    app = FastAPI(
        title=current_settings.PROJECT_NAME,
        version=current_settings.VERSION,
        openapi_url=f"{current_settings.API_V1_STR}/openapi.json",
        docs_url=f"{current_settings.API_V1_STR}/docs",
        redoc_url=f"{current_settings.API_V1_STR}/redoc",
        lifespan=lifespan,
    )

    # Attach settings to application state for easy retrieval in handlers/middleware
    app.state.settings = current_settings

    # 1. Custom Request ID Tracing and Access Logging Middleware
    app.add_middleware(RequestContextMiddleware)

    # 2. CORS Middleware
    cors_origins = (
        current_settings.BACKEND_CORS_ORIGINS
        if isinstance(current_settings.BACKEND_CORS_ORIGINS, list)
        else [str(current_settings.BACKEND_CORS_ORIGINS)]
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Request-ID", "X-Response-Time"],
    )

    # 3. Centralized Exception Handlers
    register_exception_handlers(app)

    # 4. Mount API v1 Routers
    app.include_router(api_v1_router, prefix=current_settings.API_V1_STR)

    # 5. Root & Top-level Health Endpoints
    @app.get("/", include_in_schema=False)
    async def root() -> dict[str, str]:
        return {
            "name": current_settings.PROJECT_NAME,
            "version": current_settings.VERSION,
            "status": "healthy",
            "docs": f"{current_settings.API_V1_STR}/docs",
            "health": f"{current_settings.API_V1_STR}/health",
        }

    @app.get("/health", include_in_schema=False)
    async def root_health() -> RedirectResponse:
        """Convenience redirect for cloud orchestrators (Railway / Docker healthchecks)."""
        return RedirectResponse(url=f"{current_settings.API_V1_STR}/health")

    return app


# Default ASGI application instance for uvicorn
app = create_app()
