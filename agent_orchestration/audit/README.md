# Audit Agent

The Audit Agent is the final stage of the workflow and is responsible for saving immutable, non-sensitive audit metadata records in-memory.

## Responsibilities

- **Immutable In-Memory Storage**: Logs are saved using a thread-safe `InMemoryAuditStorage` preventing any modification or deletion.
- **Enterprise Security Compliance**: Prohibits storage of sensitive enterprise data (e.g. document contents, prompts, chat history, RAG responses, embeddings).
- **AuditRecord Schema**: Enforces schema structure containing execution, verification, and confirmation status, duration, and timestamps.

## Prohibited Sensitive Fields

The following fields will cause verification to fail to prevent data leaks:
- `document_content`, `document_contents`
- `prompt`, `prompt_contents`
- `chat_history`
- `rag_response`, `rag_responses`
- `embeddings`
- `knowledge_graph`, `kg_data`
- `retrieved_documents`

## Usage

```python
from agent_orchestration.audit.audit_agent import AuditAgent
from agent_orchestration.audit.audit_events import AuditEvent

agent = AuditAgent()

# Record an event
record = agent.record_event({
    "audit_id": "aud-101",
    "workflow_id": "wf-123",
    "request_id": "req-999",
    "user_id": "user-45",
    "tool_id": "jira.create_ticket",
    "workflow_state": "AUDITED",
    "execution_status": "SUCCESS",
    "verification_status": "VERIFIED",
    "confirmation_status": "CONFIRMED",
    "timestamp": "2026-07-04T12:00:00Z",
    "execution_duration": 0.45,
    "metadata": {"template": "jira"}
})
```
