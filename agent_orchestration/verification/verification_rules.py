from typing import Any, Dict
from agent_orchestration.verification.verification_interfaces import VerificationRule
from agent_orchestration.verification.verification_errors import (
    VerificationFailedError,
    InvalidExecutionResultError,
    SchemaMismatchError,
    MissingFieldError
)

class ExecutionStatusSuccessRule(VerificationRule):
    """Checks that the tool execution status was SUCCESS."""
    
    def validate(self, result: Any) -> bool:
        if not hasattr(result, "execution_status"):
            raise InvalidExecutionResultError("Result is missing 'execution_status' attribute.")
        if result.execution_status != "SUCCESS":
            raise VerificationFailedError(
                f"Execution failed with status: {result.execution_status}. Message: {getattr(result, 'error_message', '')}"
            )
        return True

    def get_rule_name(self) -> str:
        return "ExecutionStatusSuccessRule"

    def get_description(self) -> str:
        return "Ensures that the execution status of the tool is SUCCESS."


class PayloadExistsRule(VerificationRule):
    """Checks that the result payload exists and is not None."""
    
    def validate(self, result: Any) -> bool:
        if not hasattr(result, "result_payload"):
            raise InvalidExecutionResultError("Result is missing 'result_payload' attribute.")
        if result.result_payload is None:
            raise MissingFieldError("The execution result payload is missing (None).")
        if not isinstance(result.result_payload, dict):
            raise SchemaMismatchError("The execution result payload must be a dictionary.")
        return True

    def get_rule_name(self) -> str:
        return "PayloadExistsRule"

    def get_description(self) -> str:
        return "Ensures the result payload is a non-None dictionary."


class SchemaValidationRule(VerificationRule):
    """Validates the payload against predefined schemas for each tool."""

    # Schema mapping: tool_id -> {field_name: expected_type}
    EXPECTED_SCHEMAS: Dict[str, Dict[str, type]] = {
        "jira.create_ticket": {
            "ticket_id": str,
            "status": str
        },
        "document.create": {
            "document_id": str,
            "status": str
        },
        "email.send": {
            "email_id": str,
            "status": str
        },
        "meeting.summarize": {
            "summary_id": str,
            "status": str,
            "summary": str
        }
    }

    def validate(self, result: Any) -> bool:
        if not hasattr(result, "tool_id"):
            raise InvalidExecutionResultError("Result is missing 'tool_id' attribute.")
        
        tool_id = result.tool_id
        payload = result.result_payload

        if tool_id not in self.EXPECTED_SCHEMAS:
            # If the tool has no defined schema check in verification, we skip schema validation
            return True

        expected_schema = self.EXPECTED_SCHEMAS[tool_id]
        for field, expected_type in expected_schema.items():
            if field not in payload:
                raise MissingFieldError(f"Required field '{field}' is missing from payload for tool '{tool_id}'.")
            if not isinstance(payload[field], expected_type):
                raise SchemaMismatchError(
                    f"Field '{field}' in payload for tool '{tool_id}' has incorrect type. "
                    f"Expected {expected_type.__name__}, got {type(payload[field]).__name__}."
                )
        return True

    def get_rule_name(self) -> str:
        return "SchemaValidationRule"

    def get_description(self) -> str:
        return "Enforces schema conformity (presence and types of fields) per tool adapter."
