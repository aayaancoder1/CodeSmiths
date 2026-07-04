from typing import Dict, Any, Optional
from enum import Enum

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

class WorkflowState(str, Enum):
    PENDING = "PENDING"
    PLANNED = "PLANNED"
    WAITING_CONFIRMATION = "WAITING_CONFIRMATION"
    EXECUTING = "EXECUTING"
    VERIFYING = "VERIFYING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"
    AUDITED = "AUDITED"

class WorkflowTransition(BaseModel):
    workflow_id: str
    from_state: WorkflowState
    to_state: WorkflowState
    timestamp: str
