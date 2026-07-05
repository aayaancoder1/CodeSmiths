# Hybrid Retrieval Subsystem Architecture

This document describes the flow of a user search request through the hybrid retrieval subsystem.

```
Query
  │
  ▼
Vector Search ──┐
                ├──► Result Fusion ──► Reranking ──► Final Retrieval Set
BM25 Search ────┘
```

## Flow Description

1. **Query**: The text search query entered by the user.
2. **Vector Search / BM25 Search**: Parallel processes that output sorted candidate lists.
   - *Vector Search* scores items using semantic embeddings (Qdrant).
   - *BM25 Search* scores items using keyword matching (Inverted Index).
3. **Result Fusion**:
   - Matches candidate lists using **Reciprocal Rank Fusion (RRF)** to combine ordinal ranks rather than absolute values.
   - Can alternate to **Weighted Fusion** to perform weighted additions on normalized scores.
4. **Reranking**: Candidate items pass to the `HybridRanker` layer where they are prioritized using high-accuracy semantic cross-encoder modules.
5. **Final Retrieval Set**: Top-k candidates are sliced and compiled into the `HybridSearchOutput` model, which is returned to the RAG context synthesizer.
