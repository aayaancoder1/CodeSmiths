from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List
from pydantic import BaseModel, Field


class ConnectorPermission(BaseModel):
    """Permission configuration fetched from the source system."""
    principal_id: str = Field(description="User or Group ID in the source system")
    principal_type: str = Field(description="Type of principal: 'user' or 'group'")
    level: str = Field(default="read", description="Permission level: 'read', 'write', 'admin'")


class ConnectorDocument(BaseModel):
    """Standardized document data payload returned by connectors."""
    source_id: str = Field(description="Unique ID of the document in the source system")
    title: str = Field(description="Title of the document")
    content: bytes = Field(description="Raw file content bytes or plain text bytes")
    mime_type: str = Field(description="MIME type of the file, e.g. 'application/pdf'")
    file_extension: str = Field(description="File extension, e.g. '.pdf', '.docx', '.txt'")
    created_at: datetime | None = Field(default=None, description="Original creation time in source system")
    updated_at: datetime | None = Field(default=None, description="Last modification time in source system")
    author: str | None = Field(default=None, description="Author name from source metadata")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom connector-specific metadata")
    permissions: List[ConnectorPermission] = Field(default_factory=list, description="ACL rules fetched from source")


class BaseConnector(ABC):
    """Abstract Base Class defining the lifecycle and operational interface for all connectors."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the connector with configuration settings (e.g. auth credentials, domain limits)."""
        self.config = config

    @abstractmethod
    async def connect(self) -> None:
        """Establish session or authenticate with the external system."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close connection pools or end sessions with the external system."""
        pass

    @abstractmethod
    async def fetch_documents(self) -> List[ConnectorDocument]:
        """Fetch all documents available from the source system (full ingestion)."""
        pass

    @abstractmethod
    async def fetch_updates(self, since: datetime) -> List[ConnectorDocument]:
        """Fetch documents updated or created since the specified timestamp (incremental sync)."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Verify the validity of connection credentials and check external API status."""
        pass
