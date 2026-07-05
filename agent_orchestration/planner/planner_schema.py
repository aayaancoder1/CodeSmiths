from typing import Dict, Any, List

# Predefined tool registry identifiers
SUPPORTED_TOOLS = {
    "jira.create_ticket",
    "retrieval.search_kb",
    "doc.draft_document",
    "transcript.get_today",
    "summary.generate",
    "email.send_approval",
    "audit.log_action"
}

# Mapping of keywords to predefined workflows
WORKFLOW_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "jira": {
        "goal": "Create a Jira ticket",
        "confirmation_required": True,
        "tool_requirements": ["retrieval.search_kb", "jira.create_ticket", "audit.log_action"],
        "expected_result": "Jira ticket created successfully and audited",
        "steps": [
            {
                "task_id": "retrieve_context",
                "tool_id": "retrieval.search_kb",
                "dependencies": [],
                "confirmation_required": False,
                "description": "Search the knowledge base for existing context/tickets"
            },
            {
                "task_id": "create_ticket",
                "tool_id": "jira.create_ticket",
                "dependencies": ["retrieve_context"],
                "confirmation_required": True,
                "description": "Create a new ticket in Jira with context"
            },
            {
                "task_id": "log_audit",
                "tool_id": "audit.log_action",
                "dependencies": ["create_ticket"],
                "confirmation_required": False,
                "description": "Audit-log the creation of the Jira ticket"
            }
        ]
    },
    "onboarding": {
        "goal": "Draft onboarding document",
        "confirmation_required": False,
        "tool_requirements": ["doc.draft_document", "audit.log_action"],
        "expected_result": "Onboarding document drafted and audited",
        "steps": [
            {
                "task_id": "draft_doc",
                "tool_id": "doc.draft_document",
                "dependencies": [],
                "confirmation_required": False,
                "description": "Draft onboarding document content"
            },
            {
                "task_id": "log_audit",
                "tool_id": "audit.log_action",
                "dependencies": ["draft_doc"],
                "confirmation_required": False,
                "description": "Audit-log the onboarding draft creation"
            }
        ]
    },
    "summarize": {
        "goal": "Summarize today's meeting",
        "confirmation_required": False,
        "tool_requirements": ["transcript.get_today", "summary.generate", "audit.log_action"],
        "expected_result": "Meeting summarized successfully and audited",
        "steps": [
            {
                "task_id": "get_transcript",
                "tool_id": "transcript.get_today",
                "dependencies": [],
                "confirmation_required": False,
                "description": "Get transcript for today's meeting"
            },
            {
                "task_id": "generate_summary",
                "tool_id": "summary.generate",
                "dependencies": ["get_transcript"],
                "confirmation_required": False,
                "description": "Generate meeting summary"
            },
            {
                "task_id": "log_audit",
                "tool_id": "audit.log_action",
                "dependencies": ["generate_summary"],
                "confirmation_required": False,
                "description": "Audit-log the summary generation"
            }
        ]
    },
    "email": {
        "goal": "Send approval email",
        "confirmation_required": True,
        "tool_requirements": ["email.send_approval", "audit.log_action"],
        "expected_result": "Approval email sent and audited",
        "steps": [
            {
                "task_id": "send_email",
                "tool_id": "email.send_approval",
                "dependencies": [],
                "confirmation_required": True,
                "description": "Send approval email to recipient"
            },
            {
                "task_id": "log_audit",
                "tool_id": "audit.log_action",
                "dependencies": ["send_email"],
                "confirmation_required": False,
                "description": "Audit-log the email delivery"
            }
        ]
    }
}
