import unittest
from agent_orchestration.planner.planner_agent import PlannerAgent
from agent_orchestration.planner.planner_errors import (
    EmptyRequestError,
    InvalidRequestError,
    UnsupportedActionError,
    InvalidPlanError
)
from agent_orchestration.planner.planner_models import ExecutionPlan, TaskNode
from agent_orchestration.planner.planner_validator import PlannerValidator

class TestPlannerAgent(unittest.TestCase):

    def test_planner_successful_jira_plan(self):
        planner = PlannerAgent()
        result = planner.create_plan("Create a Jira ticket for payment outage.")
        
        self.assertTrue(result.workflow_id.startswith("wf-"))
        self.assertTrue(result.confirmation_flag)
        self.assertIn("jira.create_ticket", result.tool_requirements)
        self.assertIn("retrieval.search_kb", result.tool_requirements)
        self.assertEqual(
            result.estimated_execution_order,
            ["retrieve_context", "create_ticket", "log_audit"]
        )

    def test_planner_successful_summarize_plan(self):
        planner = PlannerAgent()
        result = planner.create_plan("Summarize today's meeting on payments.")
        
        self.assertTrue(result.workflow_id.startswith("wf-"))
        self.assertFalse(result.confirmation_flag)
        self.assertEqual(
            result.estimated_execution_order,
            ["get_transcript", "generate_summary", "log_audit"]
        )

    def test_planner_empty_request(self):
        planner = PlannerAgent()
        with self.assertRaises(EmptyRequestError):
            planner.create_plan("   ")

    def test_planner_none_request(self):
        planner = PlannerAgent()
        with self.assertRaises(InvalidRequestError):
            planner.create_plan(None)

    def test_planner_unsupported_action(self):
        planner = PlannerAgent()
        with self.assertRaises(UnsupportedActionError):
            planner.create_plan("Deploy code to production.")

    def test_validator_circular_dependency(self):
        # Construct invalid plan with cycle
        task1 = TaskNode(
            task_id="task_1",
            tool_id="retrieval.search_kb",
            dependencies=["task_2"],
            description="First task"
        )
        task2 = TaskNode(
            task_id="task_2",
            tool_id="audit.log_action",
            dependencies=["task_1"],
            description="Second task"
        )
        
        plan = ExecutionPlan(
            workflow_id="wf-cycle",
            goal="Test cycle detection",
            steps=[task1, task2],
            confirmation_required=False,
            tool_requirements=["retrieval.search_kb", "audit.log_action"],
            expected_result="Will fail"
        )
        
        with self.assertRaises(InvalidPlanError):
            PlannerValidator.validate_plan(plan)

    def test_validator_missing_dependency(self):
        task1 = TaskNode(
            task_id="task_1",
            tool_id="retrieval.search_kb",
            dependencies=["non_existent_task"],
            description="Task referencing missing dependency"
        )
        
        plan = ExecutionPlan(
            workflow_id="wf-missing",
            goal="Test missing dependency",
            steps=[task1],
            confirmation_required=False,
            tool_requirements=["retrieval.search_kb"],
            expected_result="Will fail"
        )
        
        with self.assertRaises(InvalidPlanError):
            PlannerValidator.validate_plan(plan)

if __name__ == "__main__":
    unittest.main()
