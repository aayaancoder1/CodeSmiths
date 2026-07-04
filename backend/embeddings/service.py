from typing import List, Dict, Any, Optional
from .interface import IEmbeddingService
from .models import DocumentEmbedding, ChunkEmbedding, EmbeddingMetadata
from .provider import IEmbeddingProvider
from .qdrant_client import IQdrantClient
from .document_pipeline import DocumentEmbeddingPipeline
from .chunk_pipeline import ChunkEmbeddingPipeline

class EmbeddingService(IEmbeddingService):
    """
    Placeholder service implementation coordinating providers, pipelines, and the vector client.
    """

    def __init__(self, provider: IEmbeddingProvider, qdrant_client: IQdrantClient):
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
        points = []
        for emb in embeddings:
            points.append({
                "id": getattr(emb, "chunk_id", getattr(emb, "document_id")),
                "vector": emb.embedding,
                "payload": {
                    "tenant_id": emb.tenant_id,
                    "document_id": emb.document_id,
                    "metadata": {
                        "source_type": emb.metadata.source_type,
                        "created_at": emb.metadata.created_at,
                        "permissions": emb.metadata.permissions,
                        "additional_info": emb.metadata.additional_info
                    }
                }
            })
        self.qdrant_client.upsert_vectors(collection_name, points)

    def update_embeddings(self, collection_name: str, embeddings: List[Any]) -> None:
        # For updates, upsert is structurally identical in Qdrant placeholder
        self.store_embeddings(collection_name, embeddings)

    def delete_embeddings(self, collection_name: str, document_id: Optional[str] = None, chunk_ids: Optional[List[str]] = None) -> None:
        if chunk_ids:
            self.qdrant_client.delete_vectors(collection_name, chunk_ids)
        elif document_id:
            self.qdrant_client.delete_by_filter(collection_name, {"document_id": document_id})
