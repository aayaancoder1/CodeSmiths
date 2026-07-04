# AI / RAG Pipeline Architecture

This document describes the flow of information through the core intelligence layer.

```
User Query
    │
    ▼
Permission Filter
    │
    ▼
BM25 Retrieval ──┐
                 ├──► Hybrid Merge ──► Reranker ──► Knowledge Graph Expansion ──► Context Builder ──► LLM ──► Citation Generator
Vector Retrieval ┘
```

## Detailed Stage Breakdown

### 1. User Query
The input text submitted by the user alongside session context (e.g. user details, requesting client metadata).

### 2. Permission Filter
Retrieves the requesting user's Access Control Lists (ACLs) and filters out any namespaces, collections, or documents the user is unauthorized to access before performing vector or lexical retrieval.

### 3. BM25 Retrieval
Standard keyword-based lexical retrieval matching explicit terms within candidate text chunks.

### 4. Vector Retrieval
Dense semantic search using generated embeddings queried against the Qdrant vector database to extract conceptually similar chunks.

### 5. Hybrid Merge
Fuses lexical (BM25) and semantic (Vector) search results, normalizing scores to generate a ranked candidate list.

### 6. Reranker
Evaluates candidates using a Cross-Encoder model to compute high-accuracy relevance scores, discarding low-scoring chunks to optimize top-k candidates.

### 7. Knowledge Graph Expansion
Identifies key entities in the query and top-k candidate chunks, traverses related nodes in the Neo4j graph database to retrieve contextually linked relational information.

### 8. Context Builder
Assembles the final structured prompt containing candidate text chunks, relational graph data, and instructions for synthesis.

### 9. LLM
Synthesizes a response using the contextual data injected in the prompt, avoiding outside knowledge hallucinations.

### 10. Citation Generator
Maps spans of generated text back to the retrieved sources (documents, chunks, databases) for exact attribution.
