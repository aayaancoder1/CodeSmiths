from abc import ABC, abstractmethod
from typing import Any, List, Optional

class IAuditAgent(ABC):
    """
    Interface for the Audit Agent.
    """

    @abstractmethod
    def record_event(self, event: Any) -> Any:
        """
        Records an audit event into immutable storage.
        """
        pass

    @abstractmethod
    def get_audit_log(self, audit_id: str) -> Optional[Any]:
        """
        Retrieves a single audit log by its audit_id.
        """
        pass

class AuditStorage(ABC):
    """
    Interface for the Audit Storage Engine.
    """

    @abstractmethod
    def save(self, record: Any) -> None:
        """
        Saves a record to the storage. Raises DuplicateAuditRecordError if already exists.
        """
        pass

    @abstractmethod
    def get(self, audit_id: str) -> Any:
        """
        Retrieves a record by its unique audit_id.
        """
        pass

    @abstractmethod
    def list(self) -> List[Any]:
        """
        Lists all recorded audit records.
        """
        pass

    @abstractmethod
    def exists(self, audit_id: str) -> bool:
        """
        Checks if an audit record exists by audit_id.
        """
        pass
