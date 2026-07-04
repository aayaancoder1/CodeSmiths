import time
from typing import List, Dict, Any
from agent_orchestration.tool_executor.tool_registry import ToolRegistry
from agent_orchestration.tool_executor.tool_models import ExecutionResult, ToolStatus
from agent_orchestration.tool_executor.tool_errors import (
    UnknownToolError,
    InvalidExecutionPlanError,
    ExecutionFailureError,
    ToolTimeoutError
)

class ToolExecutor:
    """
    Executes tools referenced in an ExecutionPlan.
    """

    def __init__(self, registry: ToolRegistry = None):
        self.registry = registry or ToolRegistry()

    def execute(self, plan: Any) -> List[ExecutionResult]:
        """
        Executes all task steps defined in the ExecutionPlan.
        """
        # Validate plan structure duck-typing style or model validation
        if not plan or not hasattr(plan, "steps") or not hasattr(plan, "workflow_id"):
            raise InvalidExecutionPlanError("Execution plan is missing required fields.")

        results = []

        for step in plan.steps:
            if not hasattr(step, "tool_id") or not hasattr(step, "task_id"):
                raise InvalidExecutionPlanError("Task step is missing tool_id or task_id.")

            # Validate input context
            inputs = getattr(step, "inputs", {})
            
            start_time = time.perf_counter()
            status = ToolStatus.SUCCESS
            payload = {}
            error_msg = None

            try:
                # 1. Look up tool in registry
                tool = self.registry.get(step.tool_id)

                # 2. Simulate timeout if requested
                if inputs.get("force_timeout"):
                    raise ToolTimeoutError(f"Execution of tool {step.tool_id} timed out.")

                # 3. Validate inputs on tool adapter
                if not tool.validate_input(inputs):
                    raise ExecutionFailureError(f"Validation failed for tool {step.tool_id} with inputs {inputs}")

                # 4. Execute tool adapter
                payload = tool.execute(inputs)

            except UnknownToolError as e:
                status = ToolStatus.FAILED
                error_msg = str(e)
                # Re-raise or capture? The task description says "Handle only Unknown Tool ... Return structured errors only."
                # We will capture it as a FAILED status and also support raising if desired, but returning structured results is best.
                # Let's raise the specific error to match "Return structured errors only" when appropriate, or return a FAILED execution result.
                # Let's raise it to align with strict error handling guidelines if it's an unrecognized tool or plan error.
                raise e
            except ToolTimeoutError as e:
                status = ToolStatus.TIMEOUT
                error_msg = str(e)
            except Exception as e:
                status = ToolStatus.FAILED
                error_msg = str(e)

            end_time = time.perf_counter()
            execution_time = end_time - start_time

            result = ExecutionResult(
                workflow_id=plan.workflow_id,
                tool_id=step.tool_id,
                execution_status=status,
                execution_time=execution_time,
                result_payload=payload,
                error_message=error_msg
            )
            results.append(result)

            # Stop executing subsequent tasks if one fails
            if status != ToolStatus.SUCCESS:
                break

        return results
