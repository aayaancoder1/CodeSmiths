import unittest
from agent_orchestration.workflow.workflow_state_machine import WorkflowStateMachine
from agent_orchestration.workflow.workflow_models import WorkflowState
from agent_orchestration.workflow.workflow_errors import (
    InvalidStateTransitionError,
    UnknownWorkflowStateError,
    DuplicateTransitionError,
    InvalidWorkflowError
)

class TestWorkflowStateMachine(unittest.TestCase):

    def setUp(self):
        self.machine = WorkflowStateMachine()
        self.wf_id = "wf-test"

    def test_initial_state_is_pending(self):
        self.assertEqual(self.machine.current_state(self.wf_id), WorkflowState.PENDING)

    def test_success_path_transitions(self):
        # PENDING -> PLANNED
        self.machine.transition(self.wf_id, WorkflowState.PLANNED)
        self.assertEqual(self.machine.current_state(self.wf_id), WorkflowState.PLANNED)

        # PLANNED -> WAITING_CONFIRMATION
        self.machine.transition(self.wf_id, WorkflowState.WAITING_CONFIRMATION)
        self.assertEqual(self.machine.current_state(self.wf_id), WorkflowState.WAITING_CONFIRMATION)

        # WAITING_CONFIRMATION -> EXECUTING
        self.machine.transition(self.wf_id, WorkflowState.EXECUTING)
        self.assertEqual(self.machine.current_state(self.wf_id), WorkflowState.EXECUTING)

        # EXECUTING -> VERIFYING
        self.machine.transition(self.wf_id, WorkflowState.VERIFYING)
        self.assertEqual(self.machine.current_state(self.wf_id), WorkflowState.VERIFYING)

        # VERIFYING -> SUCCESS
        self.machine.transition(self.wf_id, WorkflowState.SUCCESS)
        self.assertEqual(self.machine.current_state(self.wf_id), WorkflowState.SUCCESS)

        # SUCCESS -> AUDITED (Terminal)
        self.machine.transition(self.wf_id, WorkflowState.AUDITED)
        self.assertEqual(self.machine.current_state(self.wf_id), WorkflowState.AUDITED)

    def test_rollback_path_transitions(self):
        # Transition to VERIFYING first
        self.machine.transition(self.wf_id, WorkflowState.PLANNED)
        self.machine.transition(self.wf_id, WorkflowState.WAITING_CONFIRMATION)
        self.machine.transition(self.wf_id, WorkflowState.EXECUTING)
        self.machine.transition(self.wf_id, WorkflowState.VERIFYING)

        # VERIFYING -> FAILED
        self.machine.transition(self.wf_id, WorkflowState.FAILED)
        self.assertEqual(self.machine.current_state(self.wf_id), WorkflowState.FAILED)

        # FAILED -> ROLLED_BACK
        self.machine.transition(self.wf_id, WorkflowState.ROLLED_BACK)
        self.assertEqual(self.machine.current_state(self.wf_id), WorkflowState.ROLLED_BACK)

        # ROLLED_BACK -> AUDITED (Terminal)
        self.machine.transition(self.wf_id, WorkflowState.AUDITED)
        self.assertEqual(self.machine.current_state(self.wf_id), WorkflowState.AUDITED)

    def test_invalid_transitions(self):
        # PENDING to WAITING_CONFIRMATION directly (skip PLANNED)
        with self.assertRaises(InvalidStateTransitionError):
            self.machine.transition(self.wf_id, WorkflowState.WAITING_CONFIRMATION)

        # Transition to PLANNED
        self.machine.transition(self.wf_id, WorkflowState.PLANNED)

        # PLANNED to SUCCESS directly (skip intermediate steps)
        with self.assertRaises(InvalidStateTransitionError):
            self.machine.transition(self.wf_id, WorkflowState.SUCCESS)

    def test_duplicate_transitions(self):
        # Initial is PENDING
        with self.assertRaises(DuplicateTransitionError):
            self.machine.transition(self.wf_id, WorkflowState.PENDING)

        self.machine.transition(self.wf_id, WorkflowState.PLANNED)
        with self.assertRaises(DuplicateTransitionError):
            self.machine.transition(self.wf_id, WorkflowState.PLANNED)

    def test_unknown_states(self):
        with self.assertRaises(UnknownWorkflowStateError):
            self.machine.transition(self.wf_id, "NONEXISTENT_STATE")

    def test_invalid_workflow_identifiers(self):
        with self.assertRaises(InvalidWorkflowError):
            self.machine.current_state("")
            
        with self.assertRaises(InvalidWorkflowError):
            self.machine.transition(None, WorkflowState.PLANNED)

    def test_terminal_audited_state_transition_fails(self):
        # Move all the way to AUDITED
        self.machine.transition(self.wf_id, WorkflowState.PLANNED)
        self.machine.transition(self.wf_id, WorkflowState.WAITING_CONFIRMATION)
        self.machine.transition(self.wf_id, WorkflowState.EXECUTING)
        self.machine.transition(self.wf_id, WorkflowState.VERIFYING)
        self.machine.transition(self.wf_id, WorkflowState.SUCCESS)
        self.machine.transition(self.wf_id, WorkflowState.AUDITED)

        # AUDITED is terminal, cannot transition to anything
        with self.assertRaises(InvalidStateTransitionError):
            self.machine.transition(self.wf_id, WorkflowState.PENDING)

if __name__ == "__main__":
    unittest.main()
