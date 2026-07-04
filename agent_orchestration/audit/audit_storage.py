import copy
import threading
from typing import Dict, List, Any
from agent_orchestration.audit.audit_interfaces import AuditStorage
from agent_orchestration.audit.audit_errors import DuplicateAuditRecordError, AuditStorageError

class InMemoryAuditStorage(AuditStorage):
    """
    Thread-safe, immutable in-memory storage for audit records.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._store: Dict[str, Any] = {}

    def save(self, record: Any) -> None:
        """
        Saves an audit record to the store.
        Raises DuplicateAuditRecordError if the record already exists.
        """
        if not record or not hasattr(record, "audit_id"):
            from agent_orchestration.audit.audit_errors import InvalidAuditRecordError
            raise InvalidAuditRecordError("Cannot save invalid record without audit_id.")

        audit_id = record.audit_id

        with self._lock:
            if audit_id in self._store:
                raise DuplicateAuditRecordError(f"Audit record with id {audit_id} already exists.")
            # Store deepcopy to preserve immutability
            self._store[audit_id] = copy.deepcopy(record)

    def get(self, audit_id: str) -> Any:
        """
        Retrieves an audit record by its unique audit_id.
        Raises AuditStorageError if the record does not exist.
        """
        with self._lock:
            if audit_id not in self._store:
                raise AuditStorageError(f"Audit record with id {audit_id} not found.")
            # Return deepcopy to ensure caller cannot modify stored version
            return copy.deepcopy(self._store[audit_id])

    def list(self) -> List[Any]:
        """
        Lists all recorded audit records.
        """
        with self._lock:
            return [copy.deepcopy(record) for record in self._store.values()]

    def exists(self, audit_id: str) -> bool:
        """
        Checks if an audit record exists.
        """
        with self._lock:
            return audit_id in self._store
