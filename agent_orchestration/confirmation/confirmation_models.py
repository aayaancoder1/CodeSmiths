from datetime import datetime, timezone
from typing import Optional

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
        def dict(self) -> dict:
            return self.__dict__
        def model_dump(self) -> dict:
            return self.__dict__
        def __repr__(self) -> str:
            return f"{self.__class__.__name__}({self.__dict__})"

from enum import Enum

class ConfirmationState(str, Enum):
    WAITING_CONFIRMATION = "WAITING_CONFIRMATION"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    TIMED_OUT = "TIMED_OUT"

class ConfirmationResult(BaseModel):
    """Result of a confirmation decision.

    Attributes:
        workflow_id: Identifier of the workflow.
        confirmation_status: One of the ConfirmationState values.
        approved: Boolean indicating if the workflow was approved.
        decision_timestamp: ISO‑8601 UTC timestamp of the decision.
        decision_reason: Optional human‑readable reason provided by the user.
    """

    workflow_id: str
    confirmation_status: ConfirmationState
    approved: bool
    decision_timestamp: str
    decision_reason: Optional[str] = None

    @classmethod
    def from_decision(
        cls,
        workflow_id: str,
        status: ConfirmationState,
        reason: Optional[str] = None,
    ) -> "ConfirmationResult":
        """Factory method creating a result with the current UTC timestamp.
        """
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        approved = status == ConfirmationState.APPROVED
        return cls(
            workflow_id=workflow_id,
            confirmation_status=status,
            approved=approved,
            decision_timestamp=timestamp,
            decision_reason=reason,
        )
