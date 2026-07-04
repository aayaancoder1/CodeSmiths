from typing import Any, Dict


class BrainException(Exception):
    """Base exception for all AI Company Brain backend errors."""
    def __init__(self, message: str, code: str = "INTERNAL_SERVER_ERROR", details: Dict[str, Any] | None = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}


class TenantIsolationError(BrainException):
    """Raised when tenant contexts mix or dynamic tenant scoping fails."""
    def __init__(self, message: str = "Access denied: Tenant isolation policy violation"):
        super().__init__(message, code="TENANT_ISOLATION_VIOLATION")


class EntityNotFoundError(BrainException):
    """Raised when a requested DB record is missing."""
    def __init__(self, entity_name: str, entity_id: Any):
        super().__init__(
            f"{entity_name} with identifier {entity_id} was not found.",
            code="ENTITY_NOT_FOUND",
            details={"entity_name": entity_name, "entity_id": str(entity_id)}
        )


class PermissionDeniedError(BrainException):
    """Raised when a user lacks sufficient ACL permissions to complete an operation."""
    def __init__(self, message: str = "Permission denied: Operation not authorized"):
        super().__init__(message, code="PERMISSION_DENIED")


class ConnectorError(BrainException):
    """Raised when external systems (Google Drive, Notion, Slack, Jira) fail during connection or fetch."""
    def __init__(self, connector_type: str, message: str, details: Dict[str, Any] | None = None):
        super().__init__(
            f"Connector '{connector_type}' failed: {message}",
            code="CONNECTOR_FAILURE",
            details={"connector_type": connector_type, **(details or {})}
        )


class ParserError(BrainException):
    """Raised when document parsing fails."""
    def __init__(self, file_type: str, message: str, details: Dict[str, Any] | None = None):
        super().__init__(
            f"Failed to parse {file_type} document: {message}",
            code="PARSING_FAILURE",
            details={"file_type": file_type, **(details or {})}
        )


class EventPublishError(BrainException):
    """Raised when broadcasting indexing events fails."""
    def __init__(self, message: str, details: Dict[str, Any] | None = None):
        super().__init__(message, code="EVENT_PUBLISH_FAILURE", details=details)


class ValidationError(BrainException):
    """Raised when document payload or configurations violate constraints."""
    def __init__(self, message: str, details: Dict[str, Any] | None = None):
        super().__init__(message, code="VALIDATION_ERROR", details=details)
