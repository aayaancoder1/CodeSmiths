import uuid
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class PermissionCheckRequest(BaseModel):
    """Schema validating access permission checks."""
    document_id: uuid.UUID
    required_level: Literal["read", "write", "admin"] = "read"


class PermissionCheckResponse(BaseModel):
    """Schema representing authorization status responses."""
    allowed: bool
    user_id: uuid.UUID
    document_id: uuid.UUID
    level: str


class PermissionGrantRequest(BaseModel):
    """Schema validating new ACL grants."""
    principal_id: uuid.UUID = Field(description="UUID of the User or Group to grant access to")
    principal_type: Literal["user", "group"]
    level: Literal["read", "write", "admin"] = "read"


class PermissionResponse(BaseModel):
    """Schema representing an ACL policy entry response."""
    id: uuid.UUID
    document_id: uuid.UUID
    user_id: uuid.UUID | None = None
    group_id: uuid.UUID | None = None
    level: str
    created_at: datetime

    model_config = {"from_attributes": True}
