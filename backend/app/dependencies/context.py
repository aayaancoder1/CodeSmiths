import uuid
from typing import AsyncGenerator
from fastapi import Header, HTTPException, status
from app.core.context import set_current_tenant_id, set_current_request_id


async def get_tenant_id(x_tenant_id: str = Header(..., description="Target Tenant UUID")) -> uuid.UUID:
    """FastAPI dependency extracting X-Tenant-ID from HTTP Headers.

    Sets the thread-local ContextVar to enforce database scoping.
    """
    try:
        tenant_uuid = uuid.UUID(x_tenant_id)
        # Propagate tenant UUID onto thread context variable
        set_current_tenant_id(tenant_uuid)
        return tenant_uuid
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Header 'X-Tenant-ID' must be a valid UUID string format."
        )


async def get_user_id(x_user_id: str = Header(..., description="Requesting User UUID")) -> uuid.UUID:
    """FastAPI dependency extracting X-User-ID from HTTP Headers."""
    try:
        return uuid.UUID(x_user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Header 'X-User-ID' must be a valid UUID string format."
        )
