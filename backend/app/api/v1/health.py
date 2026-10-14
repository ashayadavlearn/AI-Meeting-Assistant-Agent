"""Health check endpoint providing service status, version, and uptime."""

import time

from fastapi import APIRouter, status

from app.core.dependencies import SettingsDep
from app.schemas.common import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])

SERVER_START_TIME = time.time()


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Returns service availability, application version, environment, and uptime.",
)
async def health_check(settings: SettingsDep) -> HealthResponse:
    """Returns application health metrics and runtime metadata."""
    uptime = time.time() - SERVER_START_TIME
    return HealthResponse(
        status="ok",
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        uptime_seconds=round(uptime, 2),
    )
