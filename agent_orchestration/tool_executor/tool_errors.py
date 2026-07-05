class ToolExecutorError(Exception):
    """Base exception for all Tool Executor Agent errors."""
    pass

class UnknownToolError(ToolExecutorError):
    """Raised when the requested tool_id is not registered in the Tool Registry."""
    pass

class InvalidExecutionPlanError(ToolExecutorError):
    """Raised when the execution plan is malformed or invalid."""
    pass

class ExecutionFailureError(ToolExecutorError):
    """Raised when a tool adapter execution fails or returns an error."""
    pass

class ToolTimeoutError(ToolExecutorError):
    """Raised when a tool execution exceeds its allowed duration."""
    pass
