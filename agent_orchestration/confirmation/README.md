# Confirmation System

The Confirmation System manages explicit user approval decisions for workflows that are in the **WAITING_CONFIRMATION** state. It provides a deterministic, in‑memory API that records decisions and validates state transitions.

## Components

- **confirmation_interfaces.py** – Abstract base class `IConfirmationManager` defining the public API.
- **confirmation_models.py** – Pydantic‑style data models:
  - `ConfirmationState` – Enum of allowed states.
  - `ConfirmationResult` – Result object returned after a decision.
- **confirmation_errors.py** – Domain specific exception hierarchy.
- **confirmation_validator.py** – Helper to validate enum values.
- **confirmation_manager.py** – Concrete implementation storing state in dictionaries.
- **tests/test_confirmation.py** – Unit tests exercising all success and error paths.

## Usage Example
```python
from agent_orchestration.confirmation.confirmation_manager import ConfirmationManager
from agent_orchestration.confirmation.confirmation_models import ConfirmationState

manager = ConfirmationManager()
manager.request_confirmation('wf-123', 'Create ticket in Jira')
result = manager.approve('wf-123', reason='All good')
print(result)
```

## Design Guarantees
- No external calls, databases, or side‑effects.
- Deterministic behaviour – the same inputs always produce the same outputs.
- Strict state machine: a workflow can only transition from `WAITING_CONFIRMATION` to one of the final states.
- Errors are raised for duplicate requests, invalid states, missing data, and timeouts.
