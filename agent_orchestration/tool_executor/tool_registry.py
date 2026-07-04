from typing import Dict
from agent_orchestration.tool_executor.tool_interfaces import ToolAdapter
from agent_orchestration.tool_executor.tool_errors import UnknownToolError
from agent_orchestration.tool_executor.tool_adapters import (
    JiraCreateTicketAdapter,
    DocumentCreateAdapter,
    EmailSendAdapter,
    MeetingSummarizeAdapter
)

class ToolRegistry:
    """
    Registry for managing and resolving tool adapters by tool_id.
    """

    def __init__(self):
        self._registry: Dict[str, ToolAdapter] = {}
        self._register_default_tools()

    def register(self, tool_id: str, adapter: ToolAdapter) -> None:
        """
        Registers a tool adapter associated with a tool_id.
        """
        self._registry[tool_id] = adapter

    def get(self, tool_id: str) -> ToolAdapter:
        """
        Resolves and returns the tool adapter for tool_id.
        Raises UnknownToolError if tool_id is not registered.
        """
        if tool_id not in self._registry:
            raise UnknownToolError(f"Tool {tool_id} is not registered in the Tool Registry.")
        return self._registry[tool_id]

    def _register_default_tools(self) -> None:
        """
        Registers default mock adapters.
        """
        self.register("jira.create_ticket", JiraCreateTicketAdapter())
        self.register("document.create", DocumentCreateAdapter())
        self.register("email.send", EmailSendAdapter())
        self.register("meeting.summarize", MeetingSummarizeAdapter())
