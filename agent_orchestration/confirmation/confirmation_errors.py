class ConfirmationError(Exception):
    """Base class for all confirmation related errors."""
    pass


class ConfirmationTimeoutError(ConfirmationError):
    """Raised when a confirmation request times out without a decision."""
    pass


class InvalidConfirmationStateError(ConfirmationError):
    """Raised when an invalid state transition is attempted."""
    pass


class DuplicateConfirmationError(ConfirmationError):
    """Raised when a confirmation is attempted more than once for the same workflow."""
    pass


class MissingDecisionError(ConfirmationError):
    """Raised when a confirmation request is missing a required decision."""
    pass
