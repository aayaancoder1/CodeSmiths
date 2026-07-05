from typing import Any, Optional, List
from agent_orchestration.audit.audit_interfaces import IAuditAgent
from agent_orchestration.audit.audit_storage import InMemoryAuditStorage
from agent_orchestration.audit.audit_models import AuditRecord
from agent_orchestration.audit.audit_errors import (
    InvalidAuditRecordError,
    MissingAuditFieldError,
    DuplicateAuditRecordError
)

class AuditAgent(IAuditAgent):
    """
    Audit Agent that records immutable and non-sensitive audit logs in-memory.
    """

    # List of prohibited sensitive fields
    PROHIBITED_FIELDS = {
        "document_content", "document_contents", "prompt", "prompt_contents",
        "chat_history", "rag_response", "rag_responses", "embeddings",
        "knowledge_graph", "kg_data", "retrieved_documents"
    }

    # List of required fields for an AuditRecord
    REQUIRED_FIELDS = [
        "audit_id", "workflow_id", "request_id", "user_id", "tool_id",
        "workflow_state", "execution_status", "verification_status",
        "confirmation_status", "timestamp", "execution_duration", "metadata"
    ]

    def __init__(self, storage: InMemoryAuditStorage = None):
        self.storage = storage or InMemoryAuditStorage()

    def record_event(self, event: Any) -> AuditRecord:
        """
        Records an event into storage as an immutable AuditRecord.
        """
        if event is None:
            raise InvalidAuditRecordError("Event payload cannot be None.")

        # Determine if event is an instance of AuditEvent or dict
        if hasattr(event, "to_dict"):
            data = event.to_dict()
        elif isinstance(event, dict):
            data = event
        else:
            raise InvalidAuditRecordError("Event must be a dictionary or expose to_dict().")

        # 1. Check for missing required fields
        for field in self.REQUIRED_FIELDS:
            if field not in data or data[field] is None:
                raise MissingAuditFieldError(f"Missing required audit field: {field}")

        # 2. Check for prohibited sensitive data fields (in data or metadata)
        # Search top-level keys
        for key in data.keys():
            if key.lower() in self.PROHIBITED_FIELDS:
                raise InvalidAuditRecordError(f"Sensitive enterprise field '{key}' is prohibited in audit logs.")

        # Search metadata keys
        metadata = data.get("metadata", {})
        if isinstance(metadata, dict):
            for key in metadata.keys():
                if key.lower() in self.PROHIBITED_FIELDS:
                    raise InvalidAuditRecordError(f"Sensitive enterprise field '{key}' is prohibited in audit metadata.")

        # 3. Create AuditRecord
        record = AuditRecord(
            audit_id=str(data["audit_id"]),
            workflow_id=str(data["workflow_id"]),
            request_id=str(data["request_id"]),
            user_id=str(data["user_id"]),
            tool_id=str(data["tool_id"]),
            workflow_state=str(data["workflow_state"]),
            execution_status=str(data["execution_status"]),
            verification_status=str(data["verification_status"]),
            confirmation_status=str(data["confirmation_status"]),
            timestamp=str(data["timestamp"]),
            execution_duration=float(data["execution_duration"]),
            error_message=data.get("error_message"),
            metadata=dict(metadata)
        )

        # 4. Save to storage (raises DuplicateAuditRecordError if exists)
        self.storage.save(record)
        return record

    def get_audit_log(self, audit_id: str) -> Optional[AuditRecord]:
        """
        Retrieves a single audit record by its audit_id.
        """
        if not self.storage.exists(audit_id):
            return None
        return self.storage.get(audit_id)
        
    def list_audit_logs(self) -> List[AuditRecord]:
        """
        Lists all recorded audit records.
        """
        return self.storage.list()
