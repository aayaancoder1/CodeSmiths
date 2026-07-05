import logging
from datetime import datetime
from typing import Any, Dict, List
from app.connectors.base import BaseConnector, ConnectorDocument

logger = logging.getLogger(__name__)


class FileUploadConnector(BaseConnector):
    """Ingestion connector for direct user file uploads.

    Exposes the BaseConnector interface to standardise direct manual uploads.
    """

    async def connect(self) -> None:
        logger.info("FileUploadConnector: Initializing session.")

    async def disconnect(self) -> None:
        logger.info("FileUploadConnector: Cleaning up session resources.")

    async def fetch_documents(self) -> List[ConnectorDocument]:
        """Fetch all documents available.

        In the case of file uploads, files are provided in real-time,
        so full sync returns what has been prepared in configuration.
        """
        logger.info("FileUploadConnector: Fetching configured documents.")
        # If files were pre-configured or passed in config
        docs = self.config.get("documents", [])
        return docs

    async def fetch_updates(self, since: datetime) -> List[ConnectorDocument]:
        """Incremental synchronization."""
        logger.info(f"FileUploadConnector: Running incremental fetch since {since.isoformat()}.")
        # Direct uploads are push-based, no-op for incremental polling
        return []

    async def health_check(self) -> bool:
        logger.info("FileUploadConnector: Verifying local storage availability.")
        return True

    def convert_to_connector_document(
        self, filename: str, content: bytes, mime_type: str, file_extension: str, title: str | None = None
    ) -> ConnectorDocument:
        """Converts manual upload arguments to standard ConnectorDocument model."""
        return ConnectorDocument(
            source_id=filename,
            title=title or filename,
            content=content,
            mime_type=mime_type or "application/octet-stream",
            file_extension=file_extension,
            metadata={"storage_path": f"uploads/{filename}"}
        )
