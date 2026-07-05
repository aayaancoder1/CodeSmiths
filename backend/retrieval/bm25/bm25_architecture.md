# BM25 Lexical Retrieval Subsystem Architecture

This document describes the workflow of documents and search queries within the BM25 lexical retrieval subsystem.

```
Document
   │
   ▼
Tokenization
   │
   ▼
Inverted Index
   │
   ▼
BM25 Scoring
   │
   ▼
Ranked Documents
```

## Flow Description

1. **Document**: Raw text metadata representations parsed from documents or chunks (associated with unique `document_id` and isolated by `tenant_id`).
2. **Tokenization**: Documents (at indexing phase) and incoming search queries (at search phase) are processed by the `ITokenizer` interface into arrays of normalized term stems.
3. **Inverted Index**: Term mappings pointing back to their structural sources are indexed by the `IIndexManager` implementation, optimizing lookups for matched term queries.
4. **BM25 Scoring**: When a search is processed, the `IBM25Scorer` interface computes terms weightings using TF-IDF style values (tuned by parameters `k1` and `b`) against matched terms.
5. **Ranked Documents**: The resulting `BM25Result` list containing chunk texts, similarity matching scores, parent origins, and metadata parameters is returned to the retrieval service client.
