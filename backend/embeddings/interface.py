from abc import ABC, abstractmethod
from typing import List, Dict, Any

class IEmbeddingService(ABC):
    """
    Interface for the Embedding Service.
    Responsible for generating representations for documents, chunks, and queries/metadata.
    """
    
    @abstractmethod
    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of document texts."""
        pass

    @abstractmethod
    def embed_chunks(self, chunks: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of chunked texts."""
        pass

    @abstractmethod
    def embed_query(self, query: str) -> List[float]:
        """Generate embedding representation for a search query."""
        pass
