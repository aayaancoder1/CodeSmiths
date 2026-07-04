# Evaluation Subsystem Architecture

This document describes the flow of RAG query evaluations through the evaluation subsystem.

```
Query
  │
  ▼
Retrieval Metrics ──┐
Citation Metrics ───┼──► Latency Metrics ──► Evaluation Report
Answer Metrics ─────┘
```

## Flow Description

1. **Query**: The root user query containing RAG pipeline processing inputs and targets.
2. **Evaluation Dimensions**:
   - **Retrieval Metrics**: Measures lexical/vector match quality using `recall@k`, `precision@k`, and `MRR`.
   - **Citation Metrics**: Measures source coverage and alignment correctness.
   - **Answer Metrics**: Evaluates answer quality along the dimensions of `faithfulness`, `relevance`, and `completeness`.
3. **Latency Metrics**: Logs duration stamps for search phases, graph traversal phases, and overall answer synthesis.
4. **Evaluation Report**: Packages computed metrics together with execution metadata into the `EvaluationReport` format.
