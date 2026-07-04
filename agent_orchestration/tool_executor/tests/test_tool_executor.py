import unittest
from agent_orchestration.tool_executor.tool_executor import ToolExecutor
from agent_orchestration.tool_executor.tool_registry import ToolRegistry
from agent_orchestration.tool_executor.tool_models import ToolStatus
from agent_orchestration.tool_executor.tool_errors import (
    UnknownToolError,
    InvalidExecutionPlanError
)
from agent_orchestration.tool_executor.tool_adapters import JiraCreateTicketAdapter

# Dummy class structure to mimic ExecutionPlan for testing
class DummyStep:
    def __init__(self, task_id, tool_id, inputs=None):
        self.task_id = task_id
        self.tool_id = tool_id
        self.inputs = inputs or {}

class DummyPlan:
    def __init__(self, workflow_id, steps):
        self.workflow_id = workflow_id
        self.steps = steps

class TestToolExecutor(unittest.TestCase):

    def setUp(self):
        self.registry = ToolRegistry()
        self.executor = ToolExecutor(self.registry)

    def test_tool_registration_and_lookup(self):
        custom_adapter = JiraCreateTicketAdapter()
        self.registry.register("custom.tool", custom_adapter)
        
        resolved = self.registry.get("custom.tool")
        self.assertEqual(resolved, custom_adapter)

    def test_unknown_tool_lookup_raises_error(self):
        with self.assertRaises(UnknownToolError):
            self.registry.get("nonexistent.tool")

    def test_successful_execution(self):
        step1 = DummyStep("task_1", "jira.create_ticket", {"summary": "Critical DB Outage"})
        plan = DummyPlan("wf-test-123", [step1])
        
        results = self.executor.execute(plan)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].tool_id, "jira.create_ticket")
        self.assertEqual(results[0].execution_status, ToolStatus.SUCCESS)
        self.assertEqual(results[0].result_payload["ticket_id"], "JIRA-1001")
        self.assertTrue(results[0].execution_time >= 0)

    def test_unknown_tool_in_plan_raises_error(self):
        step1 = DummyStep("task_1", "nonexistent.tool")
        plan = DummyPlan("wf-test-abc", [step1])
        
        with self.assertRaises(UnknownToolError):
            self.executor.execute(plan)

    def test_invalid_plan_structure_raises_error(self):
        with self.assertRaises(InvalidExecutionPlanError):
            self.executor.execute(None)
            
        with self.assertRaises(InvalidExecutionPlanError):
            self.executor.execute(DummyPlan("wf-123", [object()])) # Step missing tool_id/task_id

    def test_execution_failure_scenario(self):
        step1 = DummyStep("task_1", "email.send", {"force_failure": True})
        plan = DummyPlan("wf-fail", [step1])
        
        results = self.executor.execute(plan)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].execution_status, ToolStatus.FAILED)
        self.assertIn("Mock execution failure", results[0].error_message)

    def test_timeout_scenario(self):
        step1 = DummyStep("task_1", "meeting.summarize", {"force_timeout": True})
        plan = DummyPlan("wf-timeout", [step1])
        
        results = self.executor.execute(plan)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].execution_status, ToolStatus.TIMEOUT)
        self.assertIn("timed out", results[0].error_message)

if __name__ == "__main__":
    unittest.main()
