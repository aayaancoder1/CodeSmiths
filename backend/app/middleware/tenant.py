import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response
from app.core.context import tenant_id_ctx, request_id_ctx

logger = logging.getLogger(__name__)


class RequestContextMiddleware(BaseHTTPMiddleware):
    """FastAPI Middleware managing Request Correlation ID and Multi-Tenant Context propagation."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # 1. Correlation/Request ID extraction or generation
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

        # 2. Dynamic logical Multi-Tenancy context extraction (best effort)
        tenant_id_str = request.headers.get("X-Tenant-ID")
        tenant_id = None
        if tenant_id_str:
            try:
                tenant_id = uuid.UUID(tenant_id_str)
            except ValueError:
                # Log context parsing issues but allow flow to proceed so routes or dependencies can return structured errors
                logger.warning(f"RequestContextMiddleware: Invalid UUID format received for X-Tenant-ID: {tenant_id_str}")

        # 3. Bind context variables to current request thread/task
        token_request_id = request_id_ctx.set(request_id)
        token_tenant_id = tenant_id_ctx.set(tenant_id)

        try:
            # Process the downstream pipeline
            response = await call_next(request)
            
            # 4. Attach request correlation ID onto response headers
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            # 5. Clean up task context variables to prevent bleed across concurrent requests
            request_id_ctx.reset(token_request_id)
            tenant_id_ctx.reset(token_tenant_id)
