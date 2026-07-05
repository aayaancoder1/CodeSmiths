from typing import Dict, Any
from agent_orchestration.tool_executor.tool_interfaces import ToolAdapter

class JiraCreateTicketAdapter(ToolAdapter):
    """
    Mock adapter for 'jira.create_ticket'.
    """

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        # Validate first
        if not self.validate_input(inputs):
            raise ValueError("Invalid inputs for JiraCreateTicketAdapter")
        
        # Simulating potential mock failures/timeouts for testing
        if inputs.get("force_failure"):
            raise RuntimeError("Mock execution failure in Jira Adapter")

        return {
            "ticket_id": "JIRA-1001",
            "status": "created",
            "summary": inputs.get("summary", "Database connection outage ticket")
        }

    def validate_input(self, inputs: Dict[str, Any]) -> bool:
        # Require some request_context or summary
        return isinstance(inputs, dict)

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": "Jira Ticket Creator",
            "description": "Mock tool to create JIRA tickets",
            "required_inputs": []
        }

class DocumentCreateAdapter(ToolAdapter):
    """
    Mock adapter for 'document.create'.
    """

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_input(inputs):
            raise ValueError("Invalid inputs for DocumentCreateAdapter")
        
        if inputs.get("force_failure"):
            raise RuntimeError("Mock execution failure in Document Adapter")

        return {
            "document_id": "DOC-2026",
            "status": "drafted",
            "title": inputs.get("title", "Draft Document")
        }

    def validate_input(self, inputs: Dict[str, Any]) -> bool:
        return isinstance(inputs, dict)

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": "Document Creator",
            "description": "Mock tool to create docs",
            "required_inputs": []
        }

class EmailSendAdapter(ToolAdapter):
    """
    Mock adapter for 'email.send'.
    """

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_input(inputs):
            raise ValueError("Invalid inputs for EmailSendAdapter")
        
        if inputs.get("force_failure"):
            raise RuntimeError("Mock execution failure in Email Adapter")

        return {
            "email_id": "MSG-9988",
            "status": "sent",
            "recipient": inputs.get("recipient", "approvals@company.com")
        }

    def validate_input(self, inputs: Dict[str, Any]) -> bool:
        return isinstance(inputs, dict)

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": "Email Sender",
            "description": "Mock tool to send approval emails",
            "required_inputs": []
        }

class MeetingSummarizeAdapter(ToolAdapter):
    """
    Mock adapter for 'meeting.summarize'.
    """

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        if not self.validate_input(inputs):
            raise ValueError("Invalid inputs for MeetingSummarizeAdapter")
        
        if inputs.get("force_failure"):
            raise RuntimeError("Mock execution failure in Summary Adapter")

        return {
            "summary_id": "SUM-456",
            "status": "completed",
            "summary": "Deterministic meeting summary."
        }

    def validate_input(self, inputs: Dict[str, Any]) -> bool:
        return isinstance(inputs, dict)

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": "Meeting Summarizer",
            "description": "Mock tool to summarize meeting transcripts",
            "required_inputs": []
        }
