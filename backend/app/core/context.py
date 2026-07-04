from contextvars import ContextVar
from uuid import UUID

# ContextVar storing tenant ID for the current task/request to enforce dynamic logical multi-tenancy
tenant_id_ctx: ContextVar[UUID | None] = ContextVar("tenant_id_ctx", default=None)

# ContextVar storing request ID for structured logging and correlation
request_id_ctx: ContextVar[str | None] = ContextVar("request_id_ctx", default=None)


def get_current_tenant_id() -> UUID | None:
    """Retrieve the tenant ID from the current thread/task context."""
    return tenant_id_ctx.get()


def set_current_tenant_id(tenant_id: UUID | None) -> None:
    """Set the tenant ID in the current thread/task context."""
    tenant_id_ctx.set(tenant_id)


def get_current_request_id() -> str | None:
    """Retrieve the request ID from the current thread/task context."""
    return request_id_ctx.get()


def set_current_request_id(request_id: str | None) -> None:
    """Set the request ID in the current thread/task context."""
    request_id_ctx.set(request_id)
