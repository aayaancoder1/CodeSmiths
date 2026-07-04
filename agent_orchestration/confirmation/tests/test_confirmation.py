import unittest
from agent_orchestration.confirmation.confirmation_manager import ConfirmationManager
from agent_orchestration.confirmation.confirmation_models import ConfirmationState
from agent_orchestration.confirmation.confirmation_errors import (
    DuplicateConfirmationError,
    InvalidConfirmationStateError,
    MissingDecisionError,
    ConfirmationTimeoutError,
)


class TestConfirmationManager(unittest.TestCase):
    def setUp(self):
        self.manager = ConfirmationManager()
        self.wf_id = "wf-001"
        self.plan = "Create Jira ticket"
        self.manager.request_confirmation(self.wf_id, self.plan)

    def test_approve(self):
        result = self.manager.approve(self.wf_id, reason="All good")
        self.assertEqual(result.confirmation_status, ConfirmationState.APPROVED)
        self.assertTrue(result.approved)
        self.assertEqual(self.manager.get_state(self.wf_id), ConfirmationState.APPROVED)

    def test_reject(self):
        result = self.manager.reject(self.wf_id, reason="Not needed")
        self.assertEqual(result.confirmation_status, ConfirmationState.REJECTED)
        self.assertFalse(result.approved)
        self.assertEqual(self.manager.get_state(self.wf_id), ConfirmationState.REJECTED)

    def test_cancel(self):
        result = self.manager.cancel(self.wf_id, reason="User cancelled")
        self.assertEqual(result.confirmation_status, ConfirmationState.CANCELLED)
        self.assertFalse(result.approved)
        self.assertEqual(self.manager.get_state(self.wf_id), ConfirmationState.CANCELLED)

    def test_timeout_raises_error(self):
        with self.assertRaises(ConfirmationTimeoutError):
            self.manager.timeout(self.wf_id, reason="No response")
        # After timeout, state should be TIMED_OUT
        self.assertEqual(self.manager.get_state(self.wf_id), ConfirmationState.TIMED_OUT)

    def test_duplicate_confirmation_request(self):
        with self.assertRaises(DuplicateConfirmationError):
            self.manager.request_confirmation(self.wf_id, "Another plan")

    def test_invalid_workflow_without_request(self):
        with self.assertRaises(InvalidConfirmationStateError):
            self.manager.approve("nonexistent", reason="test")

    def test_missing_workflow_id(self):
        with self.assertRaises(MissingDecisionError):
            self.manager.request_confirmation("", self.plan)
        with self.assertRaises(MissingDecisionError):
            self.manager.request_confirmation("wf2", "")

    def test_decision_after_final_state(self):
        self.manager.approve(self.wf_id)
        with self.assertRaises(InvalidConfirmationStateError):
            self.manager.reject(self.wf_id)

if __name__ == "__main__":
    unittest.main()
