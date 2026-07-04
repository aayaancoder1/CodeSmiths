# AI Company Brain Integration Architecture

This document describes the complete integrated document ingestion and search retrieval execution pipeline.

## System Ingestion Pipeline

During ingestion, files and logs are parsed, embedded, and added to the structural index:

```
Document Ingestion ──► Embeddings (Vector Upsert) ──► Knowledge Graph (Neo4j update)
```

## System Query & Retrieval Pipeline

During search, user queries undergo multi-stage filtering, retrieval, graph traversal, synthesis, and validation:

```
User Query
    │
    ▼
Embeddings / Vector Retrieval ──┐
                                ├──► Hybrid Retrieval ──► Graph Expansion ──► Graph RAG ──► Citations ──► Evaluation ──► Report
BM25 Lexical Retrieval ─────────┘
```

## Integrated Subsystems

- **Embeddings**: Vector representation generator.
- **Retrieval (Dense)**: Qdrant semantic space similarity search.
- **BM25 (Lexical)**: Keyword matching inverted indexes.
- **Hybrid Retrieval**: Blending rankings using RRF / Weighted scoring, followed by semantic cross-encoder reranking.
- **Knowledge Graph**: NLP/LLM-driven entity/relation extraction and storage.
- **Graph Expansion**: Graph neighborhood traversals using Neo4j to collect relational context.
- **Graph RAG**: Compiles text chunks and relation graphs into prompt formats for LLM synthesis.
- **Citations**: Attributes generated answer strings to original text source chunks.
- **Evaluation**: Scores response latency, faithfulness, and precision.
