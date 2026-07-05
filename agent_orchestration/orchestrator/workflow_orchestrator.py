# workflow_orchestrator.py
"""Workflow Orchestrator implementation.

The orchestrator coordinates the end‑to‑end flow using the already‑implemented
agents. No business logic from those agents is duplicated here – the orchestrator
only drives state transitions, generates identifiers, and records the final
audit event.
"""

import uuid
import datetime
from typing import Dict, Any

# Import public interfaces / classes from existing modules (read‑only)
from agent_orchestration.planner.planner_agent import PlannerAgent
from agent_orchestration.confirmation.confirmation_manager import ConfirmationManager
from agent_orchestration.tool_executor.tool_executor import ToolExecutor
from agent_orchestration.verification.verification_agent import VerificationAgent
from agent_orchestration.audit.audit_agent import AuditAgent
from agent_orchestration.workflow.workflow_state_machine import WorkflowStateMachine

# Orchestrator specific contracts / models / errors
from .orchestrator_interfaces import IWorkflowOrchestrator
from .orchestrator_models import WorkflowContext
from .orchestrator_errors import (
    OrchestratorError,
    InvalidConfirmationDecisionError,
    WorkflowOrchestratorStateError,
)


class WorkflowOrchestrator(IWorkflowOrchestrator):
    """Concrete implementation of the workflow orchestrator.

    Parameters
    ----------
    planner : PlannerAgent, optional
        Inject a custom planner (useful for testing). Defaults to the standard
        ``PlannerAgent``.
    confirmation_manager : ConfirmationManager, optional
        Inject a custom confirmation manager. Defaults to ``ConfirmationManager``.
    tool_executor : ToolExecutor, optional
        Inject a custom tool executor. Defaults to ``ToolExecutor``.
    verification_agent : VerificationAgent, optional
        Inject a custom verification agent. Defaults to ``VerificationAgent``.
    audit_agent : AuditAgent, optional
        Inject a custom audit agent. Defaults to ``AuditAgent``.
    state_machine : WorkflowStateMachine, optional
        Inject a custom state machine. Defaults to ``WorkflowStateMachine``.
    """

    # Class attributes for easy patching in tests
    planner: PlannerAgent = None
    confirmation_manager: ConfirmationManager = None
    tool_executor: ToolExecutor = None
    verification_agent: VerificationAgent = None
    audit_agent: AuditAgent = None
    state_machine: WorkflowStateMachine = None

    def __init__(
        self,
        planner: PlannerAgent = None,
        confirmation_manager: ConfirmationManager = None,
        tool_executor: ToolExecutor = None,
        verification_agent: VerificationAgent = None,
        audit_agent: AuditAgent = None,
        state_machine: WorkflowStateMachine = None,
    ):
        self.planner = planner or PlannerAgent()
        self.confirmation_manager = confirmation_manager or ConfirmationManager()
        self.tool_executor = tool_executor or ToolExecutor()
        self.verification_agent = verification_agent or VerificationAgent()
        self.audit_agent = audit_agent or AuditAgent()
        self.state_machine = state_machine or WorkflowStateMachine()

    # ---------------------------------------------------------------------
    # Helper methods
    # ---------------------------------------------------------------------
    def _generate_id(self) -> str:
        """Return a short, random identifier using ``uuid4``.

        The identifier is deterministic enough for the orchestrator's purpose
        while keeping the output readable.
        """

        return uuid.uuid4().hex[:8]

    def _record_audit(self, ctx: WorkflowContext, final_state: str) -> str:
        """Create an audit event and persist it via the AuditAgent.

        Parameters
        ----------
        ctx : WorkflowContext
            The context containing all information gathered during the workflow.
        final_state : str
            The terminal workflow state (``SUCCESS`` or ``FAILED``).

        Returns
        -------
        str
            The ``audit_id`` of the persisted record.
        """

        audit_id = self._generate_id()
        total_duration = sum(
            getattr(r, "execution_time", 0) for r in ctx.execution_results
        )
        first_result = ctx.execution_results[0] if ctx.execution_results else None
        tool_id = getattr(first_result, "tool_id", "none")
        execution_status = getattr(first_result, "execution_status", "none")
        verification_status = (
            getattr(ctx.verification_result, "verification_status", "none")
            if ctx.verification_result
            else "none"
        )
        confirmation_status = ctx.confirmation_state or "none"
        error_message = str(ctx.error) if ctx.error else None

        audit_event = {
            "audit_id": audit_id,
            "workflow_id": ctx.workflow_id,
            "request_id": ctx.request_id,
            "user_id": ctx.user_id,
            "tool_id": tool_id,
            "workflow_state": final_state,
            "execution_status": execution_status,
            "verification_status": verification_status,
            "confirmation_status": confirmation_status,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat().replace(
                "+00:00", "Z"
            ),
            "execution_duration": total_duration,
            "error_message": error_message,
            "metadata": {},
        }

        self.audit_agent.record_event(audit_event)
        return audit_id

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def run_workflow(
        self, user_request: str, user_id: str, confirmation_decision: str = "approve"
    ) -> Dict[str, Any]:
        """Execute the full workflow.

        The method follows the strict ordering required by the architecture and
        never implements any of the business logic of the individual agents.
        """

        decision = confirmation_decision.lower()
        if decision not in {"approve", "reject", "cancel", "timeout"}:
            raise InvalidConfirmationDecisionError(
                f"Unsupported confirmation decision: {confirmation_decision}"
            )

        workflow_id = self._generate_id()
        request_id = self._generate_id()
        ctx = WorkflowContext(
            workflow_id=workflow_id,
            request_id=request_id,
            user_id=user_id,
        )

        # Initialise state – default is PENDING, transition to PLANNED
        try:
            self.state_machine.transition(workflow_id, "PLANNED")
        except Exception as e:
            raise WorkflowOrchestratorStateError(str(e))

        # Planning phase
        try:
            planner_result = self.planner.create_plan(user_request)
            ctx.plan = planner_result
        except Exception as e:
            ctx.error = e
            # Planner error occurs before any valid transition to FAILURE; avoid invalid state changes.
            # Directly record audit without transitioning through disallowed states.
            audit_id = self._record_audit(ctx, "FAILED")
            return {
                "workflow_id": workflow_id,
                "request_id": request_id,
                "final_state": "AUDITED",
                "audit_id": audit_id,
                "error": str(e),
            }

        # Confirmation handling if required
        if getattr(planner_result, "confirmation_flag", False):
            self.state_machine.transition(workflow_id, "WAITING_CONFIRMATION")
            self.confirmation_manager.request_confirmation(
                workflow_id, planner_result.execution_plan.goal
            )
            try:
                if decision == "approve":
                    self.confirmation_manager.approve(workflow_id)
                elif decision == "reject":
                    self.confirmation_manager.reject(workflow_id)
                elif decision == "cancel":
                    self.confirmation_manager.cancel(workflow_id)
                else:
                    self.confirmation_manager.timeout(workflow_id)
            except Exception as e:
                ctx.error = e
                ctx.confirmation_state = "FAILED"
                self.state_machine.transition(workflow_id, "FAILED")
                self.state_machine.transition(workflow_id, "ROLLED_BACK")
                audit_id = self._record_audit(ctx, "FAILED")
                self.state_machine.transition(workflow_id, "AUDITED")
                return {
                    "workflow_id": workflow_id,
                    "request_id": request_id,
                    "final_state": "AUDITED",
                    "audit_id": audit_id,
                    "error": str(e),
                }
            ctx.confirmation_state = decision.upper()
            self.state_machine.transition(workflow_id, "EXECUTING")
        else:
            self.state_machine.transition(workflow_id, "EXECUTING")

        # Execution phase
        try:
            exec_results = self.tool_executor.execute(ctx.plan.execution_plan)
            ctx.execution_results = exec_results
        except Exception as e:
            ctx.error = e
            self.state_machine.transition(workflow_id, "FAILED")
            self.state_machine.transition(workflow_id, "ROLLED_BACK")
            audit_id = self._record_audit(ctx, "FAILED")
            self.state_machine.transition(workflow_id, "AUDITED")
            return {
                "workflow_id": workflow_id,
                "request_id": request_id,
                "final_state": "AUDITED",
                "audit_id": audit_id,
                "error": str(e),
            }

        # Verification phase (first failing result aborts)
        verification_failed = False
        try:
            for result in exec_results:
                verification_res = self.verification_agent.verify(result)
                ctx.verification_result = verification_res
                if not getattr(verification_res, "verified", True):
                    verification_failed = True
                    break
        except Exception as e:
            verification_failed = True
            ctx.error = e

        if verification_failed:
            self.state_machine.transition(workflow_id, "FAILED")
            self.state_machine.transition(workflow_id, "ROLLED_BACK")
            audit_id = self._record_audit(ctx, "FAILED")
            self.state_machine.transition(workflow_id, "AUDITED")
            return {
                "workflow_id": workflow_id,
                "request_id": request_id,
                "final_state": "AUDITED",
                "audit_id": audit_id,
                "error": str(ctx.error) if ctx.error else "Verification failed",
            }

        # Success path
        self.state_machine.transition(workflow_id, "SUCCESS")
        audit_id = self._record_audit(ctx, "SUCCESS")
        self.state_machine.transition(workflow_id, "AUDITED")

        return {
            "workflow_id": workflow_id,
            "request_id": request_id,
            "final_state": "AUDITED",
            "audit_id": audit_id,
            "result": [
                r.model_dump() if hasattr(r, "model_dump") else r for r in ctx.execution_results
            ],
        }

# End of file
