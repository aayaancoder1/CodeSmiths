from typing import List, Dict, Any
from .models import DocumentEmbedding, EmbeddingMetadata
from .provider import IEmbeddingProvider

class DocumentEmbeddingPipeline:
    """
    Pipeline responsible for handling full document text structure and feeding it to the provider.
    """
    def __init__(self, provider: IEmbeddingProvider):
        self.provider = provider

    def run(self, document_id: str, tenant_id: str, text: str, metadata: EmbeddingMetadata) -> DocumentEmbedding:
        # Placeholder calculation
        vectors = self.provider.embed_texts([text])
        return DocumentEmbedding(
            document_id=document_id,
            tenant_id=tenant_id,
            embedding=vectors[0],
            metadata=metadata
        )
