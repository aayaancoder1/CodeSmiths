from abc import ABC, abstractmethod
from typing import Optional

class IConfirmationManager(ABC):
    """Interface for the Confirmation Manager responsible for handling user decisions.

    The manager records a pending confirmation request and later records the user's
    explicit decision (approve, reject, cancel, or timeout). All methods raise
    appropriate domain errors on invalid usage.
    """

    @abstractmethod
    def request_confirmation(self, workflow_id: str, plan_summary: str) -> None:
        """Register a confirmation request for a workflow.

        Args:
            workflow_id: Unique identifier of the workflow awaiting confirmation.
            plan_summary: Human‑readable description of the execution plan.
        """
        pass

    @abstractmethod
    def approve(self, workflow_id: str, reason: Optional[str] = None) -> "ConfirmationResult":
        """Mark the workflow as approved.

        Returns a populated :class:`ConfirmationResult`.
        """
        pass

    @abstractmethod
    def reject(self, workflow_id: str, reason: Optional[str] = None) -> "ConfirmationResult":
        """Mark the workflow as rejected.
        """
        pass

    @abstractmethod
    def cancel(self, workflow_id: str, reason: Optional[str] = None) -> "ConfirmationResult":
        """Mark the workflow as cancelled.
        """
        pass

    @abstractmethod
    def timeout(self, workflow_id: str, reason: Optional[str] = None) -> "ConfirmationResult":
        """Mark the workflow as timed out.
        """
        pass
