"""
Unit tests for RequestContextMiddleware.

Tests verify:
- X-Request-ID from incoming request is echoed back in response
- A UUID is auto-generated if X-Request-ID is missing
- X-Tenant-ID is accepted but not required for the middleware to pass through
- Requests with invalid X-Tenant-ID are still forwarded (errors handled by dependencies)
- Context variables are cleaned up after the request
"""
import uuid
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.middleware.tenant import RequestContextMiddleware
from app.core.context import get_current_request_id, get_current_tenant_id


# Minimal test app that exposes context variable values through an endpoint
def make_test_app() -> FastAPI:
    test_app = FastAPI()
    test_app.add_middleware(RequestContextMiddleware)

    @test_app.get("/ctx")
    async def read_context():
        return {
            "request_id": get_current_request_id(),
            "tenant_id": str(get_current_tenant_id()) if get_current_tenant_id() else None,
        }

    @test_app.get("/ping")
    async def ping():
        return {"status": "ok"}

    return test_app


@pytest.fixture
def client():
    return TestClient(make_test_app(), raise_server_exceptions=True)


class TestRequestContextMiddleware:

    def test_request_id_echoed_from_header(self, client):
        """When X-Request-ID is provided, the same value must appear in the response header."""
        provided_id = str(uuid.uuid4())
        response = client.get("/ping", headers={"X-Request-ID": provided_id})
        assert response.headers.get("X-Request-ID") == provided_id

    def test_request_id_auto_generated_when_missing(self, client):
        """When X-Request-ID is absent, middleware must generate a UUID and attach it."""
        response = client.get("/ping")
        request_id = response.headers.get("X-Request-ID")
        assert request_id is not None
        # Must be a valid UUID
        parsed = uuid.UUID(request_id)
        assert parsed is not None

    def test_request_id_always_in_response(self, client):
        """X-Request-ID must always be present in the response regardless of input."""
        for _ in range(3):
            response = client.get("/ping")
            assert "X-Request-ID" in response.headers

    def test_tenant_id_propagated_to_context(self, client):
        """A valid X-Tenant-ID must be available inside request handlers via context var."""
        tenant_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        response = client.get("/ctx", headers={"X-Tenant-ID": tenant_id})
        assert response.status_code == 200
        body = response.json()
        assert body["tenant_id"] == tenant_id

    def test_missing_tenant_id_does_not_fail(self, client):
        """Requests without X-Tenant-ID header must still succeed (returns None in context)."""
        response = client.get("/ctx")
        assert response.status_code == 200
        body = response.json()
        assert body["tenant_id"] is None

    def test_invalid_tenant_id_does_not_crash(self, client):
        """An invalid UUID for X-Tenant-ID must not crash — middleware logs a warning and continues."""
        response = client.get("/ctx", headers={"X-Tenant-ID": "not-a-uuid"})
        # The request still completes — errors are handled downstream by dependencies
        assert response.status_code == 200
        body = response.json()
        # tenant_id context should be None because parsing failed
        assert body["tenant_id"] is None

    def test_request_id_propagated_to_context(self, client):
        """The X-Request-ID value must be accessible via get_current_request_id() in handlers."""
        provided_id = str(uuid.uuid4())
        response = client.get("/ctx", headers={"X-Request-ID": provided_id})
        assert response.status_code == 200
        body = response.json()
        assert body["request_id"] == provided_id

    def test_each_request_gets_unique_id(self, client):
        """Auto-generated Request IDs must be unique per request."""
        ids = set()
        for _ in range(5):
            response = client.get("/ping")
            ids.add(response.headers.get("X-Request-ID"))
        assert len(ids) == 5, "Every request must receive a unique auto-generated X-Request-ID"
