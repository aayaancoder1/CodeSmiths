import time
from typing import List, Any
from agent_orchestration.verification.verification_interfaces import VerificationRule
from agent_orchestration.verification.verification_models import VerificationResult
from agent_orchestration.verification.verification_rules import (
    ExecutionStatusSuccessRule,
    PayloadExistsRule,
    SchemaValidationRule
)
from agent_orchestration.verification.verification_errors import VerificationError

class VerificationAgent:
    """
    Orchestrates deterministic validation on execution results.
    """

    def __init__(self, rules: List[VerificationRule] = None):
        self.rules = rules if rules is not None else [
            ExecutionStatusSuccessRule(),
            PayloadExistsRule(),
            SchemaValidationRule()
        ]

    def verify(self, result: Any) -> VerificationResult:
        """
        Runs all verification rules against the tool ExecutionResult.
        """
        # Validate that result is not None
        if result is None:
            from agent_orchestration.verification.verification_errors import InvalidExecutionResultError
            raise InvalidExecutionResultError("Execution result cannot be None.")

        start_time = time.perf_counter()
        verified = True
        status = "VERIFIED"
        message = "Verification succeeded. All rules passed."
        failure_reason = None

        workflow_id = getattr(result, "workflow_id", "unknown")
        tool_id = getattr(result, "tool_id", "unknown")

        try:
            for rule in self.rules:
                rule.validate(result)
        except VerificationError as e:
            verified = False
            status = "FAILED"
            message = f"Verification failed on rule: {e.__class__.__name__}"
            failure_reason = str(e)
            # Re-raise the structured error as requested by error handling contract
            raise e

        end_time = time.perf_counter()
        verification_time = end_time - start_time

        return VerificationResult(
            workflow_id=workflow_id,
            tool_id=tool_id,
            verified=verified,
            verification_status=status,
            verification_message=message,
            verification_time=verification_time,
            failure_reason=failure_reason
        )
