# Workflow Orchestrator

This module coordinates the end‑to‑end execution of a user request by invoking the already‑implemented agents:

- **Planner Agent** – creates a deterministic execution plan.
- **Confirmation Manager** – records a user decision when required.
- **Tool Executor** – runs the tools defined in the plan.
- **Verification Agent** – validates the execution results.
- **Audit Agent** – persists an immutable audit record.
- **Workflow State Machine** – guarantees that state transitions follow the allowed graph.

The orchestrator **does not** implement any business logic of the individual agents; it only drives the workflow, generates identifiers, and records the final audit event.

## Usage
```python
from agent_orchestration.orchestrator.workflow_orchestrator import WorkflowOrchestrator

orchestrator = WorkflowOrchestrator()
result = orchestrator.run_workflow(
    user_request="Create a Jira ticket",
    user_id="user-123",
    confirmation_decision="approve"  # or "reject", "cancel", "timeout"
)
print(result)
```

The returned dictionary contains at least:
- `workflow_id`
- `request_id`
- `final_state`
- `audit_id`
- Optional `error` information if something failed.

## Testing
Run the integration suite with:
```bash
python -m unittest discover -s agent_orchestration/orchestrator/tests
```

All tests are deterministic and rely only on in‑memory implementations.
