import uuid
from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel


class AuditLogResponse(BaseModel):
    """Schema representing compliance audit logs response."""
    id: uuid.UUID
    tenant_id: uuid.UUID
    timestamp: datetime
    user_id: uuid.UUID | None = None
    document_id: uuid.UUID | None = None
    operation: str
    status: str
    details: Dict[str, Any]
    ip_address: str | None = None

    model_config = {"from_attributes": True}
