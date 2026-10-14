"""Tests for health check endpoints and response headers."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_endpoint(async_client: AsyncClient) -> None:
    """Verifies that GET /api/v1/health returns 200 OK and expected structure."""
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"
    assert data["environment"] == "testing"
    assert "uptime_seconds" in data
    assert "timestamp" in data
    assert data["uptime_seconds"] >= 0.0

    # Verify tracking headers
    assert "x-request-id" in response.headers
    assert "x-response-time" in response.headers


@pytest.mark.asyncio
async def test_custom_request_id_header_propagation(async_client: AsyncClient) -> None:
    """Verifies that an incoming X-Request-ID is preserved in the response."""
    custom_id = "test-custom-tracing-uuid-9999"
    response = await async_client.get("/api/v1/health", headers={"X-Request-ID": custom_id})
    assert response.status_code == 200
    assert response.headers.get("x-request-id") == custom_id


@pytest.mark.asyncio
async def test_root_endpoint(async_client: AsyncClient) -> None:
    """Verifies root endpoint returns service metadata."""
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["docs"] == "/api/v1/docs"
