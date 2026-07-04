from .models import DocumentEmbedding, EmbeddingMetadata
from .provider import IEmbeddingProvider

class DocumentEmbeddingPipeline:
    """
    Ingests document strings and calls IEmbeddingProvider to create a DocumentEmbedding.
    """
    def __init__(self, provider: IEmbeddingProvider):
        self.provider = provider

    def run(self, document_id: str, tenant_id: str, text: str, metadata: EmbeddingMetadata) -> DocumentEmbedding:
        vector = self.provider.embed_texts([text])[0]
        return DocumentEmbedding(
            document_id=document_id,
            tenant_id=tenant_id,
            embedding=vector,
            metadata=metadata
        )
