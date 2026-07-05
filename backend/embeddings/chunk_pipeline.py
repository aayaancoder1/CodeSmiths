from .models import ChunkEmbedding, EmbeddingMetadata
from .provider import IEmbeddingProvider

class ChunkEmbeddingPipeline:
    """
    Ingests chunk strings and calls IEmbeddingProvider to create a ChunkEmbedding.
    """
    def __init__(self, provider: IEmbeddingProvider):
        self.provider = provider

    def run(self, document_id: str, chunk_id: str, tenant_id: str, text: str, metadata: EmbeddingMetadata) -> ChunkEmbedding:
        vector = self.provider.embed_texts([text])[0]
        return ChunkEmbedding(
            chunk_id=chunk_id,
            document_id=document_id,
            tenant_id=tenant_id,
            embedding=vector,
            metadata=metadata
        )
