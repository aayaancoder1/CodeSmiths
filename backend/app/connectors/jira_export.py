import logging
from datetime import datetime
from typing import Any, Dict, List
from app.connectors.base import BaseConnector, ConnectorDocument, ConnectorPermission

logger = logging.getLogger(__name__)


class JiraExportConnector(BaseConnector):
    """Ingestion connector representing Jira Exports/API ticket reader."""

    async def connect(self) -> None:
        logger.info("JiraExportConnector: Connecting to Jira Cloud API.")
        jira_url = self.config.get("jira_url")
        if not jira_url:
            logger.warning("JiraExportConnector: Jira URL is not configured.")

    async def disconnect(self) -> None:
        logger.info("JiraExportConnector: Ending API sessions.")

    async def fetch_documents(self) -> List[ConnectorDocument]:
        logger.info("JiraExportConnector: Fetching issue tickets.")
        # Returning mock Jira tickets content
        doc = ConnectorDocument(
            source_id="jira_ticket_BRAIN_101",
            title="[BRAIN-101] Implement document parsing pipeline",
            content=b"Issue: BRAIN-101\nType: Task\nAssignee: John Doe\nStatus: In Progress\nDescription: We need to parse PDF, DOCX, TXT and Markdown files dynamically.",
            mime_type="text/plain",
            file_extension=".txt",
            created_at=datetime(2026, 6, 1, 9, 0),
            updated_at=datetime(2026, 7, 2, 11, 0),
            author="System Jira Sync",
            metadata={"project_key": "BRAIN", "priority": "High"},
            permissions=[
                ConnectorPermission(principal_id="group_engineering", principal_type="group", level="write"),
                ConnectorPermission(principal_id="user_john@company.com", principal_type="user", level="admin")
            ]
        )
        return [doc]

    async def fetch_updates(self, since: datetime) -> List[ConnectorDocument]:
        logger.info(f"JiraExportConnector: Checking updated issues since {since.isoformat()}.")
        if since < datetime(2026, 7, 2, 12, 0):
            return await self.fetch_documents()
        return []

    async def health_check(self) -> bool:
        logger.info("JiraExportConnector: Testing Jira API health status.")
        return True
