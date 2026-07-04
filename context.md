# Project Context

You own the core intelligence layer.

Everything else depends on your outputs.

---

# Input

From Backend:

- chunks
- metadata
- permissions
- ACL information

---

# Output

To Frontend:

- answers
- citations
- graphs

To Agents:

- retrieval API
- graph API

---

# Databases

Qdrant
Neo4j
PostgreSQL

---

# Pipeline

User Query
↓
Permission Filter
↓
BM25 Retrieval
↓
Vector Retrieval
↓
Hybrid Merge
↓
Cross Encoder Rerank
↓
Knowledge Graph Expansion
↓
Context Builder
↓
LLM
↓
Answer + Citations

---

# Future Features

- expertise discovery
- decision memory
- onboarding generation
- incident reconstruction