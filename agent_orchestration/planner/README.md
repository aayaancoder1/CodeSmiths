# Planner Agent

The Planner Agent is the entry point for orchestrating workflows in the Enterprise AI Company Brain. It deterministically parses incoming user requests, validates them, and maps them to structural execution plans (task graphs) without executing any tools or invoking LLMs.

## Responsibilities

- **Validation**: Ensures requests are non-empty, valid strings, and conform to supported actions.
- **Predefined Registry Matching**: Deterministically matches requests to templates (e.g., Jira ticket creation, onboarding drafting, meeting summarization, sending approval email) based on patterns/keywords.
- **Task Graph Generation**: Constructs a dependency graph of steps (TaskNodes) indicating execution order and confirmation requirements.
- **Topological Sorting**: Resolves task dependencies to estimate a valid execution sequence.

## Component Structure

- `planner_agent.py`: Implementation of `PlannerAgent` containing graph construction and sorting.
- `planner_models.py`: Pydantic models (`TaskNode`, `WorkflowMetadata`, `ExecutionPlan`, `PlannerResult`).
- `planner_schema.py`: Registry configurations for tools and workflows.
- `planner_validator.py`: Static validation rules for plans and requests.
- `planner_interfaces.py`: Abstract Base Class definition (`IPlannerAgent`).
- `planner_errors.py`: Domain-specific exceptions (`UnsupportedActionError`, `InvalidRequestError`, etc.).

## Usage

```python
from agent_orchestration.planner.planner_agent import PlannerAgent

planner = PlannerAgent()
result = planner.create_plan("Create a Jira ticket for the database outage.")

print(result.workflow_id)
print(result.estimated_execution_order)
```
