# Slack Thread: Database Migration Failures

**Aayaan**: Hey team, anyone seeing locks on the transactions table during migrations?
**Dev**: Yes, the migration script is attempting to alter a column without using an online schema migration tool.
**Aayaan**: Good catch. Let's write a rollback step and run it with long timeout offsets.
