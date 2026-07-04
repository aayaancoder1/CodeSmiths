import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    """Schema for document container metadata response."""
    id: uuid.UUID
    tenant_id: uuid.UUID
    title: str
    source: str
    original_filename: str | None = None
    current_version: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DocumentUploadResponse(BaseModel):
    """Schema representing successful manual document ingestion."""
    message: str = "Document uploaded and ingested successfully."
    document_id: uuid.UUID
    title: str
    version: int
    chunks_count: int
