# Retrieval Module

## Responsibility
Combines lexical lookup (BM25) and dense search (Qdrant Vector DB) into a unified hybrid result. This layer enforces strict user ACL / permission policies to filter out chunks that the user is not authorized to view.
