from typing import Dict, Type
from app.connectors.base import BaseConnector, ConnectorDocument, ConnectorPermission
from app.connectors.google_drive import GoogleDriveConnector
from app.connectors.notion import NotionConnector
from app.connectors.slack_export import SlackExportConnector
from app.connectors.jira_export import JiraExportConnector

# Registry map for dynamic connector instantiation
CONNECTOR_REGISTRY: Dict[str, Type[BaseConnector]] = {
    "google_drive": GoogleDriveConnector,
    "notion": NotionConnector,
    "slack": SlackExportConnector,
    "jira": JiraExportConnector,
}


def get_connector_class(name: str) -> Type[BaseConnector]:
    """Retrieve connector class from the registry by its source name."""
    if name not in CONNECTOR_REGISTRY:
        raise ValueError(f"Unknown connector type: '{name}'. Supported types: {list(CONNECTOR_REGISTRY.keys())}")
    return CONNECTOR_REGISTRY[name]


__all__ = [
    "BaseConnector",
    "ConnectorDocument",
    "ConnectorPermission",
    "GoogleDriveConnector",
    "NotionConnector",
    "SlackExportConnector",
    "JiraExportConnector",
    "CONNECTOR_REGISTRY",
    "get_connector_class",
]
