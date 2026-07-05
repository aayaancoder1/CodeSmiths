# Confirmation manager implementation

from .confirmation_interfaces import IConfirmationManager
from .confirmation_models import ConfirmationResult, ConfirmationState
from .confirmation_errors import (
    ConfirmationTimeoutError,
    InvalidConfirmationStateError,
    DuplicateConfirmationError,
    MissingDecisionError,
)
from .confirmation_validator import validate_confirmation_state


class ConfirmationManager(IConfirmationManager):
    """In‑memory manager for user confirmation decisions.

    Stores pending confirmations keyed by workflow ID and ensures a workflow can only be
    confirmed once. All state transitions are validated against the allowed states.
    """

    def __init__(self) -> None:
        self._states: dict[str, ConfirmationState] = {}
        self._plan_summaries: dict[str, str] = {}

    def _ensure_workflow_exists(self, workflow_id: str) -> None:
        if workflow_id not in self._states:
            raise InvalidConfirmationStateError(
                f"Workflow '{workflow_id}' has no pending confirmation request."
            )

    def request_confirmation(self, workflow_id: str, plan_summary: str) -> None:
        if not workflow_id or not workflow_id.strip():
            raise MissingDecisionError("Workflow ID cannot be empty.")
        if not plan_summary or not plan_summary.strip():
            raise MissingDecisionError("Plan summary cannot be empty.")
        if workflow_id in self._states:
            raise DuplicateConfirmationError(f"Confirmation already requested for workflow '{workflow_id}'.")
        self._states[workflow_id] = ConfirmationState.WAITING_CONFIRMATION
        self._plan_summaries[workflow_id] = plan_summary

    def _finalize(
        self, workflow_id: str, target_state: ConfirmationState, reason: str | None = None
    ) -> ConfirmationResult:
        self._ensure_workflow_exists(workflow_id)
        current = self._states[workflow_id]
        if current != ConfirmationState.WAITING_CONFIRMATION:
            raise InvalidConfirmationStateError(
                f"Workflow '{workflow_id}' is in state {current.value} and cannot transition to {target_state.value}."
            )
        self._states[workflow_id] = target_state
        return ConfirmationResult.from_decision(workflow_id, target_state, reason)

    def approve(self, workflow_id: str, reason: str | None = None) -> ConfirmationResult:
        return self._finalize(workflow_id, ConfirmationState.APPROVED, reason)

    def reject(self, workflow_id: str, reason: str | None = None) -> ConfirmationResult:
        return self._finalize(workflow_id, ConfirmationState.REJECTED, reason)

    def cancel(self, workflow_id: str, reason: str | None = None) -> ConfirmationResult:
        return self._finalize(workflow_id, ConfirmationState.CANCELLED, reason)

    def timeout(self, workflow_id: str, reason: str | None = None) -> ConfirmationResult:
        result = self._finalize(workflow_id, ConfirmationState.TIMED_OUT, reason)
        # Raising a dedicated error after creating a result allows callers to both catch the error and inspect the result.
        raise ConfirmationTimeoutError(
            f"Confirmation for workflow '{workflow_id}' timed out. Reason: {reason or 'No reason provided.'}"
        )

    # Utility for tests
    def get_state(self, workflow_id: str) -> ConfirmationState:
        if workflow_id not in self._states:
            raise InvalidConfirmationStateError(f"Workflow '{workflow_id}' not found.")
        return self._states[workflow_id]
