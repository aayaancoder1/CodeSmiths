"""
Shared pytest fixtures and configuration for the AI Company Brain test suite.

Fixtures here are available to every test module automatically via conftest.py discovery.
"""
import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient

from app.main import app
from app.core.context import set_current_tenant_id


# ---------------------------------------------------------------------------
# Reusable Identity Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def tenant_id() -> uuid.UUID:
    """Return a deterministic tenant UUID for test isolation."""
    return uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")


@pytest.fixture
def user_id() -> uuid.UUID:
    """Return a deterministic user UUID for test isolation."""
    return uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")


@pytest.fixture
def document_id() -> uuid.UUID:
    """Return a deterministic document UUID for test isolation."""
    return uuid.UUID("cccccccc-cccc-cccc-cccc-cccccccccccc")


@pytest.fixture(autouse=False)
def set_tenant_context(tenant_id: uuid.UUID):
    """Set tenant context variable before each test that uses it."""
    set_current_tenant_id(tenant_id)
    yield
    set_current_tenant_id(None)


# ---------------------------------------------------------------------------
# FastAPI Test Client
# ---------------------------------------------------------------------------

@pytest.fixture
def test_client() -> TestClient:
    """Synchronous TestClient wrapping the FastAPI app for HTTP-level tests."""
    return TestClient(app, raise_server_exceptions=False)


# ---------------------------------------------------------------------------
# Mock Repository / DB Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_db():
    """Return a mock AsyncSession object for service/repository unit tests."""
    db = AsyncMock()
    return db


@pytest.fixture
def mock_permission_repo():
    """Return a mock PermissionRepository."""
    return AsyncMock()
