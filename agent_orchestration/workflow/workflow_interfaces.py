from abc import ABC, abstractmethod
from typing import Any

class IWorkflowStateMachine(ABC):
    """
    Interface for managing and validating workflow state transitions.
    """

    @abstractmethod
    def transition(self, workflow_id: str, to_state: Any) -> Any:
        """
        Transitions the workflow to a new state.
        Raises InvalidStateTransitionError if the transition is invalid.
        """
        pass

    @abstractmethod
    def can_transition(self, workflow_id: str, to_state: Any) -> bool:
        """
        Checks if the transition to the specified state is valid from the current state.
        """
        pass

    @abstractmethod
    def current_state(self, workflow_id: str) -> Any:
        """
        Returns the current state of the workflow.
        """
        pass

    @abstractmethod
    def reset(self, workflow_id: str) -> None:
        """
        Resets the state of the workflow to PENDING.
        """
        pass
