from typing import List
from sentence_transformers import SentenceTransformer
from .provider import IEmbeddingProvider

class SentenceTransformerProvider(IEmbeddingProvider):
    """
    Concrete implementation of the IEmbeddingProvider using sentence-transformers.
    Uses 'all-MiniLM-L6-v2' model for local embedding generation.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def get_embedding_dimension(self) -> int:
        return 384

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
