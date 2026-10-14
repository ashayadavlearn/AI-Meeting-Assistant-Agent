"""Common shared schemas for consistent API request and response envelopes."""

from datetime import UTC, datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ErrorDetail(BaseModel):
    """Inner error payload containing error code, message, and diagnostic details."""

    model_config = ConfigDict(extra="ignore")

    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error description")
    details: Any | None = Field(
        default=None,
        description="Detailed validation errors or contextual metadata",
    )


class ErrorResponse(BaseModel):
    """Uniform error envelope format required across all API endpoints."""

    model_config = ConfigDict(extra="ignore")

    error: ErrorDetail


class HealthResponse(BaseModel):
    """Health check status response payload."""

    model_config = ConfigDict(extra="ignore")

    status: str = Field(default="ok", description="Overall service status")
    version: str = Field(..., description="Application semantic version")
    environment: str = Field(..., description="Runtime environment")
    uptime_seconds: float = Field(..., description="Server uptime in seconds")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Current server UTC timestamp",
    )


class PaginationParams(BaseModel):
    """Standard pagination query parameters."""

    model_config = ConfigDict(extra="ignore")

    page: int = Field(default=1, ge=1, description="Page index (1-based)")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page (max 100)")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class PaginationMeta(BaseModel):
    """Pagination metadata included in paginated list responses."""

    model_config = ConfigDict(extra="ignore")

    page: int
    page_size: int
    total: int
    total_pages: int


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic envelope for paginated resource collections."""

    model_config = ConfigDict(extra="ignore")

    items: list[T]
    pagination: PaginationMeta
