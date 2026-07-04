from typing import List, Any, Optional
from .interface import IEmbeddingService
from .models import DocumentEmbedding, ChunkEmbedding, EmbeddingMetadata
from .provider import IEmbeddingProvider
from .qdrant_client import IQdrantClient
from .document_pipeline import DocumentEmbeddingPipeline
from .chunk_pipeline import ChunkEmbeddingPipeline

class EmbeddingService(IEmbeddingService):
    """
    Coordinates providers and pipelines to generate actual embeddings.
    """
    def __init__(self, provider: IEmbeddingProvider, qdrant_client: Optional[IQdrantClient] = None):
        self.provider = provider
        self.qdrant_client = qdrant_client
        self.document_pipeline = DocumentEmbeddingPipeline(provider)
        self.chunk_pipeline = ChunkEmbeddingPipeline(provider)

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        return self.provider.embed_texts(documents)

    def embed_chunks(self, chunks: List[str]) -> List[List[float]]:
        return self.provider.embed_texts(chunks)

    def embed_query(self, query: str) -> List[float]:
        return self.provider.embed_texts([query])[0]

    def generate_document_embeddings(self, document_id: str, tenant_id: str, text: str, metadata: EmbeddingMetadata) -> DocumentEmbedding:
        return self.document_pipeline.run(document_id, tenant_id, text, metadata)

    def generate_chunk_embeddings(self, document_id: str, chunk_id: str, tenant_id: str, text: str, metadata: EmbeddingMetadata) -> ChunkEmbedding:
        return self.chunk_pipeline.run(document_id, chunk_id, tenant_id, text, metadata)

    def store_embeddings(self, collection_name: str, embeddings: List[Any]) -> None:
        if not self.qdrant_client:
            raise ValueError("Qdrant client not initialized")
        self.qdrant_client.store_embeddings(collection_name, embeddings)

    def update_embeddings(self, collection_name: str, embeddings: List[Any]) -> None:
        self.store_embeddings(collection_name, embeddings)

    def delete_embeddings(self, collection_name: str, document_id: Optional[str] = None, chunk_ids: Optional[List[str]] = None) -> None:
        if not self.qdrant_client:
            raise ValueError("Qdrant client not initialized")
        self.qdrant_client.delete_embeddings(collection_name, document_id, chunk_ids)
