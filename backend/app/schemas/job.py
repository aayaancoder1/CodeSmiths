import uuid
from datetime import datetime
from pydantic import BaseModel


class JobResponse(BaseModel):
    """Schema for background task execution logs."""
    id: uuid.UUID
    tenant_id: uuid.UUID
    job_type: str
    status: str
    error_message: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConnectorSyncResponse(BaseModel):
    """Schema for connector synchronization status logs."""
    id: uuid.UUID
    tenant_id: uuid.UUID
    connector_type: str
    last_sync_time: datetime | None = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConnectorSyncRequest(BaseModel):
    """Schema for trigger connector synchronization configurations."""
    config: dict = {}
