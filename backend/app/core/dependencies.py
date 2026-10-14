"""Dependency injection providers for FastAPI endpoints."""

from typing import Annotated

from fastapi import Depends, Query, Request

from app.core.config import Settings, get_settings
from app.core.logging import request_id_ctx
from app.schemas.common import PaginationParams


def get_request_id(request: Request) -> str:
    """Dependency returning the current request ID from state or context."""
    return getattr(request.state, "request_id", None) or request_id_ctx.get() or "unknown"


def get_pagination(
    page: Annotated[int, Query(ge=1, description="Page number (1-based)")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 20,
) -> PaginationParams:
    """Dependency injecting parsed pagination parameters."""
    return PaginationParams(page=page, page_size=page_size)


SettingsDep = Annotated[Settings, Depends(get_settings)]
RequestIdDep = Annotated[str, Depends(get_request_id)]
PaginationDep = Annotated[PaginationParams, Depends(get_pagination)]
