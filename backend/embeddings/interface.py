from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from .models import DocumentEmbedding, ChunkEmbedding, EmbeddingMetadata

class IEmbeddingService(ABC):
    """
    Interface for the Embedding Service.
    Responsible for generating representations for documents, chunks, and queries/metadata,
    and managing storage (store, update, delete) in the vector store.
    """
    
    @abstractmethod
    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """Generate raw embeddings for a list of document texts."""
        pass

    @abstractmethod
    def embed_chunks(self, chunks: List[str]) -> List[List[float]]:
        """Generate raw embeddings for a list of chunked texts."""
        pass

    @abstractmethod
    def embed_query(self, query: str) -> List[float]:
        """Generate embedding representation for a search query."""
        pass

    @abstractmethod
    def generate_document_embeddings(self, document_id: str, tenant_id: str, text: str, metadata: EmbeddingMetadata) -> DocumentEmbedding:
        """Create a full DocumentEmbedding record."""
        pass

    @abstractmethod
    def generate_chunk_embeddings(self, document_id: str, chunk_id: str, tenant_id: str, text: str, metadata: EmbeddingMetadata) -> ChunkEmbedding:
        """Create a ChunkEmbedding record."""
        pass

    @abstractmethod
    def store_embeddings(self, collection_name: str, embeddings: List[Any]) -> None:
        """Store generated embeddings (document or chunk) to the vector store."""
        pass

    @abstractmethod
    def update_embeddings(self, collection_name: str, embeddings: List[Any]) -> None:
        """Update existing embeddings in the vector store."""
        pass

    @abstractmethod
    def delete_embeddings(self, collection_name: str, document_id: Optional[str] = None, chunk_ids: Optional[List[str]] = None) -> None:
        """Delete embeddings from the vector store by document_id or explicit chunk_ids."""
        pass
