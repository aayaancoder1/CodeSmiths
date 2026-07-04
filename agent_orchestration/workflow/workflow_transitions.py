from typing import Dict, Set
from agent_orchestration.workflow.workflow_models import WorkflowState
from agent_orchestration.workflow.workflow_errors import UnknownWorkflowStateError

# Define standard allowed transitions mapping
VALID_TRANSITIONS: Dict[WorkflowState, Set[WorkflowState]] = {
    WorkflowState.PENDING: {WorkflowState.PLANNED},
    WorkflowState.PLANNED: {WorkflowState.WAITING_CONFIRMATION},
    WorkflowState.WAITING_CONFIRMATION: {WorkflowState.EXECUTING},
    WorkflowState.EXECUTING: {WorkflowState.VERIFYING},
    WorkflowState.VERIFYING: {WorkflowState.SUCCESS, WorkflowState.FAILED},
    WorkflowState.FAILED: {WorkflowState.ROLLED_BACK},
    WorkflowState.SUCCESS: {WorkflowState.AUDITED},
    WorkflowState.ROLLED_BACK: {WorkflowState.AUDITED},
    WorkflowState.AUDITED: set() # Terminal state
}

def validate_state(state: Any) -> WorkflowState:
    """
    Validates if a state string is one of the allowed WorkflowState values.
    Raises UnknownWorkflowStateError if invalid.
    """
    try:
        return WorkflowState(state)
    except ValueError:
        raise UnknownWorkflowStateError(f"State '{state}' is not an allowed workflow state.")
