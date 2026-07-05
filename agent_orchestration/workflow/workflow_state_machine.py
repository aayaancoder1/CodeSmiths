import datetime
from typing import Dict, Any
from agent_orchestration.workflow.workflow_interfaces import IWorkflowStateMachine
from agent_orchestration.workflow.workflow_models import WorkflowState, WorkflowTransition
from agent_orchestration.workflow.workflow_errors import (
    InvalidWorkflowError,
    InvalidStateTransitionError,
    DuplicateTransitionError,
    UnknownWorkflowStateError
)
from agent_orchestration.workflow.workflow_transitions import VALID_TRANSITIONS, validate_state

class WorkflowStateMachine(IWorkflowStateMachine):
    """
    Coordinates deterministic workflow state transitions.
    """

    def __init__(self):
        self._states: Dict[str, WorkflowState] = {}
        self._transition_history: Dict[str, list] = {}

    def _validate_id(self, workflow_id: str) -> None:
        if not workflow_id or not isinstance(workflow_id, str) or not workflow_id.strip():
            raise InvalidWorkflowError("Workflow ID must be a non-empty string.")

    def current_state(self, workflow_id: str) -> WorkflowState:
        """
        Returns the current state of the workflow. Initializes to PENDING if not tracked.
        """
        self._validate_id(workflow_id)
        if workflow_id not in self._states:
            self._states[workflow_id] = WorkflowState.PENDING
        return self._states[workflow_id]

    def can_transition(self, workflow_id: str, to_state: Any) -> bool:
        """
        Checks if the transition to the specified state is valid from the current state.
        """
        self._validate_id(workflow_id)
        target_state = validate_state(to_state)
        curr = self.current_state(workflow_id)

        allowed = VALID_TRANSITIONS.get(curr, set())
        return target_state in allowed

    def transition(self, workflow_id: str, to_state: Any) -> WorkflowTransition:
        """
        Transitions the workflow to a new state.
        Raises InvalidStateTransitionError or DuplicateTransitionError if invalid.
        """
        self._validate_id(workflow_id)
        target_state = validate_state(to_state)
        curr = self.current_state(workflow_id)

        # Reject duplicate transition to current state
        if curr == target_state:
            raise DuplicateTransitionError(f"Workflow {workflow_id} is already in state {target_state.value}")

        # Check if transition is valid
        if not self.can_transition(workflow_id, target_state):
            raise InvalidStateTransitionError(
                f"Transition from {curr.value} to {target_state.value} is not permitted."
            )

        # Perform transition
        self._states[workflow_id] = target_state
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

        transition_record = WorkflowTransition(
            workflow_id=workflow_id,
            from_state=curr,
            to_state=target_state,
            timestamp=timestamp
        )

        if workflow_id not in self._transition_history:
            self._transition_history[workflow_id] = []
        self._transition_history[workflow_id].append(transition_record)

        return transition_record

    def reset(self, workflow_id: str) -> None:
        """
        Resets the state of the workflow to PENDING.
        """
        self._validate_id(workflow_id)
        self._states[workflow_id] = WorkflowState.PENDING
        if workflow_id in self._transition_history:
            self._transition_history[workflow_id].clear()
