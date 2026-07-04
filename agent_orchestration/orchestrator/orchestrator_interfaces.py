from abc import ABC, abstractmethod
from typing import Any, Dict

class IWorkflowOrchestrator(ABC):
    """Interface for coordinating the deterministic workflow.

    The orchestrator drives the state machine, invokes the planner, confirmation manager,
    tool executor, verification agent and audit agent. It must not contain any business logic
    that belongs to those agents.
    """

    @abstractmethod
    def run_workflow(self, user_request: str, user_id: str, confirmation_decision: str = "approve") -> Dict[str, Any]:
        """Execute the full workflow for a user request.

        Parameters
        ----------
        user_request: str
            The raw user request string.
        user_id: str
            Identifier of the user initiating the request.
        confirmation_decision: str, optional
            Decision for confirmation step ("approve", "reject", "cancel", "timeout").
        Returns
        -------
        Dict[str, Any]
            Result payload containing workflow identifiers and final state.
        """
        pass
