class PlannerError(Exception):
    """Base exception for all Planner Agent errors."""
    pass

class InvalidRequestError(PlannerError):
    """Raised when the request itself is malformed or invalid."""
    pass

class EmptyRequestError(PlannerError):
    """Raised when the request string is empty or only whitespace."""
    pass

class UnsupportedActionError(PlannerError):
    """Raised when the user request cannot be mapped to any supported workflows/actions."""
    pass

class MissingToolError(PlannerError):
    """Raised when a mapped workflow requires a tool that is not in the registry or config."""
    pass

class InvalidPlanError(PlannerError):
    """Raised when the generated plan fails structure or validation rules."""
    pass
