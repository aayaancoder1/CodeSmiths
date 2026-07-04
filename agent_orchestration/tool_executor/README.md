# Tool Executor Agent

The Tool Executor Agent is responsible for receiving an `ExecutionPlan` from the Planner Agent, resolving the tools referenced in the steps via the `ToolRegistry`, and executing their respective `ToolAdapter`s.

## Responsibilities

- **Deterministic Tool Registry**: Resolves tools by unique `tool_id` string only.
- **Common Adapter Interface**: Every tool implements `execute()`, `validate_input()`, and `get_metadata()`.
- **Mock Execution**: Executes deterministic mock implementations for `jira.create_ticket`, `document.create`, `email.send`, and `meeting.summarize` without calling external services.
- **Result Packaging**: Compiles `ExecutionResult` including status, execution time, payload, and any errors.

## Supported Tools

- `jira.create_ticket`
- `document.create`
- `email.send`
- `meeting.summarize`

## Usage

```python
from agent_orchestration.tool_executor.tool_executor import ToolExecutor
from agent_orchestration.tool_executor.tool_registry import ToolRegistry

registry = ToolRegistry()
executor = ToolExecutor(registry)

# Execute an ExecutionPlan
results = executor.execute(plan)
for res in results:
    print(res.tool_id, res.execution_status, res.execution_time)
```
