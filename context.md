# Project Context

You are building the action layer.

Your agents consume:

- retrieval APIs
- graph APIs
- backend APIs

---

# Example

User:

Create a Jira ticket for the payment outage.

Workflow:

retrieve
↓
analyze
↓
generate
↓
confirm
↓
execute
↓
audit

---

# Constraints

- every action must be auditable
- every action must be reversible
- require confirmation for destructive actions