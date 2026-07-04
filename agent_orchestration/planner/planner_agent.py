import uuid
from typing import Dict, Any, List
from agent_orchestration.planner.planner_interfaces import IPlannerAgent
from agent_orchestration.planner.planner_errors import UnsupportedActionError
from agent_orchestration.planner.planner_models import TaskNode, ExecutionPlan, PlannerResult
from agent_orchestration.planner.planner_schema import WORKFLOW_TEMPLATES
from agent_orchestration.planner.planner_validator import PlannerValidator

class PlannerAgent(IPlannerAgent):
    """
    Deterministic Planner Agent that maps requests to predefined workflows.
    """

    def create_plan(self, request: str) -> PlannerResult:
        """
        Creates an execution plan from a user request deterministically.
        """
        # Validate request
        PlannerValidator.validate_request(request)

        # Match request to templates
        req_lower = request.lower()
        matched_template_key = None

        if "jira" in req_lower or "ticket" in req_lower:
            matched_template_key = "jira"
        elif "onboarding" in req_lower or "draft" in req_lower:
            matched_template_key = "onboarding"
        elif "summarize" in req_lower or "summary" in req_lower or "meeting" in req_lower:
            matched_template_key = "summarize"
        elif "email" in req_lower or "approval" in req_lower or "send" in req_lower:
            matched_template_key = "email"

        if not matched_template_key:
            raise UnsupportedActionError(
                f"Requested action in '{request}' is not supported by the predefined registry."
            )

        template = WORKFLOW_TEMPLATES[matched_template_key]

        # Generate a distinct workflow ID
        workflow_id = f"wf-{uuid.uuid4().hex[:8]}"

        # Construct TaskNodes
        steps = []
        for idx, step_data in enumerate(template["steps"]):
            # For testing/execution we can inject mock inputs depending on the request context
            inputs = {"request_context": request}
            task_node = TaskNode(
                task_id=step_data["task_id"],
                tool_id=step_data["tool_id"],
                dependencies=step_data["dependencies"],
                inputs=inputs,
                confirmation_required=step_data["confirmation_required"],
                description=step_data["description"]
            )
            steps.append(task_node)

        # Construct ExecutionPlan
        plan = ExecutionPlan(
            workflow_id=workflow_id,
            goal=template["goal"],
            steps=steps,
            confirmation_required=template["confirmation_required"],
            tool_requirements=template["tool_requirements"],
            expected_result=template["expected_result"],
            metadata={"template_key": matched_template_key}
        )

        # Validate the generated plan
        self.validate_plan(plan)

        # Build task graph (dependencies map)
        ordered_task_graph = self.build_task_graph(plan)

        # Determine estimated execution order (topological sort of task graph)
        estimated_execution_order = self._topological_sort(plan.steps)

        return PlannerResult(
            workflow_id=workflow_id,
            execution_plan=plan,
            ordered_task_graph=ordered_task_graph,
            confirmation_flag=plan.confirmation_required,
            tool_requirements=plan.tool_requirements,
            estimated_execution_order=estimated_execution_order
        )

    def validate_plan(self, plan: ExecutionPlan) -> bool:
        """
        Validates the structure and soundness of the generated execution plan.
        """
        return PlannerValidator.validate_plan(plan)

    def build_task_graph(self, plan: ExecutionPlan) -> Dict[str, List[str]]:
        """
        Builds an ordered task graph (adjacency list representing execution flows) from the execution plan.
        Key indicates the task, list indicates tasks that depend on it.
        """
        graph: Dict[str, List[str]] = {step.task_id: [] for step in plan.steps}
        for step in plan.steps:
            for dep in step.dependencies:
                if dep in graph:
                    graph[dep].append(step.task_id)
        return graph

    def _topological_sort(self, steps: List[TaskNode]) -> List[str]:
        """
        Performs a topological sort on task nodes to determine estimated execution order.
        """
        in_degree = {step.task_id: 0 for step in steps}
        adj = {step.task_id: [] for step in steps}

        for step in steps:
            for dep in step.dependencies:
                # dep must execute before step, so dep -> step is the directed edge
                if dep in adj:
                    adj[dep].append(step.task_id)
                    in_degree[step.task_id] += 1

        # Queue nodes with no dependencies (in_degree = 0)
        queue = [task_id for task_id, deg in in_degree.items() if deg == 0]
        # Keep it sorted to ensure deterministic order if there are multiple independent tasks
        queue.sort()

        order = []
        while queue:
            curr = queue.pop(0)
            order.append(curr)
            for neighbor in adj[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
            # Re-sort to maintain deterministic behavior when neighbors are added
            queue.sort()

        return order
