# orchestrator_models.py
"""Data models used by the Workflow Orchestrator.

The orchestrator only needs a lightweight context object to hold identifiers
and intermediate results. All heavy‑weight models (ExecutionPlan, ExecutionResult,
VerificationResult, etc.) are defined in their respective modules and are used
as‑is.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class WorkflowContext:
    """Container for data that flows through the orchestrated workflow.

    Attributes
    ----------
    workflow_id: str
        Unique identifier for the workflow instance.
    request_id: str
        Unique identifier for the user request.
    user_id: str
        Identifier of the user who initiated the request.
    plan: Optional[Any] = None
        The PlannerResult returned by the Planner Agent.
    execution_results: list[Any] = field(default_factory=list)
        List of ExecutionResult objects from the Tool Executor.
    verification_result: Optional[Any] = None
        VerificationResult from the Verification Agent.
    confirmation_state: Optional[str] = None
        Final state from the Confirmation Manager (e.g., "APPROVED").
    error: Optional[Exception] = None
        Captured exception if any step fails.
    """

    workflow_id: str
    request_id: str
    user_id: str
    plan: Optional[Any] = None
    execution_results: list[Any] = field(default_factory=list)
    verification_result: Optional[Any] = None
    confirmation_state: Optional[str] = None
    error: Optional[Exception] = None
