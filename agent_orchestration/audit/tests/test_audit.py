import unittest
from agent_orchestration.audit.audit_agent import AuditAgent
from agent_orchestration.audit.audit_storage import InMemoryAuditStorage
from agent_orchestration.audit.audit_errors import (
    DuplicateAuditRecordError,
    MissingAuditFieldError,
    InvalidAuditRecordError,
    AuditStorageError
)

class TestAuditAgent(unittest.TestCase):

    def setUp(self):
        self.storage = InMemoryAuditStorage()
        self.agent = AuditAgent(self.storage)
        self.valid_payload = {
            "audit_id": "aud-1",
            "workflow_id": "wf-1",
            "request_id": "req-1",
            "user_id": "usr-1",
            "tool_id": "jira.create_ticket",
            "workflow_state": "AUDITED",
            "execution_status": "SUCCESS",
            "verification_status": "VERIFIED",
            "confirmation_status": "CONFIRMED",
            "timestamp": "2026-07-04T12:00:00Z",
            "execution_duration": 0.5,
            "metadata": {}
        }

    def test_record_creation_and_retrieval(self):
        record = self.agent.record_event(self.valid_payload)
        
        self.assertEqual(record.audit_id, "aud-1")
        self.assertEqual(record.workflow_id, "wf-1")
        self.assertEqual(record.execution_duration, 0.5)

        # Retrieve
        retrieved = self.agent.get_audit_log("aud-1")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.audit_id, "aud-1")

    def test_duplicate_record_raises_error(self):
        self.agent.record_event(self.valid_payload)
        
        with self.assertRaises(DuplicateAuditRecordError):
            self.agent.record_event(self.valid_payload)

    def test_missing_required_fields(self):
        payload = self.valid_payload.copy()
        del payload["user_id"]
        
        with self.assertRaises(MissingAuditFieldError):
            self.agent.record_event(payload)

    def test_prohibited_sensitive_fields_in_top_level(self):
        payload = self.valid_payload.copy()
        payload["chat_history"] = "User: Create a ticket. Agent: Okay."
        
        with self.assertRaises(InvalidAuditRecordError):
            self.agent.record_event(payload)

    def test_prohibited_sensitive_fields_in_metadata(self):
        payload = self.valid_payload.copy()
        payload["metadata"] = {"document_content": "Sensitive business info"}
        
        with self.assertRaises(InvalidAuditRecordError):
            self.agent.record_event(payload)

    def test_storage_failure_get_nonexistent(self):
        retrieved = self.agent.get_audit_log("nonexistent-id")
        self.assertIsNone(retrieved)

        with self.assertRaises(AuditStorageError):
            self.storage.get("nonexistent-id")

    def test_immutability_of_stored_records(self):
        record = self.agent.record_event(self.valid_payload)
        
        # Modify the local returned object or metadata
        record.metadata["modified_key"] = "hack"
        record.workflow_state = "COMPROMISED"

        # Fetch from storage again
        fetched = self.agent.get_audit_log("aud-1")
        self.assertEqual(fetched.workflow_state, "AUDITED")
        self.assertNotIn("modified_key", fetched.metadata)

        # Ensure we can't save directly back to storage to overwrite
        with self.assertRaises(DuplicateAuditRecordError):
            self.storage.save(record)

if __name__ == "__main__":
    unittest.main()
