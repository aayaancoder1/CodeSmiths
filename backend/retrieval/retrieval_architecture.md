# Retrieval Subsystem Architecture

This document describes the flow of a search request within the vector retrieval subsystem.

```
Query
  │
  ▼
Embedding
  │
  ▼
Qdrant Search
  │
  ▼
Similarity Scores
  │
  ▼
Retrieved Chunks
```

## Flow Description

1. **Query**: The incoming search request string submitted by the user alongside the tenant boundary identifiers (`tenant_id`).
2. **Embedding**: The text query is converted into a dense vector using the embedding generator service.
3. **Qdrant Search**: The query vector and metadata filter rules (such as access control filters or isolated collection namespaces) are formatted and issued to Qdrant.
4. **Similarity Scores**: Qdrant executes approximate nearest neighbor search to compute similarity scores (cosine distance metrics) between the query vector and candidate chunk vectors.
5. **Retrieved Chunks**: High-scoring items are packaged along with their text contents, unique database entity keys (`chunk_id`), parent origins (`source_id`), and associated metadata payloads.
