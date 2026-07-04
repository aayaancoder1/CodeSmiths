from typing import List
from .interface import IEmbeddingService

class EmbeddingService(IEmbeddingService):
    """
    Placeholder service implementation for generating embeddings.
    """

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        # Placeholder implementation
        return [[0.0] * 384 for _ in documents]

    def embed_chunks(self, chunks: List[str]) -> List[List[float]]:
        # Placeholder implementation
        return [[0.0] * 384 for _ in chunks]

    def embed_query(self, query: str) -> List[float]:
        # Placeholder implementation
        return [0.0] * 384
