# Redis Outage Post-Mortem

## Summary
Redis cache cluster ran out of memory (OOM) due to unexpired session tokens. This caused user log-ins to fail globally.

## Fix
Enabled volatile-lru eviction policy and set strict 24-hour TTL expiration configurations on all session tokens.
