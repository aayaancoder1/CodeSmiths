class WorkflowError(Exception):
    """Base exception for all workflow state machine errors."""
    pass

class InvalidStateTransitionError(WorkflowError):
    """Raised when trying to perform an illegal state transition."""
    pass

class UnknownWorkflowStateError(WorkflowError):
    """Raised when encountering a state not in the allowed list of states."""
    pass

class DuplicateTransitionError(WorkflowError):
    """Raised when attempting a transition that has already occurred or is duplicate."""
    pass

class InvalidWorkflowError(WorkflowError):
    """Raised when the workflow_id is invalid or missing."""
    pass
