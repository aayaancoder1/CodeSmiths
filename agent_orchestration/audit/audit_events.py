from typing import Dict, Any

class AuditEvent:
    """
    Represents an incoming audit event wrapping details of tool execution and validation.
    """

    def __init__(self, payload: Dict[str, Any]):
        self.payload = payload

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a field from the event payload.
        """
        return self.payload.get(key, default)
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Returns the event payload.
        """
        return self.payload
