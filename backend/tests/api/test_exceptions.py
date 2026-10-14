"""Tests for global exception handlers and uniform error envelopes."""

import pytest
from fastapi import APIRouter
from httpx import ASGITransport, AsyncClient

from app.core.config import Settings, get_settings
from app.core.exceptions import (
    EntityNotFoundException,
    ForbiddenException,
    PayloadTooLargeException,
    UnauthorizedException,
)
from app.main import create_app

# Router containing endpoints that raise custom exceptions for testing
error_test_router = APIRouter(prefix="/api/v1/test-errors")


@error_test_router.get("/not-found")
async def trigger_not_found() -> None:
    raise EntityNotFoundException(entity_name="Meeting", entity_id=42)


@error_test_router.get("/unauthorized")
async def trigger_unauthorized() -> None:
    raise UnauthorizedException("Session has expired.")


@error_test_router.get("/forbidden")
async def trigger_forbidden() -> None:
    raise ForbiddenException()


@error_test_router.get("/payload-too-large")
async def trigger_payload_too_large() -> None:
    raise PayloadTooLargeException("Audio file exceeds 100MB limit.")


@error_test_router.get("/unhandled")
async def trigger_unhandled() -> None:
    raise RuntimeError("Simulated unexpected crash.")


@pytest.fixture
async def error_client() -> AsyncClient:
    settings = Settings(ENVIRONMENT="testing", DEBUG=False)
    app = create_app(settings=settings)
    app.dependency_overrides[get_settings] = lambda: settings
    app.include_router(error_test_router)
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client


@pytest.mark.asyncio
async def test_entity_not_found_envelope(error_client: AsyncClient) -> None:
    response = await error_client.get("/api/v1/test-errors/not-found")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "NOT_FOUND"
    assert "Meeting with identifier '42' was not found" in data["error"]["message"]
    assert data["error"]["details"]["entity"] == "Meeting"
    assert data["error"]["details"]["id"] == "42"


@pytest.mark.asyncio
async def test_unauthorized_envelope(error_client: AsyncClient) -> None:
    response = await error_client.get("/api/v1/test-errors/unauthorized")
    assert response.status_code == 401
    data = response.json()
    assert data["error"]["code"] == "UNAUTHORIZED"
    assert data["error"]["message"] == "Session has expired."


@pytest.mark.asyncio
async def test_unhandled_exception_safe_envelope(error_client: AsyncClient) -> None:
    response = await error_client.get("/api/v1/test-errors/unhandled")
    assert response.status_code == 500
    data = response.json()
    assert data["error"]["code"] == "INTERNAL_SERVER_ERROR"
    # When DEBUG is false, details are hidden from clients
    assert data["error"]["details"] is None
