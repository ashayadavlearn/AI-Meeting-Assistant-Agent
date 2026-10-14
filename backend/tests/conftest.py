"""Pytest fixtures for backend tests."""

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import Settings, get_settings
from app.main import create_app


@pytest.fixture
def test_settings() -> Settings:
    """Fixture providing test-specific configuration."""
    return Settings(
        ENVIRONMENT="testing",
        DEBUG=False,
        SECRET_KEY="test-secret-key-for-unit-testing-only-12345",
        BACKEND_CORS_ORIGINS=["http://testserver"],
        LOG_LEVEL="WARNING",
    )


@pytest.fixture
async def async_client(test_settings: Settings) -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client fixture configured against the test app."""
    app = create_app(settings=test_settings)
    app.dependency_overrides[get_settings] = lambda: test_settings

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
