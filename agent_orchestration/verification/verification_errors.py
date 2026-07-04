class VerificationError(Exception):
    """Base exception for all Verification Agent errors."""
    pass

class VerificationFailedError(VerificationError):
    """Raised when verification process as a whole fails."""
    pass

class InvalidExecutionResultError(VerificationError):
    """Raised when the execution result itself is invalid or malformed."""
    pass

class SchemaMismatchError(VerificationError):
    """Raised when the payload schema does not match the expected structure."""
    pass

class MissingFieldError(VerificationError):
    """Raised when a required field is missing from the result payload."""
    pass
