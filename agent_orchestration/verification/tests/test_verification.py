import unittest
from agent_orchestration.verification.verification_agent import VerificationAgent
from agent_orchestration.verification.verification_errors import (
    VerificationFailedError,
    InvalidExecutionResultError,
    SchemaMismatchError,
    MissingFieldError
)

# Mock execution result for testing
class DummyExecutionResult:
    def __init__(self, workflow_id, tool_id, execution_status, result_payload, error_message=None):
        self.workflow_id = workflow_id
        self.tool_id = tool_id
        self.execution_status = execution_status
        self.result_payload = result_payload
        self.error_message = error_message

class TestVerificationAgent(unittest.TestCase):

    def setUp(self):
        self.verifier = VerificationAgent()

    def test_successful_verification(self):
        result = DummyExecutionResult(
            workflow_id="wf-123",
            tool_id="jira.create_ticket",
            execution_status="SUCCESS",
            result_payload={"ticket_id": "JIRA-1001", "status": "created"}
        )
        
        verify_res = self.verifier.verify(result)
        self.assertTrue(verify_res.verified)
        self.assertEqual(verify_res.verification_status, "VERIFIED")
        self.assertEqual(verify_res.tool_id, "jira.create_ticket")

    def test_failed_execution_status(self):
        result = DummyExecutionResult(
            workflow_id="wf-123",
            tool_id="jira.create_ticket",
            execution_status="FAILED",
            result_payload={},
            error_message="Connection timed out"
        )
        
        with self.assertRaises(VerificationFailedError):
            self.verifier.verify(result)

    def test_missing_payload(self):
        result = DummyExecutionResult(
            workflow_id="wf-123",
            tool_id="jira.create_ticket",
            execution_status="SUCCESS",
            result_payload=None
        )
        
        with self.assertRaises(MissingFieldError):
            self.verifier.verify(result)

    def test_missing_required_fields(self):
        result = DummyExecutionResult(
            workflow_id="wf-123",
            tool_id="meeting.summarize",
            execution_status="SUCCESS",
            result_payload={"summary_id": "SUM-12"} # Missing 'summary' and 'status'
        )
        
        with self.assertRaises(MissingFieldError):
            self.verifier.verify(result)

    def test_schema_mismatch_type(self):
        result = DummyExecutionResult(
            workflow_id="wf-123",
            tool_id="document.create",
            execution_status="SUCCESS",
            result_payload={"document_id": 2026, "status": "drafted"} # document_id must be str
        )
        
        with self.assertRaises(SchemaMismatchError):
            self.verifier.verify(result)

    def test_invalid_execution_result_structure(self):
        with self.assertRaises(InvalidExecutionResultError):
            self.verifier.verify(None)

        # Missing payload attribute entirely
        class MalformedResult:
            workflow_id = "wf-123"
            tool_id = "document.create"
            execution_status = "SUCCESS"
            
        with self.assertRaises(InvalidExecutionResultError):
            self.verifier.verify(MalformedResult())

if __name__ == "__main__":
    unittest.main()
