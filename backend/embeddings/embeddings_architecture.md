# Embeddings Subsystem Architecture

This document describes the flow of a document as it is chunked, embedded, associated with metadata, and loaded into Qdrant.

```
Document
   │
   ▼
 Chunk
   │
   ▼
Embedding
   │
   ▼
Metadata
   │
   ▼
Qdrant
```

## Flow Description

1. **Document**: The raw document input originating from the ingestion pipeline containing text, a `document_id`, and `tenant_id` ownership constraints.
2. **Chunk**: The raw document is split into smaller chunks (semantic boundaries or token window chunks) containing a unique `chunk_id` referring back to the parent `document_id`.
3. **Embedding**: The chunk text is passed through the `IEmbeddingProvider` abstraction (e.g. SentenceTransformers, OpenAI, Cohere) to generate dense vector representation values.
4. **Metadata**: The vector is augmented with the `EmbeddingMetadata` schema containing tenant isolation fields (`tenant_id`), document lineage (`document_id`), and ACL permissions.
5. **Qdrant**: The generated vector along with its payload is stored via the `IQdrantClient` abstraction using tenant isolation and ACL properties for filtered vector querying.
