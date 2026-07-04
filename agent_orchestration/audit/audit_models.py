from typing import Dict, Any, Optional

try:
    from pydantic import BaseModel
except ImportError:
    class BaseModel:
        def __init__(self, **kwargs):
            for name, val in kwargs.items():
                setattr(self, name, val)
            for name, field_type in getattr(self, '__annotations__', {}).items():
                if name not in kwargs:
                    setattr(self, name, None)

        def dict(self) -> Dict[str, Any]:
            return self._to_dict(self)

        def model_dump(self) -> Dict[str, Any]:
            return self._to_dict(self)

        def _to_dict(self, obj: Any) -> Any:
            if isinstance(obj, BaseModel):
                return {k: self._to_dict(v) for k, v in obj.__dict__.items()}
            elif isinstance(obj, list):
                return [self._to_dict(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: self._to_dict(v) for k, v in obj.items()}
            return obj

class AuditRecord(BaseModel):
    audit_id: str
    workflow_id: str
    request_id: str
    user_id: str
    tool_id: str
    workflow_state: str
    execution_status: str
    verification_status: str
    confirmation_status: str
    timestamp: str
    execution_duration: float
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = dict
