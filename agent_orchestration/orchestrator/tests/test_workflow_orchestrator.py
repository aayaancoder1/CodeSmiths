# test_workflow_orchestrator.py
"""Integration tests for the deterministic Workflow Orchestrator.

The orchestrator coordinates the Planner, Confirmation, Tool Executor,
Verification, and Audit agents. These tests cover the primary execution
paths using the real implementations but monkey‑patching components to
force failures where needed. All tool identifiers used are the deterministic
mock tools defined in `agent_orchestration.tool_executor.tool_registry`:

- jira.create_ticket
- document.create
- email.send
- meeting.summarize
"""

import pytest
from unittest.mock import patch, MagicMock

from agent_orchestration.orchestrator.workflow_orchestrator import WorkflowOrchestrator
from agent_orchestration.orchestrator.orchestrator_errors import (
    InvalidConfirmationDecisionError,
    WorkflowOrchestratorStateError,
)

# Helper to create a simple request that triggers the "jira" template (requires confirmation)
JIRA_REQUEST = "Please create a Jira ticket for the new feature."

# ---------------------------------------------------------------------------
# Successful workflow execution (approval path)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Confirmation rejected path
# ---------------------------------------------------------------------------
def test_confirmation_rejected():
    orchestrator = WorkflowOrchestrator()
    result = orchestrator.run_workflow(JIRA_REQUEST, user_id="user123", confirmation_decision="reject")
    # Rejection should still result in an audited state with no execution results
    assert result["final_state"] == "AUDITED"
    # When rejected, execution should be skipped, so result list is empty
    assert result.get("result", []) == []

# ---------------------------------------------------------------------------
# Tool execution failure (force timeout via special input)
# ---------------------------------------------------------------------------
def test_tool_execution_failure():
    # Patch the planner to return a plan whose first step uses a mock tool with force_timeout input
    with patch.object(WorkflowOrchestrator, "planner") as mock_planner:
        mock_step = MagicMock()
        mock_step.tool_id = "jira.create_ticket"
        # Force timeout triggers ToolTimeoutError in ToolExecutor
        mock_step.inputs = {"force_timeout": True}
        mock_plan = MagicMock()
        mock_plan.execution_plan = MagicMock()
        mock_plan.execution_plan.steps = [mock_step]
        mock_plan.confirmation_flag = False
        mock_planner.create_plan.return_value = MagicMock(
            workflow_id="wf123",
            execution_plan=mock_plan.execution_plan,
            confirmation_flag=False,
        )
        orchestrator = WorkflowOrchestrator(planner=mock_planner)
        result = orchestrator.run_workflow("dummy", user_id="u1")
        assert result["final_state"] == "AUDITED"
        assert "error" in result

# ---------------------------------------------------------------------------
# Verification failure path
# ---------------------------------------------------------------------------
def test_verification_failure():
    # Force verification to return a result with verified=False
    with patch.object(WorkflowOrchestrator, "verification_agent") as mock_verif:
        mock_verif.verify.return_value = MagicMock(verified=False)
        orchestrator = WorkflowOrchestrator(verification_agent=mock_verif)
        result = orchestrator.run_workflow(JIRA_REQUEST, user_id="u1", confirmation_decision="approve")
        assert result["final_state"] == "AUDITED"
        assert "error" in result

# ---------------------------------------------------------------------------
# Audit record creation is exercised in all paths; we assert the audit_id exists
# ---------------------------------------------------------------------------
def test_audit_record_created():
    orchestrator = WorkflowOrchestrator()
    result = orchestrator.run_workflow("Summarize today's meeting", user_id="u2")
    assert "audit_id" in result

# ---------------------------------------------------------------------------
# Invalid confirmation decision raises an error
# ---------------------------------------------------------------------------
def test_invalid_confirmation_decision():
    orchestrator = WorkflowOrchestrator()
    with pytest.raises(InvalidConfirmationDecisionError):
        orchestrator.run_workflow("Create ticket", user_id="u3", confirmation_decision="unknown")

# ---------------------------------------------------------------------------
# Invalid state transition – simulate by patching state_machine.transition to raise
# ---------------------------------------------------------------------------
def test_invalid_state_transition():
    with patch.object(WorkflowOrchestrator, "state_machine") as mock_sm:
        mock_sm.transition.side_effect = Exception("bad transition")
        orchestrator = WorkflowOrchestrator(state_machine=mock_sm)
        with pytest.raises(WorkflowOrchestratorStateError):
            orchestrator.run_workflow("Create ticket", user_id="u4")

# ---------------------------------------------------------------------------
# Rollback path is exercised when any step fails; we assert the final state is AUDITED and
# the error is reported.
# ---------------------------------------------------------------------------
def test_rollback_path_on_planner_error():
    with patch.object(WorkflowOrchestrator, "planner") as mock_planner:
        mock_planner.create_plan.side_effect = Exception("planner exploded")
        orchestrator = WorkflowOrchestrator(planner=mock_planner)
        result = orchestrator.run_workflow("Create ticket", user_id="u5")
        assert result["final_state"] == "AUDITED"
        assert "error" in result
