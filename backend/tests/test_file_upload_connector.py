"""
Unit tests for the FileUploadConnector and manual upload flow.

Tests verify:
- Connector registry includes "file_upload"
- FileUploadConnector implements BaseConnector interfaces
- Ingestion works via file_upload connector mapping
- API upload route runs correctly using FileUploadConnector
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import uuid

from app.connectors import get_connector_class, CONNECTOR_REGISTRY
from app.connectors.file_upload import FileUploadConnector
from app.connectors.base import ConnectorDocument


class TestFileUploadConnectorRegistry:

    def test_connector_registration(self):
        """Verify file_upload connector type is registered."""
        assert "file_upload" in CONNECTOR_REGISTRY
        assert get_connector_class("file_upload") == FileUploadConnector


@pytest.mark.asyncio
class TestFileUploadConnectorMethods:

    async def test_connector_lifecycle(self):
        """Verify lifecycle operations do not crash."""
        connector = FileUploadConnector(config={})
        await connector.connect()
        await connector.disconnect()
        assert await connector.health_check() is True

    async def test_fetch_documents_returns_empty_or_configured_list(self):
        """fetch_documents returns mock files if configured, or default empty list."""
        conn_no_config = FileUploadConnector(config={})
        assert await conn_no_config.fetch_documents() == []

        mock_doc = ConnectorDocument(
            source_id="test-f",
            title="test.txt",
            content=b"test data",
            mime_type="text/plain",
            file_extension=".txt"
        )
        conn_with_config = FileUploadConnector(config={"documents": [mock_doc]})
        fetched = await conn_with_config.fetch_documents()
        assert len(fetched) == 1
        assert fetched[0].title == "test.txt"

    async def test_fetch_updates_is_noop(self):
        """fetch_updates is not active for direct upload and returns empty."""
        connector = FileUploadConnector(config={})
        from datetime import datetime
        updates = await connector.fetch_updates(datetime.utcnow())
        assert updates == []

    def test_convert_to_connector_document(self):
        """Verify mapping details to ConnectorDocument format."""
        connector = FileUploadConnector(config={})
        doc = connector.convert_to_connector_document(
            filename="user_doc.pdf",
            content=b"pdf binary content",
            mime_type="application/pdf",
            file_extension=".pdf",
            title="User Report"
        )
        assert isinstance(doc, ConnectorDocument)
        assert doc.source_id == "user_doc.pdf"
        assert doc.title == "User Report"
        assert doc.content == b"pdf binary content"
        assert doc.mime_type == "application/pdf"
        assert doc.file_extension == ".pdf"
        assert doc.metadata.get("storage_path") == "uploads/user_doc.pdf"


class TestFileUploadAPIIntegration:

    @patch("app.api.documents.IngestionService")
    @patch("app.api.documents.PermissionRepository")
    @patch("app.repositories.document.DocumentRepository")
    def test_api_upload_flow_invokes_connector(self, mock_doc_repo_cls, mock_perm_repo_cls, mock_ingest_service_cls, test_client, tenant_id, user_id, mock_db):
        """The FastAPI upload endpoint should route execution through FileUploadConnector."""
        mock_ingest = AsyncMock()
        mock_doc = MagicMock()
        mock_doc.id = uuid.uuid4()
        mock_doc.title = "test_file.txt"
        mock_doc.current_version = 1
        mock_doc.tenant_id = tenant_id
        mock_doc.versions = []
        mock_ingest.ingest_connector_document.return_value = mock_doc
        mock_ingest_service_cls.return_value = mock_ingest

        mock_perm = AsyncMock()
        mock_perm.get_acl_for_document.return_value = []
        mock_perm_repo_cls.return_value = mock_perm

        mock_doc_repo = AsyncMock()
        mock_doc_repo.get_active_version.return_value = None
        mock_doc_repo_cls.return_value = mock_doc_repo

        file_payload = {"file": ("test_file.txt", b"plain text uploaded contents", "text/plain")}
        
        headers = {
            "X-Tenant-ID": str(tenant_id),
            "X-User-ID": str(user_id)
        }

        from app.main import app
        from app.db.session import get_db_session
        
        app.dependency_overrides[get_db_session] = lambda: mock_db

        try:
            response = test_client.post(
                "/documents/upload",
                files=file_payload,
                data={"title": "Custom Test File", "source": "file_upload"},
                headers=headers
            )
        finally:
            app.dependency_overrides.clear()

        assert response.status_code == 201, f"Error message: {response.text}"
        data = response.json()
        assert data["title"] == "test_file.txt"
        
        # Verify ingestion was called using mapped ConnectorDocument
        mock_ingest.ingest_connector_document.assert_called_once()
        args, kwargs = mock_ingest.ingest_connector_document.call_args
        conn_doc_arg = args[0]
        assert isinstance(conn_doc_arg, ConnectorDocument)
        assert conn_doc_arg.source_id == "test_file.txt"
        assert conn_doc_arg.title == "Custom Test File"
        assert conn_doc_arg.content == b"plain text uploaded contents"
        assert conn_doc_arg.mime_type == "text/plain"
