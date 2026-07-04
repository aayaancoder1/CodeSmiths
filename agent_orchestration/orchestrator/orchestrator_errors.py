# orchestrator_errors.py
"""Custom exceptions for the Workflow Orchestrator.
"""

class OrchestratorError(Exception):
    """Base exception for orchestrator failures."""
    pass

class InvalidConfirmationDecisionError(OrchestratorError):
    """Raised when an unsupported confirmation decision is provided."""
    pass

class WorkflowOrchestratorStateError(OrchestratorError):
    """Raised when a state transition is invalid within the orchestrator logic."""
    pass
