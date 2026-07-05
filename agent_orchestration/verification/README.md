# Verification Agent

The Verification Agent is responsible for performing deterministic post-execution checks on the output (ExecutionResult) of the Tool Executor.

## Responsibilities

- **Deterministic Rule Checks**: No AI inference or LLM processing. Validates output structure, schema types, and execution status.
- **VerificationRules**: Extendable rule interface exposing `validate()`, `get_rule_name()`, and `get_description()`.
- **Result Packaging**: Compiles a `VerificationResult` with status, message, verification time, and failure reasons.

## Verification Pipeline

1. **Status Success**: Ensures status is `SUCCESS`.
2. **Payload Exists**: Verifies a valid dictionary payload is present.
3. **Schema Compliance**: Evaluates target fields and types per tool (e.g. `ticket_id` for Jira, `document_id` for Doc).

## Usage

```python
from agent_orchestration.verification.verification_agent import VerificationAgent

verifier = VerificationAgent()
try:
    verification_result = verifier.verify(execution_result)
    print(verification_result.verified)
except VerificationError as e:
    print(f"Failed verification: {e}")
```
