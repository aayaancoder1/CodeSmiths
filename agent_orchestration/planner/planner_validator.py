from typing import Set
from agent_orchestration.planner.planner_errors import (
    EmptyRequestError,
    InvalidRequestError,
    InvalidPlanError,
    MissingToolError
)
from agent_orchestration.planner.planner_models import ExecutionPlan
from agent_orchestration.planner.planner_schema import SUPPORTED_TOOLS

class PlannerValidator:
    """
    Validates incoming planner requests and constructed execution plans.
    """

    @staticmethod
    def validate_request(request: str) -> None:
        """
        Validates the incoming user request.
        """
        if request is None:
            raise InvalidRequestError("Request cannot be None.")
        if not isinstance(request, str):
            raise InvalidRequestError("Request must be a string.")
        
        stripped = request.strip()
        if not stripped:
            raise EmptyRequestError("Request cannot be empty or only whitespace.")

    @staticmethod
    def validate_plan(plan: ExecutionPlan) -> bool:
        """
        Validates the structure and soundness of the generated execution plan.
        Raises InvalidPlanError or MissingToolError if invalid.
        """
        if not plan.workflow_id:
            raise InvalidPlanError("Plan is missing a workflow ID.")
        if not plan.goal:
            raise InvalidPlanError("Plan is missing a goal description.")
        if not plan.steps:
            raise InvalidPlanError("Plan must contain at least one step.")

        task_ids = set()
        for step in plan.steps:
            if not step.task_id:
                raise InvalidPlanError("A task step is missing its task_id.")
            if step.task_id in task_ids:
                raise InvalidPlanError(f"Duplicate task ID found: {step.task_id}")
            task_ids.add(step.task_id)

            # Ensure referenced tools are in supported registry
            if step.tool_id not in SUPPORTED_TOOLS:
                raise MissingToolError(f"Tool {step.tool_id} required by task {step.task_id} is not supported.")

        # Check dependencies exist and are acyclic
        # First, ensure all dependencies refer to tasks present in the plan
        for step in plan.steps:
            for dep in step.dependencies:
                if dep not in task_ids:
                    raise InvalidPlanError(f"Task {step.task_id} has invalid dependency: {dep}")

        # Check for circular dependency using DFS
        visited = {} # task_id -> state (0 = unvisited, 1 = visiting, 2 = visited)
        
        # Build adjacency graph
        adj = {step.task_id: step.dependencies for step in plan.steps}

        def has_cycle(u: str) -> bool:
            visited[u] = 1 # visiting
            for v in adj.get(u, []):
                if visited.get(v, 0) == 1:
                    return True
                if visited.get(v, 0) == 0:
                    if has_cycle(v):
                        return True
            visited[u] = 2 # visited
            return False

        for task_id in task_ids:
            if visited.get(task_id, 0) == 0:
                if has_cycle(task_id):
                    raise InvalidPlanError("Circular dependency detected in execution plan task graph.")

        return True
