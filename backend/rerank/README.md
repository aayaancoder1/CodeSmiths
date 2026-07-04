# Rerank Module

## Responsibility
Applies deep semantic matching (e.g., using a Cross-Encoder) to re-evaluate the relevance of candidates retrieved by the multi-stage retriever. This module prunes and re-orders the candidate set to optimize the top-k results passed to synthesis.
